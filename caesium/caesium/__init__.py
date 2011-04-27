
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
def caesium(speed=1.0, range=0.25):
    _caesium.create_caesium(speed, range)
    
    yield Caesium(speed, range)
    
    _caesium.destroy_caesium()
