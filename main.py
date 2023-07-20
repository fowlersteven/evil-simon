from machine import Pin, PWM
import utime
import random

# setup ins and outs:
btn_green   = Pin(12, Pin.IN, Pin.PULL_UP)
btn_yellow  = Pin(14, Pin.IN, Pin.PULL_UP)
btn_red     = Pin(26, Pin.IN, Pin.PULL_UP)
btn_blue    = Pin(28, Pin.IN, Pin.PULL_UP)

sw1 = Pin(7, Pin.IN, Pin.PULL_UP)
sw2 = Pin(8, Pin.IN, Pin.PULL_UP)
sw3 = Pin(9, Pin.IN, Pin.PULL_UP)
sw4 = Pin(10, Pin.IN, Pin.PULL_UP)

led_green   = Pin(13, Pin.OUT)
led_yellow  = Pin(15, Pin.OUT)
led_red     = Pin(27, Pin.OUT)
led_blue   = Pin(29, Pin.OUT)

led_green.value(0)
led_yellow.value(0)
led_red.value(0)
led_blue.value(0)

musicnotes = [262, 330, 392, 494]

# MAX_DUTY    = 32512
# PART_DUTY   = 16256
# CHORD_DUTY  = 8128
# OFF_DUTY    = 0

MAX_DUTY    = 1200
PART_DUTY   = 1200
CHORD_DUTY  = 945
OFF_DUTY    = 0

note_green  = PWM(Pin(0))
note_green.freq(musicnotes[0])
note_green.duty_u16(OFF_DUTY)

note_yellow = PWM(Pin(2))
note_yellow.freq(musicnotes[1])
note_yellow.duty_u16(OFF_DUTY)

note_red    = PWM(Pin(4))
note_red.freq(musicnotes[2])
note_red.duty_u16(OFF_DUTY)

note_blue   = PWM(Pin(6))
note_blue.freq(musicnotes[3])
note_blue.duty_u16(OFF_DUTY)

pwmlist = [note_green, note_yellow, note_red, note_blue]
ledlist = [led_green, led_yellow, led_red, led_blue]
btnlist = [btn_green, btn_yellow, btn_red, btn_blue]
swslist = [sw1, sw2, sw3, sw4]

seed = None

def displayLoseSplash():
    hertzarray = [
                    392,
                    370, 
                    349,
                    330,
                    311,
                    294,
                    277,
                    262
                ]
    timearray = [
                    160,
                    160,
                    160,
                    160,
                    160,
                    160,
                    160,
                    1440
                ]
    
    for i in range(8):
        note_green.freq(hertzarray[i])
        note_green.duty_u16(MAX_DUTY)
        ledlist[i%4].value(1)
        utime.sleep_ms(timearray[i])
        ledlist[i%4].value(0)
        
    note_green.freq(musicnotes[0])
    note_green.duty_u16(OFF_DUTY)

def displayEvilLoseSplash():
    
    evil_notes1 = [440, 659, 3136]
    evil_notes2 = [933, 1047, 3136]
    
    for i in range(5):
        for j in range(3):
            pwmlist[j].freq(evil_notes1[j])
            pwmlist[j].duty_u16(32512)
        for k in ledlist:
            k.value(1)
        
        utime.sleep_ms(500)

        for j in range(3):
            pwmlist[j].freq(evil_notes2[j])
            pwmlist[j].duty_u16(32512)
        for k in ledlist:
            k.value(0)
        
        utime.sleep_ms(500)

    for i in range(len(pwmlist)):
        pwmlist[i].duty_u16(OFF_DUTY)
        pwmlist[i].freq(musicnotes[i])
    utime.sleep_ms(500)
    
def displayStartSplash():
    beats_ms = 160
    notes_array = [
                    [1, 0, 0, 0], 
                    [0, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],

                    [1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 1],

                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 0, 0],

                    [0, 0, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],

                    [0, 0, 1, 1], 
                    [0, 0, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],

                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],

                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],

                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],

                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                 ]
    

    for i in notes_array:
        count = 0
        duty = 0

        for j in i:
            if j == 1:
                count = count +1

        if count == 0:
            duty = OFF_DUTY
        elif count == 1:
            duty = MAX_DUTY
        elif count == 2:
            duty = PART_DUTY
        else:
            duty = CHORD_DUTY
        
        for k in range(len(i)):
            if i[k] == 1:
                pwmlist[k].duty_u16(duty)
                ledlist[k].value(1)
            else:
                pwmlist[k].duty_u16(OFF_DUTY)
                ledlist[k].value(0)

        utime.sleep_ms(beats_ms)

    for s in pwmlist:
        s.duty_u16(OFF_DUTY)

    for r in ledlist:
        r.value(0)

