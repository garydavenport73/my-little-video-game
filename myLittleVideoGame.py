# MyLittleVideoGame class
# for making simple classic 2d video games

from tkinter import Label
from tkinter import PhotoImage
from tkinter import Canvas
from tkinter import NW
from tkinter import CENTER
import time
from preferredsoundplayer import *
from math import sin, cos, pi, sqrt


class MyLittleVideoGame:
    def __init__(self, window, title, backgroundfilenamePNG="", backgroundcolor="#cba428", canvasWidth=320, canvasHeight=569):
        self.title = title
        self.font = ("Courier", 21, "bold")
        self.window = window
        self.backgroundcolor = backgroundcolor
        self.window.configure(bg=self.backgroundcolor)
        self.window.winfo_toplevel().title(self.title)
        self.window.resizable(False, False)
        self.score = 0
        self.lives = 3
        self.level = 1
        self.other = ""
        # make labels and canvas
        self.labelScore = Label(
            window, text="SCORE: "+str(self.score), font=self.font, bg=self.backgroundcolor)
        self.labelLives = Label(
            window, text=" LIVES: "+str(self.lives), font=self.font, bg=self.backgroundcolor)
        self.labelLevel = Label(
            window, text=" LEVEL: "+str(self.level), font=self.font, bg=self.backgroundcolor)
        self.labelOther = Label(window, text=self.other,
                                font=self.font, bg=self.backgroundcolor)

        # if there is not background file, make small screen canvas
        if backgroundfilenamePNG != "":
            self.backgroundPhotoImage = PhotoImage(file=backgroundfilenamePNG)
            self.canvasWidth = self.backgroundPhotoImage.width()
            self.canvasHeight = self.backgroundPhotoImage.height()

        else:
            self.canvasWidth = canvasWidth
            self.canvasHeight = canvasHeight
            if canvasWidth <= 320:
                self.font = ("Courier", 14, "bold")
            elif canvasWidth > 320 and canvasWidth < 450:
                self.font = ("Courier", 18, "bold")
            self.refreshScoreboard()

        self.canvas = Canvas(window, width=self.canvasWidth,
                             height=self.canvasHeight, bg=self.backgroundcolor)

        if backgroundfilenamePNG != "":
            try:
                self.backgroundCanvasImage = self.canvas.create_image(
                    1, 0, image=self.backgroundPhotoImage, anchor=NW)  # ,tag="background")
            except:
                print(self.backgroundPhotoImage +
                      " not found, or otherwise could not be loaded.")

        self.messageXPosition = self.canvasWidth//2
        self.messageYPosition = self.canvasHeight//2

        self.labelScore.grid(row=0, column=0)
        self.labelLevel.grid(row=0, column=1)
        self.labelOther.grid(row=0, column=2)
        self.labelLives.grid(row=0, column=3)
        self.canvas.grid(row=1, column=0, columnspan=4)
        self.key = ""
        self.movex = 0
        self.movey = 0
        self.space = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.escape = False
        self.paused = False
        self.messageOnScreen = False
        self.simpleKey = ""
        self.backgroundMusicLoop = None
        self.isBackGroundMusicPlaying = False
        self._bindEscapeKey()
        self._bindControlKeys()

    def refreshScoreboard(self):
        # make labels and canvas
        self.labelScore = Label(
            self.window, text="SCORE: "+str(self.score), font=self.font, bg=self.backgroundcolor)
        self.labelLives = Label(
            self.window, text=" LIVES: "+str(self.lives), font=self.font, bg=self.backgroundcolor)
        self.labelLevel = Label(
            self.window, text=" LEVEL: "+str(self.level), font=self.font, bg=self.backgroundcolor)
        self.labelOther = Label(self.window, text=self.other,
                                font=self.font, bg=self.backgroundcolor)

    def getCanvasHeight(self):  # returns height of canvas
        return(self.canvasHeight)

    def getCanvasWidth(self):  # returns width of canvas
        return(self.canvasWidth)

    def setTitle(self, title):
        self.title = title
        self.window.winfo_toplevel().title(self.title)

    def _backgroundDelete(self):  # removes background and leaves blank canvas
        self.canvas.delete(self.backgroundCanvasImage)
        self.window.update()

    # loads a background image file, sets the canvas to image width, loads image
    def backgroundLoad(self, fileName):
        self.backgroundPhotoImage = PhotoImage(file=fileName)
        self.canvasWidth = self.backgroundPhotoImage.width()
        self.canvasHeight = self.backgroundPhotoImage.height()
        self.canvas.config(width=self.canvasWidth, height=self.canvasHeight)
        self.backgroundCanvasImage = self.canvas.create_image(
            1, 0, image=self.backgroundPhotoImage, anchor=NW)
        self.canvas.tag_lower(self.backgroundCanvasImage, "all")
        self.window.update()

    # changes background by deleting background and loading one in.
    def backgroundChange(self, fileName):
        self._backgroundDelete()
        self.backgroundLoad(fileName)

    def getScore(self):  # returns score
        return(self.score)

    def setScore(self, score):
        self.score = score  # sets score and displays
        self.labelScore.configure(text="SCORE: "+str(self.score))
        self.window.update()

    def addToScore(self, addToScoreThisAmount):
        self.score = self.score + int(addToScoreThisAmount)
        self.labelScore.configure(text="SCORE: "+str(self.score))
        self.window.update()

    def subtractFromScore(self, subtractFromScoreThisAmount):
        self.score = self.score - int(subtractFromScoreThisAmount)
        self.labelScore.configure(text="SCORE: "+str(self.score))
        self.window.update()

    def getLives(self):
        return(self.lives)

    def setLives(self, lives):
        self.lives = lives
        self.labelLives.configure(text="LIVES: "+str(self.lives))
        self.window.update()

    def addLives(self, livesToAdd):
        self.lives = self.lives + int(livesToAdd)
        self.labelLives.configure(text="LIVES: "+str(self.lives))
        self.window.update()

    def subtractLives(self, livesToSubtract):
        self.lives = self.lives - int(livesToSubtract)
        self.labelLives.configure(text="LIVES: "+str(self.lives))
        self.window.update()

    def getLevel(self):
        return(self.level)

    def setLevel(self, level):
        self.level = level
        self.labelLevel.configure(text="LEVEL: "+str(self.level))
        self.window.update()

    def increaseLevel(self, increaseLevelByThisAmount):
        self.level = self.level + int(increaseLevelByThisAmount)
        self.labelLevel.configure(text="LEVEL: "+str(self.level))
        self.window.update()

    def getOther(self):  # other is a string, could be anything you want displayed
        return(self.other)

    def setOther(self, whateverString):  # other is a string, could be anything you want displayed
        self.other = whateverString
        self.labelOther.configure(text=self.other)
        self.window.update()

    # play background music while game is playing.  Supply mp3 filename, and volume which is a float (0.0to1.0)ex .7
    def playBackgroundMusic(self, backgroundMusicfileName):
        self.backgroundMusicLoop = loopsound(backgroundMusicfileName)
        return(self.backgroundMusicLoop)

    # play background music while game is playing.  Supply mp3 filename, and volume which is a float (0.0to1.0)ex .7
    # def playBackgroundMusic(self, backgroundMusicfileName, optionalForMp3s_CheckRestartHowOften=.2):
    #    self.backgroundMusicLoop = loopsound(
    #        backgroundMusicfileName, optionalForMp3s_CheckRestartHowOften)
    #    return(self.backgroundMusicLoop)

    # stop background music, maybe between switching levels or similar

    def stopBackgroundMusic(self, backgroundMusicLoopObject):
        stoploop(backgroundMusicLoopObject)

    # this is not for playing background music, this is for playing short things like an explosion or firing a shot
    def playSoundandKeepGoing(self, fileName):
        return(soundplay(fileName))

    def playSoundAndPauseWhilePlaying(self, fileName):
        return(soundplay(fileName, block=True))

    # this places a text message in the middle of the screen, remove before showing another
    def showMessage(self, messageText):
        self.window.update()
        self.messageXPosition = self.canvasWidth//2
        self.messageYPosition = self.canvasHeight//2
        self.message = self.canvas.create_text(
            self.messageXPosition, self.messageYPosition, text=messageText, font=self.font)
        self.messageOnScreen = True
        self.window.update()

    def moveMessage(self, Xmove, Ymove):
        self.canvas.move(self.message, Xmove, Ymove)
        self.messageXPosition = self.messageXPosition+Xmove
        self.messageYPosition = self.messageYPosition+Ymove
        self.window.update()

    def isMessageOnScreen(self):
        return(self.messageOnScreen)

    def deleteMessage(self):
        self.canvas.delete(self.message)
        self.messageOnScreen = False
        self.window.update()

    """
    This is used when there is a game pause.  Like press Y to continue for example.  Background music
    will play, but keypress must happen for it to break out of loop and continue
    """

    # game will pause until a keypress occurs, also returns the keypress
    def waitForKeyPress(self):
        self._unbindControlKeys()
        self.keyPress = ""
        while (self.keyPress == ""):
            self.window.bind("<Key>", lambda e: self._reportKeyPress(e))
            time.sleep(.3)
            self.window.update()
        self._bindControlKeys()
        return(self.keyPress)

    # sets value of the keypress which is then returned in the waitForKeyPress method
    def _reportKeyPress(self, e):
        # print(e.keysym)
        self.keyPress = e.keysym

    def destroyAllObjects(self):
        self.canvas.delete("all")

    def sleep(self, timeInSeconds):  # sleeps/pauses game for however many seconds
        time.sleep(timeInSeconds)
        self.window.update()

    def _bindControlKeys(self):
        self.window.bind("<KeyPress-Left>", lambda e: self._left())
        self.window.bind("<KeyPress-Right>", lambda e: self._right())
        self.window.bind("<KeyRelease-Left>", lambda e: self._stopLeft())
        self.window.bind("<KeyRelease-Right>", lambda e: self._stopRight())
        self.window.bind("<KeyPress-Up>", lambda e: self._up())
        self.window.bind("<KeyPress-Down>", lambda e: self._down())
        self.window.bind("<KeyRelease-Up>", lambda e: self._stopUp())
        self.window.bind("<KeyRelease-Down>", lambda e: self._stopDown())
        self.window.bind("<KeyPress-p>", lambda e: self._pausePress(e))
        self.window.bind("<KeyPress-space>", lambda e: self._space(e))
        self.window.bind("<KeyRelease-space>", lambda e: self._stopSpace(e))
        self.window.update()

    def _unbindControlKeys(self):
        self.window.unbind("<KeyPress-Left>")
        self.window.unbind("<KeyPress-Right>")
        self.window.unbind("<KeyRelease-Left>")
        self.window.unbind("<KeyRelease-Right>")
        self.window.unbind("<KeyPress-Up>")
        self.window.unbind("<KeyPress-Down>")
        self.window.unbind("<KeyRelease-Up>")
        self.window.unbind("<KeyRelease-Down>")
        self.window.unbind("<KeyPress-p>")
        self.window.unbind("<KeyPress-space>")
        self.window.unbind("<KeyRelease-space>")
        self.window.update()

    # returns if left or right was pressed and returns the amount to move
    def getMoves(self):  # , leftXamount, rightXamount, upYamount,downYamount):
        self.window.update()
        return [self.left, self.right, self.up, self.down]

    def getLeft(self):
        return(self.left)

    def getRight(self):
        return(self.right)

    def getUp(self):
        return(self.up)

    def getDown(self):
        return(self.down)

    def getSpace(self):
        return(self.space)

    def _left(self):
        self.left = True

    def _right(self):
        self.right = True

    def _stopLeft(self):
        self.left = False

    def _stopRight(self):
        self.right = False

    def _up(self):
        self.up = True

    def _down(self):
        self.down = True

    def _stopUp(self):
        self.up = False

    def _stopDown(self):
        self.down = False

    def _space(self, e):
        self.space = True

    def _stopSpace(self, e):
        self.space = False

    def _pausePress(self, e):
        self.paused = True
        self.waitForKeyPress()
        self.paused = False

    # binds esc to exit game
    def _bindEscapeKey(self):
        self.window.bind("<KeyPress-Escape>", lambda e: self._escape(e))
        self.window.bind("<KeyRelease-Escape>", lambda e: self._stopEscape(e))
        return(self.escape)

    def _escape(self, e):
        self.escape = True
        self.exitProgram()

    def exitProgram(self):
        self.stopBackgroundMusic(self.backgroundMusicLoop)
        self.window.destroy()

