
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
