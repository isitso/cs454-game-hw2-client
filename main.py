""" Panda3D imports """
from direct.showbase.ShowBase import ShowBase

""" Custom imports"""
from common.Constants import Constants
from net.ConnectionManager import ConnectionManager

from login import Login
from characterSelection import CharacterSelection
from game import Game

class Main(ShowBase):
    def __init__(self):
        self.state = Constants.GAMESTATE_NOT_LOGGED_IN
        self.cManager = ConnectionManager(self)

        if self.startConnection():
            ShowBase.__init__(self)
            self.cManager.initTasks()

            self.login = Login(self)
            self.characterSelection = CharacterSelection(self)
            self.game = Game(self)

            self.login.createLoginWindow()
            #self.characterSelection.createSelectionWindow()
            #self.game.init()

            self.run()

    def startConnection(self):
        """Create a connection to the remote host.

        If a connection cannot be created, it will ask the user to perform
        additional retries.

        """
        if self.cManager.connection == None:
            print 'Connecting...'
            if not self.cManager.startConnection():
                print 'Connection failed!'
                answer = raw_input('Reconnect? (Y/N): ').lower()
                if answer == 'y':
                    return self.startConnection()
                else:
                    return False

        return True

if __name__ == '__main__':
    app = Main()
