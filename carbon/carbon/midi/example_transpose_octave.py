########################################################################
# manganese - midi analysis & visualization platform
# Copyright (c) 2010, 2011, 2013 Maximilian Marx <mmarx@wh2.tu-dresden.de>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA.
########################################################################

from MidiOutFile import MidiOutFile
from MidiInFile import MidiInFile

"""
This is an example of the smallest possible type 0 midi file, where 
all the midi events are in the same track.
"""


class Transposer(MidiOutFile):
    
    "Transposes all notes by 1 octave"
    
    def _transp(self, ch, note):
        if ch != 9: # not the drums!
            note += 12
            if note > 127:
                note = 127
        return note


    def note_on(self, channel=0, note=0x40, velocity=0x40):
        note = self._transp(channel, note)
        MidiOutFile.note_on(self, channel, note, velocity)
        
        
    def note_off(self, channel=0, note=0x40, velocity=0x40):
        note = self._transp(channel, note)
        MidiOutFile.note_off(self, channel, note, velocity)


out_file = 'midiout/transposed.mid'
midi_out = Transposer(out_file)

#in_file = 'midiout/minimal_type0.mid'
#in_file = 'test/midifiles/Lola.mid'
in_file = 'test/midifiles/tennessee_waltz.mid'
midi_in = MidiInFile(midi_out, in_file)
midi_in.read()

