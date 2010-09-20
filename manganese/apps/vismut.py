# vismut - mutabor-ng platform visualization
# Copyright (c) 2010, Maximilian Marx <mmarx@wh2.tu-dresden.de>
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

import _apps

import manganese.vismut as vismut
import manganese.vismut.video


class Application(_apps.Application):

    def run(self):
        print "Hello, World! (from vismut application)"
        print "got args: `", self.args, "'"
        print "got config: `", self.config, "'"

        self.context = vismut.video.SDLContext()

        modes = vismut.video.list_video_modes()
        preferred_mode = self.cfg('mode', '640x480')
        rect = vismut.video.SDLRect.from_string(preferred_mode)

        if rect in modes:
            print 'got it!'
        else:
            print 'meh'