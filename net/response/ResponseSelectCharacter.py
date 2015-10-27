from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseSelectCharacter(ServerResponse):
    def execute(self, data):
        try:
            self.msg = data.getString()
            # TODO

            self.log('Received [' + str(Constants.S_SELECT_CHARACTER) + '] ResponseSelectCharacter')
        except:
            self.log('Bad [' + str(Constants.S_SELECT_CHARACTER) + '] ResponseSelectCharacter')
            print_exc()
