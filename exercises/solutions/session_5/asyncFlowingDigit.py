#
# Solution de l'exercice_3: Flowing Digit avec asyncio co-routine
#
# U. Raich 4. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from asyncHexDisplay import HexDisplay
import uasyncio as asyncio

async def main():
    hexDisplay = HexDisplay()
    # hex counter
    for value in range(100):
        # print("main")
        hexDisplay.setHexValue(value)
        await asyncio.sleep_ms(500)
    # decimal counter
    for value in range(100):
        # print("main")
        hexDisplay.setDecValue(value)
        await asyncio.sleep_ms(500)
    # Flowing Digit
    base = 0
    while True:
        for i in range(16):
            if base > 15:
                base = 0
            value = base << 12 | ((base+1) % 16) << 8 | ((base+2) % 16) << 4 | (base+3) % 16
            base += 1
            hexDisplay.setHexValue(value)
            await asyncio.sleep_ms(500)

asyncio.run(main())