# pick a color to make transparent


def makeTransparent(img, colorToMakeTransparentInHexFormat):
    newPhotoImage = PhotoImage(width=img.width(), height=img.height())
    for x in range(img.width()):
        for y in range(img.height()):
            rgb = '#%02x%02x%02x' % img.get(x, y)
            if rgb != colorToMakeTransparentInHexFormat:
                newPhotoImage.put(rgb, (x, y))
    return newPhotoImage

# returns a photoimage that color switch


def switchColors(img, currentColorInHexFormat, futureColorInHexFormat):
    newPhotoImage = PhotoImage(width=img.width(), height=img.height())
    for x in range(img.width()):
        for y in range(img.height()):
            rgb = '#%02x%02x%02x' % img.get(x, y)
            if rgb == currentColorInHexFormat:
                newPhotoImage.put(futureColorInHexFormat, (x, y))
            else:
                newPhotoImage.put(rgb, (x, y))
    return newPhotoImage

# returns a rotated PhotoImage


def rotatedPhotoImage(img, angle, colorToMakeTransparentInHexFormat=""):
    angleInRads = angle * pi / 180
    diagonal = sqrt(img.width()**2 + img.height()**2)
    xmidpoint = img.width()/2
    ymidpoint = img.height()/2
    newPhotoImage = PhotoImage(width=int(diagonal), height=int(diagonal))
    for x in range(img.width()):
        for y in range(img.height()):

            # convert to ordinary mathematical coordinates
            xnew = float(x)
            ynew = float(-y)

            # shift to origin
            xnew = xnew - xmidpoint
            ynew = ynew + ymidpoint

            # new rotated variables, rotated around origin (0,0) using simoultaneous assigment
            xnew, ynew = xnew*cos(angleInRads) - ynew*sin(angleInRads), xnew * \
                sin(angleInRads) + ynew*cos(angleInRads)

            # shift back to quadrant iv (x,-y), but centered in bigger box
            xnew = xnew + diagonal/2
            ynew = ynew - diagonal/2

            # convert to -y coordinates
            xnew = xnew
            ynew = -ynew

            # get pixel data from the pixel being rotated in hex format
            rgb = '#%02x%02x%02x' % img.get(x, y)

            if rgb != colorToMakeTransparentInHexFormat:
                # put that pixel data into the new image
                newPhotoImage.put(rgb, (int(xnew), int(ynew)))

                # this helps fill in empty pixels due to rounding issues
                newPhotoImage.put(rgb, (int(xnew+1), int(ynew)))

    return newPhotoImage


