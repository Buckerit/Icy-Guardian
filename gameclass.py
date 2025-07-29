#import all python libraries and modules
from tkinter import Tk, Canvas, messagebox, Button, PhotoImage
import random, os, pyglet, math
from PIL import Image, ImageTk  
from enum import Enum

class HealthPowerUp:
    def __init__(self, canvas, screen_width=1200, screen_height=671, interval=10):
        """creates a projectile, in the form of a health powerup

        Args:
            canvas (CanvasID): The Canvas object where the healthpowerup will go across.
            screen_width (int, optional): the with of the screen. Defaults to 1200.
            screen_height (int, optional): the height of the screen. Defaults to 671.
            interval (int, optional): the amount of time the user has to wait before spawning another powerup. Defaults to 10.
        """        
        self.__canvas = canvas
        self.__currentimage = ImageTk.PhotoImage(Image.open(f'images_misc/healthpowerup.png'))
        self.__interval = interval
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__collided = False  # Prevent multiple collisions

        # Randomly select the side wiich the health powerup will spawn
        spawn_side = random.choice(["right", "bottom", "left", "top"])
        #spawn from the top
        if spawn_side == "top":
            self.__x = random.randint(30, screen_width+30)  
            self.__y = -self.__currentimage.height()  
            self.__dx = 0
            self.__dy = 2 # Moves downward
        #spawn form the bottom
        elif spawn_side == "bottom":
            self.__x = random.randint(30, screen_width+30) 
            self.__y = screen_height                    
            self.__dx = 0
            self.__dy = -2  # Moves upward
        #spawn from the left
        elif spawn_side == "left":
            self.__x = -self.__currentimage.width()  
            self.__y = random.randint(30, screen_height+30) 
            self.__dx = 2 #moves rightward
            self.__dy = 0
        #spawn from the right
        elif spawn_side == "right":
            self.__x = screen_width  
            self.__y = random.randint(30, screen_height+30) 
            self.__dx = 2 #moves leftward
            self.__dy = 0
        #creating the image and placing it on the canvas
        self.__healthID = self.__canvas.create_image(self.__x, self.__y, image=self.__currentimage, anchor='nw')

    #deletes the health powerup
    def healthremove(self):    
        """ remove the healthID
        """        
        self.__canvas.delete(self.__healthID)

    def getID(self):
        """ Returns the healthID.
        Returns:
           int : The timer ID of the health
        """
        print(type(self.healthID))
        return self.__healthID
    
    def move(self):
        #add the x and y of the image to the dx and dy
        self.__x += self.__dx
        self.__y += self.__dy

        #if the image goes off the screen remove it
        if (self.__x < -self.__currentimage.width() or self.__x > self.__screen_width or self.__y < -self.__currentimage.height() or self.__y > self.__screen_height):
            self.healthremove() 
            return
        # updates health objects position
        self.__canvas.coords(self.__healthID, self.__x, self.__y)
        
        #moves after the interval
        self.__canvas.after(self.__interval, self.move)
        
    def getX(self):
        """ Returns the x-position of the health powerup.
        Returns:
            int: The x-position of the health powerup.
        """        
        return self.__x
    

    def getRight(self):
        """ Returns the right side of the health powerup (that is, its x-position + its width).

        Returns:
            int: The right side of the healthpowerup.
        """        
        return self.__x + self.__currentimage.width()
    
    def getBottom(self):
        """ Returns the bottom side of the healthpowerup (that is, its y-position + its height).

        Returns:
            int: The bottom side of the healthpowerup.
        """        
        return self.__y + self.__currentimage.height()
    
    def getY(self):
        """ Returns the top (i.e., y-position) of the healthpowerup.

        Returns:
            int: The top (or y-position) of the healthpowerup.
        """        
        return self.__y
    
    # Define properties for x, y, right, and bottom
    x = property(getX)
    y = property(getY)
    right = property(getRight)
    bottom = property(getBottom)

class Orb:
    def __init__(self, canvas, x=0, y=0, xs=0, ys= 0, angle=0):
        """ Creates a projectile, in this case, in the form of a Orb

        Args:
            canvas (CanvasID): The Canvas object where the Orb will be drawn.
            x (int, optional): Where the left side of the orb will be positioned on the canvas. Defaults to 0.
            y (int, optional): Where the top side of the orb will be positioned on the canvas. Defaults to 0.
            xs (int, optional): The direction the orb will be travelling along the x-axis. Defaults to 0.
            ys (int, optional): The direction the orb will be travelling along the y-axis. Defaults to 0.
            angle (int, optional): The angle the orb will be travelling along both the axis. Defaults to 0.
        """        
        self.__canvas = canvas
        self.__x = x
        self.__y= y
        self.__xspeed = xs
        self.__yspeed = ys
        self.__angle = angle 
        self.__image = (ImageTk.PhotoImage(Image.open(f'images_misc/Orb2.png')))
        self.__orbID = canvas.create_image(x, y, image=self.__image, anchor='center')  # Draw orb
        self.__active = True  # Indicates if the orb is still active

    
    def move(self):
        """
        Moves the orb along its trajectory based on its speed and angle.
        Removes the orb if it leaves the canvas bounds.
        """
        
        # Update position
        self.__x += self.__xspeed
        self.__y += self.__yspeed

        # Check if the orb is out of the window
        if (self.__x < 0 or self.__x > self.__canvas.winfo_width() or
                self.__y < 0 or self.__y > self.__canvas.winfo_height()):
            self.remove()
        else:
            # updates orbs objects position
            self.__canvas.coords(self.__orbID, self.__x, self.__y)
            
    def getX(self):
        """ Returns the x-position (left side) of the healthpowerup.

        Returns:
            int: The x-position of the Orb.
        """        
        return self.__x
    
    def remove(self):
        """
        Removes the orb from the canvas and deactivates it.
        """
        if self.__active:
            self.__canvas.delete(self.__orbID)
            self.__active = False

    def getRight(self):
        """ Returns the right side of the Orb (that is, its x-position + its width).

        Returns:
            int: The right side of the Orb.
        """        
        return self.__x + self.__image.width()
    
    def getBottom(self):
        """ Returns the bottom side of the Orb (that is, its y-position + its height).

        Returns:
            int: The bottom side of the Orb.
        """        
        return self.__y + self.__image.height()
    
    def getY(self):
        """ Returns the top (i.e., y-position) of the Orb.

        Returns:
            int: The top (or y-position) of the Orb.
        """        
        return self.__y
    
    def isActive(self):
        """
        Returns whether the orb is still active (not removed).
        """
        return self.__active
    
    # Define properties for x, y, right, and bottom
    x = property(getX)
    y = property(getY)
    right = property(getRight)
    bottom = property(getBottom)


