from traceback import print_exc

from direct.distributed.PyDatagram import PyDatagram
from common.Constants import Constants
from net.request.ServerRequest import ServerRequest

class RequestMove(ServerRequest):
    def send(self, kwargs):
        try:
            pkg = PyDatagram()
            pkg.addUint16(Constants.C_MOVE)
            pkg.addFloat32(kwargs['x'])
            pkg.addFloat32(kwargs['y'])
            pkg.addFloat32(kwargs['z'])
            pkg.addFloat32(kwargs['h'])
            pkg.addFloat32(kwargs['p'])
            pkg.addFloat32(kwargs['r'])

            self.cWriter.send(pkg, self.connection)

            self.log('Sent [' + str(Constants.C_MOVE) + '] RequestMove')
        except:
            self.log('Bad [' + str(Constants.C_MOVE) + '] RequestMove')
            print_exc()
