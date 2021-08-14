from rtmidi import MidiIn
from inputConfig import InputMap

class MidiInput(object):
    def __init__(self, device_id: int) -> None:
        super().__init__()
        self.midiin = MidiIn()
        self.midiin.open_port(device_id)
        self.midiin.set_callback(self)
        self.verbose = False
        self.registred_actions = {}

    def __keyvalue(self, message) -> str:
        return f'{message[0]}.{message[1]}', message[2]

    def __call__(self, event, data=None) -> None:
        key, value = self.__keyvalue(event[0])
        if self.verbose:
            print(f"{key} -> {value}")
        if key not in InputMap:
            return
        action = InputMap[key]
        if action not in self.registred_actions:
            return
        self.registred_actions[action](value)

    def close(self):
        self.midiin.close_port()
        del self.midiin

    def register_action(self, name: str, callback) -> None:
        self.registred_actions[name] = callback