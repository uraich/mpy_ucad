#
# Solution de l'exercice_2: Flowing Digit
# Le programme utilise la classe HexDigit pour:
# * afficher un nombre en hex
# * afficher un nombre den décimale
# * faire tourner une serie de digits 0..f (Flowing Digit)
# U. Raich 4. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from hexDisplay import HexDisplay

hexDisplay = HexDisplay()
hexDisplay.clear()
'''
for i in range(4):
    hexDisplay.clear()
    hexDisplay.showHexDigit(i,8)
    sleep_ms(500)
hexDisplay.clear()
'''
print("1234 in hex= 0x{:x}".format(1234))
for i in range(100):
    hexDisplay.showHexValue(1234)

print("1234 in dec= 0x{:d}".format(1234))
for i in range(100):
    hexDisplay.showDecValue(1234)
    
base = 0
while True:
    for i in range(16):
        if base > 15:
            base = 0
        value = base << 12 | ((base+1) % 16) << 8 | ((base+2) % 16) << 4 | (base+3) % 16
        base += 1

        for tim in range(25):       # showDigit takes 20 ms, we therefore show the number for 500 ms
            hexDisplay.showHexValue(value)


