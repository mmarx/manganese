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

from contextlib import contextmanager

import _caesium


class Caesium(object):
    def __init__(self, speed, range):
        self._speed = speed
        self._range = range
        self._running = False

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        self._range = value
        _caesium.set_range(value)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
        _caesium.set_speed(value)

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value
        _caesium.set_running(value)


@contextmanager
def caesium(speed=1.0, range=0.25, factor=1.0, offset=21, markers=[], controls={}):
    for controller in ['range', 'stop', 'start', 'reset', 'next', 'prev', 'rebase']:
        if controller not in controls:
            controls[controller] = 0

    _caesium.create_caesium(speed, range, factor, offset, markers, controls)

    yield Caesium(speed, range)

    _caesium.destroy_caesium()
