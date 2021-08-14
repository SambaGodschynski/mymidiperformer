from src.EventProvider import EventProvider
from mido import Message
from rtmidi import MidiOut

class MidiPlayer(object):
    def __init__(self, eventProvider: EventProvider, device_index: int) -> None:
        super().__init__()
        self.eventProvider = eventProvider
        self.midiout = MidiOut()
        self.midiout.open_port(device_index)
    
    def process(self, millis: float):
        for x in self.eventProvider.get_next_events(millis):
            message: Message = x
            bytes = message.bytes()
            if message.is_meta:
                continue
            self.midiout.send_message(bytes)