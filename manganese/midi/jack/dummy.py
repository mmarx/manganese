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
