from mido import MidiFile, MidiTrack, Message, MetaMessage


class MidiBuilder:

    TICKS_PER_BEAT = 480

    def build(self, score, filename="output.mid"):
        mid = MidiFile(type=0, ticks_per_beat=self.TICKS_PER_BEAT)
        track = MidiTrack()
        mid.tracks.append(track)

        track.append(MetaMessage("track_name", name=score.title, time=0))
        tempo_us = int(60_000_000 / score.tempo)
        track.append(MetaMessage("set_tempo", tempo=tempo_us, time=0))
        track.append(Message("program_change", program=0, time=0))

        events = []
        for note in score.get_notes():
            events.append((note.start_tick, "on", note.pitch, note.velocity))
            events.append((note.start_tick + note.duration, "off", note.pitch, 0))

        events.sort(key=lambda e: (e[0], 0 if e[1] == "off" else 1))

        prev_tick = 0
        for abs_tick, event_type, pitch, velocity in events:
            delta = abs_tick - prev_tick
            msg_type = "note_on" if event_type == "on" else "note_off"
            track.append(Message(msg_type, note=pitch,
                                 velocity=velocity, time=delta))
            prev_tick = abs_tick

        track.append(MetaMessage("end_of_track", time=0))
        mid.save(filename)

        return filename
