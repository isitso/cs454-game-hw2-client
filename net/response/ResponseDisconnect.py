from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseDisconnect(ServerResponse):
    def execute(self, data):
        try:
            # TODO

            self.log('Received [' + str(Constants.S_DISCONNECT) + '] ResponseDisconnect')
        except:
            self.log('Bad [' + str(Constants.S_DISCONNECT) + '] ResponseDisconnect')
            print_exc()
