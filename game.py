import math

from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode
from panda3d.core import Point3, Vec3, Vec4
from panda3d.core import CompassEffect, KeyboardButton, WindowProperties
from direct.interval.LerpInterval import LerpPosInterval, LerpPosHprInterval
from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectButton
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor

from common.Constants import Constants

# helpers
from direct.showbase.PythonUtil import clampScalar

def addInstructions(pos, msg):
    return OnscreenText(text = msg, style = 1, fg = (1, 1, 1, 1),
                        pos = (-1.3, pos), align = TextNode.ALeft, scale = .05)

def addTitle(text):
    return OnscreenText(text = text, style = 1, fg = (1, 1, 1, 1),
                        pos = (1.3, -0.95), align = TextNode.ARight, scale = .07)

class Camera(object):
    """Uses mouse controls to orbit the camera around a parent."""

    def __init__(self, game, parent):
        self.game = game

        # class properties for camera rotation
        self.heading = 0
        self.pitch = 0

        # class properties for camera zoom
        self.targetY = -6
        self.interval = None

        # find screen center
        props = base.win.getProperties()
        self.centerX = props.getXSize() / 2
        self.centerY = props.getYSize() / 2

        # constrain mouse
        base.disableMouse() # disable default mouse camera control
        self.hideMouse()

        # set up floater
        self.floater = render.attachNewNode('floater')
        self.floater.reparentTo(parent) # inherit position from parent, but rotation and scale from render
        self.floater.setEffect(CompassEffect.make(render, CompassEffect.P_rot | CompassEffect.P_scale))
        self.floater.setZ(1) # distance above model

        # set up camera
        base.camera.reparentTo(self.floater)
        base.camera.setY(self.targetY) # original distance from model
        base.camera.lookAt(self.floater)

        # camera zooming
        # TODO move into method, clamp Y value?
        base.accept('wheel_up', lambda: self.zoom(2))
        base.accept('shift-wheel_up', lambda: self.zoom(2))
        base.accept('wheel_down', lambda: self.zoom(-2))
        base.accept('shift-wheel_down', lambda: self.zoom(-2))

        # start task
        taskMgr.add(self.mouseControl, 'Camera.mouseControl')

    def hideMouse(self):
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        base.win.requestProperties(props)

    def showMouse(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        props.setMouseMode(WindowProperties.M_absolute)
        base.win.requestProperties(props)

    def mouseControl(self, task):
        if self.game.isChatting: return task.cont

        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()

        # update heading & pitch based on mouse movement from screen center
        if base.win.movePointer(0, self.centerX, self.centerY):
            self.heading -= (x - self.centerX) * 0.5
            self.pitch -= (y - self.centerY) * 0.5

        # constrain pitch
        if self.pitch < 280: self.pitch = 280
        if self.pitch > 360: self.pitch = 360

        # update floater
        self.floater.setHpr(self.heading, self.pitch, 0)

        return task.cont

    def zoom(self, amount):
        if self.game.isChatting: return

        self.targetY = clampScalar(self.targetY + amount, -2, -15)

        if self.interval is not None: self.interval.pause()
        self.interval = LerpPosInterval(base.camera,
                                        duration = 0.6,
                                        pos = Vec3(base.camera.getX(), self.targetY, base.camera.getZ()),
                                        blendType = 'easeOut',
                                        name = 'Camera.zoom')
        self.interval.start()

class Character(object):
    """Handles character models and animations."""

    def __init__(self, id, name, model):
        # class properties
        self.id = id
        self.name = name
        self.modelType = model

        self.isMoving = False

        self.entity = render.attachNewNode('entity')
        self.target = render.attachNewNode('target')

        # set up model
        if model == Constants.CHAR_RALPH:
            self.model = Actor('models/ralph',
                                    {'run': 'models/ralph-run',
                                     'walk': 'models/ralph-walk'})
            self.model.setScale(0.2)
        elif model == Constants.CHAR_PANDA:
            self.model = Actor('models/panda-model',
                                    {'run': 'models/panda-walk4',
                                     'walk': 'models/panda-walk4'})
            self.model.setScale(0.003)
        elif model == Constants.CHAR_VEHICLE:
            self.model = Actor('models/car', {})
            self.model.setScale(0.3)
            self.model.setPos(0, 0.2, 0.1)

        self.model.reparentTo(self.entity)

        # start movement task
        taskMgr.doMethodLater(1.0 / Constants.TICKRATE, self.move, 'Character[' + str(id) + '].move')

    def move(self, task):
        diffPos = self.target.getPos() - self.entity.getPos()
        diffH = (self.target.getH() - self.entity.getH()) % 360

        if diffPos.lengthSquared() < 0.001 and -0.1 < diffH < 0.1:
            if self.isMoving:
                self.model.stop()
                self.model.pose('walk', 5)
                self.isMoving = False
        else:
            if not self.isMoving:
                self.model.loop('run')
                self.isMoving = True

            interval = LerpPosHprInterval(self.entity,
                                          duration = task.getDelay(),
                                          pos = self.target.getPos(),
                                          hpr = self.target.getHpr(),
                                          name = 'Character[' + str(self.id) + '].move.interval')
            interval.start()

        return task.again

    def destroy(self):
        self.entity.removeNode()
        self.entity = None
        self.model = None
        self.target.removeNode()
        self.target = None
        taskMgr.remove('Character[' + str(self.id) + '].move')

class Player(object):
    """Handles player character motion from user input."""

    def __init__(self, game, character):
        self.game = game
        self.character = character

        # class properties
        self.buttons = {
            'forward': KeyboardButton.ascii_key('w'),
            'backward': KeyboardButton.ascii_key('s'),
            'left': KeyboardButton.ascii_key('a'),
            'right': KeyboardButton.ascii_key('d'),
            'sprint': KeyboardButton.shift()
        }
        self.moved = False

        # start movement task
        taskMgr.add(self.move, 'Player.move')
        taskMgr.doMethodLater(1.0 / Constants.TICKRATE, self.sendLoc, 'Player.sendLoc')

    def move(self, task):
        if self.game.isChatting: return task.cont

        oldPos = self.character.target.getPos()

        # use polling to detect keypresses
        is_down = base.mouseWatcherNode.is_button_down

        move = is_down(self.buttons['forward']) - is_down(self.buttons['backward'])
        turn = is_down(self.buttons['right']) - is_down(self.buttons['left'])
        sprint = is_down(self.buttons['sprint']) + 1

        # move character as needed
        dt = globalClock.getDt()
        if turn: self.character.target.setH(self.character.target.getH() + turn * -300 * dt)
        if move:
            vec = Vec3(0, move * sprint * -8 * dt, 0)

            # collision checking
            self.character.target.setPos(self.character.target, vec)

        # update
        if turn or move:
            self.moved = True

        return task.cont

    def sendLoc(self, task):
        if self.moved:
            self.moved = False
            self.game.main.cManager.sendRequest(Constants.C_MOVE,
                { 'x': self.character.target.getX()
                , 'y': self.character.target.getY()
                , 'z': self.character.target.getZ()
                , 'h': self.character.target.getH()
                , 'p': self.character.target.getP()
                , 'r': self.character.target.getR()
                })
        return task.again

class Sphere(object):
    """A mostly static sphere that spins when a Character is nearby."""

    def __init__(self, game, type):
        self.game = game

        self.model = loader.loadModel('models/planet_sphere')
        self.model.reparentTo(render)

        if type == 'sun':
            self.model.setTexture(loader.loadTexture('models/sun_1k_tex.jpg'), 1)
            self.scale = 8
        elif type == 'earth':
            self.model.setTexture(loader.loadTexture('models/earth_1k_tex.jpg'), 1)
            self.scale = 4
        elif type == 'venus':
            self.model.setTexture(loader.loadTexture('models/venus_1k_tex.jpg'), 1)
            self.scale = 3

        self.model.setScale(self.scale)
        self.spin = self.model.hprInterval(self.scale * 3, Vec3(360, 0, 0))
        self.spin.loop()  # set up the interval to loop
        self.spin.pause() # then pause so we don't start in motion

        self.maxDist = self.scale * 2.5
        taskMgr.add(self.move, 'Sphere.move')

    def move(self, task):
        spinning = self.checkDistance(self.game.character)
        if not spinning:
            for id in self.game.characters:
                spinning = self.checkDistance(self.game.characters[id])
                if spinning: break

        if spinning != self.spin.isPlaying():
            if spinning:
                self.spin.resume()
            else:
                self.spin.pause()

        return task.cont

    def checkDistance(self, character):
        if character is None: return False
        return self.model.getPos(character.entity).lengthSquared() <= (self.maxDist * self.maxDist)

class Chat(object):
    """Handles all chat."""

    def __init__(self, game):
        self.game = game
        self.lines = []
        self.whisperTarget = None

        props = base.win.getProperties()
        ratio = float(props.getXSize()) / props.getYSize()

        self.frame = DirectFrame(frameColor = (0, 0, 0, 0),
                                 frameSize = (0, 1, 0, 1),
                                 pos = (-ratio, 0, -1))

        self.text = OnscreenText(text = '',
                                 pos = (0.01, 0.45),
                                 scale = 0.05,
                                 fg = (1, 1, 1, 1),
                                 bg = (0, 0, 0, 0.2),
                                 parent = self.frame,
                                 align = TextNode.ALeft,
                                 mayChange = True)

        self.entry = DirectEntry(parent = self.frame,
                                 text = '',
                                 scale = 0.05,
                                 pos = (0.01, 0, 0.02),
                                 initialText = '',
                                 width = 26,
                                 numLines = 1)

        self.targetText = OnscreenText(text = '',
                                       pos = (1.34, 0.025),
                                       scale = 0.05,
                                       fg = (1, 1, 1, 1),
                                       bg = (0, 0, 0, 0.4),
                                       parent = self.frame,
                                       align = TextNode.ALeft,
                                       mayChange = True)

        base.accept('t', self.startChatting)
        base.accept('shift-t', self.startChatting)
        base.accept('y', self.startWhispering)
        base.accept('shift-y', self.startWhispering)
        base.accept('arrow_up', lambda: self.changeTarget(1))
        base.accept('shift-arrow_up', lambda: self.changeTarget(1))
        base.accept('arrow_down', lambda: self.changeTarget(-1))
        base.accept('shift-arrow_down', lambda: self.changeTarget(-1))
        base.accept('enter', self.sendChat)
        base.accept('shift-enter', self.sendChat)

    def startChatting(self):
        if not self.game.isChatting:
            self.game.isChatting = True

            # focus on the DirectEntry
            self.entry['focus'] = 1

            # reset whisper target (just in case)
            self.whisperTarget = None

            # enable UI mode
            if self.game.camera is not None:
                self.game.camera.showMouse()

    def startWhispering(self):
        if not self.game.isChatting:
            if not self.game.characters:
                self.addLine('<<System>> Nobody to whisper!')
            else:
                self.startChatting()
                self.changeTarget(0)

    def changeTarget(self, amt):
        if self.game.isChatting:
            targets = self.game.characters.keys()
            targets.sort()

            # find target (or the closest id before target, or 0)
            index = 0
            match = False
            for i in range(len(targets)):
                if targets[i] < self.whisperTarget:
                    index = i
                elif targets[i] == self.whisperTarget:
                    index = i
                    match = True
                    break
                else:
                    break

            # if not found but going back 1 anyway, set amt to 0
            if not match and amt == -1:
                amt = 0

            # set new whisper target
            index = (index + amt) % len(targets)
            self.whisperTarget = targets[index]
            self.targetText.setText('to: ' + str(self.game.characters[self.whisperTarget].name))

    def sendChat(self):
        if self.game.isChatting:
            message = self.entry.get().strip()
            if len(message) > 0:
                # figure out target
                target = ''
                if self.whisperTarget in self.game.characters:
                    target = self.game.characters[self.whisperTarget].name

                # submit message
                self.game.main.cManager.sendRequest(Constants.C_CHAT, {'message': message, 'target': target})

            # stop chatting
            self.stopChatting()

    def stopChatting(self):
        if self.game.isChatting:
            self.game.isChatting = False

            # disable chat entry
            self.entry['focus'] = 0

            # clear text box
            self.entry.enterText('')

            # remove whisper target
            self.whisperTarget = None
            self.targetText.setText('')

            # disable UI mode
            if self.game.camera is not None:
                self.game.camera.hideMouse()

    def addLine(self, line):
        self.lines.append(line)
        self.text.setText('\n'.join(self.lines[-8:]))

class PlayerList(object):
    """Handles the list of players and the associated UI."""

    def __init__(self, game):
        self.game = game
        self.display = False

        props = base.win.getProperties()
        ratio = float(props.getXSize()) / props.getYSize()

        self.frame = DirectFrame(frameColor = (0, 0, 0, 0),
                                 frameSize = (-1, 0, -1, 0),
                                 pos = (ratio, 0, 1))

        self.text = OnscreenText(text = '',
                                 pos = (-0.02, -0.05),
                                 scale = 0.05,
                                 fg = (1, 1, 1, 1),
                                 parent = self.frame,
                                 align = TextNode.ARight,
                                 mayChange = True)

        base.accept('tab', self.toggleDisplay)

    def toggleDisplay(self):
        if not self.game.isChatting:
            self.display = not self.display
            self.updateDisplay()

    def updateDisplay(self):
        if self.display:
            list = 'Current Players:'
            if self.game.character is not None:
                list += '\n' + self.describe(self.game.character)
            for id in self.game.characters:
                list += '\n' + self.describe(self.game.characters[id])
            self.text.setText(list)
            self.display = True
        else:
            self.text.setText('')

    def describe(self, character):
        desc = character.name + ' ('
        if character.modelType == Constants.CHAR_RALPH: desc += 'Ralph'
        if character.modelType == Constants.CHAR_PANDA: desc += 'Panda'
        if character.modelType == Constants.CHAR_VEHICLE: desc += 'Car'
        return desc + ')'

class Game(object):
    """Handles the entire game environment."""

    def __init__(self, main):
        self.main = main
        self.isChatting = False

    def init(self):
        # window setup
        base.win.setClearColor(Vec4(0, 0, 0, 1))

        # display instructions
        addTitle('CS454 HW2')
        addInstructions(0.95, '[ESC]: Quit')
        addInstructions(0.90, '[Mouse Move]: Move camera')
        addInstructions(0.85, '[Mouse Wheel]: Zoom camera')
        addInstructions(0.80, '[W,A,S,D]: Move character')
        addInstructions(0.75, '[T]: Open chat box')
        addInstructions(0.70, '[Y]: Open whisper box')
        addInstructions(0.65, '[Up,Down]: Select whisper target')
        addInstructions(0.60, '[Tab]: Show players')

        # create environment
        environ = loader.loadModel('models/square')      
        environ.reparentTo(render)
        environ.setPos(0, 0, 0)
        environ.setScale(100, 100, 1)
        environ.setTexture(loader.loadTexture('models/moon_1k_tex.jpg'), 1)

        # create lighting
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        render.setLight(render.attachNewNode(ambientLight))

        directionalLight = DirectionalLight('directionalLight')
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(directionalLight))

        # accept special keys
        base.accept('escape', self.exit)
        base.accept('shift-escape', self.exit)

        # create spheres
        sun = Sphere(self, 'sun')
        sun.model.setPos(-15, -15, 8)

        earth = Sphere(self, 'earth')
        earth.model.setPos(-12, 12, 5)

        venus = Sphere(self, 'venus')
        venus.model.setPos(10, 10, 3.5)

        # track game entities
        self.character = None
        self.player = None
        self.camera = None
        self.characters = {}

        self.chat = Chat(self)
        self.playerList = PlayerList(self)

        # DEBUG offline: create character and camera
        #self.character = Character(1, 'Ralph', Constants.CHAR_RALPH)
        #self.player = Player(self, self.character)
        #self.camera = Camera(self, self.character.entity)
        #self.characters[2] = Character(2, 'Panda', Constants.CHAR_PANDA)
        #self.characters[3] = Character(3, 'Car', Constants.CHAR_VEHICLE)

    def exit(self):
        if self.isChatting:
            self.chat.stopChatting()
        else:
            self.main.cManager.sendRequest(Constants.C_DISCONNECT)
