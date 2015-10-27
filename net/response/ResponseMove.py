from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseMove(ServerResponse):
    def execute(self, data):
        try:
            # TODO

            self.log('Received [' + str(Constants.S_PLAYER_MOVE) + '] ResponseMove')
        except:
            self.log('Bad [' + str(Constants.S_PLAYER_MOVE) + '] ResponseMove')
            print_exc()
