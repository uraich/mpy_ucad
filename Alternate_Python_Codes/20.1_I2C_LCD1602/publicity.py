#!/opt/bin/lv_micropython
#
# Some publicity on the 2 line display
#
import sys,lcdDisplayClass
import time

pub = '''This is some
publicity for
the course on
the Internet 
of things (IoT)
at UCAD'''

lines = []
line = ""
i = 0
while i < len(pub):
    if pub[i] == "\n":
        for _ in range(16-len(line)):
            line += " "
        lines.append(line)
        line = ""
    else:
        line += pub[i]
    i += 1
for _ in range(16-len(line)):
    line += " "
lines.append(line)
# print(lines)

lcd = lcdDisplayClass.LcdDisplayClass()
lcd.setBacklight(True)

lcd.clear()

line_no = 0
while True:
#    lcd.clear()
    lcd.setDDramAddr(0)
    lcd.putS(lines[line_no])
    lcd.secondLine()
    if line_no == len(lines) - 1:
        lcd.putS(lines[0])
    else:
        lcd.putS(lines[line_no+1])
    time.sleep(1)
    line_no += 1
    if line_no == len(lines):
        line_no = 0
        
