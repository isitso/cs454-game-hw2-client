from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseChat(ServerResponse):
    def execute(self, data):
        try:
            # TODO

            self.log('Received [' + str(Constants.S_CHAT) + '] ResponseChat')
        except:
            self.log('Bad [' + str(Constants.S_CHAT) + '] ResponseChat')
            print_exc()
