#
# the main program reading out the IR controller
# copyright U. Raich 6.May 2021
# 
# This program is part of the course on IoT
# at the Université Cheikh Anta Diop, Dakar, Senegal
# It is released under the MIT license
from ir import IR
ir = IR(21)
IR_code = {0xff6897 : "0", 0xff30cf : "1", 0xff18e7 : "2", 0xff7a85 : "3", 0xff10ef : "4",
           0xff38c7 : "5", 0xff5aa5 : "6", 0xff42bd : "7", 0xff4ab5 : "8", 0xff52ad : "9",
           0xffa25d : "CH-", 0xff629d : "CH", 0xffe21d : "CH+", 0xff22dd : "|<<", 0xff02fd : "|>>", 0xffc23d : ">||",
           0xffe01f: "-", 0xffa857 : "+", 0xff906f : "EQ", 0xff9867 : "100+", 0xffb04f : "200+"}

print("Ready to receive IR commands")
while True:
    irValue = ir.read()
    if irValue:
        print("length of timeList: %d"%len(ir.timeList))
        print(ir.bitBuffer)
        print(ir.timeList)
        print(hex(irValue))
        print("key: " + IR_code[irValue])
