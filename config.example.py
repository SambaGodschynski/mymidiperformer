# device names must containing, not exact match
OutputDevice = 'SC-8850 Part B'
InputDevice = 'Launchkey MK2 49 MIDI 1'

#### register the note off events
TriggerVelocity = 0 # some devices (LPD 8) send 128 note off velocity

# event array [153, 40, 50] => "153.40", no whitespaces
InputMap = {
    "176.114": "stop", 
    "176.115": "start",
    "176.113": "next",
    "176.112": "prev"
}