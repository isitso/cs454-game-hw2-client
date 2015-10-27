from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestChat(ServerRequest):
    def send(self, kwargs):
        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.C_CHAT)
            if kwargs['target']:
                pkg.addInt32(1)
                pkg.addString(kwargs['target'])
            else:
                pkg.addInt32(0)
            pkg.addString(kwargs['message'])

            self.cWriter.send(pkg, self.connection)

            self.log('Sent [' + str(Constants.C_CHAT) + '] RequestChat')
        except:
            self.log('Bad [' + str(Constants.C_CHAT) + '] RequestChat')
            print_exc()
