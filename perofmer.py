def run_main_loop() -> None:
    from pygame import init
    from pygame import time
    init()
    t = 0
    while True:
        t = time.get_ticks()
        time.wait(1)


def list_mididevices() -> None:
    from rtmidi import MidiOut
    midiout = MidiOut()
    ports = midiout.get_ports()
    for idx, port in enumerate(ports):
        print(f'{idx}: {port}')


if __name__ == '__main__':
    import argparse
    import sys
    import os
    import os.path as path
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=int, help='the device id of the midi taret device')
    parser.add_argument('--list', action='store_const', const=True, help='lists the MIDI devices connected to this machine')
    args = parser.parse_args()
    if args.list:
        list_mididevices()
        sys.exit(0)