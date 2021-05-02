from machine import ADC,Pin
from utime import sleep_us, sleep_ms
import uasyncio as asyncio

LED_PIN = 2
ADC_PIN = 36
class Trace():
    
    TRACE_LENGTH=500
    TRIG_SLOPE_RISING  = 0
    TRIG_SLOPE_FALLING = 1
    
    def __init__(self):
        print("Init trace")
        self.traceBuf = bytearray(self.TRACE_LENGTH)
        self.pulse_T   = 10   # sample freq: 100 Hz (10 ms between samples)
        self.trigLevel =  100
        self.trigPos = 250
        self.trigSlope = self.TRIG_SLOPE_FALLING
        self.traceIndex = 0
        self.sampleCount = 0
        self.singleShot = 1
        self.no_trig = False
        self.trigCond = False
        self.triggeredAt = 0
        self.readCnt = 0
        self.led = Pin(LED_PIN, Pin.OUT, value=0)

    async def read_trace(self):
        print("read trace started")
        self.adc = ADC(Pin(ADC_PIN))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        # print("no_trig: ",self.no_trig)
        # print("trigger level: ", self.trigLevel)
        # print("trigger position: ",self.trigPos)
        self.sampleCount = 0
        self.traceIndex = 0
        self.trigCond = False
        # restrict trigger level to give 6 bits margin
        if self.trigLevel < 3:
            tl = 3
        elif self.trigLevel > 252:
            tl = 252
        else:
            tl = self.trigLevel
            
        if self.pulse_T < 1:
            delay = int(self.pulse_T*1000)
            print("delay: {:d}us".format(delay))
        else:
            print("delay: {:d}ms".format(int(self.pulse_T)))

        self.triggeredAt = 0    
        if not self.no_trig:
            print("Detecting trigger")
            while True:
                value = self.adc.read() >> 4
                if self.pulse_T < 1:
                    sleep_us(delay)
                    self.readCnt +=1
                    if self.readCnt >= 500:
                        await asyncio.sleep_ms(0)  # allows task switch after 100ms (T=0.2)  or 250ms (T=0.5)
                        self.readCnt = 0
                else:
                    sleep_ms(int(self.pulse_T))                    
                    await asyncio.sleep_ms(0)
                
                self.traceBuf[self.traceIndex] = value
                self.traceIndex += 1
                if self.traceIndex == 500:      # the trace buffer is a circular buffer
                    self.traceIndex = 0
            
                self.sampleCount += 1
                if self.sampleCount > 500:
                    self.sampleCount = 500
            
                if self.trigSlope == self.TRIG_SLOPE_RISING:
                    # print("trigger rising")

                    if self.trigCond and value > tl+3 and self.sampleCount > self.trigPos:
                        # print("trigCond: ", self.trigCond,end= " ")
                        # print("value: %d, trigger level: %d"%(value,self.trigLevel))
                        break
                    elif value <= tl-3:
                        self.trigCond = True
                        continue
                else:
                    # print("trigger falling")
                    if self.trigCond and value < tl -3 and self.sampleCount > self.trigPos:
                        # print("trigCond: ", self.trigCond,end= " ")
                        # print("value: %d, trigger level: %d"%(value,self.trigLevel))                
                        break
                    elif value >= tl + 3:
                        self.trigCond = True
                        continue

        print("Trigger seen")
        self.triggeredAt = self.traceIndex
        print("Triggered at trace buffer index ",self.triggeredAt)
        print("value: ",self.traceBuf[self.traceIndex-1])

        if self.no_trig:
            maxcount = 500
        else:
            maxcount = 500 - self.trigPos
        print("maxcount: ",maxcount)
        
        for i in range(maxcount):
            value = self.adc.read() 
            self.traceBuf[self.traceIndex] = value >> 4 # restrict to 8 bits
            # print(value)
            self.traceIndex += 1
            if self.traceIndex == 500:                  # traceBuf is a circular buffer
                 self.traceIndex = 0
            if self.pulse_T < 1:
                sleep_us(delay)
            else:
                sleep_ms(int(self.pulse_T))
                await asyncio.sleep_ms(0)
                
        self.led.value(not self.led.value())
        # await asyncio.sleep_ms(0)
        # print("Writing data to disk")
        # self.writeToDisk()
        


    async def measure(self):
        print("Measurement task started")

        while True:
            self.read_trace()
            await asyncio.sleep_ms(0)
            
    def writeToDisk(self):
        f = open("/data/trace.txt","w")
        start_index = self.triggeredAt - self.trigPos
        if start_index < 0:
            start_index += 500
        for i in range(start_index,500):
            f.write(str(self.traceBuf[i]) + "\n")
        for i in range(0,start_index):
            f.write(str(self.traceBuf[i]) + "\n")
        # for i in range(500):
        #     f.write(str(self.traceBuf[i]) + "\n")
        j = 0
        for i in range(start_index,500):
            if not j % 10 and j != 0:
                print("")
            print(self.traceBuf[i],end =" ")
            j += 1
        for i in range(0,start_index):
            if not j % 10 and j != 0:
                print("")
            print(self.traceBuf[i],end =" ")
            j += 1          
        f.close()
               
# trace = Trace()
# trace.read_trace()
