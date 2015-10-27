from common.Constants import Constants

from net.request.RequestAuth import RequestAuth
from net.request.RequestDisconnect import RequestDisconnect
from net.request.RequestGoToCharacterSelection import RequestGoToCharacterSelection
from net.request.RequestSelectCharacter import RequestSelectCharacter
from net.request.RequestRegister import RequestRegister
from net.request.RequestMove import RequestMove
from net.request.RequestChat import RequestChat
from net.request.RequestHeartbeat import RequestHeartbeat

class ServerRequestTable:
    """
    The ServerRequestTable contains a mapping of all requests for use
    with the networking component.
    """
    requestTable = {}

    def __init__(self):
        """Initialize the request table."""
        self.add(Constants.C_AUTH, 'RequestAuth')
        self.add(Constants.C_DISCONNECT, 'RequestDisconnect')
        self.add(Constants.C_GO_TO_CHARACTER_SELECTION, 'RequestGoToCharacterSelection')
        self.add(Constants.C_SELECT_CHARACTER, 'RequestSelectCharacter')
        self.add(Constants.C_REGISTER, 'RequestRegister')
        #self.add(Constants.C_CREATE_CHARACTER, 'RequestCreateCharacter')
        self.add(Constants.C_MOVE, 'RequestMove')
        self.add(Constants.C_CHAT, 'RequestChat')
        self.add(Constants.C_HEARTBEAT, 'RequestHeartbeat')

    def add(self, constant, name):
        """Map a numeric request code with the name of an existing request module."""
        if name in globals():
            self.requestTable[constant] = name
        else:
            print 'Add Request Error: No module named ' + str(name)

    def get(self, requestCode):
        """Retrieve an instance of the corresponding request."""
        serverRequest = None

        if requestCode in self.requestTable:
            serverRequest = globals()[self.requestTable[requestCode]]()
        else:
            print 'Bad Request Code: ' + str(requestCode)

        return serverRequest
