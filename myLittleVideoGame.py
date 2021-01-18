from tkinter import Tk
from tkinter import Label
from tkinter import PhotoImage
from tkinter import Canvas
from tkinter import NW
from tkinter import CENTER
from tkinter import *
import time
from playsound import playsound
import math
import pygame

class MyLittleVideoGame:
    def __init__(self, window, title, backgroundfilenamePNG):
        self.title=title
        self.font=("Courier",21,"bold")
        self.window=window
        #self.window.title(self.title)
        self.window.winfo_toplevel().title(self.title)
        self.window.resizable(False, False)
        self.score=0
        self.lives=3
        self.level=1
        self.other="Other"
        # make labels and canvas
        self.labelScore = Label (window, text="SCORE: "+str(self.score),font=self.font)
        self.labelLives = Label (window, text="LIVES: "+str(self.lives),font=self.font)
        self.labelLevel = Label (window, text="LEVEL: "+str(self.level),font=self.font)
        self.labelOther = Label (window, text=self.other,font=self.font)
        self.background = PhotoImage(file=backgroundfilenamePNG)
        self.width=self.background.width()
        self.height=self.background.height()
        self.messageXPosition=self.width//2
        self.messageYPosition=self.height//2
        self.canvas=Canvas(window, width=self.width, height=self.height)
        self.backgroundPNG = self.canvas.create_image(1,0, image=self.background,anchor=NW)#,tag="background")
        self.labelScore.grid(row=0, column=0)
        self.labelLevel.grid(row=0,column=1)
        self.labelOther.grid(row=0, column=2)
        self.labelLives.grid(row=0, column=3)
        self.canvas.grid(row=1,column=0, columnspan=4)
        self.key=""
        self.movex=0
        self.movey=0
        self.space=False
        self.escape=False
        self.paused=False
        self.messageOnScreen=False
        self.getEscapePress()
        self.getPausePress()
        self.simpleKey=""

    def getHeight(self): # returns height of canvas
        return(self.height)

    def getWidth(self): # returns width of canvas
        return(self.width)

    def setTitle(self,title):
        self.title=title
        self.window.winfo_toplevel().title(self.title)

    def _backgroundDelete(self): #removes background and leaves blank canvas
        self.canvas.delete(self.backgroundPNG)
        self.window.update()

    def backgroundLoad(self,fileName): #loads a background image file, sets the canvas to image width, loads image
        self.background = PhotoImage(file=fileName)
        self.width=self.background.width()
        self.height=self.background.height()
        self.canvas.config(width=self.width, height=self.height)
        self.backgroundPNG = self.canvas.create_image(1,0, image=self.background,anchor=NW)
        self.canvas.tag_lower(self.backgroundPNG,"all")

    def backgroundChange(self,fileName):# changes background by deleting background and loading one in.
        self.fileName=fileName
        self._backgroundDelete()
        self.backgroundLoad(self.fileName)
        
    #************* get/set scores etc ************
    def getScore(self):# returns score
        return(self.score)

    def setScore(self,score):
        self.score=score # sets score and displays
        self.labelScore.configure(text="SCORE: "+str(self.score))
        self.window.update()

    def getLives(self):
        return(self.lives)

    def setLives(self, lives):
        self.lives=lives
        self.labelLives.configure(text="LIVES: "+str(self.lives))
        self.window.update()

    def getLevel(self):
        return(self.level)

    def setLevel(self, level):
        self.level=level
        self.labelLevel.configure(text="LEVEL: "+str(self.level))
        self.window.update()

    def getOther(self): # other is a string, could be anything you want displayed
        return(self.other)

    def setOther(self, whateverString): # other is a string, could be anything you want displayed
        self.other=whateverString
        self.labelOther.configure(text=self.other)
        self.window.update()

    #play background music while game is playing.  Supply mp3 filename, and volume which is a float (0.0to1.0)ex .7
    def backgroundMusicPlay(self,backgroundMusicfileName,volumeFloat_0to1):
        try:
            self.backgroundMusicFileName=backgroundMusicfileName
            self.volumeFloat_0to1=volumeFloat_0to1
            pygame.mixer.init()
            pygame.mixer.music.load(self.backgroundMusicFileName)
            pygame.mixer.music.set_volume(volumeFloat_0to1)
            pygame.mixer.music.play(-1,0.0)
        except:
            print ("backgroundMusicPlay failed")

    #stop background music, maybe between switching levels or similar
    def backgroundMusicStop(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except:
            print ("backgroundMusicStop failed")
    #this is not for playing background music, this is for playing short things like an explosion or firing a shot
    def playSoundandKeepGoing(self,fileName):
        self.fileName=fileName
        try:
            playsound(self.fileName,0) # the 0 is a flag to not stop while playing works in windows, not linux currently
        except:
            print("There was a problem playing the file", self.fileName)

    def playSoundAndPauseWhilePlaying(self,fileName):
        self.fileName=fileName
        try:
            playsound(self.fileName,1) # pause while playing
        except:
            print("There was a problem playing the file", self.fileName)

    def showMessage(self,text): # this places a text message in the middle of the screen, remove before showing another
        self.text=text
        self.window.update()
        self.messageXPosition=self.width//2
        self.messageYPosition=self.height//2
        self.message = self.canvas.create_text(self.messageXPosition,self.messageYPosition,text=self.text,font=self.font)
        self.messageOnScreen=True
        self.window.update()
        
    def moveMessage(self,Xmove,Ymove):
        self.moveMessageX=Xmove
        self.moveMessageY=Ymove
        self.messageXPosition=self.messageXPosition+self.moveMessageX
        self.messageYPosition=self.messageYPosition+self.moveMessageY
        self.canvas.move(self.message,self.moveMessageX,self.moveMessageY)
        self.window.update()

    def isMessageOnScreen(self):
        return(self.messageOnScreen)

    def deleteMessage(self):
        self.message=self.message
        self.canvas.delete(self.message)
        self.messageOnScreen=False
        self.window.update()

    """
    This is used when there is a game pause.  Like press Y to continue for example.  Background music
    will play, but keypress must happen for it to break out of loop and continue
    """
    def waitForKeyPress(self):# game will pause until a keypress occurs, also returns the keypress
        print("waiting for KeyPress")
        self.keyPress=""
        while (self.keyPress==""):# unbind standard controls in case they are being used for movement
            self.window.unbind("<space>")
            self.window.unbind("<Left>")
            self.window.unbind("<Right>")
            self.window.unbind("<Up>")
            self.window.unbind("<Down>")
            self.window.unbind("<p>") # unbinding the pause button
            self.window.bind("<Key>",lambda e: self._reportKeyPress(e))
            time.sleep(.3)
            print("slept for.3")
            print(self.keyPress)
            self.window.update()
        self.window.bind("<KeyPress-p>", lambda e: self._pausePress(e)) #rebind pause button
        return(self.keyPress) #return keypress which is set with the function _reportKeyPress

    def _reportKeyPress(self,e):#sets value of the keypress which is then returned in the waitForKeyPress method
        print(e.keysym)
        self.keyPress=e.keysym


    """
    This is used not to stop the program and wait on a keypress, but this can be used to while
    the main game loop is running to get keystrokes.  Like if j is pressed move left and k is pressed move
    right.  The main difference between using getKey instead of the binding of controls below is there
    can only be one return.  So if you press up and right at the same time, there will not be diaganol
    movement.  In other words only one key can be returned at at time.  The standard controls are disabled
    in case they have been bound by using the controls.  Also the pause button is turned off if you are
    using this method that way p can be accessed as a key.  If you need to keep pause on places
    incorporate the getPausePress method in the main game loop to keep it on.  place it after getKey
    method in the main game loop.
    """
    def getKey(self):
        self.window.unbind("<space>")
        self.window.unbind("<Left>")
        self.window.unbind("<Right>")
        self.window.unbind("<Up>")
        self.window.unbind("<Down>")
        self.window.unbind("<p>")
        self.window.bind("<KeyRelease>", lambda e: self._keyReleased(e))
        self.window.bind("<KeyPress>",lambda e: self._keyTriggered(e))

        print("returning self.key",self.key)
        return(self.key)

    def _unBindControls(self):
        self.window.unbind("<space>")
        self.window.unbind("<Left>")
        self.window.unbind("<Right>")
        self.window.unbind("<Up>")
        self.window.unbind("<Down>")
        self.window.unbind("<p>")
        #self.window.unbind("<KeyPress>")
        #self.window.unbind("<KeyRelease>")


    def destroyAllObjects(self):
        self.canvas.delete("all")

    # these 2 methods are used by they getKey method
    def _keyTriggered(self,e):
        print("got to _keyTriggered")
        print(e)
        print(e.keysym)
        self.key=e.keysym
        #print(self.simpleKey)

    def _keyReleased(self,e):
        print("got to _keyReleased")
        self.key=""

    def sleep(self,timeInSeconds): #sleeps/pauses game for however many seconds
        self.timeInSeconds=timeInSeconds
        time.sleep(self.timeInSeconds)
        self.window.update()


    """
    These are standard controls.  The left key, right key, up key down key, space key, pause p, and esc
    to quit.  
    """
    # returns if left or right was pressed and returns the amount to move
    def getXMove(self,leftXamount,rightXamount):
        self.leftXamount=leftXamount
        self.rightXamount=rightXamount
        self.window.bind("<KeyPress-Left>", lambda e: self._left(e)) 
        self.window.bind("<KeyPress-Right>", lambda e: self._right(e)) 
        self.window.bind("<KeyRelease-Left>", lambda e: self._stopLeft(e)) 
        self.window.bind("<KeyRelease-Right>", lambda e: self._stopRight(e))
        self.window.bind("")
        return(self.movex)

    def _left(self,e):
        self.movex=self.leftXamount
        print("_left", e.keysym)

    def _right(self,e):
        self.movex=self.rightXamount
        print("_right",e.keysym)

    def _stopLeft(self,e):
        self.movex=0
        print(e.keysym)

    def _stopRight(self,e):
        self.movex=0
        print(e.keysym)    

    # returns if up or down was pressed and returns the amount to move
    def getYMove(self,upYamount,downYamount):
        self.upYamount=upYamount
        self.downYamount=downYamount
        self.window.bind("<KeyPress-Up>", lambda e: self._up(e)) 
        self.window.bind("<KeyPress-Down>", lambda e: self._down(e)) 
        self.window.bind("<KeyRelease-Up>", lambda e: self._stopUp(e)) 
        self.window.bind("<KeyRelease-Down>", lambda e: self._stopDown(e))
        return(self.movey)

    def _up(self,e):
        self.movey=self.upYamount
        print("_up",e.keysym)

    def _down(self,e):
        self.movey=self.downYamount
        print("_down",e.keysym)

    def _stopUp(self,e):
        self.movey=0
        print(e.keysym)

    def _stopDown(self,e):
        self.movey=0
        print(e.keysym)

    # returns if space was pressed
    def getSpacePress(self):
        self.window.bind("<KeyPress-space>", lambda e: self._space(e))
        self.window.bind("<KeyRelease-space>", lambda e: self._stopSpace(e))
        return(self.space)

    def _space(self,e):
        self.space=True
        print("_space",e.keysym)

    def _stopSpace(self,e):
        self.space=False
        print(e.keysym)

    # binds p to game pause, game restarts when another key is pressed
    def getPausePress(self):
        self.window.bind("<KeyPress-p>", lambda e: self._pausePress(e))

    def _pausePress(self,e):
        self.paused=True
        self.waitForKeyPress()
        self.paused=False

    # binds esc to exit game
    def getEscapePress(self):
        self.window.bind("<KeyPress-Escape>", lambda e: self._escape(e))
        self.window.bind("<KeyRelease-Escape>", lambda e: self._stopEscape(e))
        return(self.escape)

    def _escape(self,e):
        self.escape=True
        self.exitProgram()
        print(e.keysym)

    def _stopEscape(self,e):
        self.escape=False
        print(e.keysym)

    def exitProgram(self):
        self.backgroundMusicStop()
        self.window.destroy()    

class LittleObjects:
    def __init__(self,game,x,y,imageFilePNG):
        self.window=game.window
        self.canvas=game.canvas
        self.x=x
        self.y=y
        self.movex=0
        self.movey=0
        self.imageFilePNG=imageFilePNG
        self.objectExists=True
        self.objectImagePNG = PhotoImage(file=imageFilePNG)
        self.littleObject = self.canvas.create_image(self.x,self.y, image=self.objectImagePNG,anchor=CENTER)
        self.window.update()

    def moveObject(self,movex,movey):
        self.movex=movex
        self.movey=movey
        self.x=self.x+self.movex
        self.y=self.y+self.movey
        self.canvas.move(self.littleObject,self.movex,self.movey)
        self.window.update()

    def destroy(self):
        self.canvas.delete(self.littleObject)
        self.objectExists=False
        self.window.update()

    def getXPosition(self):
        return(self.x)

    def setXPosition(self,newXPosition):
        self.newXPosition=newXPosition
        self.moveObject(self.newXPosition-self.x,0)
        self.window.update()

    def getYPosition(self):
        return(self.y)

    def setYPosition(self,newYPosition):
        self.newYPosition=newYPosition
        self.moveObject(0,self.newYPosition-self.y)
        self.window.update()

    def getObjectExists(self):#should change to ObjectExists
        return(self.objectExists)

class RotatingCannon:
    def __init__(self,game,radAngle,launcherLength,launcherWidth,launcherXLocation,launcherYLocation):
        self.radAngle=radAngle
        self.launcherLength=launcherLength
        self.launcherWidth=launcherWidth
        self.canvas=game.canvas
        self.window=game.window
        self.height=game.getHeight()
        self.width=game.getWidth()
        self.launcherXLocation=launcherXLocation
        self.launcherYLocation=launcherYLocation

        #make 2 circles around the base of the cannon
        self.base1=self.canvas.create_oval(self.launcherXLocation-self.launcherLength/2,self.launcherYLocation-self.launcherLength/2,self.launcherXLocation+self.launcherLength/2,self.launcherYLocation+self.launcherLength/2, width=self.launcherWidth/2, fill="dark grey")
        self.base2=self.canvas.create_oval(self.launcherXLocation-self.launcherWidth,self.launcherYLocation-self.launcherWidth,self.launcherXLocation+self.launcherWidth,self.launcherYLocation+self.launcherWidth, fill="black")
        #make a line which is a cannon
        self.cannon=self.canvas.create_line(self.launcherXLocation,self.launcherYLocation,self.launcherXLocation+self.launcherLength*math.cos(radAngle), self.launcherYLocation-self.launcherLength*math.sin(radAngle)+self.launcherWidth, width=self.launcherWidth)
        
        #take note of the location of the end of the cannon, which is where object wouldbe launched on
        self.cannonEndXPosition=self.launcherXLocation+self.launcherLength*math.cos(radAngle)
        self.cannonEndYPosition=self.launcherYLocation-self.launcherLength*math.sin(radAngle)#+self.launcherWidth
        game.window.update()

    def rotate(self,moveRadAngle):
        self.moveRandAngle=moveRadAngle
        self.radAngle=self.radAngle+self.moveRandAngle
        #delete the cannon
        self.canvas.delete(self.cannon)
        #create a cannon with new angle
        self.createCannon(self.radAngle,self.launcherLength,self.launcherWidth)
        self.window.update()

    def createCannon(self,radAngle,launcherLength,launcherWidth):
        self.radAngle=radAngle
        self.launcherLength=launcherLength
        self.launcherWidth=launcherWidth
        #self.launcherXLocation=self.width//2
        self.cannon = self.canvas.create_line(self.launcherXLocation,self.launcherYLocation,self.launcherXLocation+self.launcherLength*math.cos(radAngle), self.launcherYLocation-self.launcherLength*math.sin(radAngle)+self.launcherWidth, width=self.launcherWidth)
        self.cannonEndXPosition=self.launcherXLocation+self.launcherLength*math.cos(radAngle)
        self.cannonEndYPosition=self.launcherYLocation-self.launcherLength*math.sin(radAngle)#+self.launcherWidth
        self.window.update()

    def getCannonEndXPosition(self):
        return(self.cannonEndXPosition)

    def getCannonEndYPosition(self):
        return(self.cannonEndYPosition)

    def getRadAngle(self):
        return(self.radAngle)

    def setRadAngle(self,radAngle):
        self.radAngle=radAngle

    def getLauncherLength(self):
        return(self.launcherLength)
    
    def getLauncherXLocation(self):
        return(self.launcherXLocation)

    def getLauncherWidth(self):
        return(self.launcherWidth)

    def destroyAll(self):
        self.canvas.delete(self.cannon)
        self.canvas.delete(self.base1)
        self.canvas.delete(self.base2)
    
