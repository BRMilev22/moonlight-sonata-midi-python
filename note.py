class Note:

    def __init__(self, pitch, duration, velocity=64, start_tick=0):
        self._pitch = pitch
        self._duration = duration
        self._velocity = velocity
        self._start_tick = start_tick

    @property
    def pitch(self):
        return self._pitch

    @property
    def duration(self):
        return self._duration

    @property
    def velocity(self):
        return self._velocity

    @property
    def start_tick(self):
        return self._start_tick

    def __repr__(self):
        return f"Note(pitch={self._pitch}, dur={self._duration}, vel={self._velocity}, t={self._start_tick})"
