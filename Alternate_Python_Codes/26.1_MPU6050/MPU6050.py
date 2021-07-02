# MPU6050: a class to drive the MPU 6050 accelerometer and gyroscope
#

from machine import Pin,I2C
from micropython import const
from utime import sleep_ms

MPU6050_ADDR              = const(0x68)

MPU6050_SMPLRT_DIV        = const(0x19)
MPU6050_CONFIG            = const(0x1a)
MPU6050_GYRO_CONFIG       = const(0x1b)
MPU6050_ACCEL_CONFIG      = const(0x1c)
MPU6050_FIFO_EN           = const(0x23)

MPU6050_ACCEL_XOUT_H      = const(0x3b)
MPU6050_ACCEL_XOUT_L      = const(0x3c)
MPU6050_ACCEL_YOUT_H      = const(0x3d)
MPU6050_ACCEL_YOUT_L      = const(0x3c)
MPU6050_ACCEL_ZOUT_H      = const(0x3f)
MPU6050_ACCEL_ZOUT_L      = const(0x40)

MPU6050_TEMP_OUT_H        = const(0x41)
MPU6050_TEMP_OUT_L        = const(0x42)

MPU6050_GYRO_XOUT_H       = const(0x43)
MPU6050_GYRO_XOUT_L       = const(0x44)
MPU6050_GYRO_YOUT_H       = const(0x45)
MPU6050_GYRO_YOUT_L       = const(0x46)
MPU6050_GYRO_ZOUT_H       = const(0x47)
MPU6050_GYRO_ZOUT_L       = const(0x48)

MPU6050_WHO_AM_I          = const(0x75)

MPU6050_PWR_MGMT_1        = const(0x6b)
MPU6050_PWR_MGMT_2        = const(0x6c)

MPU6050_AFS_SEL_MASK      = const(0x18)
MPU6050_BW_MASK           = const(0x07)

MPU6050_DEVICE_RESET      = const(0x80)
    