def buttonPressed(btn):
    if btn.value() == 0:
        utime.sleep_ms(20)
        if btn.value() == 0:
            
            return True
    
    return False

def waitForInitiation():
    while True:
        for i in btnlist:
            if buttonPressed(i):
                seed = utime.ticks_ms
                for i in range(4):
                    for i in ledlist:
                        i.value(1)
                    utime.sleep_ms(160)
                    for i in ledlist:
                        i.value(0)
                    utime.sleep_ms(160)
                return

def determineVictory(expected):
    
    BTN_PLAY_TIME = 110
    BTN_PAUSE_TIME = 110
    
    while True:
        for i in range(len(btnlist)):
            if buttonPressed(btnlist[i]):
                #play music and light up light
                playSoundAndLight(BTN_PLAY_TIME, BTN_PAUSE_TIME, i)
                
                # check for correctness of button press and return True or False
                if i == expected:
                    return True
                return False

def playSoundAndLight(playtime, pausetime, index):
    ledlist[index].value(1)
    pwmlist[index].duty_u16(MAX_DUTY)
    utime.sleep_ms(playtime)
    ledlist[index].value(0)
    pwmlist[index].duty_u16(OFF_DUTY)
    utime.sleep_ms(pausetime)
    
def gameLoop():
    
    PLAY_TIME_MS = 155
    WAIT_TIME_MS = 190
    random.seed(seed)
    
    while True:   
        
        gamelist = []
        gamelist.append(random.randint(0,3))
        victory_condition = True
        while victory_condition:
            utime.sleep_ms(500)
            for i in gamelist:
                playSoundAndLight(PLAY_TIME_MS, WAIT_TIME_MS, i)
            for i in gamelist:
                if not determineVictory(i):
                    victory_condition = False
                    break
            if not victory_condition:
                updateHighScore(len(gamelist))
                utime.sleep_ms(50)
                displayLoseSplash()
                utime.sleep_ms(250)
                
            gamelist.append(random.randint(0,3))
            
def evilGameLoop():
    
    PLAY_TIME_MS = 155
    WAIT_TIME_MS = 190
    random.seed(seed)
    
    while True:   
        
        gamelist = []
        gamelist.append(random.randint(0,3))
        victory_condition = True
        while victory_condition:
            utime.sleep_ms(500)
            for i in gamelist:
                playSoundAndLight(PLAY_TIME_MS, WAIT_TIME_MS, i)
            for i in gamelist:
                if not determineVictory(i):
                    victory_condition = False
                    break
            if not victory_condition:
                updateHighScore(len(gamelist))
                utime.sleep_ms(50)
                displayEvilLoseSplash()
                utime.sleep_ms(250)
                
            gamelist.append(random.randint(0,3))
    
def updateHighScore(score):
    print(score)

def startSimon():
    displayStartSplash()
    waitForInitiation()
    gameLoop()

def startEvilSimon():
    displayStartSplash()
    waitForInitiation()
    evilGameLoop()

def startBloopySynth():
    while True:
        determineVictory(0)

def main():
    
    startup_vals = ''

    for i in swslist:
        startup_vals += str(abs(i.value()-1))

    mode_selection = int(startup_vals, 2)
    
    if mode_selection == 0:
        startSimon()
    if mode_selection == 1:
        startBloopySynth()
    if mode_selection == 2:
        pass
    if mode_selection == 3:
        pass
    if mode_selection == 4:
        pass
    if mode_selection == 5:
        pass
    if mode_selection == 6:
        pass
    if mode_selection == 7:
        pass
    if mode_selection == 8:
        pass
    if mode_selection == 9:
        pass
    if mode_selection == 10:
        pass
    if mode_selection == 11:
        pass
    if mode_selection == 12:
        pass
    if mode_selection == 13:
        pass
    if mode_selection == 14:
        pass
    if mode_selection == 15:
        displayEvilLoseSplash()


    
main()