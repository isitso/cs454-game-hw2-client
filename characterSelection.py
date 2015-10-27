from panda3d.core import TextNode
from direct.gui.DirectGui import DirectFrame, DirectButton
from direct.gui.OnscreenText import OnscreenText

from common.Constants import Constants

class CharacterSelection(object):
    def __init__(self, main):
        self.main = main

        self.frame = None
        self.title = None
        self.ralphBtn = None
        self.pandaBtn = None
        self.carBtn = None

    def createSelectionWindow(self):
        self.frame = DirectFrame(frameColor = (0, 0, 0, 1),
                                 frameSize = (-3, 3, -3, 3),
                                 pos = (-0.5, 0, 0.9))

        self.title = OnscreenText(text = 'Select Character',
                                  pos = (0.5, -0.2),
                                  scale = 0.15,
                                  fg = (1, 0.5, 0.5, 1),
                                  align = TextNode.ACenter,
                                  parent = self.frame,
                                  mayChange = False)

        self.ralphBtn = DirectButton(self.frame,
                                     text = 'Ralph',
                                     scale = 0.1,
                                     command = lambda: self.clicked(Constants.CHAR_RALPH),
                                     pos = (-0.3, 0, -1))

        self.pandaBtn = DirectButton(self.frame,
                                     text = 'Panda',
                                     scale = 0.1,
                                     command = lambda: self.clicked(Constants.CHAR_PANDA),
                                     pos = (0.5, 0, -1))

        self.carBtn = DirectButton(self.frame,
                                   text = 'Car',
                                   scale = 0.1,
                                   command = lambda: self.clicked(Constants.CHAR_VEHICLE),
                                   pos = (1.3, 0, -1))

    def destroySelectionWindow(self):
        self.frame.destroy()
        self.frame = None
        self.title = None
        self.ralphBtn = None
        self.pandaBtn = None
        self.carBtn = None

    def clicked(self, char):
        self.main.cManager.sendRequest(Constants.C_SELECT_CHARACTER, {'character': char})
