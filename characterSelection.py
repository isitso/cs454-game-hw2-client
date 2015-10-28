from panda3d.core import TextNode
from direct.gui.DirectGui import DirectFrame, DirectButton
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
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
        self.frame = DirectFrame(frameColor = (0, 0, 0, 0),
                                 frameSize = (-3, 3, -3, 3),
                                 pos = (-0.5, 0, 0.9))

        self.title = OnscreenText(text = 'Select Character',
                                  pos = (0.5, -0.2),
                                  scale = 0.15,
                                  fg = (1, 0.5, 0.5, 1),
                                  align = TextNode.ACenter,
                                  parent = self.frame,
                                  mayChange = False)

        #load button maps
        self.btn_maps = self.main.loader.loadModel('models/button_maps.egg')
        self.ralphBtn = DirectButton(self.frame,
                                     text = 'Ralph',
                                     scale = 0.1,
                                     command = lambda: self.clicked(Constants.CHAR_RALPH),
                                     pos = (-0.3, 0, -1.8),
                                     geom = (self.btn_maps.find('models/button_ready'),
                                             self.btn_maps.find('models/button_click'),
                                             self.btn_maps.find('models/button_rollover')))


        self.pandaBtn = DirectButton(self.frame,
                                     text = 'Panda',
                                     scale = 0.1,

                                     command = lambda: self.clicked(Constants.CHAR_PANDA),
                                     pos = (0.5, 0, -1.8))

        self.carBtn = DirectButton(self.frame,
                                   text = 'Car',
                                   scale = 0.1,
                                   command = lambda: self.clicked(Constants.CHAR_VEHICLE),
                                   pos = (1.3, 0, -1.8))


        # disable the mouse
        base.disableMouse()
        
        # load environment
        self.environ = self.main.loader.loadModel('models/environment')
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)
        self.environ.reparentTo(self.main.render)
        
		# load the models
        print 'loading models'
        self.panda = Actor('models/panda-model',
                                    {'run': 'models/panda-walk4',
                                     'walk': 'models/panda-walk4'})
        self.ralph = Actor('models/ralph',
                           {'run': 'models/ralph-run',
                            'walk': 'models/ralph-walk'})
        self.panda.setScale(0.001, 0.001, 0.001)
        self.panda.setPos(0, 0, 0)
        self.ralph.setScale(0.1, 0.1, 0.1)
        self.ralph.setPos(-1, 0, 0)
        
        # set camera
        base.camera.setPos(0, -5, 1)
        base.camera.lookAt(0, 0, .5)
        
#         self.main.camera.lookAt(self.panda.getPos())
#         seek.ralph = Actor('models/ralph',
#                                     {'run': 'models/ralph-run',
#                                      'walk': 'models/ralph-walk'})
#         self.ralph.setScale(0.003)
        self.panda.reparentTo(render)
        self.ralph.reparentTo(render)
        self.panda.loop('walk')
        self.ralph.loop('walk')
		
    def destroySelectionWindow(self):
        self.frame.destroy()
        self.frame = None
        self.title = None
        self.ralphBtn = None
        self.pandaBtn = None
        self.carBtn = None

    def clicked(self, char):
        self.main.cManager.sendRequest(Constants.C_SELECT_CHARACTER, {'character': char})
