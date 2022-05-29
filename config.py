###########################################
# config.py                               #
# Some globals for translating MIDI data  #
# and settings for pyPiMgb                #
# kuneho 2022                             #
# https://furryhu.org/                    #
###########################################

MIDI_DEVICE = "/dev/midi"

# MIDI commands
MIDI_CMD_NOTE_OFF              = 0x80       # Note OFF
MIDI_CMD_NOTE_ON               = 0x90       # Note ON
MIDI_CMD_AFTERTOUCH            = 0xA0       # Aftertouch
MIDI_CMD_CONTINUOUS_CONTROLLER = 0xB0       # Continuous Controller
MIDI_CMD_PROGRAM_CHANGE 	   = 0xC0       # Program Change
MIDI_CMD_CHANNEL_PRESSURE      = 0xD0       # Channel Pressure
MIDI_CMD_PITCH_BEND 		   = 0xE0       # Pitch Bend
MIDI_CMD_SYSTEM 			   = 0xF0       # System reserved

SETTING_CHANNEL_PIANOKEYS = 14              # Defines which channel will be used as playable piano keys
SETTING_CHANNEL_CONTROL   = 9               # Defines which channel will be a control channel for pyPiMgb to receive Program Changes
SETTING_CHANNEL_PU1       = 0               # Pulse 1 channel of Game Boy
SETTING_CHANNEL_PU2       = 1               # Pulse 2 channel of Game Boy
SETTING_CHANNEL_WAV       = 2               # Wavetable channel of Game Boy
SETTING_CHANNEL_NOI       = 3               # Noise channel of Game Boy
SETTING_CHANNEL_POLY      = 4               # POLY mode (see: https://github.com/trash80/mGB)

DELAY_GB_MIDI = 500                         # Delay needed by the Game Boy's shift register

LOW  = 0                                    # Logical LOW
HIGH = 1                                    # Logical HIGH

PIN_GB_SCLK = 14                            # Serial Clock line of Game Boy, GPIO pin of Raspberry Pi
PIN_GB_SIN  = 15                            # Serial In line of Game Boy, GPIO pin of Raspberry Pi