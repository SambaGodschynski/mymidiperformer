from src.Track import Track

class Performance(object):
    def __init__(self) -> None:
        super().__init__()
        self.tracks = []
        self.current_track_index: int = -1

    def next_track(self) -> Track:
        if self.is_finished:
            return
        self.current_track_index += 1
        return self.current_track
    
    @property
    def is_finished(self) -> bool:
        return self.current_track_index >= len(self.tracks)

    @property
    def current_track(self) -> Track: 
        if self.is_finished or self.current_track_index < 0:
            return None
        return self.tracks[self.current_track_index]