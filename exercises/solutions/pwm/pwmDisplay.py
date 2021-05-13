import array
import dht11Raw
import uos
from machine import Pin,PWM

#initialize the array to 32 zeros
pwmData =  array.array("I",[0]*32)

# check if the data directory exists, if not, create it
try:
    uos.stat("/data")
except OSError as e:
    if len(e.args) > 0 and e.args[0] == errno.ENOENT:
        print("/data does not exist, creating it")
        uos.mkdir("/data")
        
# open the file /data/pwm.txt

f = open("/data/pwm.txt","w")

pwmSource = PWM(Pin(18), freq=10000, duty=920)

pwmSampler= Pin(19)

dht11Raw.dht11ReadRaw(pwmSampler,pwmData)

for i in range(32):
    # the 'new' way of formatting the number
    dataString = '0x{:08x}\n'.format(pwmData[i])
    print(dataString,end="")
    # the 'old' way of formatting
    # dataString="0x%08x"%dht11Data[i]
    f.write(dataString)
f.close()
