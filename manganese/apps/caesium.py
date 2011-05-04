
import _apps


from manganese.caesium import caesium


class Application(_apps.Application):

    def run(self):
        try:
            with caesium():
                while True:
                    pass
        except KeyboardInterrupt:
            pass