class LittleObjects:
    def __init__(self, game, x, y, imageFilenamePNG="", photoImage="", rotatable=False, colorToMakeTransparent=""):
        self.rotatable = rotatable
        self.window = game.window
        self.canvas = game.canvas
        self.x = x
        self.y = y
        self.angle = 0.0
        self.imageFilePNG = imageFilenamePNG
        self.objectExists = True
        if imageFilenamePNG != "":
            self.photoImage = PhotoImage(file=imageFilenamePNG)
        if photoImage != "":  # if both designations are present, photoImage takes precedence
            self.photoImage = photoImage

        self.canvasImage = self.canvas.create_image(
            self.x, self.y, image=self.photoImage, anchor=CENTER)
        self.onCanvas = True
        self.window.update()
        if self.rotatable == True:
            # make an array
            self.rotatedPhotoImage = []
            for i in range(16):
                angle = i*22.5
                self.rotatedPhotoImage.append(
                    rotatedPhotoImage(self.photoImage, angle, colorToMakeTransparent))
            pass
        self.game = game

    def setPhotoImage(self, photoimage):
        self.canvas.delete(self.canvasImage)
        self.onCanvas = False
        self.photoImage = photoimage
        self.canvasImage = self.canvas.create_image(
            self.x, self.y, image=self.photoImage, anchor=CENTER)
        self.onCanvas = True
        self.window.update()

    def switchColorsInObject(self, currentColorInHexFormat, futureColorInHexFormat):
        self.photoImage = switchColors(
            self.photoImage, currentColorInHexFormat, futureColorInHexFormat)
        self.setPhotoImage(self, self.photoimage)

    def makeColorTransparentInObject(self, colorToMakeTransparentInHexFormat):
        self.photoImage = makeTransparent(
            self.photoImage, colorToMakeTransparentInHexFormat)
        self.setPhotoImage(self, self.photoimage)

    def loadNewImageFromFile(self, imageFilePNG):
        newImage = PhotoImage(file=imageFilePNG)
        self.setPhotoImage(newImage)

    def rotateToAngle(self, angle):
        if self.rotatable == False:
            print("not rotatable")
            return
        self.angle = angle
        angle = angle % 360
        index = (angle-11.25)/22.5 + 1
        index = int(index)
        index = index % 16
        self.setPhotoImage(self.rotatedPhotoImage[index])
        # return(index)

    def rotateByAngle(self, moveAngleByDegrees):
        if self.rotatable == False:
            print("not rotatable")
            return
        self.angle = self.angle + moveAngleByDegrees
        self.rotateToAngle(self.angle)

    def getPhotoImage(self):
        return self.photoImage

    def moveObject(self, moveRightByPx, moveDownByPx):
        self.x = self.x+moveRightByPx
        self.y = self.y+moveDownByPx
        self.canvas.move(self.canvasImage, moveRightByPx, moveDownByPx)
        self.window.update()

    def destroy(self):
        self.canvas.delete(self.canvasImage)
        self.onCanvas = False
        self.objectExists = False
        self.window.update()
        # self.destroy()

    def deleteCanvasImage(self):
        self.canvas.delete(self.canvasImage)
        self.onCanvas = False
        self.window.update()

    def getXPosition(self):
        return(self.x)

    def setXPosition(self, newXPosition):
        self.moveObject(newXPosition-self.x, 0)
        self.window.update()

    def getYPosition(self):
        return(self.y)

    def setYPosition(self, newYPosition):
        self.moveObject(0, newYPosition-self.y)
        self.window.update()

    def getObjectExists(self):  # should change to ObjectExists
        return(self.objectExists)

    def getOnCanvas(self):
        return self.onCanvas

    def respondToControls(self, negX, posX, negY, posY):
        if self.game.getLeft() == True:
            self.moveObject(negX, 0)
        if self.game.getRight() == True:
            self.moveObject(posX, 0)
        if self.game.getUp() == True:
            self.moveObject(0, negY)
        if self.game.getDown() == True:
            self.moveObject(0, posY)
        self.game.window.update()
