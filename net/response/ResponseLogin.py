from traceback import print_exc

from common.Constants import Constants
from net.response.ServerResponse import ServerResponse

class ResponseLogin(ServerResponse):

    def execute(self, data):

        try:
			self.flag = data.getInt32()
			if self.flag:
				# success. grab character list
				self.characterCount = self.getInt32()
				print 'Login success. Character count = ', self.charCount
				# loop through the list
				for i in range(self.charCount):
					characterID = data.getInt32()
					characterType = data.getInt32()
					characterName = data.getString()
					print 'Character ' , i, ': ID = ', characterID, '. Type = ', characterType, '. Name = ', characterName
			else:
				# login fail. check error type. error type msg will be added in Constants later
				errorID = data.getInt32()
				print 'Error ID: ', errorID
				
#            self.msg = data.getString()

#            print "ResponseLogin - ", self.msg

            #self.log('Received [' + str(Constants.RAND_STRING) + '] String Response')

        except:
            self.log('Bad [' + str(Constants.RAND_STRING) + '] String Response')
            print_exc()
