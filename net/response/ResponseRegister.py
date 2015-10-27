from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseRegister(ServerResponse):
    def execute(self, data):
        try:
            self.result = data.getInt32()
            if not self.result:
                self.error = data.getInt32()

            # TODO

            self.log('Received [' + str(Constants.S_REGISTER) + '] ResponseRegister')
        except:
            self.log('Bad [' + str(Constants.S_REGISTER) + '] ResponseRegister')
            print_exc()
