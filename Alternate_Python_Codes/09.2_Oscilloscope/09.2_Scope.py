from machine import ADC,Pin
from utime import sleep_us, sleep_ms

TRIG_SLOPE_RISING  = 0
TRIG_SLOPE_FALLING = 1

class Oscilloscope():
    
    TRACE_LENGTH=500
    
    def __init__(self,adcPin=36):
        self.adc = ADC(Pin(adcPin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        self.traceBuf = bytearray(self.TRACE_LENGTH)
        self.pulse_T   = 10   # sample freq: 100 Hz (10 ms between samples)
        self.trigLevel =  100
        self.trigPos = 250
        self.trigSlope = TRIG_SLOPE_FALLING
        self.traceIndex = 0
        self.sampleCount = 0
        self.no_trig = False
        self.trigCond = False
        self.triggeredAt = 0

    def read_trace(self):
        self.sampleCount = 0
        self.traceIndex = 0
        self.trigCond = False
        if self.pulse_T < 1:
            delay = self.pulse_T*1000
        print("Waiting for trigger")
        while not self.trig():
            pass
        else:
            print("Trigger seen")
            self.triggeredAt = self.traceIndex
            print("Triggered at trace buffer index ",self.triggeredAt)
            print("value: ",self.traceBuf[self.traceIndex-1])
        if self.no_trig:
            maxcount = 500-1
        else:
            maxcount = 500 - self.trigPos
        print("maxcount: ",maxcount)
        for i in range(maxcount):
            value = self.adc.read()
            self.traceBuf[self.traceIndex] = value >> 4 # restrict to 8 bits
            self.traceIndex += 1
            if self.traceIndex == 500:                  # traceBuf is a circular buffer
                 self.traceIndex = 0
            if self.pulse_T < 1:
                sleep_us(delay)
            else:
                sleep_ms(self.pulse_T)
        print("Writing data to disk")
        self.writeToDisk()
        
    
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
        
        
        
    # detect a trigger
    
    def trig(self):
        value = self.adc.read() >> 4
        self.traceBuf[self.traceIndex] = value
        self.traceIndex += 1
        if self.traceIndex == 500:      # the trace buffer is a circular buffer
            self.traceIndex = 0
            
        self.sampleCount += 1
        if self.sampleCount > 500:
            self.sampleCount = 500
            
        # if no_trig is set, start measurement immediately 
        if self.no_trig:
            return True

        if self.trigSlope == TRIG_SLOPE_RISING:
            if self.trigCond and value > self.trigLevel and self.sampleCount > self.trigPos:
                print("trigCond: ", self.trigCond,end= " ")
                print("value: %d, trigger level: %d"%(value,self.trigLevel))
                return True
            elif value <= self.trigLevel:
                self.trigCond = True
                return False
        else:            
            if self.trigCond and value < self.trigLevel and self.sampleCount > self.trigPos:
                print("trigCond: ", self.trigCond,end= " ")
                print("value: %d, trigger level: %d"%(value,self.trigLevel))                
                return True
            elif value >= self.trigLevel:
                self.trigCond = True
                return False       


scope = Oscilloscope()
scope.read_trace()
