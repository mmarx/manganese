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


import time


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
            self.context.set_mode(rect)
            time.sleep(5)
        else:
            print 'meh'
