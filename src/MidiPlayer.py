from src.Performance import Performance
from mido import Message
from rtmidi import MidiOut
from time import sleep
import subprocess
from signal import SIGINT

Note = lambda ch, pitch, vel, duration: [ch, pitch, vel, duration]
Rest = lambda duration: [None, None, None, duration]
STOP_SEQUENCE = [Note(0, 55, 85, 35), Rest(50), Note(0, 50, 26, 80)]
PERFORMANCE_END_SEQUENCE = [Note(0, 25, 100, 20)]
PERFORMANCE_BEGIN_SEQUENCE = [Note(0, 25, 50, 5)]
NEXT_SEQUENCE = [Note(0, 100, 100, 5)]
PREV_SEQUENCE = [Note(0, 90, 100, 5)]
TRACK_END_OFFSET_MILLIS = 500

class MidiPlayer(object):
    def __init__(self, performance: Performance, device_index: int) -> None:
        super().__init__()
        self.performance: Performance = performance
        self.midiout = MidiOut()
        self.midiout.open_port(device_index)
        self.timestamp = -1
        self.played_millis: int = 0
        self.track_end_at_millis = 0
        self.loop_begin_millis = None
        self.current_sheet = None
        self.player_process:subprocess.Popen = None

    @property
    def is_playing(self) -> bool:
        return self.player_process != None

    def panic(self):
        for ch in range(0, 15):
            self.midiout.send_message([0xb << 4 | ch, 0x7b, 0])

    def play_sequence(self, sequence: list, quiet: bool = False) -> None:
        if quiet:
            return
        for x in sequence:
            ch, pitch, vel, duration = x
            if ch is not None:
                self.midiout.send_message([0x9 << 4 | ch, pitch, vel])        
            sleep(duration/1000.0)
            if ch is not None:
                self.midiout.send_message([0x8 << 4 | ch, pitch, vel])        

    def close(self) -> None:
        self.panic()
        self.midiout.close_port()
        del self.midiout

    def open_sheetfile(self, path):
        self.current_sheet = path
        
    def start_playback(self):
        if self.is_playing:
            return
        self.open_sheetfile(self.performance.current_track.file)
        print(f"play {self.current_sheet}")
        self.player_process = subprocess.Popen(['sheetp', self.current_sheet])
        
    def check_if_player_process_active(self):
        if self.player_process == None:
            return
        if self.player_process.poll() == None:
            return
        self.player_process = None
        self.__set_next_track(True)

    def process(self):
        self.check_if_player_process_active()

    def stop_playback(self):
        if not self.is_playing:
            self.play_sequence(STOP_SEQUENCE)
            return
        print(f"stop {self.current_sheet}")
        self.player_process.send_signal(SIGINT)
        self.player_process = None

    def __set_next_track(self, quiet: bool = False):
        if self.performance.has_next:
            self.performance.next_track()
            self.play_sequence(NEXT_SEQUENCE, quiet)
        else:
            self.play_sequence(PERFORMANCE_END_SEQUENCE, quiet)
            self.performance.reset()

    def __set_prev_track(self, quiet: bool = False):
        if self.performance.has_prev:
            self.performance.prev_track()
            self.play_sequence(PREV_SEQUENCE, quiet)
        else:
            self.play_sequence(PERFORMANCE_BEGIN_SEQUENCE)

    def next(self):
        if not self.is_playing:
            self.__set_next_track()

    def prev(self):
        if not self.is_playing:
            self.__set_prev_track()  
