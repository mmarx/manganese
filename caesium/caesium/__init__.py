
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
def caesium(speed=1.0, range=0.25, markers=[], controls={}):
    for controller in ['range', 'stop', 'start', 'reset', 'next', 'prev']:
        if controller not in controls:
            controls[controller] = 0

    _caesium.create_caesium(speed, range, markers, controls)

    yield Caesium(speed, range)

    _caesium.destroy_caesium()