class Direction(Enum):
    """sets the direction to East, west,up or down
    """    
    EAST = 0
    WEST = 1
    UP = 2
    DOWN = 3
    
class Hero:
    def __init__(self, canvas, eastimages, westimages, dir=Direction.EAST, ypos = 0, xpos = 0):
        """ Creates an hero object using the canvas and images provided.

        Args:
            canvas (CanvasID): The tkinter Canvas that will be used to draw the Hero object.
            eastimages (list): A list of ImageTk.PhotoImage objects to represent the Hero moving east.
            westimages (list): A list of ImageTk.PhotoImage objects to represent the hero moving west.
            dir (Direction, optional): The direction the hero is facing (options are either Direction.EAST or Direction.WEST). Defaults to Direction.EAST.
            ypos (int, optional): The location of the Hero along the y-axis. Defaults to 0.
            xpos (int, optional): The location of the Hero along the x-axis. Defaults to 0.
        """        
        self.__canvas = canvas
        self.__eastimages = eastimages
        self.__westimages = westimages
        self.__direction = dir
        self.__plshootonce = True # checker for setting index to 0 once
        self.__joemama = False # set the checker for one time to shoot boolean variable
        self.__idleID = self.__canvas.after(35, self.idle)
        self.__shootID = None
        self.__index = 0
        self.__xpos = xpos
        self.__ypos = ypos
        self.__health = 3
        self.__healthimages = [ImageTk.PhotoImage(Image.open('Health/0.png')), ImageTk.PhotoImage(Image.open('Health/2.png')), ImageTk.PhotoImage(Image.open('Health/4.png')), ImageTk.PhotoImage(Image.open('Health/6.png'))] # A list of images
        self.__deadimageseast, self.__deadimageswest, self.__idleimageseast, self.__idleimageswest, self.__shooteastimg, self.__shootwestimg = [], [], [], [], [], []
        self.__healthID = self.__canvas.create_image(20, 37, image = self.__healthimages[self.__health], anchor ='nw')
        
        for counter in range(10):
            #append the idle and shoot images to their respective lists
            self.__idleimageseast.append(ImageTk.PhotoImage(Image.open(f'Hero-Guy-PNG/_Mode-Gun/01-Idle/JK_P_Gun__Idle_00{counter}.png')))
            self.__idleimageswest.append(ImageTk.PhotoImage(Image.open(f'Hero-Guy-PNG/_Mode-Gun/01-IdleWest/JK_P_Gun__Idle_00{counter}.png')))
            self.__shooteastimg.append(ImageTk.PhotoImage(Image.open(f'Hero-Guy-PNG/_Mode-Gun/03-Shot/JK_P_Gun__Attack_00{counter}.png')))
            self.__shootwestimg.append(ImageTk.PhotoImage(Image.open(f'Hero-Guy-PNG/_Mode-Gun/03-ShotWest/JK_P_Gun__Attack_00{counter}.png')))
        for counter in range(7):
            #append the dead images to their respective lists
            self.__deadimageseast.append(ImageTk.PhotoImage(Image.open(f'Hero-Guy-PNG/06-Die/JK_P__Die_00{counter}.png')))
            self.__deadimageswest.append(ImageTk.PhotoImage(Image.open(f'Hero-Guy-PNG/06-DieWest/JK_P__Die_00{counter}.png')))
        
        #if you are looking east make the current image eastward, 
        if self.__direction == Direction.EAST:
            self.__currentimage = self.__eastimages[self.__index]
        else:
            #if you are looking west, make currenet image look westward
            self.__currentimage = self.__westimages[self.__index]
        # create the image of the hero
        self.__heroID = self.__canvas.create_image(self.__xpos, self.__ypos, image = self.__currentimage, anchor ='nw')
    def kill(self):
        """ Kills the Hero by setting the image to the Hero on the ground and facing the direction it was facing before it dies.
        """      
        #stop the timers 
        self.__canvas.after_cancel(self.__shootID)
        self.__canvas.after_cancel(self.__idleID)

        #if you are looking east make the current image eastward, 
        if self.__direction == Direction.EAST:
            self.__currentimage = self.__deadimageseast[self.__index]
        #if you are looking west, make currenet image look westward
        elif self.__direction == Direction.WEST:
            self.__currentimage = self.__deadimageswest[self.__index]
        #change the current image
        self.__canvas.itemconfig(self.__heroID, image=self.__currentimage)
        self.__dead = True
        # Schedule the kill method to execute after 500ms
        self.__killplayertimerID = self.__canvas.after(500, self.kill)
        self.__index += 1
        #Reset index and stop the animation
        if self.__index >= len(self.__deadimageseast):
            self.__index = -1
            self.__canvas.after_cancel(self.__killplayertimerID)
            
    def setIndex(self, index):
        """sets the index
        Args:
            index(int): the index
        """
        self.__index = index
    
    def getHealth(self):
        """returns the health of the hero

        Returns:
            int : healthID
        """        
        return self.__health
    def setHealth(self, health):
        """sets the health of the hero
        Args
           health (int): the healthID
        """       
        self.__health = health
        self.__canvas.itemconfig(self.__healthID, image=self.__healthimages[self.__health])
    
    def getDead(self):
        """ Returns whether or not the hero is dead or not.

        Returns:
            bool: The state of the hero (that is, True if it is dead, otherwise False).
        """        
        return self.__dead

    def getHeight(self):
        """ Returns the height of the hero.

        Returns:
            int: The height of the hero.
        """        
        return self.__currentimage.height()
    
    def getWidth(self):
        """ Returns the width of the hero.

        Returns:
            int: The width of the hero.
        """        
        return self.__currentimage.width()
    
    def getY(self):
        """ Returns the y-position of the hero.

        Returns:
            int: The y-position of the hero.
        """        
        return self.__ypos
    
    def setY(self, y):
        """ Sets the y-position of the hero.

        Args:
            y (int): The y-position of the hero.
        """        
        self.__ypos = y
        #Updates the location and the image of the Hero.
        self.__canvas.itemconfig(self.__heroID, image=self.__currentimage)
        self.__canvas.coords(self.__heroID, self.__xpos, self.__ypos)
    
    def getX(self):
        """ Returns the x-position of the hero.

        Returns:
            int: The x-position of the hero.
        """        
        return self.__xpos
    
    def setX(self, x):
        """ Sets the x-position of the Hero.

        Args:
            x (int): The x-position of the Hero.
        """        
        self.__xpos = x
        #Updates the location and the image of the Hero.
        self.__canvas.itemconfig(self.__heroID, image=self.__currentimage)
        self.__canvas.coords(self.__heroID, self.__xpos, self.__ypos)

    def endtimer(self):
        """End the timer for idleID 
        """        
        self.__canvas.after_cancel(self.__idleID)
    def shoot(self):
        """ Sets the image of the Hero to it shooting.
        """        
        self.__joemama = True
        self.__canvas.after_cancel(self.__idleID) # stop the idle timer
        if self.__plshootonce == True:  #boolean for reload delay 
            self.__index = 0
        self.__plshootonce = False
        self.__index += 1
        self.__shootID = self.__canvas.after(35, self.shoot) #shoot the bullet after the timer
        if self.__index >= len(self.__shooteastimg):         # if the index is less than the length of the list,
            self.__index = 0                                 #Reset index
            self.__canvas.after_cancel(self.__shootID)       # stop shooting
            self.__idleID = self.__canvas.after(35, self.idle), #switch to idle
            self.__plshootonce = True                           # update booleans
            self.__joemama = False
        
        #if the direction is east, shoot east, if west, shoot west
        if self.__direction == Direction.EAST:                  
            self.__currentimage = self.__shooteastimg[self.__index]
        else:
            self.__currentimage = self.__shootwestimg[self.__index]

        #Updates the location and the image of the Hero.
        self.__canvas.itemconfig(self.__heroID, image=self.__currentimage)
        self.__canvas.coords(self.__heroID, self.__xpos, self.__ypos)
        
        
    def idle(self):
        """ Sets the image of the Hero to it standing idle.
        """        
        #if index is more than the length of the list, update the index
        self.__index += 1
        if self.__index >= len(self.__idleimageseast):
            self.__index = 0
        #if direction is east, idle facing east, if direction is west, idle facing west
        if self.__direction == Direction.EAST:
            self.__currentimage = self.__idleimageseast[self.__index]
        else:
            self.__currentimage = self.__idleimageswest[self.__index]
        #Updates the location and the image of the Hero, and idle annimation
        self.__canvas.itemconfig(self.__heroID, image=self.__currentimage)
        self.__canvas.coords(self.__heroID, self.__xpos, self.__ypos)
        self.__idleID = self.__canvas.after(35, self.idle)
        
    
    def getBottom(self):
        """ Gets the bottom location of the hero.

        Returns:
            int: Where the bottom of the hero is located along the y-axis.
        """        
        return self.__ypos + self.__currentimage.height()
    
    def setBottom(self, y):
        """ Sets the bottom location of the hero.

        Args:
            y (int): The bottom of the hero along the y-axis.
        """        
        self.__ypos = y - self.__currentimage.height()
        #Updates the location and the image of the Hero.
        self.__canvas.itemconfig(self.__heroID, image=self.__currentimage)
        self.__canvas.coords(self.__heroID, self.__xpos, self.__ypos)


    def health(self):
        #
        self.__healthbar = self.__canvas.create_rectangle(self)

    def getRight(self):
        """ Returns the right side of the hero.

        Returns:
            int: Returns the right side of the hero.
        """        
        return self.__xpos + self.__currentimage.width()
    
    def setRight(self, x):
        """ Sets the location of the right side of the hero.

        Args:
            x (int): The right side of the hero.
        """        
        self.__xpos = x - self.__currentimage.width()
    
    def getDirection(self):
        """ Returns the direction of the hero is facing (either Direction.EAST or Direction.WEST)

        Returns:
            Direction: The direction the hero is facing.
        """        
        return self.__direction

    
    def getCenterY(self):
        """ Returns the center position of the Hero vertically.

        Returns:
            int: The center position of the Hero vertically.
        """        
        return self.__ypos + (self.__currentimage.height() // 2)

    def getCenterX(self):
        """ Returns the center position of the hero horizontally.

        Returns:
            int: The center position of the hero horizontally.
        """        
        return self.__xpos + (self.__currentimage.width() // 2)
    
    def move(self, xspeed, yspeed):
        """ Moves the hero along the x- and y-axis based on the xspeed and yspeed values provided. If the xspeed or yspeed values are not provided, the hero will not move.

        Args:
            xspeed (int, optional): The speed of the hero along the x-axis. Defaults to 0.
            yspeed (int, optional): The speed of the hero along the y-axis. Defaults to 0.
        """        
        #update xspeed and yspeed
        self.__xpos += xspeed
        self.__ypos += yspeed
        
        #stop the timer 
        self.__canvas.after_cancel(self.__idleID)
        
        #look east if expeed is more than 0, look west if xspeed is less than zero
        if xspeed > 0:
            self.__direction = Direction.EAST
        elif xspeed < 0:
            self.__direction = Direction.WEST
        
        # If boolean is False, increment the index and reset it to 0
        if self.__joemama == False:
            self.__index += 1
            #reset it to 0 if index is greater than or equal to the length of east images
            if self.__index >= len(self.__eastimages):
                self.__index = 0
            
            #if direction is east , make current image east 
            if self.__direction == Direction.EAST:
                self.__currentimage = self.__eastimages[self.__index]
            else:
                self.__currentimage = self.__westimages[self.__index]
        #Updates the location and the image of the Hero.
            self.__canvas.itemconfig(self.__heroID, image=self.__currentimage)
        self.__canvas.coords(self.__heroID, self.__xpos, self.__ypos)
    
    # Set up properties for attributes with getter and setter methods 
    height = property(getHeight)
    width = property(getWidth)
    y = property(getY, setY)
    x = property(getX, setX)
    bottom = property(getBottom, setBottom)
    right = property(getRight, setRight)
    dead = property(getDead)
    direction = property(getDirection)
    centery = property(getCenterY)
    centerx = property(getCenterX)
    health = property(getHealth, setHealth)
    
class Bullet:
    def __init__(self, canvas, x=0, y=0, xs=0):
        """ Creates a projectile, in this case, in the form of a bullet.

        Args:
            canvas (CanvasID): The Canvas object where the bullet will be drawn.
            x (int, optional): Where the left side of the bullet will be positioned on the canvas. Defaults to 0.
            y (int, optional): Where the top side of the bullet will be positioned on the canvas. Defaults to 0.
            xs (int, optional): The direction the bullet will be travelling along the x-axis. Defaults to 0.
        """        
        self.__canvas = canvas
        self.__xbpos = x
        self.__ybpos = y
        self.__xspeed = xs
        self.__image = (ImageTk.PhotoImage(Image.open(f'Hero-Guy-PNG/_Weapon/Bullet.png')))
        self.__bulletID = None
    
    def move(self):
        """ Moves the bullet along the x-axis based on its speed. If the weapon has not been created yet, then it will be created; otherwise, the image will simply be updated.
        """        
        #update the xbpos
        self.__xbpos += self.__xspeed
        # id bulletId is none, create the bullet 
        if self.__bulletID == None:
            self.__bulletID = self.__canvas.create_image(self.__xbpos, self.__ybpos, image=self.__image, anchor='nw')
        else:
            #change the image of the bulletID
            self.__canvas.itemconfig(self.__bulletID, image=self.__image)
        #Updates the location of the Hero.
        self.__canvas.coords(self.__bulletID, self.__xbpos, self.__ybpos)
    
    def getX(self):
        """ Returns the x-position (left side) of the bullet.

        Returns:
            int: The x-position of the bullet.
        """        
        return self.__xbpos
    
    def getRight(self):
        """ Returns the right side of the bullet (that is, its x-position + its width).

        Returns:
            int: The right side of the bullet.
        """        
        return self.__xbpos + self.__image.width()
    
    def getBottom(self):
        """ Returns the bottom side of the bullet (that is, its y-position + its height).

        Returns:
            int: The bottom side of the bullet.
        """        
        return self.__ybpos + self.__image.height()
    
    def getY(self):
        """ Returns the top (i.e., y-position) of the bullet.

        Returns:
            int: The top (or y-position) of the bullet.
        """        
        return self.__ybpos
    # Set up properties for attributes with getter and setter methods 
    x = property(getX)
    y = property(getY)
    right = property(getRight)
    bottom = property(getBottom)

class IceShard:
    def __init__(self, canvas, xPos = 0, yPos = 0):
        """ Creates a floating IceShard

        Args:
            canvas (CanvasID): The Canvas object where the IceShard will spawn in.
            xPos (int, optional): The position on the x-axis. Defaults to 0.
            yPos (int, optional): The psoition on the y-axis. Defaults to 0.
        """              
        self.__canvas = canvas
        self.__currentimage = ImageTk.PhotoImage(Image.open(f'images_misc/Ice_Shard.png'))
        self.__x = xPos
        self.__y = yPos
        self.__hovering = False
        self.__hovervelocity = 0
        self.__gravity = 1
        self.__width = self.__currentimage.width()
        self.__height = self.__currentimage.height()
        self.__shardID = self.__canvas.create_image(self.__x, self.__y, image = self.__currentimage, anchor='nw')
    
    def getHoverID(self):
        """pause the hoverID
        Returns:
            [type]: [description]
        """        
        self.__canvas.after_cancel(self.__hoverID)
    
    def hover(self, ground = 0):
        """make the shard hover 

        Args:
            ground (int, optional): the ground. Defaults to 0.
        """        
        #set the hover velocity to -4 and make hovering true
        if self.__hovering == False:
            self.__hovervelocity = -4
            self.__hovering = True
        # Update vertical position based on hover velocity and gravity
        self.__y += self.__hovervelocity
        self.__hovervelocity += self.__gravity
        #schedule next hover update
        self.__hoverID = self.__canvas.after(40, lambda: self.hover(ground))
        #update shard position
        self.__canvas.coords(self.__shardID, self.__x, self.__y)
            #make hovering false if y+height is greater than ground
        if self.__y + self.__height >= ground:
            self.__hovering = False
           
    def shardremove(self):
        """remove the shardID
        """        
        self.__canvas.delete(self.__shardID)
        self.__canvas.after_cancel(self.__hoverID)
    def getID(self):
        """ Returns the ShardID.
        Returns:
           int : The timer ID of the shard
        """   
        return self.__shardID
    def getRightSide(self):
        """ Returns the right side of the shard 
        Returns:
            int: add the x and the width to get the right side
        """        
        return self.__x + self.__width
    def getBottom(self):
        """Returns the bottom side of the shard 

        Returns:
            int: add the y and the height to get the bottom of the shard
        """        
        return self.__y + self.__height
    def getX(self):
        """Returns the bottom side of the shard 

        Returns:
            int: returns the x
        """        
        return self.__x
    def getY(self):
        """Returns the y of the shard 

        Returns:
            int: returns the y
        """        
        return self.__y
    def getID(self):
        """Returns the HoverID 

        Returns:
            int: returns the HoverID
        """        
        return self.__hoverID
    def setX(self, x):
        """ Sets the x-position of the IceShard

        Args:
            x (int): The x-position of the Iceshard.
        """       
        self.__x = x
    def setY(self, y):
        """ Sets the y-position of the IceShard

        Args:
            y (int): The y-position of the Iceshard.
        """         
        self.__y = y
    def getID(self):
        """Returns the ShardID 

        Returns:
            int: returns the ShardID
        """        
        return self.__shardID
    # Set up properties for attributes with getter and setter methods 
    right = property(getRightSide)
    left = property(getX, setX)
    top = property(getY)
    bottom = property(getBottom)
    x = property(getX, setX)
    y = property(getY, setY)
    

class Wolf:
    def __init__(self, canvas, xPos = 0, yPos = 0, interval = 0, direction = Direction.EAST, xspeed = 0, yspeed = 0):
        """ Creates an Wolf object using the canvas with death, attack, run and direction animations and movement

        Args:
            canvas (CanvasID): The Canvas object where the wolf will go across.
            xPos (int, optional): The position on the x-axis. Defaults to 0.
            yPos (int, optional): The psoition on the y-axis. Defaults to 0.
            interval (int, optional): the amount of time the user has to wait before spawning another wolf. Defaults to 0.
            direction (Enum, optional): the direction that the wolf is facing. Defaults to Direction.EAST.
            xspeed (int, optional): The speed of the wolf along the x-axis. Defaults to 0.
            yspeed (int, optional): The speed of the wolf along the y-axis. Defaults to 0.
        """      

        self.__canvas = canvas
        self.__direction = direction
        self.__eastimages, self.__westimages, self.__attackeast, self.__attackwest = [], [], [], []
        for i in range(8):
            self.__eastimages.append(ImageTk.PhotoImage(Image.open(f'Wolf/Run/__Wolf_Run_00{i}.png')))
            self.__westimages.append(ImageTk.PhotoImage(Image.open(f'Wolf/RunWest/__Wolf_Run_00{i}.png')))
            self.__attackeast.append(ImageTk.PhotoImage(Image.open(f'Wolf/Attack/__Wolf_Attack_00{i}.png')))
            self.__attackwest.append(ImageTk.PhotoImage(Image.open(f'Wolf/AttackWest/__Wolf_Attack_00{i}.png')))
        self.__interval = interval
        self.__x = xPos
        self.__y = yPos
        self.__killtimer = None
        self.__xspeed = xspeed
        self.__yspeed = yspeed
        self.__index = 0
        self.__playerdead = False
        self.__currentimage = self.__eastimages[self.__index]
        self.__width = self.__currentimage.width()
        self.__height = self.__currentimage.height()
        self.__wolfID = self.__canvas.create_image(self.__x, self.__y, image = self.__currentimage, anchor='nw')
    
    def getDirection (self): 
       """Returns the wolfs direction

        Returns:
            int: returns the directions
        """ 
       return self.__direction
    def setDirection (self, dir):
       """ Sets the Direction of the Wolf

        Args:
            y (int): The direction of the Iceshard.
        """  
       self.__direction = dir
    def getHeight(self):
        """Returns the wolfs height

        Returns:
            int: returns the height
        """ 
        return self.__height
    def getWidth(self):
        """Returns the wolfs Width

        Returns:
            int: returns the Width
        """ 
        return self.__width
    def getRightSide(self):
        """ Returns the right side of the shard 
        Returns:
            int: add the x and the width to get the right side
        """   
        return self.__x + self.__width
    def getBottom(self):
        """Returns the bottom side of the shard 

        Returns:
            int: add the y and the height to get the bottom of the shard
        """  
        return self.__y + self.__height
    def getX(self):
        """Returns the X of the shard 

        Returns:
            int: returns the x
        """
        return self.__x
    def getY(self):
        """Returns the y of the shard 

        Returns:
            int: returns the y
        """        
        return self.__y
    def setIndex(self, ind):
        """sets the index
        Args:
            index(int): the index
        """
        self.__index = ind
    def setX(self, x):
        """ Sets the x-position of the Wolf

        Args:
            x (int): The x-position of the Wolf.
        """  
        self.__x = x
    def setY(self, y):
        """ Sets the y-position of the Wolf

        Args:
            y (int): The y-position of the Wolf.
        """    
        self.__y = y
    def getWolfID(self):
        """Returns the WolfID 

        Returns:
            int: returns the WolfID
        """  
        return self.__wolfID

    def kill(self, interval=100):
        """Kill the wolf

        Args:
            interval (int, optional): the interval time. Defaults to 100.
        """        
        #make the xspeed and yspeed 
        self.__xspeed = 0
        self.__yspeed = 0
        #if the direction of the woldf is east , make the death image east
        if self.__direction == Direction.EAST:
            self.__currentimage = ImageTk.PhotoImage(Image.open(f'Wolf/Dead/__Wolf_Dead_007.png'))
        #if the direction of the woldf is west , make the death image west
        elif self.__direction == Direction.WEST:
            self.__currentimage = ImageTk.PhotoImage(Image.open(f'Wolf/DeadWest/__Wolf_Dead_007.png'))
        # Update the wolf's image
        self.__canvas.itemconfig(self.__wolfID, image=self.__currentimage)
        #schedule its removal
        self.__killtimer = self.__canvas.after(500, self.removewolf)
        #cancel the ongoing wolf timer.
        self.__canvas.after_cancel(self.__wolftimerID)
    def removewolf(self):
        """ Remove the wolfID
        """        
        self.__canvas.after_cancel(self.__killtimer)
        self.__canvas.delete(self.__wolfID)
        
    def endtimer(self):
        """End the timer for idleID 
        """ 
        self.__canvas.after_cancel(self.__wolftimerID)
        self.__playerdead = True
    
    def attack(self):
        """Handle the wolf's attack animation and behavior"""      
        if self.__playerdead == False: # Proceed only if the player is not dead
            self.__canvas.after_cancel(self.__wolftimerID) # Cancel the wolf's current movement timer
            # Update the wolf's image based on its attack direction
            if self.__direction == Direction.EAST:
                self.__currentimage = self.__attackeast[self.__index]
                self.__canvas.itemconfig(self.__wolfID, image=self.__currentimage)
            elif self.__direction == Direction.WEST:
                self.__currentimage = self.__attackwest[self.__index]
                self.__canvas.itemconfig(self.__wolfID, image=self.__currentimage)
            self.__index += 1 # Move to the next frame in the attack animation
            # Schedule the next frame of the attack animation
            self.__wolfattacktimer = self.__canvas.after(40, self.attack)
            # If the animation is complete, reset the wolf's movement timer
            if self.__index >= len(self.__attackeast):
                self.__canvas.after_cancel(self.__wolfattacktimer)  # Stop the attack animation
                self.__wolftimerID = self.__canvas.after(self.__interval, self.move)# Resume movement after the attack
             
    def move(self):
        """Handle the wolf's movement, direction, and animation."""       
         # Update the wolf's position based on its speed
        self.__x += self.__xspeed
        self.__y += self.__yspeed
        # loop it until the index is greater than eastimages
        self.__index += 1
        if self.__index >= len(self.__eastimages):
            self.__index = 0
        
         # Check for horizontal boundaries and adjust direction and speed 
        if self.__x + self.__width - 75 >= self.__canvas.winfo_reqwidth():
            self.__direction = Direction.WEST
            self.__xspeed = -(abs(self.__xspeed))
        elif self.__x + 75 <= 0:
            self.direction = Direction.EAST
            self.__xspeed = abs(self.__xspeed)
        # Check for vertical boundaries and adjust direction and speed 
        if self.y +self.__height - 50 > self.__canvas.winfo_reqheight():
            self.__yspeed = -(self.__yspeed)
        elif self.y + (self.height // 2) + 15 < 0:
            self.__yspeed = -(self.__yspeed)
        
        #update image based on the direction the wolf is facing
        if self.__direction == Direction.EAST:
            self.__currentimage = self.__eastimages[self.__index]
        elif self.__direction == Direction.WEST:
            self.__currentimage = self.__westimages[self.__index]
        #update wolfs image based on its directions
        self.__canvas.coords(self.__wolfID, self.__x, self.__y)
        self.__canvas.itemconfig(self.__wolfID, image=self.__currentimage)
        # wait for the next movement update
        self.__wolftimerID = self.__canvas.after(self.__interval, self.move)
    
    # Set up properties for attributes with getter and setter methods 
    right = property(getRightSide)
    left = property(getX, setX)
    top = property(getY)
    bottom = property(getBottom)
    x = property(getX, setX)
    y = property(getY, setY)
    width = property(getWidth)
    direction = property(getDirection, setDirection)
    height = property(getHeight)

idle = False
class Wizard:
    def __init__(self, canvas, xPos = 0, yPos = 0, interval = 0, direction = Direction.EAST, xspeed = 0):
        """The Wizard spawner that spawns wizards and an instance of it with images in it for animation, shooting, moving, and idling

        Args:
            canvas (CanvasID): The Canvas object where the wizard will go across.
            xPos (int, optional): The position on the x-axis. Defaults to 0.
            yPos (int, optional): The psoition on the y-axis. Defaults to 0.
            interval (int, optional): the amount of time the user has to wait before spawning another wizard. Defaults to 0.
            direction (Enum, optional): the direction that the Wizard is facing. Defaults to Direction.EAST.
            xspeed (int, optional): The speed of the wolf along the x-axis. Defaults to 0.
        """        
        self.__canvas = canvas
        self.__direction = direction
        self.__eastimages, self.__westimages, self.__idleEastImg, self.__idleWestImg, self.__shootwestimg, self.__shooteastimg = [], [], [], [], [], []
        if self.__direction == Direction.EAST:
            #upload the runreast, ildeeast, and castspelleast images
            for i in range(7):
                self.__eastimages.append(ImageTk.PhotoImage(Image.open(f'Wizard/RunEast/__blue_cape_wizzard_run_00{i}.png')))
                self.__idleEastImg.append(ImageTk.PhotoImage(Image.open(f'Wizard/IdleEast/__blue_cape_wizzard_idle_00{i}.png')))
                self.__shooteastimg.append(ImageTk.PhotoImage(Image.open(f'Wizard/CastSpellEast/__blue_cape_wizzard_cast_spell_00{i}.png')))
        elif self.__direction == Direction.WEST:
            #upload the Runwest, IdleWest, CastspellWest images
            for i in range(7):
                self.__westimages.append(ImageTk.PhotoImage(Image.open(f'Wizard/RunWest/__blue_cape_wizzard_run_00{i}.png')))
                self.__idleWestImg.append(ImageTk.PhotoImage(Image.open(f'Wizard/IdleWest/__blue_cape_wizzard_idle_00{i}.png')))
                self.__shootwestimg.append(ImageTk.PhotoImage(Image.open(f'Wizard/CastSpellWest/__blue_cape_wizzard_cast_spell_00{i}.png')))
        self.__interval = interval
        self.__x = xPos
        self.__y = yPos
        self.__xspeed = xspeed
        self.__idle = False
        self.__index = 0
        self.__attacking = False
        self.__currentimage = ImageTk.PhotoImage(Image.open(f'Wizard/CastSpellWest/__blue_cape_wizzard_cast_spell_000.png'))
        self.__width = self.__currentimage.width()
        self.__height = self.__currentimage.height()
        self.__wizzID = self.__canvas.create_image(self.__x, self.__y, image = self.__currentimage, anchor='nw')
        self.__wizztimerID = None
    
    def getHeight(self):
        """Returns the wizards height

        Returns:
            int: returns the height
        """    
        return self.__height
    def getWidth(self):
        """Returns the Wizards Width

        Returns:
            int: returns the Width
        """ 
        return self.__width
    def getleftSide(self):
        """Returns the Wizards left side

        Returns:
            int: adds the x and the width to get the left side
        """ 
        return self.__x + self.__width
    def getBottom(self):
        """Returns the bottom side of the Wizards 

        Returns:
            int: add the y and the height to get the bottom of the wizard
        """  
        return self.__y + self.__height
    def getX(self):
        """Returns the X of the Wizards

        Returns:
            int: returns the x
        """
        return self.__x
    def getY(self):
        """Returns the Y of the Wizard

        Returns:
            int: returns the Y
        """
        return self.__y
    def setIndex(self, ind):
        """sets the index
        Args:
            index(int): the ind
        """
        self.__index = ind
    def setX(self, x):
        """ Sets the x-position of the Wizard

        Args:
            x (int): The x-position of the Wizard
        """  
        self.__x = x
    def setY(self, y):
        """ Sets the y-position of the Wizard

        Args:
            y (int): The y-position of the Wizard.
        """  
        self.__y = y
    def setIndex(self, index):
        """sets the index
        Args:
            index(int): the index
        """
        self.__index = index
    def returnidle(self):
        """Returns the idle

        Returns:
            int: returns idle
        """     
        return self.__idle
    def getOrbPosition(self):
        """Returns the orbx and orby of the Wizard

        Returns:
            int: returns the x and y of the orbs
        """
        return self.__OrbX, self.__OrbY
    
    def enablewizardshot(self):
        """enable the wizard shot
        """        
        self.__index = 0
        self.__attacking = True
        self.shootem()
        
    def shootem(self):
        """ Handles the wizard's shooting animation."""
        # Cancel wizard movement timer.
        self.__canvas.after_cancel(self.__wizztimerID)
        if self.__direction == Direction.EAST:
            self.__currentimage = self.__shooteastimg[self.__index]
        elif self.__direction == Direction.WEST:
            self.__currentimage = self.__shootwestimg[self.__index]
        #shooting animation timer
        self.__wizardshootTimerID = self.__canvas.after(65, self.shootem)
        self.__index += 1
        #resets animation and states if the shooting sequence is complete
        if self.__index >= 7:
            self.__canvas.after_cancel(self.__wizardshootTimerID)
            self.__index = 0
            self.__attacking = False
            self.move()
            self.__shootwaiterID = self.__canvas.after(5000, self.enablewizardshot)
        #update the wizards position and image on th canvas
        self.__canvas.coords(self.__wizzID, self.__x, self.__y)
        self.__canvas.itemconfig(self.__wizzID, image=self.__currentimage)  

    def endTimers (self):
        """Pause the timer"""
        self.__canvas.after_cancel(self.__wizztimerID)
        
    def isAttacking(self):
        """Returns isAttacking

        Returns:
            int: returns attaking
        """   
        return self.__attacking
    def setAttack(self, attack):
        """sets the Attack
        Args:
            index(int): the attack
        """
        self.__attacking = attack
    def deleteWizard(self):
        """Removes the wizard from the game and canvas
        """        
        self.__canvas.delete(self.__wizzID)
    def setIdle(self, idle):
        """sets the wizard Idle 
        Args:
            index(int): the idle
        """
        self.__idle = idle
    def move(self):
        # Update the wizard's horizontal position
        self.__x += self.__xspeed
        self.__index += 1
        #reset the index if it reaches 7
        if self.__index >= 7:
            self.__index = 0
        #start timer for the movement update
        self.__wizztimerID = self.__canvas.after(self.__interval, self.move)
        # update its image and check for attacking or idle state
        if self.__idle == False:
            if self.__direction == Direction.EAST:
                self.__currentimage = self.__eastimages[self.__index]
                # If the wizard's position is within the allowed range, set it to idle and prepare for shooting.
                if self.__x + 90 >= 35:
                    self.__idle = True
                    self.__attacking = True
                    self.__OrbX = self.__x
                    self.__OrbY = self.__y
                    self.enablewizardshot()
            #If the direction is westward, 
            elif self.__direction == Direction.WEST:
                self.__currentimage = self.__westimages[self.__index]
                # If the wizard's position is within the allowed range, set it to idle and prepare for shooting.
                if self.__x + 90 <= self.__canvas.winfo_reqwidth() - 125:
                    self.__idle = True
                    self.__OrbX = self.__x
                    self.__OrbY = self.__y
                    self.enablewizardshot()
        # if the wizrad is idle, stop its movement and set the appropriate idle image based on its direction
        elif self.__idle == True:
            self.__xspeed = 0
            if self.__direction == Direction.EAST:
                self.__currentimage = self.__idleEastImg[self.__index]
            elif self.__direction == Direction.WEST:
                self.__currentimage = self.__idleWestImg[self.__index]

         #update the wizards position and image on the canvas          
        self.__canvas.coords(self.__wizzID, self.__x, self.__y)
        self.__canvas.itemconfig(self.__wizzID, image=self.__currentimage)
    
    # Set up properties for attributes with getter and setter methods 
    left = property(getleftSide, setX)
    top = property(getY)
    bottom = property(getBottom)
    x = property(getX, setX)
    y = property(getY, setY)
    width = property(getWidth)
    height = property(getHeight)
    

class FlyingBat:   
    def __init__(self, canvas, xPos = 0, yPos = 0, interval = 0, direction = Direction.EAST, xspeed = 0, yspeed = 0, ydir = Direction.UP):
        """

        Args:
            canvas (Canvas ID): the gamecanvas of the game
            xPos (int, optional): the x position of the bat on the gamecanvas. Defaults to 0.
            yPos (int, optional): the y position of the bat on the gamecanvas. Defaults to 0.
            interval (int, optional): the animation refresh rate. Defaults to 0.
            direction ([type], optional): the direction that the bat goes in. Defaults to Direction.EAST.
            xspeed (int, optional): the xspeed of the bat on the screen, how fast it goes horizontally. Defaults to 0.
            yspeed (int, optional): the yspeed of the bat on the screen, how fast it goes vertically. Defaults to 0.
            ydir ([type], optional): the direction of the bat either up or down. Defaults to Direction.UP.
        """        
        self.__canvas = canvas
        self.__direction = direction
        self.__eastimages, self.__westimages, self.__attackeast, self.__attackwest = [], [], [], []
        for i in range(8):
            self.__eastimages.append(ImageTk.PhotoImage(Image.open(f'FlyingThing/02-Fly/__Bat02_Fly_00{i}.png')))
            self.__westimages.append(ImageTk.PhotoImage(Image.open(f'FlyingThing/02-FlyWest/__Bat02_Fly_00{i}.png')))
            self.__attackeast.append(ImageTk.PhotoImage(Image.open(f'FlyingThing/03-Attack/__Bat02_Attack_00{i}.png')))
            self.__attackwest.append(ImageTk.PhotoImage(Image.open(f'FlyingThing/03-AttackWest/__Bat02_Attack_00{i}.png')))
        self.__interval = interval
        self.__x = xPos
        self.__y = yPos
        self.__killtimer = None
        self.__xspeed = xspeed
        self.__ydir = ydir
        self.__yspeed = yspeed
        self.__allowFollow = True
        self.__index = 0
        self.__playerdead = False
        self.__currentimage = self.__eastimages[self.__index]
        self.__width = self.__currentimage.width()
        self.__height = self.__currentimage.height()
        self.__BatID = self.__canvas.create_image(self.__x, self.__y, image = self.__currentimage, anchor='nw')
        
    def getHeight(self):
        """Returns the flyingbats height

        Returns:
            int: returns the height
        """ 
        return self.__height
    def getWidth(self):
        """Returns the flyingbats Width

        Returns:
            int: returns the Width
        """ 
        return self.__width
    def getRightSide(self):
        """ Returns the right side of the flyingbat 
        Returns:
            int: add the x and the width to get the right side
        """  
        return self.__x + self.__width
    def getBottom(self):
        """Returns the bottom side of the flyingbat 

        Returns:
            int: add the y and the height to get the bottom of the flyingbat
        """  
        return self.__y + self.__height
    def getX(self):
        """Returns the X of the flyingbat

        Returns:
            int: returns the x
        """
        return self.__x
    def getY(self):
        """Returns the Y of the flyingbat

        Returns:
            int: returns the Y
        """
        return self.__y
    def setIndex(self, ind):
        """sets the index
        Args:
            index(int): the index
        """
        self.__index = ind
    def setX(self, x):
        """ Sets the x-position of the flyingboat

        Args:
            x (int): The x-position of the flyingboat.
        """  
        self.__x = x
    def setY(self, y):
        """ Sets the y-position of the flyingboat

        Args:
            y (int): The y-position of the flyingboat.
        """  
        self.__y = y
    def getBatID(self):
        """Gives back the ID of the bat on the game canvas

        Returns:
            ID: return the ID of the Bat and its image on the canvas
        """        
        return self.__BatID
    def setFollow(self, f):
        """Say either true or false to know if following the player is allowed or not

        Args:
            f (Boolean): Say either true or false to know if following the player is allowed or not
        """        
        self.__allowFollow = f

    def kill(self):
        """
        Kill the bat when he is dead and then play the removebat function to hold the death image for a while and show the death image
        """             
        self.__xspeed = 0
        self.__yspeed = 0
        # if the flying bat is facing east, and dies, update the current image
        if self.__direction == Direction.EAST:
            self.__currentimage = ImageTk.PhotoImage(Image.open(f'FlyingThing/05-Die/__Bat02_Die_007.png'))
        # if the flying bat is facing west, and dies, update the current image
        elif self.__direction == Direction.WEST:
            self.__currentimage = ImageTk.PhotoImage(Image.open(f'FlyingThing/05-DieWest/__Bat02_Die_006.png'))
        #self.__canvas.after_cancel(self.__zomtimer)
        self.__canvas.itemconfig(self.__BatID, image=self.__currentimage)
        self.__killtimer = self.__canvas.after(500, self.removebat)
        #self.__canvas.after_cancel(self.__batTimerID)
        
    def removebat(self):
        """
        To remove the bat's timer and the photo from the screen
        """        
        self.__canvas.after_cancel(self.__killtimer)
        self.__canvas.delete(self.__BatID)
    
    def attack(self):
        """The attack animation function for simply checking the direction of the bat, and then adequately showing the animation of the attack when it is initiated
        """       
        # If the bat is not allowed to follow and the player is not dead, perform the attack animation. 
        if self.__allowFollow == False:
            if self.__playerdead == False:
                # Update the bat's image based on its direction and attack animation.
                if self.__direction == Direction.EAST:
                    self.__currentimage = self.__attackeast[self.__index]
                    self.__canvas.itemconfig(self.__BatID, image=self.__currentimage)
                elif self.__direction == Direction.WEST:
                    self.__currentimage = self.__attackwest[self.__index]
                    self.__canvas.itemconfig(self.__BatID, image=self.__currentimage)
                # Move to the next animation frame.
                self.__index += 1
                self.__batAttackTimer = self.__canvas.after(40, self.attack)
                # If the attack animation is complete, reset and allow the bat to follow.
                if self.__index >= len(self.__attackeast):
                    self.__canvas.after_cancel(self.__batAttackTimer)
                    self.__allowFollow = True
    
    def follow(self, soldierX, soldierY):
        """The follow function for the bat, that will change the direction, speed, and spot of the bat based on the player's location

        Args:
            soldierX (int): The X locaton of the soldier that is constantly being passed to the bat
            soldierY (int): The Y locaton of the soldier that is constantly being passed to the bat
        """        
        # update the bats position and animation based on the soldier's location.
        if self.__allowFollow == True:
            self.__index += 1
            if self.__index >= len(self.__eastimages):
                self.__index = 0
            # Move the bat towards the soldier on the x-axis.   
            if self.__x > soldierX:
                self.__x += -(abs(self.__xspeed))
                #updateimage to face left
                self.__currentimage = self.__westimages[self.__index]
            if self.__x < soldierX:
                self.__x += (abs(self.__xspeed))
                #update image to face right
                self.__currentimage = self.__eastimages[self.__index]
            # Move the bat towards the soldier on the y-axis.
            if self.__y > soldierY:
                self.__y += -(abs(self.__yspeed))   
            if self.__y < soldierY:
                self.__y += (abs(self.__yspeed) )
            #update the wizards position and image on the canvas 
            self.__canvas.coords(self.__BatID, self.__x, self.__y)
            self.__canvas.itemconfig(self.__BatID, image=self.__currentimage)
        
    # the properties for the bat class, with setters and getter put inside
    right = property(getRightSide)
    left = property(getX, setX)
    top = property(getY)
    bottom = property(getBottom)
    x = property(getX, setX)
    y = property(getY, setY)
    width = property(getWidth)
    height = property(getHeight)
idle = False