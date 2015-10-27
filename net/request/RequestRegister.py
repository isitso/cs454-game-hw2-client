from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestRegister(ServerRequest):
    def send(self):
        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.C_REGISTER)
            # TODO

            self.cWriter.send(pkg, self.connection)

            self.log('Sent [' + str(Constants.C_REGISTER) + '] RequestRegister')
        except:
            self.log('Bad [' + str(Constants.C_REGISTER) + '] RequestRegister')
            print_exc()
