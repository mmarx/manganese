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


import errno
from exceptions import OSError
from contextlib import contextmanager

import _jack
from event import Event


@contextmanager
def create_client(autoconnect = [], **kwargs):
    client = _jack.create_client()

    client.autoconnect = autoconnect

    for port in client.ports():
        if port in client.autoconnect:
            client.connect_to (port)

    try:
        yield client
    finally:
        _jack.destroy_client(client)


_get_next_event = _jack.JackClient.next_event


def _next_event(self):
    return Event(_get_next_event(self))


_jack.JackClient.next_event = _next_event
_connect_to = _jack.JackClient.connect_to


def _connect(self, port):
    result = _connect_to (self, port)

    if result == 0:             # everything went fine
        return
    if result == errno.EEXIST:  # silently pass if already connected
        return

    raise OSError(result)


_jack.JackClient.connect_to = _connect


def _frame(self, frame):
    pass

_jack.JackClient.frame = _frame


def _check_auto_connect(self):
    while self.have_ports:
        port = self.next_port()
        if port in self.autoconnect:
            self.connect_to(port)


_jack.JackClient.check_auto_connect = _check_auto_connect
