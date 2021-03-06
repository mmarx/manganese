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

from os import walk
from sys import stderr
from os.path import expanduser, join


# Where to look for config files.
# Each path is passed through os.path.expanduser
# and %(app)s is replaced by the app we're bootstrapping.
# Later entries override earlier ones.

_search_path = ['~/.manganeserc',
                '~/.manganese/manganeserc',
                '~/.manganese/%(app)src',
                '~/.manganese/%(app)s.d/',
                ]


def _try_load(file, context=None):
    """Try to load file as a config file

    This executes the file and uses the locals keys for the config.
    """
    if context is None:
        config = dict()
    else:
        config = context

    try:
        execfile(file, dict(), config)
    except IOError:
        pass
    except SyntaxError as err:
        print >> stderr, ("Syntax error in config file `%s' at %d:%d"
                          % (file, err.lineno, err.offset))
        print >> stderr, err
    return config


def load(app):
    """Load the config for app

    This tries to load each file in the search path.
    """
    config = dict()

    for path in _search_path:
        expanded = expanduser(path) % {'app': app}
        if path[-1:] == '/':
            for root, dirs, files in walk(expanded, topdown=True):
                del dirs[:]
                for file in files:
                    config.update(_try_load(join(root, file), context=config))
        else:
            config.update(_try_load(expanded, context=config))

    return config
