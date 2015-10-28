from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseSelectCharacter(ServerResponse):
    def execute(self, data):
        try:
            if self.main.state == Constants.GAMESTATE_LOGGED_IN:
                self.result = data.getInt32()
                if self.result:
                    # successful
                    self.main.state = Constants.GAMESTATE_PLAYING
                    self.main.characterSelection.destroySelectionWindow()
                    self.main.game.init()
                else:
                    # unsuccessful
                    print 'Error selecting character?'

            self.log('Received [' + str(Constants.S_SELECT_CHARACTER) + '] ResponseSelectCharacter')
        except:
            self.log('Bad [' + str(Constants.S_SELECT_CHARACTER) + '] ResponseSelectCharacter')
            print_exc()