class MPU6050(object):
    
    def __init__(self,scl=22,sda=21,debug=False):
        self.debug = debug
        
        self.i2c = I2C(1,scl=Pin(scl),sda=Pin(sda))
        i2c_slaves = self.i2c.scan()
        if MPU6050_ADDR in i2c_slaves:
            if self.debug:
                print("MPU 6050 I2C address found, continuing...")
        else:
            print("Cannot find MPU 6050 address on the I2C bus")
            print("Please check your connections")
            return
            
        who_am_i = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_WHO_AM_I,1)
        if self.debug:
            print("who_am_i register content: 0x{:02x}".format(int(who_am_i[0])))
        if int(who_am_i[0]) != MPU6050_ADDR:
            print("Bad value of who_am_i register, is the device a MPU 6050?")
            return

        reset = b'\x80'
        if self.debug:
            print("resetting the MPU 6050 by sending 0x{:02x} to the PWR_MGMT_1(0x{:02x}) reg.".format(int(reset[0]),MPU6050_PWR_MGMT_1))
        self.i2c.writeto_mem(MPU6050_ADDR,MPU6050_PWR_MGMT_1,reset)
        sleep_ms(100)
        self.i2c.writeto_mem(MPU6050_ADDR,MPU6050_PWR_MGMT_1,b'\x01')
            
    def setDebug(self,onOff):
        self.debug = onOff

    def setAccelFullScale(self,scale):
        accelConfig = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_ACCEL_CONFIG,1)
        accelConfig = bytearray(accelConfig)
        scale_dict = {2:0, 4:1, 8:2, 16:3}
        if not scale in scale_dict:
            print("Illegal scale value, ignoring...")
            return
        else:
            new_scale = scale_dict[scale] << 3
        if self.debug:
            print("read from accelConfig: {:02x}".format(accelConfig[0]))

        accelConfig[0] &= ~MPU6050_AFS_SEL_MASK
        accelConfig[0] |= new_scale
        if self.debug:
            print("Writing 0x{:02x} to ACCEL_CONFIG(0x{:02x})".format(accelConfig[0],MPU6050_ACCEL_CONFIG))
        self.i2c.writeto_mem(MPU6050_ADDR,MPU6050_ACCEL_CONFIG,accelConfig)
        
    def setGyroFullScale(self,scale):
        gyroConfig = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_GYRO_CONFIG,1)
        gyroConfig = bytearray(gyroConfig)
        scale_dict = {250:0, 500:1, 1000:2, 2000:3}
        if not scale in scale_dict:
            print("Illegal scale value, ignoring...")
            return
        else:
            new_scale = scale_dict[scale] << 3
        if self.debug:
            print("read from gyroConfig: {:02x}".format(gyroConfig[0]))

        gyroConfig[0] &= ~MPU6050_AFS_SEL_MASK
        gyroConfig[0] |= new_scale
        if self.debug:
            print("Writing 0x{:02x} to GYRO_CONFIG(0x{:02x})".format(gyroConfig[0],MPU6050_GYRO_CONFIG))
        self.i2c.writeto_mem(MPU6050_ADDR,MPU6050_GYRO_CONFIG,gyroConfig)

    def getAccelFullScale(self):
        scale_dict = {0:2, 1:4, 2:8, 3:16}
        scale = int(self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_ACCEL_CONFIG,1)[0]) & MPU6050_AFS_SEL_MASK
        return scale_dict[scale >> 3]
    
    def getGyroFullScale(self):
        scale_dict = {0:250, 1:500, 2:1000, 3:2000}
        scale = int(self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_GYRO_CONFIG,1)[0]) & MPU6050_AFS_SEL_MASK
        print("gyro scale code: ",scale)
        return scale_dict[scale >> 3]
    
    def setConfig(self,bw):
        gyro_bw  = {256: 0, 188: 1, 98: 2, 42: 3, 20: 4, 10: 5, 5: 6}
        accel_bw = {260: 0, 184: 1, 94: 2, 44: 3, 21: 4, 10: 5, 5: 6}
        if bw in gyro_bw:
            bw_code = accel_bw[bw]
            if self.debug:
                print("Bandwidth code: ",bw_code)
        elif bw in accel_bw:
            bw_code = accel_bw[bw]
            if self.debug:
                print("Bandwidth code: ",bw_code)
        else:
            print("Illegal bandwidth, ignoring...")
            return
   
        config = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_CONFIG,1)
        if self.debug:
            print("read from Config reg(0x{:02x}): {:02x}".format(MPU6050_CONFIG,config[0]))
        config = bytearray(config)
        config[0] &= ~MPU6050_BW_MASK
        config[0] |= bw_code
        if self.debug:
            print("Writing 0x{:02x} to CONFIG(0x{:02x})".format(config[0],MPU6050_CONFIG))       
        self.i2c.writeto_mem(MPU6050_ADDR,MPU6050_CONFIG,config)
        
    def getConfig(self):
        config = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_CONFIG,1)
        return int(config[0])

    def setSampleRateDiv(self,divider):
        if divider < 0 or divider > 7:
            print("Illegal divider, ignoring...")
            return
        div = []
        div.append(int.to_bytes(1,"big"))
        self.i2c.writeto_mem(MPU6050_ADDR,MPU6050_SMPLRT_DIV,div)

    def getSampleRateDiv(self):
        return int(self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_SMPLRT_DIV,1)[0])

    def bytesToInt(self,hi,low):
        val = (hi << 8 ) | low
        print("value: 0x{:04x}".format(val))
        if not val & 0x8000:           # positive 16 bit value
            print ("positive value: {:d}".format(val))
            return val
        else:
            val = -((val ^ 0xffff) + 1)
            print("negative value: {:d} ".format(val)) 
            return val
        
    def getRawAccel(self):
        x_h = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_ACCEL_XOUT_H,1)[0]
        x_l = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_ACCEL_XOUT_L,1)[0]
        x_raw = self.bytesToInt(x_h,x_l)
        y_h = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_ACCEL_YOUT_H,1)[0]
        y_l = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_ACCEL_YOUT_L,1)[0]
        y_raw = self.bytesToInt(y_h,y_l)
        z_h = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_ACCEL_ZOUT_H,1)[0]
        z_l = self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_ACCEL_ZOUT_L,1)[0]
        z_raw = self.bytesToInt(z_h,z_l)
         
        if self.debug:
            print("Accelerometer: x: {:d}, y: {:d} z: {:d}".format(x_raw,y_raw,z_raw)) 
 
                                                                               
        return (x_raw,y_raw,z_raw)
    
    def getAccel(self):
        scale = self.getAccelFullScale()
        res = 2*scale/0x10000
        if self.debug:
            print("Accel scale: {:d}, resolution: {:f} bits/g".format(scale,1/res))
        x_raw, y_raw, z_raw = self.getRawAccel()
        if self.debug:
            print("accel x,y,z in [g]: {:f},{:f},{:f}".format(x_raw*res, y_raw*res, z_raw*res))
        return (x_raw*res, y_raw*res, z_raw*res)
    
    def getGyro(self):
        scale = self.getGyroFullScale()
        res = 2*scale / 0x10000
        print("Gyro scale: {:d}, resolution: {:f} bits/°/s".format(scale,1/res))
        x_raw, y_raw, z_raw = self.getRawGyro()
        print("gyro x,y,z in [°/s]: {:f},{:f},{:f}".format(x_raw*res, y_raw*res, z_raw*res))
        return (x_raw*res, y_raw*res, z_raw*res)
    
    def getRawGyro(self):
        x = self.bytesToInt(self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_GYRO_XOUT_H,1)[0],
                            self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_GYRO_XOUT_L,1)[0])
        y = self.bytesToInt(self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_GYRO_YOUT_H,1)[0],
                            self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_GYRO_YOUT_L,1)[0])
        z = self.bytesToInt(self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_GYRO_ZOUT_H,1)[0],
                            self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_GYRO_ZOUT_L,1)[0])        

        if self.debug:
            print("Gyroscope: x: {:d}, y: {:d} z: {:d}".format(x,y,z))

        return (x,y,z)
    
    def getTemperature(self):
        temp = self.bytesToInt(self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_TEMP_OUT_H,1)[0],
                               self.i2c.readfrom_mem(MPU6050_ADDR,MPU6050_TEMP_OUT_L,1)[0])
        if self.debug:
            print("Raw temperature value: {:d}".format(temp))
        temp = temp/340 + 36.53
        if self.debug:
            print("temperature: {:6.3f}".format(temp))
        return temp
    
