#!/bin/env python3
from src.Performance import Performance
from src.Track import Track
from src.EventProvider import EventProvider
from src.MidiPlayer import MidiPlayer
from src.MidiInput import MidiInput

last_line = ""

def console_update(txt: str) -> None:
    global last_line
    print('\b' * len(last_line), end="")
    print(txt, end="", flush=True)
    last_line = txt

def run_main_loop(performance: Performance, args) -> None:
    from pygame import init, quit
    from pygame import time
    global quit_pygame
    init()
    player = MidiPlayer(performance, args.outdevice, time)
    input = MidiInput(args.indevice)
    input.register_action("start", lambda val: player.start_playback())
    input.register_action("stop", lambda val: player.stop_playback())
    try:
        while True:
            player.process()
            time.wait(1)
    except KeyboardInterrupt:
        pass            
    finally:
        quit()
        player.close()
        input.close()


def list_mididevices() -> None:
    from rtmidi import MidiOut
    from rtmidi import MidiIn
    print("==========")
    print("Outputs:")
    print("==========")
    midiout = MidiOut()
    ports = midiout.get_ports()
    for idx, port in enumerate(ports):
        print(f'{idx}: {port}')
    print("\n==========")
    print("Inputs:")
    print("==========")
    midiin = MidiIn()
    ports = midiin.get_ports()
    for idx, port in enumerate(ports):
        print(f'{idx}: {port}')        


if __name__ == '__main__':
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--outdevice', type=int, help='the out device id')
    parser.add_argument('--indevice', type=int, help='the in device id')
    parser.add_argument('--list', action='store_const', const=True, help='lists the MIDI devices connected to this machine')
    parser.add_argument('--midifile', type=str, help='plays a midi file')
    parser.add_argument('--performance', type=str, help='path to a performance json')
    args = parser.parse_args()
    if args.list:
        list_mididevices()
        sys.exit(0)
    try:
        performance = Performance()
        performance.tracks.append(Track(args.midifile))
        run_main_loop(performance, args)
    finally:
        print(" ... BYE")