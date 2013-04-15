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

"""
This is an example of the smallest possible type 0 midi file, where 
all the midi events are in the same track.
"""

out_file = 'midiout/minimal_type0.mid'
midi = MidiOutFile(out_file)

# non optional midi framework
midi.header()
midi.start_of_track() 


# musical events

midi.update_time(0)
midi.note_on(channel=0, note=0x40)

midi.update_time(192)
midi.note_off(channel=0, note=0x40)


# non optional midi framework
midi.update_time(0)
midi.end_of_track()

midi.eof()
