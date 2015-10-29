from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseChat(ServerResponse):
    def execute(self, data):
        try:
            if self.main.state == Constants.GAMESTATE_PLAYING:
                type = data.getInt32()

                if type == 0: # whisper
                    sender_name = data.getString()
                    recipient_name = data.getString()
                    message = data.getString()

                    self.main.game.chat.addLine('[' + sender_name + ' -> ' + recipient_name + ']: ' + message)

                elif type == 1: # global
                    name = data.getString()
                    message = data.getString()

                    self.main.game.chat.addLine('[' + name + ']: ' + message)

                elif type == 2: # whisper fail
                    self.main.game.chat.addLine('<<Server>> Whisper failed.')

                else:
                    self.log('[' + str(Constants.S_CHAT) + '] ResponseChat - Unknown type ' + str(type))

            self.log('Received [' + str(Constants.S_CHAT) + '] ResponseChat')
        except:
            self.log('Bad [' + str(Constants.S_CHAT) + '] ResponseChat')
            print_exc()
