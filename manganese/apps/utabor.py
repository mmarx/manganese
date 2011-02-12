
import os.path

import _apps

import manganese.utabor._utabor as utabor
import manganese.midi.pitch as pitch
import manganese.utabor.net as net


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
        print '-!- initial tone net:'
        tn = net.ToneNet(pitch.PitchClassifier(naming=pitch.NamingDE))
        tn.print_net()

        for word in self.midi:
            ut.handle_midi(word)
            if ut.anchor_changed:
                tn.move(ut.anchor)
                print '-!- anchor changed'

            if ut.keys_changed:
                print '-!- keys changed'

            if ut.need_update:
                tn.print_net(mark=ut.keys)
