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

import sys
import os.path

import manganese.config as config


class Application(object):
    def __init__(self, args):
        self.args = args
        self.config = config.load(app=args[0])
        print >> sys.stderr, \
              "Hello, World! (from managenese application framework)"

        for opt in args:
            if '=' in opt:
                key, value = opt.split('=')

                while key.startswith('-'):
                    key = key[1:]

                self.config[key] = value

    def prefix(self):
        return sys.path[-1]

    def data_prefix(self, app=None):
        if app is None:
            suffix = self.args[0]
        else:
            suffix = app

        return os.path.join(self.prefix(), 'data', suffix)

    def data(self, filename, *args, **kwargs):
        return os.path.join(self.data_prefix(*args, **kwargs), filename)

    def cfg(self, key, default):
        if key in self.config:
            return self.config[key]
        else:
            return default
