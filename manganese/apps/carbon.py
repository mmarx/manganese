
from sys import stderr


import _apps


from manganese.carbon import markers


class Application(_apps.Application):

    def mark(self, marker):
        print marker, ', \t#', self.count
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

        print 'markers = ['
        markers(**args)
        print ']'
