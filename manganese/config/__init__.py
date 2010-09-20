# manganese - mutabor-ng platform
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


from sys import stderr
from os.path import expanduser


# Where to look for config files.
# Each path is passed through os.path.expanduser
# and %(app)s is replaced by the app we're bootstrapping.
# Later entries override earlier ones.

_search_path = ['~/.manganeserc',
                '~/.manganese/manganeserc',
                '~/.manganese/%(app)src',
                ]


def _try_load(file):
    """Try to load file as a config file

    This executes the file and uses the locals keys for the config.
    """
    config = dict()
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
        config.update(_try_load(expanduser(path) % {'app': app}))

    return config
