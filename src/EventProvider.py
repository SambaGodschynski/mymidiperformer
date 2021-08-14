from typing import Generator, Iterator
from mido import MidiFile, MidiTrack, Message
from sys import maxsize

MINUTE = 60.0
ONE_SECOND_MILLIS = 1000.0
MICROSECONDS_PER_MINUTE = 60000000.0

class EventIterator:
    def __init__(self, track: MidiTrack) -> None:
        self.track = track
        self.ticks = 0
        self.idx = -1

    def __iter__(self):
        self.ticks = 0
        self.idx = -1
        return self

    def __next__(self):
        self.idx += 1
        if self.idx >= len(self.track):
            raise StopIteration
        event = self.track[self.idx]
        if hasattr(event, 'time'):
            self.ticks +=  event.time
        return event
    
    def peek_ticks_of_next(self):
        idx = self.idx + 1
        if idx >= len(self.track):
            return maxsize
        event = self.track[idx]
        return event.time + self.ticks if hasattr(event, 'time') else self.ticks
            
        

class EventProvider(object):
    def __init__(self, midifile:str) -> None:
        super().__init__()
        self.file = MidiFile(midifile)
        self.bpm = 120
        self.ppq = self.file.ticks_per_beat
        self.iterators = [self.__get_events(track) for track in self.file.tracks]
    
    def millis_to_tick(self, millis: float) -> float:
        return millis * self.bpm * self.ppq / (MINUTE * ONE_SECOND_MILLIS)

    def __get_events(self, track: MidiTrack):
        return iter(EventIterator(track))

    def handle_event(self, ev: Message) -> None:
        if not ev.is_meta:
            return
        if ev.type == 'set_tempo':
            tempo = MICROSECONDS_PER_MINUTE / ev.tempo
            self.bpm = tempo
    
    def get_next_events(self, until_millis):
        end_ticks = self.millis_to_tick(until_millis)
        for it in self.iterators:
            while it.peek_ticks_of_next() <= end_ticks:
                ev = next(it)
                self.handle_event(ev)
                yield ev
            
                   
            
            