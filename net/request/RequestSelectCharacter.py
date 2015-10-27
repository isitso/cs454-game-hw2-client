from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestSelectCharacter(ServerRequest):
    def send(self, kwargs):
        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.C_SELECT_CHARACTER)
            pkg.addInt32(kwargs['character'])

            self.cWriter.send(pkg, self.connection)

            self.log('Sent [' + str(Constants.C_SELECT_CHARACTER) + '] RequestSelectCharacter')
        except:
            self.log('Bad [' + str(Constants.C_SELECT_CHARACTER) + '] RequestSelectCharacter')
            print_exc()
