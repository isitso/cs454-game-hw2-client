from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseGoToCharacterSelection(ServerResponse):
    def execute(self, data):
        try:
            # TODO

            self.log('Received [' + str(Constants.S_GO_TO_CHARACTER_SELECTION) + '] ResponseGoToCharacterSelection')
        except:
            self.log('Bad [' + str(Constants.S_GO_TO_CHARACTER_SELECTION) + '] ResponseGoToCharacterSelection')
            print_exc()
