from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseAuth(ServerResponse):
    def execute(self, data):
        try:
            self.result = data.getInt32()
            if not self.result:
                self.error = data.getInt32()
            print 'something'
				
            self.log('Received [' + str(Constants.S_AUTH) + '] ResponseAuth')
        except:
            self.log('Bad [' + str(Constants.S_AUTH) + '] ResponseAuth')
            print_exc()
