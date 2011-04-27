
from contextlib import contextmanager


import _fonts


@contextmanager
def freetype():
    ft = _fonts.init_freetype()
    yield ft
    _fonts.destroy_freetype(ft)