mpu6050 = MPU6050(debug=True)
# print("bytes to int of 0x7f 0xff: {:d}".format(mpu6050.bytesToInt(0x7f,0xff)))
# print("bytes to int of 0xff 0xff: {:d}".format(mpu6050.bytesToInt(0xff,0xff)))

mpu6050.setConfig(184)
sleep_ms(10)
print("Config register value: 0x{:02x}".format(mpu6050.getConfig()))
mpu6050.setAccelFullScale(2)
print("full scale: ",mpu6050.getAccelFullScale())
print("Accel full scale: ",mpu6050.getAccelFullScale())
              
mpu6050.setAccelFullScale(2)
mpu6050.setGyroFullScale(250)
accel = mpu6050.getAccel()
gyro = mpu6050.getGyro()
sleep_ms(200)
mpu6050.setAccelFullScale(4)
mpu6050.setGyroFullScale(500)
accel = mpu6050.getAccel()
gyro = mpu6050.getGyro()
sleep_ms(200)
mpu6050.setAccelFullScale(8)
mpu6050.setGyroFullScale(1000)
accel = mpu6050.getAccel()
gyro = mpu6050.getGyro()
sleep_ms(200)
mpu6050.setAccelFullScale(16)
mpu6050.setGyroFullScale(2000)
accel = mpu6050.getAccel()
gyro = mpu6050.getGyro()
sleep_ms(200)

temp = mpu6050.getTemperature()
