import time

# Spare code copied from maibadge, for any maimai fans interested, i made a derakuma bear a while back with these
# if you want to buy message me on discord/ telegram lmao

def buzz_funcs(hw_state):
    def buzz_on(freq, duty=32767):
      if freq > 0:
        hw_state["buzzer"].frequency = freq
        hw_state["buzzer"].duty_cycle = duty
    def buzz_off():
        hw_state["buzzer"].duty_cycle = 0
    return buzz_on, buzz_off

tones = {
    "0":0,
    'C0':16,'C#0':17,'D0':18,'D#0':19,'E0':21,'F0':22,'F#0':23,'G0':24,'G#0':26,'A0':28,'A#0':29,'B0':31,
    'C1':33,'C#1':35,'D1':37,'D#1':39,'E1':41,'F1':44,'F#1':46,'G1':49,'G#1':52,'A1':55,'A#1':58,'B1':62,
    'C2':65,'C#2':69,'D2':73,'D#2':78,'E2':82,'F2':87,'F#2':92,'G2':98,'G#2':104,'A2':110,'A#2':117,'B2':123,
    'C3':131,'C#3':139,'D3':147,'D#3':156,'E3':165,'F3':175,'F#3':185,'G3':196,'G#3':208,'A3':220,'A#3':233,'B3':247,
    'C4':262,'C#4':277,'D4':294,'D#4':311,'E4':330,'F4':349,'F#4':370,'G4':392,'G#4':415,'A4':440,'A#4':466,'B4':494,
    'C5':523,'C#5':554,'D5':587,'D#5':622,'E5':659,'F5':698,'F#5':740,'G5':784,'G#5':831,'A5':880,'A#5':932,'B5':988,
    'C6':1047,'C#6':1109,'D6':1175,'D#6':1245,'E6':1319,'F6':1397,'F#6':1480,'G6':1568,'G#6':1661,'A6':1760,'A#6':1865,'B6':1976,
    'C7':2093,'C#7':2217,'D7':2349,'D#7':2489,'E7':2637,'F7':2794,'F#7':2960,'G7':3136,'G#7':3322,'A7':3520,'A#7':3729,'B7':3951,
    'C8':4186,'C#8':4435,'D8':4699,'D#8':4978,'E8':5274,'F8':5588,'F#8':5920,'G8':6272,'G#8':6645,'A8':7040,'A#8':7459,'B8':7902,
    'C9':8372,'C#9':8870,'D9':9397,'D#9':9956,'E9':10548,'F9':11175,'F#9':11840,'G9':12544,'G#9':13290,'A9':14080,'A#9':14917,'B9':15804
}
song = [
    ("E5", 2), ("G4", 2), ("D5", 1.5), ("G4", 2),
    ("C5", 1.5), ("G4", 1), ("A4", 1), ("B4", 1), ("C5", 1), ("D5", 1), ("E5", 1), ("C5", 1),
    ("F5", 2), ("A4", 2), ("E5", 1.5), ("A4", 2),
    ("D5", 1.5), ("G4", 1), ("A4", 1), ("D5", 1), ("C5", 1), ("B4", 1), ("A4", 1), ("G4", 1)
]
def buzz_intro(hw_state):
    print("buzz")
    buzz_on, buzz_off = buzz_funcs(hw_state)    
    time_step = 1/4
    for note, steps in song:
        buzz_on(tones[note])
        time.sleep(time_step * steps)
    buzz_off()
    

### EYE SONG ###########################################################################
song_eye = [
  "B4", "FS5", "E5", "D5", "0",
  "B4", "F5", "E5", "D5", "0",
  "B4", "F5", "E5", "D5", "0",
  "AS4", "B4", "CS5", "D5", "CS5", "B4", "AS4"
]
    
steps_eye = [
  4, 4, 4, 4 + 4*3, 4,
  4, 4, 4, 4 + 4*3, 4,
  4, 4, 4, 4 + 4*3, 4,
  4, 4, 4, 4, 4, 4, 4*3
]

def buzz_eye(hw_state):
    print("buzz")
    buzz_on, buzz_off = buzz_funcs(hw_state)
    time_step = 0.070 #1/4
    for index in range(len(song_eye)):
        note, steps = song_eye[index], steps_eye[index]
        if note == "0":buzz_off()
        else:
            buzz_on(tones[note.replace("S", "#")])
        time.sleep(time_step * steps)
    buzz_off()