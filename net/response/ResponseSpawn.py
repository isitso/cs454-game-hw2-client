from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseSpawn(ServerResponse):
    def execute(self, data):
        try:
            # TODO

            self.log('Received [' + str(Constants.S_SPAWN) + '] ResponseSpawn')
        except:
            self.log('Bad [' + str(Constants.S_SPAWN) + '] ResponseSpawn')
            print_exc()
