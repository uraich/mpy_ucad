#
# This is the Python module testing access to the Hitachi hd44780
# 2-line LCD display
# U. Raich UCC, Nov.2017

import sys,lcdDisplayClass
import time

lcd = lcdDisplayClass.LcdDisplayClass()
lcd.setBacklight(True)

lcd.clear()
lcd.putS('Hello World!')
lcd.secondLine()

#
# create the negative bar characters
#
# xxxxx xxxxx xxxxx xxxxx xxxxx xxxxx xxxxx
# ----- xxxxx xxxxx xxxxx xxxxx xxxxx xxxxx
# ----- ----- xxxxx xxxxx xxxxx xxxxx xxxxx
# ----- ----- ----- xxxxx xxxxx xxxxx xxxxx
# ----- ----- ----- ----- xxxxx xxxxx xxxxx
# ----- ----- ----- ----- ----- xxxxx xxxxx
# ----- ----- ----- ----- ----- ----- xxxxx

#---------------------------------------------------------------------------
# Unfortunately the display only allows to program 8 user defined characters
#---------------------------------------------------------------------------

##barMinusChar=[]
##bar=[]
##index=0
##for index in range(0,7):
##    for height in range(0,7):
##        if height > index:
##            bar.append(0xe0)
##        else:
##            bar.append(0xff)
##    print("bar: ",bar)    
##    barMinusChar.append(bar)
##    bar=[]
##print("all chars: ",barMinusChar)
##
#
# create the positive bar characters
#
# ----- ----- ----- ----- ----- ----- xxxxx
# ----- ----- ----- ----- ----- xxxxx xxxxx
# ----- ----- ----- ----- xxxxx xxxxx xxxxx
# ----- ----- ----- xxxxx xxxxx xxxxx xxxxx
# ----- ----- xxxxx xxxxx xxxxx xxxxx xxxxx
# ----- xxxxx xxxxx xxxxx xxxxx xxxxx xxxxx
# xxxxx xxxxx xxxxx xxxxx xxxxx xxxxx xxxxx
#
barPlusChar=[]
bar=[]
index=0
for index in range(0,7):
    for height in range(0,7):
        if height >= index:
            bar.append(0xff)
        else:
            bar.append(0xe0)
#    print("bar: ",bar)    
    barPlusChar.insert(0,bar)
    bar=[]
#    print("all chars: ",barPlusChar)

for index in range(0,7):
#    print(" index for plus bars: ",index)
    lcd.userChar(index << 3, barPlusChar[index])
    
#for index in range(0,7):
#    lcd.userChar((index+7) << 3, barMinusChar[index])

for index in range(0,7):
    lcd.putC(chr(index))

for index in range(0,7):
    lcd.putC(chr(6-index))
    
time.sleep(5)
#
# now print Hello World in English and in Russian
#
lcd.clear()
time.sleep(0.1)
russian_P=[0xff,0xf1,0xf1,0xf1,0xf1,0xf1,0xf1]
russian_i=[0xf1,0xf1,0xf3,0xf5,0xf9,0xf1,0xf1]

lcd.userChar(0x0e<<3,russian_P)
lcd.userChar(0x0f<<3,russian_i)

lcd.putS('Hello World!')
lcd.secondLine()

russian_P=chr(0x0e)
russian_i=chr(0x0f)

russianHelloWorld=russian_P+"p"+russian_i+"Bet M"+russian_i+"p!"
#print(russianHelloWorld)
lcd.putS(russianHelloWorld)

lcd.entry('inc','')
#lcd.cursor('on','blink')
lcd.close()
