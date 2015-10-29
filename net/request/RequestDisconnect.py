from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestDisconnect(ServerRequest):
    def send(self, args):
        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.C_DISCONNECT)

            self.cWriter.send(pkg, self.connection)

            self.log('Sent [' + str(Constants.C_DISCONNECT) + '] RequestDisconnect')
        except:
            self.log('Bad [' + str(Constants.C_DISCONNECT) + '] RequestDisconnect')
            print_exc()
