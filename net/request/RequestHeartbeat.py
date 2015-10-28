from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestHeartbeat(ServerRequest):
    def send(self, args):
        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.C_HEARTBEAT)

            self.cWriter.send(pkg, self.connection)

            #self.log('Sent [' + str(Constants.C_HEARTBEAT) + '] RequestHeartbeat')
        except:
            self.log('Bad [' + str(Constants.C_HEARTBEAT) + '] RequestHeartbeat')
            print_exc()
