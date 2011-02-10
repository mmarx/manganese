######################################################################
# manganese - midi analysis & visualization platform
# Copyright (c) 2010, 2011 Maximilian Marx <mmarx@wh2.tu-dresden.de>
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
######################################################################

from _video import *


def list_video_modes():
    from operator import attrgetter
    return sorted(_video.list_video_modes(), key=attrgetter('size'))


def _rect_from_string(cls, string):
    width, rest = string.split('x', 1)

    if '+' in rest:
        height, rest = rest.split('+', 1)

        if '+' in rest:
            x, y = rest.split('+', 1)
        else:
            x = rest
            y = 0
    else:
        height = rest
        x = 0
        y = 0

    rect = SDLRect()
    rect.w = int(width)
    rect.h = int(height)
    rect.x = int(x)
    rect.y = int(y)

    return rect


def _rect_eq(self, other):
    return (self.h == other.h and self.w == other.w
            and self.x == other.x and self.y == other.y)

SDLRect.from_string = classmethod(_rect_from_string)
SDLRect.__eq__ = _rect_eq
