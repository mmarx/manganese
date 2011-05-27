
from manganese.carbon import midi

from midi.MidiOutStream import MidiOutStream
from midi.MidiInFile import MidiInFile


class CarbonOutStream(MidiOutStream):
    def __init__(self, name, channel, callback):
        self.name = name
        self.channel = int(channel)
        self.callback = callback
        self.the_tempo = None

    def tempo(self, value):
        if self.the_tempo is None:
            self.the_tempo = value
            self.bpm = int(60000000.0 / value)

    def header(self, format, nTracks, division):
        self.division = division

    def note_on(self, channel, *args, **kwargs):
        if channel == self.channel:
            self.callback(self.stamp(self.abs_time()))

    def stamp(self, time):
        seconds = time / self.division * 60.0 / self.bpm
        hh = int(seconds // 3600)
        mm = int(seconds // 60) % 60
        ss = int(seconds) % 60
        fr = int(30 * (seconds - int(seconds)))

        return {'hours': hh,
                'minutes': mm,
                'seconds': ss,
                'frames': fr,
                }


def markers(midifile, name, callback, channel=9):
    stream = CarbonOutStream(name=name, channel=channel, callback=callback)

    midi_in = MidiInFile(stream, midifile)
    midi_in.read()
