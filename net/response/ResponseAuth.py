from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseAuth(ServerResponse):
    def execute(self, data):
        try:
            if self.main.state == Constants.GAMESTATE_NOT_LOGGED_IN:
                self.result = data.getInt32()
                if self.result:
                    # successful login
                    self.main.state = Constants.GAMESTATE_LOGGED_IN
                    self.main.login.destroyLoginWindow()
                    self.main.characterSelection.createSelectionWindow()
                else:
                    # unsuccessful login
                    self.error = data.getInt32()
                    if self.error == 0: self.main.login.displayError('Error: Account not found.')
                    elif self.error == 1: self.main.login.displayError('Error: Incorrect password.')
                    elif self.error == 2: self.main.login.displayError('Error: Account already in use.')
                    else: self.main.login.displayError('Error: Login failed. Unknown error code: ' + str(self.error))

            self.log('Received [' + str(Constants.S_AUTH) + '] ResponseAuth')
        except:
            self.log('Bad [' + str(Constants.S_AUTH) + '] ResponseAuth')
            print_exc()
