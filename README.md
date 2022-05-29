# pyPiMgb
 Send MIDI data to Game Boy, using Python and pigpio

This is a small, draft like, heavily WIP project to bring the functionalities of the Arduinoboy (https://github.com/trash80/arduinoboy) to the Raspberry Pi.
All versions should work, I tested and used this code on a Raspberry Pi 400.

Currently it's only useful with mGB (https://github.com/defensem3ch/mGB)

You can play the channels one-by-one, and change amongst them sending Program Change 0-5 on Channel 10 to the software.

My far goal with this project is to create a small, convenient and smart USB MIDI host out from the Raspberry Pi Zero. One of its modules is this project, PimGB as a "driver" for Game Boys.

This software maps Channels 1-4 to Game Boy channels. It listens for commands on Channel 10, and you can use a MIDI controller (like a keyboard) on Channel 15.

### Wiring:
|Game Boy Link cable PIN#|Raspberry Pi PIN# (wiringPi)  |
|--|--|
| 3 (SIN) | 15 |
| 5 (SCLK) | 14 |
But all of the parameters are configurable in config.py file.

### Usage
You need to have pigpio package installed to your Raspberry Pi.

Run it:

    python3 ./main.py

The software reads from /dev/midi (but configurable in config.py) and bitbangs the data to the Game Boy.

I recommend to use virtual MIDI devices (snd-virmidi) and map your controller or player to it with aconnect.

THIS IS REALLY REALLY WIP.
A snapshot of the code.

My original project can be found here: https://github.com/eocorekuneho/PimGB

Since Raspberry Pi OS Bullseye doesn't support wiringPi anymore, I had to rewrite the whole project with pigpio, and also in Python.

It's much more better than the original, C version.
