from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseMove(ServerResponse):
    def execute(self, data):
        try:
            if self.main.state == Constants.GAMESTATE_PLAYING:
                id = data.getInt32()
                x = data.getFloat32()
                y = data.getFloat32()
                z = data.getFloat32()
                h = data.getFloat32()
                p = data.getFloat32()
                r = data.getFloat32()

                game = self.main.game
                if id in game.characters:
                    game.characters[id].target.setPosHpr(x, y, z, h, p, r)
                else:
                    self.log('[' + str(Constants.S_PLAYER_MOVE) + '] ResponseMove - Unknown character ' + str(id))

            self.log('Received [' + str(Constants.S_PLAYER_MOVE) + '] ResponseMove')
        except:
            self.log('Bad [' + str(Constants.S_PLAYER_MOVE) + '] ResponseMove')
            print_exc()
