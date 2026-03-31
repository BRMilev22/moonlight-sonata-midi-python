from note import Note
from score import Score


class MoonlightSonata(Score):

    TICKS_PER_BEAT = 480
    TRIPLET = TICKS_PER_BEAT // 3

    CS2 = 37
    GS2 = 44
    CS3 = 49
    E3  = 52
    GS3 = 56
    B3  = 59
    CS4 = 61
    E4  = 64
    GS4 = 68
    A3  = 57
    FS3 = 54
    B2  = 47
    A2  = 45
    D3  = 50
    FS4 = 66

    def __init__(self, tempo_bpm=54):
        self._tempo = tempo_bpm

    @property
    def title(self):
        return "Moonlight Sonata - Adagio sostenuto (Beethoven)"

    @property
    def tempo(self):
        return self._tempo

    @tempo.setter
    def tempo(self, value):
        self._tempo = value

    def _triplet_bar(self, bar_start, bass_notes, arpeggio_notes, velocity=50):
        notes = []
        whole = self.TICKS_PER_BEAT * 4

        for pitch in bass_notes:
            notes.append(Note(pitch, whole, velocity - 10, start_tick=bar_start))

        tick = bar_start
        for _ in range(4):
            for pitch in arpeggio_notes:
                notes.append(Note(pitch, self.TRIPLET, velocity, start_tick=tick))
                tick += self.TRIPLET

        return notes

    def get_notes(self):
        notes = []
        bar_length = self.TICKS_PER_BEAT * 4
        bar = 0

        for _ in range(4):
            notes.extend(
                self._triplet_bar(bar * bar_length,
                                  [self.CS2, self.CS3],
                                  [self.GS3, self.CS4, self.E4])
            )
            bar += 1

        notes.extend(
            self._triplet_bar(bar * bar_length,
                              [self.B2, self.B3],
                              [self.GS3, self.CS4, self.E4])
        )
        bar += 1

        notes.extend(
            self._triplet_bar(bar * bar_length,
                              [self.A2, self.A3],
                              [self.A3, self.CS4, self.E4])
        )
        bar += 1

        for _ in range(2):
            notes.extend(
                self._triplet_bar(bar * bar_length,
                                  [self.GS2, self.GS3],
                                  [self.GS3, self.B3, self.E4])
            )
            bar += 1

        return notes

        return notes
