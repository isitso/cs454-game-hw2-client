from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

from game import Character, Player, Camera

class ResponseSpawn(ServerResponse):
    def execute(self, data):
        try:
            if self.main.state == Constants.GAMESTATE_PLAYING:
                game = self.main.game

                type = data.getInt32()
                char_id = data.getInt32()
                name = data.getString()
                char_type = data.getInt32()
                x = data.getFloat32()
                y = data.getFloat32()
                z = data.getFloat32()
                h = data.getFloat32()
                p = data.getFloat32()
                r = data.getFloat32()

                character = Character(char_id, name, char_type)
                character.entity.setPosHpr(x, y, z, h, p, r)
                character.target.setPosHpr(x, y, z, h, p, r)
                if type == 2: # main player
                    game.character = character
                    game.player = Player(game, character)
                    game.camera = Camera(game, character.entity)
                elif type == 0: # other player
                    game.characters[char_id] = character
                    game.chat.addLine('<<Server>> ' + str(name) + ' logged in.')
                    game.playerList.updateDisplay()
                else: # unknown
                    self.log('[' + str(Constants.S_SPAWN) + '] ResponseSpawn - Unknown type ' + str(type))

            self.log('Received [' + str(Constants.S_SPAWN) + '] ResponseSpawn')
        except:
            self.log('Bad [' + str(Constants.S_SPAWN) + '] ResponseSpawn')
            print_exc()
