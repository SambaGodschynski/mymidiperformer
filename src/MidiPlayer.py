from src.Track import Track
from src.Performance import Performance
from src.EventProvider import EventProvider
from mido import Message
from rtmidi import MidiOut

TRACK_END_OFFSET_MILLIS = 500

class MidiPlayer(object):
    def __init__(self, performance: Performance, device_index: int, time_provider) -> None:
        super().__init__()
        self.performance: Performance = performance
        self.midiout = MidiOut()
        self.midiout.open_port(device_index)
        self.event_provider: EventProvider = None
        self.is_playing = False
        self.timestamp = -1
        self.time_provider = time_provider
        self.played_millis: int = 0
        self.track_end_at_millis = 0
        self.loop_begin_millis = None

    def panic(self):
        for ch in range(0, 15):
            self.midiout.send_message([0xb << 4 | ch, 0x7b, 0])

    def close(self) -> None:
        self.panic()
        self.midiout.close_port()
        del self.midiout

    def open_midifile(self, path):
        print(f'open "{path}"')
        self.event_provider = EventProvider(path)
        
    def start_playback(self):
        if self.is_playing:
            return
        if self.performance.is_finished:
            return
        if self.performance.current_track == None:
            self.performance.next_track()
        self.open_midifile(self.performance.current_track.file)
        self.is_playing = True
        self.timestamp = self.time_provider.get_ticks()
        self.track_end_at_millis = self.timestamp + self.event_provider.length_millis + TRACK_END_OFFSET_MILLIS

    def stop_playback(self):
        if not self.is_playing:
            return
        print("stopping")
        self.is_playing = False
        self.panic()     

    def seek(self, position_millis: float) -> None:
        self.event_provider.seek(position_millis)
        self.timestamp = self.time_provider.get_ticks() - position_millis

    def handle_beginloop_message(self, msg):
        self.loop_begin_millis = self.played_millis

    def handle_endloop_message(self, msg):
        if self.loop_begin_millis == None:
            return
        self.seek(self.loop_begin_millis)

    def handle_meta_message(self, msg):
        if msg.type == 'cue_marker':
            if msg.text == 'begin loop':
                self.handle_beginloop_message(msg)
            if msg.text == 'end loop':
                self.handle_endloop_message(msg)

    @property
    def is_looping(self):
        return self.is_playing and self.loop_begin_millis != None

    def exit_loop(self):
        self.loop_begin_millis = None

    def next(self):
        if self.is_looping:
            self.exit_loop()
    
    def prev(self):
        pass

    def process(self) -> None:
        if self.is_playing == False:
            return
        self.played_millis = self.time_provider.get_ticks() - self.timestamp
        if self.played_millis >= self.track_end_at_millis:
            self.stop_playback()
        for x in self.event_provider.get_next_events(self.played_millis):
            message: Message = x
            bytes = message.bytes()
            if message.is_meta:
                self.handle_meta_message(message)
                continue
            self.midiout.send_message(bytes)        
