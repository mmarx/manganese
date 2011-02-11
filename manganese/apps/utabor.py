
import pprint
import os.path

import _apps

import manganese.utabor._utabor as utabor


class Application(_apps.Application):

    midi = [0x00513090,
            0x00513490,
            0x00513790,
            0x00003080,
            0x00003480,
            0x00003780,
            0x00512d90,
            0x00513190,
            0x00513490,
            0x00002d80,
            0x00003180,
            0x00003480,
            ]

    def run(self):
        ut = utabor.get_uTabor()
        logic = os.path.join(self.prefix(), 'data', 'utabor', 'demo.mut')
        ut.load_logic(logic)
        ut.select_action('N', True)

        pp = pprint.PrettyPrinter(indent=2)

        pp.pprint(ut.tone_system)

        for word in self.midi:
            ut.handle_midi(word)
            print ut.width, ut.anchor, ut.keys

        pp.pprint(ut.tone_system)
