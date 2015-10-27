""" Python Imports """
from sys import exit

""" Panda3D Imports """
from panda3d.core import TextNode
from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectButton
from direct.gui.OnscreenText import OnscreenText

from common.Constants import Constants

class Login(object):
    def __init__(self, main):
        self.main = main

        self.frame = None
        self.title = None
        self.error = None
        self.username = None
        self.userTextbox = None
        self.password = None
        self.passTextbox = None
        self.cpassword = None
        self.cpassTextbox = None
        self.submitBtn = None
        self.registerBtn = None
        self.cancelBtn = None

    # login screen
    def createLoginWindow(self):
        self.frame = DirectFrame(frameColor = (0, 0, 0, 1),
                                 frameSize = (-1, 1, -1, 1),
                                 pos = (-0.5, 0, 0.5))

        self.title = OnscreenText(text = 'Login',
                                  pos = (0, 0.3),
                                  scale = 0.15,
                                  fg = (1, 0.5, 0.5, 1),
                                  align = TextNode.ACenter,
                                  parent = self.frame,
                                  mayChange = False)

        # username
        self.username = OnscreenText(text = 'Username:',
                                     pos = (-0.1, 0.0),
                                     scale = 0.05,
                                     fg = (1, 0.5, 0.5, 1),
                                     align = TextNode.ACenter,
                                     parent = self.frame,
                                     mayChange = False)
        self.userTextbox = DirectEntry(self.frame, # parent
                                       text = '',
                                       scale = 0.05,
                                       pos = (0.1, 0, 0),
                                       initialText = '[username]',
                                       numLines = 1,
                                       focus = 1,
                                       focusInCommand = self.userTextFocus,
                                       focusOutCommand = self.userTextBlur)

        # password
        self.password = OnscreenText(text = 'Password:',
                                     pos = (-0.1, -0.2),
                                     scale = 0.05,
                                     fg = (1, 0.5, 0.5, 1),
                                     align = TextNode.ACenter,
                                     parent = self.frame,
                                     mayChange = False)
        self.passTextbox = DirectEntry(self.frame, # parent
                                       text = '',
                                       scale = 0.05,
                                       pos = (0.1, 0, -0.2),
                                       initialText = '[password]',
                                       numLines = 1,
                                       focus = 0,
                                       focusInCommand = self.passTextFocus,
                                       focusOutCommand = self.passTextBlur)

        # buttons
        self.submitBtn = DirectButton(self.frame, # parent
                                      text = 'Login',
                                      scale = 0.08,
                                      command = self.clickedSubmit,
                                      pos = (0.8, 0.0, -0.90))
        self.registerBtn = DirectButton(self.frame, # parent
                                        text = 'Register',
                                        scale = 0.08,
                                        command = self.clickedRegister,
                                        pos = (0.5, 0.0, -0.90))
        self.cancelBtn = DirectButton(self.frame, # parent
                                      text = 'Cancel',
                                      scale = 0.08,
                                      command = self.clickedCancel,
                                      pos = (0.2, 0.0, -0.90))

    def destroyLoginWindow(self):
        self.frame.destroy()
        self.frame = None
        self.title = None
        self.error = None
        self.username = None
        self.userTextbox = None
        self.password = None
        self.passTextbox = None
        self.submitBtn = None
        self.registerBtn =  None
        self.cancelBtn =  None

    # register screen
    def createRegisterWindow(self):
        self.frame = DirectFrame(frameColor = (0, 0, 0, 1),
                                 frameSize = (-1, 1, -1, 1),
                                 pos = (-0.5, 0, 0.5))

        self.title = OnscreenText(text = 'Register',
                                  pos = (0, 0.3),
                                  scale = 0.15,
                                  fg = (1, 0.5, 0.5, 1),
                                  align = TextNode.ACenter,
                                  parent = self.frame,
                                  mayChange = False)

        # username
        self.username = OnscreenText(text = 'Username:',
                                     pos = (-0.1, 0.0),
                                     scale = 0.05,
                                     fg = (1, 0.5, 0.5, 1),
                                     align = TextNode.ACenter,
                                     parent = self.frame,
                                     mayChange = False)
        self.userTextbox = DirectEntry(self.frame, # parent
                                       text = '',
                                       scale = 0.05,
                                       pos = (0.1, 0, 0),
                                       initialText = '[username]',
                                       numLines = 1,
                                       focus = 1,
                                       focusInCommand = self.userTextFocus,
                                       focusOutCommand = self.userTextBlur)

        # password
        self.password = OnscreenText(text = 'Password:',
                                     pos = (-0.1, -0.2),
                                     scale = 0.05,
                                     fg = (1, 0.5, 0.5, 1),
                                     align = TextNode.ACenter,
                                     parent = self.frame,
                                     mayChange = False)
        self.passTextbox = DirectEntry(self.frame, # parent
                                       text = '',
                                       scale = 0.05,
                                       pos = (0.1, 0, -0.2),
                                       initialText = '[password]',
                                       numLines = 1,
                                       focus = 0,
                                       focusInCommand = self.passTextFocus,
                                       focusOutCommand = self.passTextBlur)

        # confirm password
        self.cpassword = OnscreenText(text = 'Confirm Password:',
                                      pos = (-0.15, -0.4),
                                      scale = 0.05,
                                      fg = (1, 0.5, 0.5, 1),
                                      align = TextNode.ACenter,
                                      parent = self.frame,
                                      mayChange = False)
        self.cpassTextbox = DirectEntry(self.frame, # parent
                                        text = '',
                                        scale = 0.05,
                                        pos = (0.1, 0, -0.4),
                                        initialText = '[confirm password]',
                                        numLines = 1,
                                        focus = 0,
                                        focusInCommand = self.cpassTextFocus,
                                        focusOutCommand = self.cpassTextBlur)

        # buttons
        self.registerBtn =  DirectButton(self.frame, # parent
                                         text = 'Register',
                                         scale = 0.08,
                                         command = self.clickedRegRegister,
                                         pos = (0.8, 0.0, -0.90))
        self.cancelBtn =  DirectButton(self.frame, # parent
                                       text = 'Cancel',
                                       scale = 0.08,
                                       command = self.clickedRegCancel,
                                       pos=(0.2, 0.0, -0.90))

    def destroyRegisterWindow(self):
        self.frame.destroy()
        self.frame = None
        self.title = None
        self.error = None
        self.username = None
        self.userTextbox = None
        self.password = None
        self.passTextbox = None
        self.cpassword = None
        self.cpassTextbox = None
        self.registerBtn = None
        self.cancelBtn = None

    # error message helper
    def displayError(self, msg):
        if self.frame is None: return
        if self.error is not None: self.error.destroy()
        self.error = OnscreenText(text = msg,
                                  pos = (0, -0.65),
                                  scale = 0.06,
                                  fg = (1, 0.5, 0.5, 1),
                                  align = TextNode.ACenter,
                                  parent = self.frame,
                                  mayChange = False)

    # userTextbox handlers
    def userTextFocus(self):
        if self.userTextbox.get() == '[username]': self.userTextbox.enterText('')

    def userTextBlur(self):
        if self.userTextbox.get().strip() == '': self.userTextbox.enterText('[username]')

    # passTextbox handlers
    def passTextFocus(self):
        if self.passTextbox.get() == '[password]': self.passTextbox.enterText('')

    def passTextBlur(self):
        if self.passTextbox.get().strip() == '': self.passTextbox.enterText('[password]')

    # cpassTextbox handlers
    def cpassTextFocus(self):
        if self.cpassTextbox.get() == '[confirm password]': self.cpassTextbox.enterText('')

    def cpassTextBlur(self):
        if self.cpassTextbox.get().strip() == '': self.cpassTextbox.enterText('[confirm password]')

    # login button handlers
    def clickedSubmit(self):
        username = self.userTextbox.get().strip()
        password = self.passTextbox.get().strip()
        if username != '' and password != '':
            self.main.cManager.sendRequest(Constants.C_AUTH, {'username': username, 'password': password})
        else:
            self.displayError('Please enter a username and password.')

    def clickedRegister(self):
        self.destroyLoginWindow()
        self.createRegisterWindow()

    def clickedCancel(self):
        exit()

    # register button handlers
    def clickedRegRegister(self):
        username = self.userTextbox.get().strip()
        password = self.passTextbox.get().strip()
        cpass = self.cpassTextbox.get().strip()
        if username != '':
            if password != '':
                if cpass == password:
                    self.main.cManager.sendRequest(Constants.C_REGISTER, {'username': username, 'password': password})
                    self.destroyRegisterWindow()
                    self.createLoginWindow()
                else:
                    self.displayError('Your passwords do not match.')
            else:
                self.displayError('Please enter a password.')
        else:
            self.displayError('Please enter a username.')

    def clickedRegCancel(self):
        self.destroyRegisterWindow()
        self.createLoginWindow()
