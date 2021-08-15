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

def trigger_on_val(trigger_val: int, val: int, f):
    if (val == trigger_val):
        f()

def run_main_loop(performance: Performance, args) -> None:
    from pygame import init, quit
    from pygame import time
    global quit_pygame
    init()
    player = MidiPlayer(performance, args.outdevice, time)
    input = MidiInput(args.indevice)
    input.verbose = args.verbose
    input.register_action("start", lambda val: trigger_on_val(0, val, player.start_playback))
    input.register_action("stop", lambda val: trigger_on_val(0, val, player.stop_playback))
    input.register_action("next", lambda val: trigger_on_val(127, val, player.next))
    input.register_action("prev", lambda val: trigger_on_val(127, val, player.prev))
    try:
        while True:
            if player.is_playing:
                player.process()
                console_update(str(player.played_millis/1000))
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


def find_midi_output(name) -> int:
    from rtmidi import MidiOut
    midiout = MidiOut()
    ports = midiout.get_ports()
    for idx, port in enumerate(ports):
        if str(port).find(name) >= 0:
            return idx
    return None

def find_midi_input(name) -> int:
    from rtmidi import MidiIn
    midiins = MidiIn()
    ports = midiins.get_ports()
    for idx, port in enumerate(ports):
        if str(port).find(name) >= 0:
            return idx
    return None

def get_in_and_out(agrs):
    import config
    indevice_idx = None
    outdevice_idx = None
    if args.indevice != None:
        indevice_idx = args.indevice
    else:
        indevice_idx = find_midi_input(config.InputDevice)
    if args.outdevice != None:
        outdevice_idx = args.outdevice
    else:
        outdevice_idx = find_midi_input(config.OutputDevice)
    return indevice_idx, outdevice_idx

def wait_for_devices(args):
    from time import sleep
    indevice_idx = None
    outdevice_idx = None
    while True:
        indevice_idx, outdevice_idx = get_in_and_out(args)
        if indevice_idx is not None and outdevice_idx is not None:
            break
        sleep(5)
    return indevice_idx, outdevice_idx
    

if __name__ == '__main__':
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--outdevice', type=int, help='the out device id')
    parser.add_argument('--indevice', type=int, help='the in device id')
    parser.add_argument('--list', action='store_const', const=True, help='lists the MIDI devices connected to this machine')
    parser.add_argument('--midifile', type=str, help='plays a midi file')
    parser.add_argument('--performance', type=str, help='path to a performance json')
    parser.add_argument('--verbose', action='store_const', const=True, help='verbose mode')
    args = parser.parse_args()
    if args.list:
        list_mididevices()
        sys.exit(0)
    try:
        indevice_idx, outdevice_idx = wait_for_devices(args)
        args.indevice = indevice_idx
        args.outdevice = outdevice_idx
        performance_json_file = args.performance
        performance = Performance()
        if performance_json_file != None:
            performance.load_json(performance_json_file)
        midi_file = args.midifile
        if midi_file != None:
            performance.tracks.append(Track(args.midifile))
        run_main_loop(performance, args)
    finally:
        print(" ... BYE")