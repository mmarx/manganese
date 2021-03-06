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



from classifier import EventClassifier


class Event(object):

    def __init__(self, event):
        self.raw = event
        self.type = event[0] & 0xf0
        self.channel = event[0] & 0x0f

    def describe_type(self):
        return EventClassifier()[self.type]

    def as_dword(self):
        length = len(self.raw)

        if length > 4:
            raise OverflowError

        dword = 0x00000000

        while length > 0:
            length -= 1
            dword |= self.raw[length]
            if length > 0:
                dword <<= 8

        return dword

    def __str__(self):
        return ("<midi event of type %(type)0x (%(typestring)s) on "
                "channel %(channel)d>") % {'type': self.type,
                                           'typestring': self.describe_type(),
                                           'channel': self.channel,
                                           }

    def __repr__(self):
        return ('[' + ', '.join([hex(byte) for byte in self.raw]) + ']')


def event_from_dword(dword):
    event = hex(dword)[2:]
    if len(event) % 2:
        event = '0' + event
    bytes = [int(event[i:(i + 2)], base=16) for i in range(0, len(event), 2)]
    bytes.reverse()
    return Event(bytes)
