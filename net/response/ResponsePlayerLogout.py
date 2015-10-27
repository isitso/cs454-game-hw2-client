from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponsePlayerLogout(ServerResponse):
    def execute(self, data):
        try:
            # TODO

            self.log('Received [' + str(Constants.S_PLAYER_LOGOUT) + '] ResponsePlayerLogout')
        except:
            self.log('Bad [' + str(Constants.S_PLAYER_LOGOUT) + '] ResponsePlayerLogout')
            print_exc()
