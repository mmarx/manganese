
from contextlib import contextmanager

from event import Event


class DummyClient(object):
    def __init__(self, events):
        self.events = events
        self.frameno = -1

    def frame(self, frameno):
        if frameno in self.events:
            self.current = self.events[frameno]
        else:
            self.current = []
        self.frameno = frameno

    @property
    def have_events(self):
        return bool(self.current)

    def next_event(self):
        event = Event(self.current[0])
        del self.current[0]
        return event

    def last_frame(self):
        ks = self.events.keys()
        ks.sort()
        return ks[-1]

def create_client(*args, **kwargs):
    @contextmanager
    def create():
        yield DummyClient(*args, **kwargs)

    return create
