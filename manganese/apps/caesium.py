
import os
import os.path

import _apps


from manganese.caesium import caesium


class Application(_apps.Application):

    def run(self):
        markers = self.cfg('markers', {})

        if 'mache' not in markers:
            print "-#- couldn't load any markers"
            the_markers = []
        else:
            the_markers = markers['mache']

        try:
            with caesium(markers=the_markers,
                         controls=self.cfg('controls', {})):
                while True:
                    pass
        except KeyboardInterrupt:
            pass
