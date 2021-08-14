from src.EventProvider import EventProvider
from mido import Message
from rtmidi import MidiOut

class MidiPlayer(object):
    def __init__(self, eventProvider: EventProvider, device_index: int) -> None:
        super().__init__()
        self.eventProvider = eventProvider
        self.midiout = MidiOut()
        self.midiout.open_port(device_index)
    
    def process(self, millis: float) -> None:
        for x in self.eventProvider.get_next_events(millis):
            message: Message = x
            bytes = message.bytes()
            if message.is_meta:
                continue
            self.midiout.send_message(bytes)

    def panic(self):
        for ch in range(0, 15):
            self.midiout.send_message([0xb << 4 | ch, 0x7b, 0])

    def close(self) -> None:
        self.panic()
        del self.midiout