from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
import time

keypico = PMK(Hardware())
keys = keypico.keys

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], 
                          out_channel=0)

# Colour selection
snow = (0, 0, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
red = (255, 0, 0)
limegreen = (0, 255, 0)
purple = (255, 0, 255)
white = (153, 204, 255)
yellow = (213,255,0)
pink = (255,0,102)
orange = (255,102,0)
brown = (102,51,0)
peach = (255,204,153)
olive = (102,102,0)
lightskyblue = (102,255,255)
violet = (153,51,255)
lawngreen = (128,255,0)
indigo = (153,0,153)
plum = (255,51,51)

# Set key colours for all keys
keypico.set_all(*white)

# Orientation
keypico.set_led(0, *red)
keypico.set_led(1, *limegreen)
keypico.set_led(2, *blue)
keypico.set_led(3, *cyan)
keypico.set_led(4, *white)
keypico.set_led(5, *yellow)
keypico.set_led(6, *pink)
keypico.set_led(7, *orange)
keypico.set_led(8, *brown)
keypico.set_led(9, *peach)
keypico.set_led(10, *olive)
keypico.set_led(11, *lightskyblue)
keypico.set_led(12, *violet)
keypico.set_led(13, *lawngreen)
keypico.set_led(14, *indigo)
keypico.set_led(15, *plum)

# Set sleep time
keypico.led_sleep_enabled = True
keypico.led_sleep_time = 30

# Midi

start_note = 70
velocity = 127

# Loop

for key in keys:
    @keypico.on_press(key)
    def press_handler(key):
        print("Key {} pressed".format(key.number))
        key.set_led(*white)
        note = start_note + key.number
        midi.send(NoteOn(note, velocity))

    @keypico.on_release(key)
    def release_handler(key):
        print("Key {} released".format(key.number))
        if key.rgb == [255, 0, 0]:
            key.set_led(*white)
        else:
            key.set_led(*snow)
        note = start_note + key.number
        midi.send(NoteOff(note, 0))

    @keypico.on_hold(key)
    def hold_handler(key):
        print("Key {} held".format(key.number))
        key.set_led(*orange)
        keypico.set_all(*red)

while True:
    keypico.update()
    