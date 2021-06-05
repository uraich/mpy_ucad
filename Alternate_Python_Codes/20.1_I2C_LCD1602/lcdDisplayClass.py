# This is the Python module implementing access to the Hitachi hd44780
# 2-line LCD display
# U. Raich UCC, Nov. 2017
# adapted to MicroPython, 5.Jun. 2021

import sys
from utime import sleep_ms
from machine import Pin,I2C

class LcdDisplayClass:
    I2C_BUS                =    1
    I2C_SDA                =   21
    I2C_SCL                =   22
    HD44780_ADDRESS        = 0x3f
    
    HD44780_CLEAR          = 0x01
    HD44780_HOME           = 0x02
    HD44780_ENTRY_MODE     = 0x04
    HD44780_CURSOR_DIR     = 0x02
    HD44780_CURSOR_SHIFT   = 0x10
    HD44780_DISPLAY_CURSOR = 0x08
    HD44780_DISPLAY_ON     = 0x04
    HD44780_DISPLAY_OFF    = 0x00
    HD44780_CURSOR_ON      = 0x02
    HD44780_CURSOR_OFF     = 0x00
    HD44780_CURSOR_BLINK   = 0x01
    HD44780_CURSOR_NOBLINK = 0x00

    HD44780_ENTIRE_DISPLAY = 0x04
    HD44780_CURSOR_ONOFF   = 0x02
    HD44780_BLINK          = 0x01
    HD44780_CURSOR         = 0x10
    HD44780_1_LINE         = 0x00
    DH44780_CURSOR_MOVE    = 0x00
    DH44780_DISPLAY_SHIFT  = 0x08
    DH44780_SHIFT_LEFT     = 0x00
    DH44780_SHIFT_RIGHT    = 0x04

    HD44780_FUNCTION       = 0x20
    
    HD44780_8_BIT_MODE     = 0x10
    HD44780_4_BIT_MODE     = 0x00
    HD44780_TWO_LINES      = 0x08
    HD44780_5x10_FONT      = 0x04
    HD44780_5x8_FONT       = 0x00
    HD44780_1_LINE         = 0x00
    HD44780_2_LINE         = 0x08
    HD44780_CURSOR_DEC     = 0x00
    HD44780_CURSOR_INC     = 0x02
    HD44780_DISPLAY_SHIFT  = 0x01
    
    HD44780_CGRAM_AHDR     = 0x10
    HD44780_HDRAM_AHDR     = 0x20
    HD44780_BUSY_FLAG      = 0x40

    HD44780_BL             = 0x08
    HD44780_BL_SHIFT       = 0x03

    HD44780_EN             = 0x04
    HD44780_READ           = 0x02
    HD44780_WRITE          = 0x00
    HD44780_CMD_REG        = 0x00
    HD44780_DATA_REG       = 0x01

    HD44780_SET_DDRAM      = 0x80
    HD44780_SET_CGRAM      = 0x40
    HD44780_2ND_LINE       = 0x40

    HD44780_INCREMENT      = True
    HD44780_DECREMENT      = False
    HD44780_ON             = True
    HD44780_OFF            = False

    HD44780_SUCCESS        = 0
    HD44780_MAX_STRLEN     = 16


    # pinout for 20x2 LCD via PCF8574AN:
    # ----------
    # 0x80    P7 -  - D7
    # 0x40    P6 -  - D6
    # 0x20    P5 -  - D5
    # 0x10    P4 -  - D4
    # -----------
    # 0x08    P3 -  - BL   Backlight (LCD has 3 RGB LEDs - common anode)
    # 0x04    P2 -  - EN   Starts Data read/write
    # 0x02    P1 -  - RW   low: write, high: read
    # 0x01    P0 -  - RS   Register Select: 0: Instruction Register (IR) (AC when read), 
    #                                       1: data register (DR)

    backlight =  1                      # backlight is on by default
    i2c       = -1
    sda       = 22
    scl       = 21
    
    def __init__(self,debug=False):
        #
        # open the I2C bus driver
        #
        self.i2c = None
        self.debug = debug
        i2c = I2C(self.I2C_BUS,scl=Pin(self.I2C_SCL),sda=Pin(self.I2C_SDA))
        addr = i2c.scan()
        if self.debug:
            print("I2C addresses found: ",addr)
        if not self.HD44780_ADDRESS in addr:
            print("Cannot find the HD44780 on the I2C bus\nIs it connected?")
            sys.exit()
        else:
            print("HD44780 was found on the I2C bus, continuing...")
            self.i2c = i2c
        #
        # initialize the controller following the init procdure described in the data sheet
        #
        cmd = self.HD44780_FUNCTION | self.HD44780_8_BIT_MODE | self.HD44780_BL

        if self.debug:
            print("in init: sending: 0x{:02x} to HD44780 at I2C address 0x{:02x}".format(
                cmd,self.HD44780_ADDRESS))
        
        for index in range(0,5):
            self.write_hd44780(cmd)

            self.__strobe__(self.HD44780_CMD_REG)
            sleep_ms(5)      # sleep for 5 ms
        #
        # now initialize the hd44780 and set it to 4 bit mode
        # this is still done in 8 bit mode and the command must be repeated
        # in order to set 5x8 pixel characters in 4 bit mode
        #
        cmd = self.HD44780_FUNCTION | self.HD44780_4_BIT_MODE | self.HD44780_BL;
        if self.debug:
            print("in init: sending: 0x{:02x}".format(cmd)) 
        self.write_hd44780(cmd)
        self.__strobe__(self.HD44780_CMD_REG)
        #
        # repeat the command, now in 4 bit mode
        #
        cmd = self.HD44780_FUNCTION | self.HD44780_4_BIT_MODE | self.HD44780_5x8_FONT | self.HD44780_2_LINE;
        #
        # from now on use the class methods to write the command register
        #
        self.__writeCmd__(cmd)
        
        self.display(False)

        self.clear()

        self.home()

        if self.debug:
            print("================== init: Initilization completed ==============================")

        retCode = self.readBusy()
        if self.debug:
            print("in init: reading busy and address: ",retCode) 
        if (retCode & 0x80):
            print("in init: still busy")

        retCode = self.display(True)

    def setDebug(onOff):
        self.debug=onOff
        
    def close(self):
        # nothing to do in MicroPython
        return


    def write_hd44780(self,data):
        if self.debug:
            print("write_hd44780: 0x{:02x}".format(data))
        self.i2c.writeto(self.HD44780_ADDRESS,data.to_bytes(1,"big"))

    def read_hd44780(self):
        readBack = self.i2c.readfrom(self.HD44780_ADDRESS,1)[0]
        if self.debug:
            print("read_hd44780: 0x{:02x}".format(readBack))
        return readBack
        
    #
    # control and save the state of the backlight
    #
    def setBacklight(self,onOff):

        readBack = self.i2c.readfrom(self.HD44780_ADDRESS,1)[0]

        if (onOff):
            readBack |= self.HD44780_BL
            self.backlight = 1
        else:
            readBack &= ~self.HD44780_BL;
            self.backlight = 0;
        self.i2c.writeto(self.HD44780_ADDRESS,readBack.to_bytes(1,"big"))
        
    #
    # local function to strobe data into the hd44780 controller
    #
    def __strobe__(self,register):

        readBack = self.read_hd44780()
        if self.debug:
            print("in strobe: readback: 0x{:02x}".format(readBack))
            print("register: 0x{:02x}".format(register))
 
        tmp = self.backlight << self.HD44780_BL_SHIFT
        if self.debug:
            print("backlight: 0x{:02x}".format(self.backlight))
            print("after shift: 0x{:02x}".format(tmp))
            print("readback + backlight: 0x{:02x}".format(readBack | self.backlight << self.HD44780_BL_SHIFT))
        readBack = readBack | self.HD44780_EN | self.backlight << self.HD44780_BL_SHIFT | register
        #
        # send the data with strobe set high
        #
        if self.debug:
            print("in strobe: sending: 0x{:02x}".format(readBack))
        self.write_hd44780(readBack)
        sleep_ms(1)        
    #
    # send the data with strobe set low
    #
        readBack = (readBack | self.backlight << self.HD44780_BL_SHIFT | register) & ~self.HD44780_EN
        if self.debug:
            print("in strobe: sending: 0x{:02x}".format(readBack))        
        self.write_hd44780(readBack)
        sleep_ms(1)               
    #
    # write a character to the lcd display
    #
    def putC(self,character):

        if self.debug:
            print("in putC: writing character:",character)
        if not self.i2c:
            printf("I2C bus is not initialized yet")
            return
        #
        # first treat the higher character nibble
        #
        #        print("H: ",format(ord(character),'04x'))
        #        print("in putC: backlight: ",self.backlight)
        pcfc = (ord(character) &0xf0) | self.backlight << self.HD44780_BL_SHIFT | self.HD44780_WRITE |  self.HD44780_DATA_REG;
        if self.debug:
            print("high nibble: ",format(pcfc,'02x'))

        self.i2c.writeto(self.HD44780_ADDRESS,pcfc.to_bytes(1,"big"))
        self.__strobe__(self.HD44780_DATA_REG)
        sleep_ms(1)         # wait for 1ms

        #
        # then the lower nibble
        #
        if self.debug:
            print("shifted by 4: ",format(pcfc,'04x'))
        pcfc = (ord(character) <<4) &0xf0 | self.backlight << self.HD44780_BL_SHIFT | self.HD44780_WRITE |  self.HD44780_DATA_REG;
        if self.debug:
            print("low nibble: ",format(pcfc,'02x'))
        self.i2c.writeto(self.HD44780_ADDRESS,pcfc.to_bytes(1,"big"))
        self.__strobe__(self.HD44780_DATA_REG)
        sleep_ms(1)          # wait for 1ms

    #
    # write a string of characters to the display
    #
    def putS(self,textString): 
        if len(textString) > self.HD44780_MAX_STRLEN:
            textString = textString[0:self.HD44780_MAX_STRLEN]
        if self.debug:
            print ("in putS: the string to be put to the display: ",textString);
        for index in range(0,len(textString)):
            self.putC(textString[index])                         
    #
    # write a command to the command register
    #
    def __writeCmd__(self,cmd):
        if not self.i2c:
            print("I2C bus not initialized yet")
            return
        #
        # this is for the high nibble
        #
        pcfCmd = (cmd &0xf0) | self.backlight << self.HD44780_BL_SHIFT | self.HD44780_WRITE | self.HD44780_CMD_REG;
        if self.debug:
            print("writeCmd: sending high nibble: 0x{:02x}".format(pcfCmd))
        self.write_hd44780(pcfCmd)
        self.__strobe__(self.HD44780_CMD_REG)
        #
        # and here for the low nibble
        #
        pcfCmd = (cmd << 4) & 0xf0 | self.backlight << self.HD44780_BL_SHIFT | self.HD44780_WRITE | self.HD44780_CMD_REG;
        if self.debug:
            print("writeCmd: sending low nibble: 0x",format(pcfCmd,'02x'))         
        self.i2c.writeto(self.HD44780_ADDRESS,pcfCmd.to_bytes(1,"big"))
        self.__strobe__(self.HD44780_CMD_REG)
        sleep_ms(1)          # wait for 1 ms

    #
    # read a byte from the hd44780 command register in 4 bit mode
    # the high nibble is read first 
    #
    def read(self,register):

        if not self.i2c:
            print("in read: the I2C bus is not initilized yet")
            return
        cmd =  0xf0 |self.backlight << self.HD44780_BL_SHIFT| self.HD44780_READ | register;
        self.i2c.writeto(self.HD44780_ADDRESS,cmd.to_bytes(1,"big"))        
        cmd |= self.HD44780_EN
        #
        # set enable high
        #
        self.i2c.writeto(self.HD44780_ADDRESS,cmd.to_bytes(1,"big")) 
        #
        # read high nibble
        #
        highNibble = self.i2c.readfrom(self.HD44780_ADDRESS,1)[0]

        #
        # bring enable down again
        #
        cmd &= ~self.HD44780_EN
        self.i2c.writeto(self.HD44780_ADDRESS,cmd.to_bytes(1,"big"))       
        #
        # enable high again
        #
        cmd |= self.HD44780_EN;
        self.i2c.writeto(self.HD44780_ADDRESS,cmd.to_bytes(1,"big"))               
        #
        # read low nibble
        #
        lowNibble = self.i2c.readfrom(self.HD44780_ADDRESS,1)[0]

        #
        # bring enable down again
        #
        cmd &= ~self.HD44780_EN
        self.i2c.writeto(self.HD44780_ADDRESS,cmd.to_bytes(1,"big"))               
        return(highNibble & 0xf0) | lowNibble >> 4
    
    #
    # clear the display
    #
    def clear(self):
        cmd = self.HD44780_CLEAR  
        retCode = self.__writeCmd__(cmd)
        return retCode
    #
    # switch the display on or off
    #
    def display(self,onOff):
        cmd = self.HD44780_DISPLAY_CURSOR
        if (onOff):
            cmd |= self.HD44780_DISPLAY_ON
        retCode = self.__writeCmd__(cmd)
        return retCode
    #
    # home the cursor
    #
    def home(self):
         cmd = self.HD44780_HOME
         retCode = self.__writeCmd__(cmd)
         return retCode

     #
     # read the busy flag
     #
    def readBusy(self):
        retCode = self.read(self.HD44780_CMD_REG)
        return retCode

    #
    # set up the address register
    #
    def setDDramAddr(self,address):
        if  address > 80:
            print("setDDramAddr: addresses 0..80 allowed")
            return
        cmd = self.HD44780_SET_DDRAM | address
        self.__writeCmd__(cmd)
    
    #
    # setting up the address register to write to the second line
    #
    def secondLine(self):
        self.setDDramAddr(self.HD44780_2ND_LINE)

    #
    # define the entry mode
    #
    def entry(self,incDec,shift):
        cmd = self.HD44780_ENTRY_MODE
        #
        # here for increment / decrement
        #
        if incDec == 'inc':
            # print("in entry: increment")
            cmd |= self.HD44780_CURSOR_INC
        elif incDec == "dec":
            # print("in entry: decrement")
            pass
        else:
            print("in entry: increment/decrement mode ",incDec," is unknown. Skipping...")
        #
        # here for shift
        #
        if shift == 'shift':
            if self.debug:
                print("in entry: setting to shift mode")
            cmd |= self.HD44780_DISPLAY_SHIFT
        elif shift == '':
            if self.debug:
                print("in entry: not shifting")
            pass
        else:
            print("in entry: shift mode ",shift," unknown. Skipping...")
        self.__writeCmd__(cmd)
    #
    # cursor definitions
    #
    def cursor(self,onOff,blink):
        cmd = self.HD44780_DISPLAY_CURSOR
        #
        # on or off
        #
        if onOff == 'on':
            cmd |= self.HD44780_CURSOR_ON
        elif onOff == 'off':
            pass
        else:
            printf("in cursor: cursor mode ",onOff," unknown. Skipping...")
        #
        # blinking or steady
        #
        if blink == 'blink':
            cmd |= self.HD44780_CURSOR_BLINK
        elif blink == 'steady':
            pass
        else:
            printf("in cursor: cursor blinking mode ",blink," unknown. Skipping...")
        self.__writeCmd__(cmd)
        
    #
    # user defined character
    #
    def userChar(self,address,dotMatrix):
        #
        # write the address of the cgram (character generator RAM)
        #
        if address < 0 or address > 0x0f<<3:
            print("in userChar: illegal address. Skipping...")
            return
        if len(dotMatrix) != 7:
            print("in userChar: dot Matrix needs 7 dot lines. Not writing!")
            return

    #
    # read the current address of the ddram
    #
        ddramAddress = self.readBusy() & 0x7f
        # setup the cgram address
        if self.debug:
            print("in userChar: ",format(address,'02x'))
        cmd = self.HD44780_SET_CGRAM | address
        self.__writeCmd__(cmd)
        # now we can write the dot matrix

        for index in range(0,7):
            if self.debug:
                print("in userChar: line[",index,"] =0x"+format(dotMatrix[index],'02x'))
            self.putC(chr(dotMatrix[index]))
        cmd = self.HD44780_SET_DDRAM | ddramAddress
        self.__writeCmd__(cmd)
                          
