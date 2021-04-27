#!/usr/bin/python3
#

from math import pi,sin

class PulseGenDisplay():
    pulse_shape = {'Rectangular' : 0,
                   'Triangular'  : 1,
                   'Sawtooth'    : 2,
                   'Sinusoidal'  : 3}

    frequencies = {'5 kHz':  0.2,
                   '2 kHz':  0.5,
                   '1 kHz':  1,
                   '500 Hz': 2,
                   '200 Hz': 5,
                   '100 Hz': 10}
    MAX_SIGNAL = 255
    MAX_VOLTAGE = 3.3
    
    def __init__(self):
        self.pulse_form = self.pulse_shape['Rectangular']
        self.pulse_height = 200   # pulse height in bits (8 bit resolution)
        self.pulse_T = 0.2        # 200 us sample frequency
        self.display_T = 0.2      # 200 us between samples
        self.pulse_data =[0]*50000
        self.display_data = [0]*500
        self.calib = self.MAX_VOLTAGE/self.MAX_SIGNAL

    def calc_pulse(self):
        data_length = int(10000*(1/self.pulse_T))
        print("pulse_T: {:f} data_length: {:d}".format(self.pulse_T,data_length))
        if self.pulse_form == self.pulse_shape['Rectangular']:
            print("Calculate rectangular wave form")
            T = 500
            j = 0
            for i in range(data_length):
                if j < 250:
                    self.pulse_data[i] = 0
                else:
                    self.pulse_data[i] = self.pulse_height
                j += 1
                if j >= 500:
                    j = 0
        elif self.pulse_form == self.pulse_shape['Sawtooth']:
            print("Calculate sawtooth wave form")
            j = 0
            value = 0
            increment = self.pulse_height / 500
            for i in range(data_length):
                self.pulse_data[i] = int(value)
                j += 1
                if j < 500:
                    value += increment
                else:
                    value = 0
                    j = 0
        elif self.pulse_form == self.pulse_shape['Triangular']:
            print("Calculate triangular wave form")
            j = 0
            value = 0
            increment = self.pulse_height / 250
            for i in range(data_length):
                self.pulse_data[i] = int(value)
                j += 1
                if j < 250:
                    value += increment
                elif j >= 250 and j < 500:
                    value -= increment
                else:
                    j = 0
                    value = 0
        elif self.pulse_form == self.pulse_shape['Sinusoidal']:
            print("Calculate sine wave")
            j = 0
            for i in range(data_length):
                self.pulse_data[i] = (sin(2*j*pi/500) + 1)*(self.pulse_height/2)
                j += 1
                if j >=500:
                    j = 0

    def get_display_data(self):

        pulse_index = 0
        
        if self.display_T < self.pulse_T:
            # one DAC sample results in several ADC samples
            increment = self.pulse_T/self.display_T
            print("No of samples with same value: ",increment)
            pulse_index = 0
            if increment > 25:
                print("Results in to few display points")
                return
            display_index = 0
            pulse_index   = 0
            next_point = display_index + increment
            while True:
                self.display_data[display_index] = self.pulse_data[pulse_index]
                display_index += 1
                if display_index >= 500:
                    break;
                if display_index >= next_point:
                    pulse_index += 1
                    next_point += increment
                    # print("display_index: {:d} next_point: {:d}".format(display_index,int(next_point)))
        else:
            # skip a number of sample points for display
            d = self.display_T/self.pulse_T
            print("no of samples to be skipped: ",d)
            for display_index in range(500):
                pulse_index = int(display_index*d)
                # print("pulse_index: ",pulse_index)
                self.display_data[display_index] = self.pulse_data[pulse_index]   

        '''
        f = open("pulse_data.txt","w")
        for i in range(500):
            f.write(str(self.display_data[i]) + "\n")
        f.close()
        '''
        
    def set_pulse_T(self,pulse_T): # time between samples in ms
        print("set_pulseT to ", pulse_T) 
        self.pulse_T = pulse_T
        
    def set_display_T(self,display_T): # time between samples on display in ms
        print("set_displayT to ", display_T) 
        self.display_T = display_T

    def set_pulse_shape(self,shape):
        self.pulse_form = self.pulse_shape[shape]
        
if __name__ == "__main__":
    pgd = PulseGenDisplay()
    pgd.set_pulse_shape('Triangular')
    #pgd.calc_pulse()
    #pgd.get_display_data()
    pgd.set_pulse_T(5)
    pgd.calc_pulse()
    pgd.get_display_data()
    #pgd.set_pulse_T(20)
    #pgd.calc_pulse()
