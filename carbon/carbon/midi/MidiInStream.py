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

# -*- coding: ISO-8859-1 -*-

from MidiOutStream import MidiOutStream

class MidiInStream:

    """
    Takes midi events from the midi input and calls the apropriate
    method in the eventhandler object
    """

    def __init__(self, midiOutStream, device):

        """

        Sets a default output stream, and sets the device from where
        the input comes

        """

        if midiOutStream is None:
            self.midiOutStream = MidiOutStream()
        else:
            self.midiOutStream = midiOutStream


    def close(self):

        """
        Stop the MidiInstream
        """


    def read(self, time=0):

        """

        Start the MidiInstream.

        "time" sets timer to specific start value.

        """


    def resetTimer(self, time=0):
        """

        Resets the timer, probably a good idea if there is some kind
        of looping going on

        """

