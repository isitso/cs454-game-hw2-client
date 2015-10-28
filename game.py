import sys, math

from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode
from panda3d.core import Point3, Vec3, Vec4
from panda3d.core import CompassEffect, KeyboardButton, WindowProperties
from direct.interval.LerpInterval import LerpPosInterval, LerpPosHprInterval
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

    def __init__(self, parent):
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

        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        base.win.requestProperties(props)

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

    def mouseControl(self, task):
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

    def __init__(self, id, model):
        # class properties
        self.entity = render.attachNewNode('entity')
        self.target = render.attachNewNode('target')
        self.id = id

        self.tickRate = Constants.TICKRATE
        self.isMoving = False

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
        taskMgr.add(self.move, 'Character.move')

    def move(self, task):
        diffPos = self.target.getPos() - self.entity.getPos()
        diffH = self.target.getH() - self.entity.getH()

        if diffPos.getX() == diffPos.getY() == diffPos.getZ() == diffH == 0:
            if self.isMoving:
                self.model.stop()
                self.model.pose('walk', 5)
                self.isMoving = False
        else:
            if not self.isMoving:
                self.model.loop('run')
                self.isMoving = True

            interval = LerpPosHprInterval(self.entity,
                                          duration = 1.0 / self.tickRate,
                                          pos = self.target.getPos(),
                                          hpr = self.target.getHpr(),
                                          name = 'Character[' + str(self.id) + '].move.interval')
            interval.start()

        return task.cont

class Player(object):
    """Handles player character motion from user input."""

    def __init__(self, character):
        self.character = character

        # class properties
        self.buttons = {
            'forward': KeyboardButton.ascii_key('w'),
            'backward': KeyboardButton.ascii_key('s'),
            'left': KeyboardButton.ascii_key('a'),
            'right': KeyboardButton.ascii_key('d'),
            'sprint': KeyboardButton.shift()
        }

        # start movement task
        taskMgr.add(self.move, 'Player.move')

    def move(self, task):
        # use polling to detect keypresses
        is_down = base.mouseWatcherNode.is_button_down

        move = is_down(self.buttons['forward']) - is_down(self.buttons['backward'])
        turn = is_down(self.buttons['right']) - is_down(self.buttons['left'])
        sprint = is_down(self.buttons['sprint']) + 1

        # move character as needed
        dt = globalClock.getDt()
        if turn: self.character.target.setH(self.character.target, turn * -300 * dt)
        if move: self.character.target.setY(self.character.target, move * sprint * -8 * dt)
        if turn or move: self.character.tickRate = 1000 / dt

        return task.cont

class Sphere(object):
    """A mostly static sphere that spins when a Character is nearby."""

    def __init__(self, type):
        self.model = loader.loadModel('models/planet_sphere')
        self.model.reparentTo(render)

        if type == 'sun':
            self.model.setTexture(loader.loadTexture('models/sun_1k_tex.jpg'), 1)
            self.model.setScale(8)
        elif type == 'earth':
            self.model.setTexture(loader.loadTexture('models/earth_1k_tex.jpg'), 1)
            self.model.setScale(4)
        elif type == 'venus':
            self.model.setTexture(loader.loadTexture('models/venus_1k_tex.jpg'), 1)
            self.model.setScale(3)

        taskMgr.add(self.move, 'Sphere.move')

    def move(self, task):
        # TODO
        return task.cont

class Game(object):
    """Handles the entire game environment."""

    def __init__(self, main):
        self.main = main

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
        addInstructions(0.65, '[Tab]: Show players')

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
        base.accept('escape', sys.exit)

        # create character
        self.character = Character(1, Constants.CHAR_RALPH)
        self.player = Player(self.character)

        # create camera
        self.camera = Camera(self.character.entity)

        # FIXME test spheres
        sun = Sphere('sun')
        sun.model.setPos(10, 10, 7)

        earth = Sphere('earth')
        earth.model.setPos(-8, -8, 5)

        venus = Sphere('venus')
        venus.model.setPos(5, -5, 3.5)
