from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestGoToCharacterSelection(ServerRequest):
    def send(self):
        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.C_GO_TO_CHARACTER_SELECTION)

            self.cWriter.send(pkg, self.connection)

            self.log('Sent [' + str(Constants.C_GO_TO_CHARACTER_SELECTION) + '] RequestGoToCharacterSelection')
        except:
            self.log('Bad [' + str(Constants.C_GO_TO_CHARACTER_SELECTION) + '] RequestGoToCharacterSelection')
            print_exc()
