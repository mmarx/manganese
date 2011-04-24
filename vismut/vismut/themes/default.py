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
