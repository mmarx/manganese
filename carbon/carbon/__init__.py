
from manganese.carbon import midi

from midi.MidiOutStream import MidiOutStream
from midi.MidiInFile import MidiInFile
from midi.MidiToText import MidiToText


class CarbonOutStream(MidiOutStream):
    def __init__(self, name, channel, callback):
        self.name = name
        self.channel = int(channel)
        self.callback = callback

    def header(self, format, nTracks, division):
        self.division = division

    def note_on(self, channel, *args, **kwargs):
        if channel == self.channel:
            self.callback(self.stamp(self.abs_time()))

    def stamp(self, time):
        seconds = time / 4.0 / self.division
        hh = int(seconds // 3600)
        mm = int(seconds // 60) % 3600
        ss = int(seconds // 1) % 60
        fr = int(30 * (seconds - ss))

        return {'hours': hh,
                'minutes': mm,
                'seconds': ss,
                'frames': fr,
                }


def markers(midifile, name, callback, channel=9):
    stream = CarbonOutStream(name=name, channel=channel, callback=callback)

    midi_in = MidiInFile(stream, midifile)
    midi_in.read()
