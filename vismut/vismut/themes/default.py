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

from . import Theme

class DefaultTheme(Theme):
    colors = {'screen_bg': (255, 255, 255, 255),
              'screen_fg': (0, 0, 0, 255),
              'screen_hl': (50, 230, 230, 128),
              'key_bg': {'active': (200, 230, 250, 255),
                         'inactive': (160, 160, 220, 255),
                         'anchor': (250, 200, 250, 255),
                         'anchor_active': (220, 220, 250, 255),
                         'anchor_initial': (200, 0, 0, 255),
                         'anchor_initial_active': (255, 0, 0, 255),
                         },
              'key_fg': (80, 80, 80, 255),
              'chord_bg': {'major': (255, 255, 0, 255),
                           'minor': (255, 200, 0, 255),
                           },
              }

    def __init__(self, *args, **kwargs):
        super(DefaultTheme, self).__init__(*args, **kwargs)
