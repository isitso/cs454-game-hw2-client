from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponsePlayerLogout(ServerResponse):
    def execute(self, data):
        try:
            game = self.main.game

            id = data.getInt32()

            if id in game.characters:
                char = game.characters[id]
                name = char.name
                char.destroy()
                del game.characters[id]
                game.chat.addLine('<<Server>> ' + str(name) + ' logged out.')
            else:
                self.log('[' + str(Constants.S_PLAYER_LOGOUT) + '] ResponsePlayerLogout - Unknown character ' + str(id))

            self.log('Received [' + str(Constants.S_PLAYER_LOGOUT) + '] ResponsePlayerLogout')
        except:
            self.log('Bad [' + str(Constants.S_PLAYER_LOGOUT) + '] ResponsePlayerLogout')
            print_exc()
