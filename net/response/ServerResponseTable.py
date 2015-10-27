from common.Constants import Constants

from net.response.ResponseAuth import ResponseAuth
from net.response.ResponseDisconnect import ResponseDisconnect
from net.response.ResponseGoToCharacterSelection import ResponseGoToCharacterSelection
from net.response.ResponseSelectCharacter import ResponseSelectCharacter
from net.response.ResponseRegister import ResponseRegister
from net.response.ResponseMove import ResponseMove
from net.response.ResponsePlayerLogout import ResponsePlayerLogout
from net.response.ResponseChat import ResponseChat
from net.response.ResponseSpawn import ResponseSpawn

class ServerResponseTable:
    """
    The ServerResponseTable contains a mapping of all responses for use
    with the networking component.
    """
    responseTable = {}

    def __init__(self):
        """Initialize the response table."""
        self.add(Constants.S_AUTH, 'ResponseAuth')
        self.add(Constants.S_DISCONNECT, 'ResponseDisconnect')
        self.add(Constants.S_GO_TO_CHARACTER_SELECTION, 'ResponseGoToCharacterSelection')
        self.add(Constants.S_SELECT_CHARACTER, 'ResponseSelectCharacter')
        self.add(Constants.S_REGISTER, 'ResponseRegister')
        #self.add(Constants.S_CREATE_CHARACTER, 'ResponseCreateCharacter')
        self.add(Constants.S_PLAYER_MOVE, 'ResponseMove')
        self.add(Constants.S_PLAYER_LOGOUT, 'ResponsePlayerLogout')
        self.add(Constants.S_CHAT, 'ResponseChat')
        self.add(Constants.S_SPAWN, 'ResponseSpawn')

    def add(self, constant, name):
        """Map a numeric response code with the name of an existing response module."""
        if name in globals():
            self.responseTable[constant] = name
        else:
            print 'Add Response Error: No module named ' + str(name)

    def get(self, responseCode):
        """Retrieve an instance of the corresponding response."""
        serverResponse = None

        if responseCode in self.responseTable:
            serverResponse = globals()[self.responseTable[responseCode]]()
        else:
            print 'Bad Response Code: ' + str(responseCode)

        return serverResponse
