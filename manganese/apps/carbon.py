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

from sys import stderr


import _apps


from manganese.carbon import markers


class Application(_apps.Application):

    def mark(self, marker):
        print '\t', marker, ', \t#', self.count
        self.count += 1

    def run(self):
        if len(self.args) < 3 or len(self.args) > 5:
            print >> stderr, '-!- usage:', \
                  self.args[0], 'name midifile [channel]'
            return

        args = {'name': self.args[1],
                'midifile': self.args[2],
                'callback': self.mark,
                }

        if len(self.args) == 4:
            args['channel'] = self.args[3]

        self.count = 0

        print "markers['%(name)s']" % args, '= ['
        markers(**args)
        print ']'
