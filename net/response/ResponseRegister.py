from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseRegister(ServerResponse):
    def execute(self, data):
        try:
            if self.main.state == Constants.GAMESTATE_NOT_LOGGED_IN:
                self.result = data.getInt32()
                if self.result:
                    # successful registration
                    self.main.login.displayError('Registration successful. Please login.')
                else:
                    # unsuccessful registration
                    self.error = data.getInt32()
                    if self.error == 0: self.main.login.displayError('Error: Registration failed. Account already exists.')
                    elif self.error == 1: self.main.login.displayError('Error: Registration failed. Please fill in all fields.')
                    else: self.main.login.displayError('Error: Registration failed. Unknown error code: ' + str(self.error))

            self.log('Received [' + str(Constants.S_REGISTER) + '] ResponseRegister')
        except:
            self.log('Bad [' + str(Constants.S_REGISTER) + '] ResponseRegister')
            print_exc()
