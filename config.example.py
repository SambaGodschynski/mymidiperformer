# device names must containing, not exact match
OutputDevice = 'SC-8850 Part B'
InputDevice = 'Launchkey MK2 49 MIDI 1'


# event array [153, 40, 50] => "153.40", no whitespaces
InputMap = {
    "128.62": "stop",  #TODO add vel values, for now these are hardcoded
    "128.64": "start",
    "144.60": "next",
    "144.59": "prev"
}