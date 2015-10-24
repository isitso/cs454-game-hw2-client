from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseCreateAccount(ServerResponse):

    def execute(self, data):

        try:
			self.flag = data.getInt32()
			if self.flag:
				# registration success.
				print 'registration success'
				# loop through the list
			else:
				# registration fail. check error type. error type msg will be added in Constants later
				errorID = data.getInt32()
				print 'Error ID: ', errorID
				
#            self.msg = data.getString()

#            print "ResponseLogin - ", self.msg

            #self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')

        except:
            self.log('Bad [' + str(Constants.RAND_STRING) + '] String Response')
            print_exc()
