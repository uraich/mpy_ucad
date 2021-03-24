from machine import Pin,PWM
from utime import sleep_ms
import uos as os
from rtttl import RTTTL
import songs

BUTTON_PIN   = 22
BUZZER_PIN   = 18
MAX_SONG     = 100
PUSHED       = 0
RELEASED     = 1

btn     = Pin(BUTTON_PIN, Pin.IN,Pin.PULL_UP)
speaker = PWM(Pin(BUZZER_PIN))
speaker.duty(0)

songList={
    1:'Super Mario - Main Theme',
    2:'Super Mario - Title Music',
    3:'SMBtheme',
    4:'SMBwater',
    5:'SMBunderground',
    6:'The Simpsons',
    7:'Indiana',
    8:'TakeOnMe',
    9:'Entertainer',
    10:'Muppets',
    11:'Xfiles',
    12:'Looney',
    13:'20thCenFox',
    14:'Bond',
    15:'MASH',
    16:'StarWars',
    17:'GoodBad',
    18:'TopGun',
    19:'A-Team',
    20:'Flinstones',
    21:'Jeopardy',
    22:'Smurfs',
    23:'MahnaMahna',
    24:'LeisureSuit',
    25:'MissionImp'
}

def play_tone(freq, msec):
    # print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    # print("Freq: %6.1f, duration: %6.1f"%(freq,msec))
    if freq > 0:
        speaker.freq(int(freq))     # Set frequency
        speaker.duty(512)           # 50% duty cycle
    sleep_ms(int(msec))             # Play for a number of msec
    speaker.duty(0)                 # Stop playing
    sleep_ms(50)                    # Delay 50 ms between notes

song_numbers = os.urandom(100)
cnt = 0
print("Push the button to sound the door bell")
while True:
    if btn.value() == PUSHED:
        song_nr = int(int(song_numbers[cnt])/10.21) +1
        songName = songList.get(song_nr)
        print("Play song ",songName)
        sleep_ms(20)                # debounce switch
        # play the song
        tune = RTTTL(songs.find(songName))
        for freq, msec in tune.notes():
            play_tone(freq, msec)
        cnt += 1
        if cnt > 99:
            songs = os.urandom(100)
            cnt = 0

        while True:
            if btn.value() != RELEASED:
                sleep_ms(20)         # debounce switch
            else:
                sleep_ms(20)
                break;

