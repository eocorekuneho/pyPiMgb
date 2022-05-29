#############################################
# main.py                                   #
# Main file of pyPiMgb.                     #
# Basic, draft like program for interfacing #
# with Game Boy via serial link, sending    #
# MIDI data, to use with ROM mGB            #
# kuneho 2022                               #
#############################################

import pigpio
import time
import os
from config import *

g_fdMIDI = None
pi = pigpio.pi()

def init():
    global g_fdMIDI
    # Needs to be adjusted.
    # It's wise to use a virtual MIDI interface and bind the controller to it with aconnect
    g_fdMIDI = os.open(MIDI_DEVICE, os.O_RDONLY)
    
    if g_fdMIDI:
        print("Device OK")
    else:
        print("Device ERR")
        return
    
    # Setting up GPIO pins
    pi.set_mode(PIN_GB_SCLK, pigpio.OUTPUT)
    pi.set_mode(PIN_GB_SIN, pigpio.OUTPUT)
    # SCLK, SIN needs to be LOW at the beginning.
    pi.write(PIN_GB_SCLK, LOW)
    pi.write(PIN_GB_SIN, LOW)
    

def usleep(val):
    time.sleep(val/1000000.0)


def Send_Byte_To_Gameboy(byte_to_send):
    output = ""
    for tick in range(0, 8, 1):
        print("1" if (byte_to_send & 0x80 == 128) else "0", end=""),
        if(byte_to_send & 0x80):
            # Setting Serial IN to HIGH before Clock Pulse (also resetting SCLK)
            GB_SET(LOW, HIGH)
            # If ready, pulling SCLK to HIGH
            GB_SET(HIGH, HIGH)
        else:
            # Setting Serial IN to LOW before Clock Pulse (also resetting SCLK)
            GB_SET(LOW, LOW)
            # If ready, pulling SCLK to HIGH
            GB_SET(HIGH, LOW)
        byte_to_send <<= 1
    print("\n", end="")

    
def GB_SET(CLK, OUT):
    pi.write(PIN_GB_SIN, OUT)
    pi.write(PIN_GB_SCLK, CLK)
    
    
def main():
    # Init software
    init()
    
    # Init values
    midi_data         = None
    midi_value_mode   = None
    midi_address_mode = None
    midi_stat_channel = None
    midi_stat_type    = None
    
    send_byte         = None
    data_out          = bytearray([0, 0, 0])
    control_mode      = None
    output_channel    = 0
    
    # Main loop
    while True:
        midi_data = os.read(g_fdMIDI, 1)
        midi_data = midi_data[0]
        print("<< midi byte:", format(midi_data, "08b"))
        if(midi_data & 0x80):
            midi_command = midi_data & 0x0F
            if(midi_command == MIDI_CMD_SYSTEM ):
				# 1111XXXX
				# MIDI rendszerüzenet.
                g_midiValueMode = False
                print("systemmsg")
            else:
                send_byte         = False
                midi_stat_channel = midi_data & 0x0F;
                midi_stat_type    = midi_data & 0xF0;
                
                if(midi_stat_channel == SETTING_CHANNEL_CONTROL):
                    print("Control message received.")
                    if(midi_stat_type == MIDI_CMD_PROGRAM_CHANGE):
                        print("Program Change")
                        send_byte         = False
                        control_mode      = True
                        midi_address_mode = False
                        midi_value_mode   = False
                    #endif
                elif(midi_stat_channel == SETTING_CHANNEL_PIANOKEYS):
                    print("MIDI input on {0}, output is {1}".format(midi_stat_channel, output_channel))
                    data_out[0] = midi_stat_type + output_channel
                    send_byte = True
                else:
                    data_out[0] = midi_stat_type + midi_stat_channel #output_channel
                    send_byte = True
                    control_mode      = False
                    midi_address_mode = False
                    midi_value_mode   = False
                
                print("--------------------------------------")
                print("Control mode? {0}".format(control_mode))
                print("Address mode? {0}".format(midi_address_mode))
                print("Value mode? {0}".format(midi_value_mode))
                print("Sending anything? {0}".format(send_byte))
                print("Output channel will be {0}".format(data_out))
                print("--------------------------------------")
                
                if(send_byte):
                    print(">> midi byte:", format(data_out[0], "08b"))
                    Send_Byte_To_Gameboy(data_out[0])
                    usleep(DELAY_GB_MIDI)
                    midi_value_mode = False
                    midi_address_mode = True
                #end
            #end
        elif(midi_address_mode):
            midi_address_mode = False
            midi_value_mode   = True
            data_out[1] = midi_data
            Send_Byte_To_Gameboy(data_out[1])
            usleep(DELAY_GB_MIDI)
        elif(midi_value_mode):
            midi_address_mode = True
            midi_value_mode   = False
            data_out[2] = midi_data
            Send_Byte_To_Gameboy(data_out[2])
            usleep(DELAY_GB_MIDI)
        elif(control_mode):
            control_mode = False
            midi_value_mode = False
            midi_address_mode = False
            output_channel = midi_data
        #end
    #end
#end


if __name__ == "__main__":
    main()