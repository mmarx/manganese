# manganese - mutabor-ng platform
# Copyright (c) 2010, 2011, Maximilian Marx <mmarx@wh2.tu-dresden.de>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from contextlib import contextmanager

import _jack
from _jack import midi_event as event
from classifier import EventClassifier


@contextmanager
def create_client():
    client = _jack.create_client()
    try:
        yield client
    finally:
        _jack.destroy_client(client)


def _describe_type(self):
    return EventClassifier()[self.type]


def _event_repr(self):
    return ("<midi event of type %(type)0x (%(typestring)s) on "
            "channel %(channel)d>") % {'type': self.type,
                                       'typestring': self.describe_type(),
                                       'channel': self.channel,
                                       }

event.__repr__ = _event_repr
event.describe_type = _describe_type
