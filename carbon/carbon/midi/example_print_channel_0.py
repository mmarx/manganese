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

from MidiOutStream import MidiOutStream
from MidiInFile import MidiInFile

"""
This prints all note on events on midi channel 0
"""


class Transposer(MidiOutStream):
    
    "Transposes all notes by 1 octave"
    
    def note_on(self, channel=0, note=0x40, velocity=0x40):
        if channel == 0:
            print channel, note, velocity, self.rel_time()


event_handler = Transposer()

in_file = 'midiout/minimal_type0.mid'
midi_in = MidiInFile(event_handler, in_file)
midi_in.read()

