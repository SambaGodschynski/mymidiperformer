from src.Track import Track

class Performance(object):
    def __init__(self) -> None:
        super().__init__()
        self.tracks = []
        self.current_track_index: int = 0

    def reset(self):
        self.current_track_index: int = 0

    def next_track(self) -> Track:
        if not self.has_next:
            return
        self.current_track_index += 1
        return self.current_track

    def prev_track(self) -> Track:
        if not self.has_prev:
            return
        self.current_track_index -= 1
        return self.current_track
        
    @property
    def has_next(self) -> bool:
        return (self.current_track_index + 1) < len(self.tracks)

    @property
    def has_prev(self) -> bool:
        return (self.current_track_index - 1) >= 0
    

    @property
    def current_track(self) -> Track: 
        if self.current_track_index < 0 or self.current_track_index >= len(self.tracks):
            return None
        return self.tracks[self.current_track_index]

    def load_json(self, path) -> None:
        from json import loads
        from os import path as ospath
        text = ''
        with open(path, 'r') as file:
            text = file.read()
        json = loads(text)
        json_dir = ospath.dirname(path)
        for json_track in json["tracks"]:
            midifile = json_track["file"]
            midifile = ospath.normpath(ospath.join(json_dir, midifile))
            track = Track(midifile)
            self.tracks.append(track)
