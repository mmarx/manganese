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

import os
import os.path

import _apps


from manganese.caesium import caesium


class Application(_apps.Application):

    def run(self):
        markers = self.cfg('markers', {})

        the_markers = self.cfg('use-markers', 'mache')

        offset = self.cfg('offset', 21)
        offset = int(offset)

        if the_markers not in markers:
            print "-#- couldn't load any markers"
            the_markers = []
        else: the_markers = markers[the_markers]

        try:
            with caesium(markers=the_markers,
                         offset=offset,
                         factor=float(self.cfg('factor', 1)),
                         controls=self.cfg('controls', {})):
                while True:
                    pass
        except KeyboardInterrupt:
            pass
