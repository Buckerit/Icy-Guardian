'''
Icy Guardian
'''

#import all python libraries and modules
from tkinter import Tk, Canvas, messagebox, Button, PhotoImage, Toplevel, Label, Entry, font, Frame, END, ttk, Scrollbar
import random, os, pyglet, time, pygame
from math import atan2, cos, sin
from PIL import Image, ImageTk  
from gameclass import Direction, Hero, Bullet, IceShard, Wolf, Wizard, FlyingBat, Orb, HealthPowerUp

# Function to spawn health power-ups on the game canvas
def spawn_health_powerup():
    global heartsonmap, healthlist, healthtracker, healthspawnintID
    # Create a new HealthPowerUp instance
    HPowerup = HealthPowerUp(canvas=gamecanvas, screen_width=1200, screen_height=671, interval=10)
    HPowerup.move()  # Start its movement
    heartsonmap += 1
    healthlist.append(HPowerup)  # Track the power-up on the canvas
    # Schedule the next health power-up spawn
    healthspawnintID = gamecanvas.after(healthspawninterval, spawn_health_powerup)

# Function to shoot an orb from the wizard towards the hero
def shooterOfOrb(wizardX, wizardY, HeroX, HeroY):
    # Calculate the angle between the wizard and hero
    dx = HeroX - wizardX
    dy = HeroY - wizardY
    angle = atan2(dy, dx) # find the angle of the distance using the atan2 maths function
    xs = 15 * cos(angle)  # X-component of the velocity
    ys = 15 * sin(angle)  # Y-component of the velocity

    # Create a new Orb instanceww wwwwwwwwwwww
    new_orb = Orb(gamecanvas, wizardX, wizardY, xs, ys, angle)
    return new_orb # return this orb when this function is called

# Function to start the game by initializing key processes
def startthegame():
    global startgame
    startgame = True  # Indicate the game has started
    wolfspawn()  # Spawn wolves
    spawnshards()  # Spawn ice shards
    playerhitter()  # Detect player hits
    move_player()  # Enable player movement
    spawn_health_powerup()  # Spawn health power-ups
           
# Function to validate player input and start the game
def checker():
    global startgame
    root.withdraw()  # Hide the root window
    start_window.deiconify()  # Show the start window
    firstname = txtFirst.get().strip(' ').upper()
    cancontinue = True  # Track if input is valid
    if txtFirst.get() == '':
        # Show an error if input is blank
        messagebox.showerror("Error", f'Please enter a name. No Blanks.\nPlease try again.')
        txtFirst.selection_range(0, END)
    else:
        # Proceed with the game
        startgame = True
        startthegame()
        start_window.withdraw()
        root.deiconify()
        
# Delay function to enable orb attacks by the wizard
def enableOrbAttack():
    global orbcanAttack
    orbcanAttack = True
    
# Function to move enemy characters (bats and wizards)
def enemyMover():
    global bats, bathithim, healthtracker, active_orbs, orbcanAttack, batsmoverID, OrbTimerShootID, wizard
    for bat in bats: # make sure the bats will follow the player
        bat.follow(Timmy.x, Timmy.y)  # Bats follow the hero
    for wizar in wizard:
        if wizar.isAttacking(): # only if the wizard is attacking, then shoot the orb
            if orbcanAttack == True: 
                new_orb = shooterOfOrb(wizar.x + 90, wizar.y + 90, Timmy.x + 50, Timmy.y + 50) # the location where the orb needs to go
                active_orbs.append(new_orb)  # Track the active orb
                wizar.setAttack(True) # the wizard is in the process of attacking
                OrbTimerShootID = gamecanvas.after(orbsspawninterval, enableOrbAttack) # the orb delay interval
                orbcanAttack = False # the orb attack delay variable
    # move the orbs
    for orb in active_orbs:  
        orb.move()  # Move all active orbs
    # Schedule the next movement check for enemies
    batsmoverID = gamecanvas.after(35, enemyMover)
    
def spawnwizard():
    global wizard, wizardspawnerID, choices, wizardcounter, wizzsidecounter
    if len(wizard) < 4: # only spawn 4 wizards
        # add one to the wizardcounter and to determine what side of the screen the wizard will spawn on
        wizardcounter += 1
        if wizardcounter >= len(wizardchoices):
            wizardcounter = 0
        wizzsidecounter += 1
        if wizzsidecounter >= 2:
            wizzsidecounter = 0    
        # choose the placement of the wizard
        placement = choices[wizzsidecounter]
        # depending on the placement, determine the direction and speed of the wizard
        if placement < 0:
            wizz = Wizard(canvas=gamecanvas, interval=70, xspeed=random.randint(3, 4), direction=Direction.EAST)
        elif placement > 0:
            wizz = Wizard(canvas=gamecanvas, interval=70, xspeed=random.randint(-4, -3), direction=Direction.WEST)
        # detemine the random position of the wizard
        wizz.y = wizardchoices[wizardcounter]  # random.randint(0, gamecanvas.winfo_reqheight() - Timmy.width)
        wizz.x = placement
        wizz.move() # move the wizard at every spawn to initiate the movement variables
        print(f"There are {len(wizard)} wizards")
        wizard.append(wizz) # append the wizard to the list
        # spawn every 5 seconds    
        wizardspawnerID = gamecanvas.after(5000, spawnwizard)
        
# Function to move bullets fired by the hero
def movebullets():
    global bulletsfired, bulletsmovetimer, wolves, bullets, totalscore
    # if the bullets are empty, cancel the timer for efficiency
    if len(bullets) == 0:
        gamecanvas.after_cancel(bulletsmovetimer)
        bulletsfired = False
    # if there are bullets, be moving them constantly
    else:
        # move each bullet
        for bullet in bullets:
            bullet.move()
            # remove the bullet if it goes off the screen
            if bullet.x > gamecanvas.winfo_reqwidth() or bullet.x < 0:
                bullets.remove(bullet)
            # if there is wolf collision detection, kill the wolf, add to the total score, and remove the wolf from the screen
            for wolf in wolves:
                if bullet.right > (wolf.x + 75) and bullet.x < (wolf.right - 75) and bullet.y < (wolf.bottom - 70) and bullet.bottom > (wolf.y + (wolf.height // 2) + 15):
                    try:
                        bullets.remove(bullet)
                    except:
                        bullets = []
                    # kill the mob, add to the totalscore, and itemconfig the totalscore, and remove it from the screen
                    wolf.kill()
                    totalscore += 3
                    gamecanvas.itemconfig(totalscoreID, text=f'SCORE: {totalscore}')
                    wolves.remove(wolf)
            # if there is bat collision detection, kill the bat, add to the total score, and remove the bat from the screen 
            for bat in bats:
                if bullet.right > (bat.x) and bullet.x < (bat.right) and bullet.y < (bat.bottom - 25) and bullet.bottom > (bat.y + 15):
                    try:
                        bullets.remove(bullet)
                    except:
                        bullets = []
                    # kill the mob, add to the totalscore, and itemconfig the totalscore, and remove it from the screen
                    bat.kill()
                    totalscore += 5
                    gamecanvas.itemconfig(totalscoreID, text=f'SCORE: {totalscore}')
                    bats.remove(bat)
        # move the bullets every 10 milliseconds if there are any bullets on the screen
        bulletsmovetimer = gamecanvas.after(10, movebullets)
    
# the delay shoot the shot variable for canshoot
def enabletheshot():
    global canshoot
    canshoot = True
# on every button click, shoot the bullet and initiate the delay 
def onbuttonpress(event):
    global Timmy, canshoot, bulletsfired
    # if all conditions for shooting are met, then shoot the bullet
    if event.num == 1 and canshoot == True and startgame == True:
        canshoot = False
        # depending on the direction, shoot the bullet from a specific side and append the bullet to the bullets list, and move the bullet
        if Timmy.direction == Direction.EAST:
            bulletspeed = 7
            bulletx = Timmy.right
            bullets.append(Bullet(canvas=gamecanvas, x=bulletx, y=Timmy.centery, xs=bulletspeed))
            Timmy.shoot()
            if bulletsfired == False:
                movebullets()
            bulletsfired = True
        # depending on the direction, shoot the bullet from a specific side and append the bullet to the bullets list, and move the bullet
        elif Timmy.direction == Direction.WEST:
            bulletspeed = -7
            bulletx = Timmy.x
            bullets.append(Bullet(canvas=gamecanvas, x=bulletx, y=Timmy.centery, xs=bulletspeed))
            Timmy.shoot()
            if bulletsfired == False:
                movebullets()
            bulletsfired = True
        # the delay variable for shooting
        gamecanvas.after(400, enabletheshot)

def onkeypress(event):
    # Handles key press events. Updates the global keys dictionary to mark the key as pressed and increments the total key press count.
    global totalkeystotal
    if startgame == True:
        if event.keysym in keys:  # Checks if the pressed key is being tracked
            keys[event.keysym] = True # make the pressed key True
            totalkeystotal += 1  # Increment the key press counter

def onkeyrelease(event):
    # Handles key release events. Updates the global keys dictionary to mark the key as released and lowers the total key press count
    global totalkeystotal
    if startgame == True:
        if event.keysym in keys:  # Checks if the released key is being tracked
            keys[event.keysym] = False
            totalkeystotal -= 1  # Decrement the key press counter
            Timmy.endtimer()  # Stops any ongoing movement timer
            Timmy.idle()  # Updates the character's state to idle

def move_player():
    # Moves the player based on the current key states
    global playermoverID
    if startgame == True:
        # Check if 'd' is pressed for right movement
        if keys['d']:
            Timmy.move(12, 0) # move the player by 12 increments
            # Prevent movement beyond the canvas' right boundary
            if Timmy.right > gamecanvas.winfo_reqwidth():
                Timmy.right = gamecanvas.winfo_reqwidth()
        # Check if 'a' is pressed for left movement
        if keys['a']:
            Timmy.move(-12, 0) # move the player by 12 increments
            # Prevent movement beyond the canvas' left boundary
            if Timmy.x <= 0:
                Timmy.x = 0
        # Check if 'w' is pressed for upward movement
        if keys['w']:
            Timmy.move(0, -12) # move the player by 12 increments
            # Prevent movement beyond the canvas' top boundary
            if Timmy.y <= 0:
                Timmy.y = 0
        # Check if 's' is pressed for downward movement
        if keys['s']:
            Timmy.move(0, 12) # move the player by 12 increments
            # Prevent movement beyond the canvas' bottom boundary
            if Timmy.bottom >= gamecanvas.winfo_reqheight():
                Timmy.bottom = gamecanvas.winfo_reqheight()
                
    # Continuously check for key presses to update the movement of the player
    playermoverID = gamecanvas.after(30, move_player)

def wolfspawn():
    global wolves, wolfspawnerID
    if len(wolves) < wolfonmap:  # Only spawn if the number of wolves is below the limit
        placement = random.choice(choices)  # Randomly decide the starting side of the canvas
        yspeedchooser = random.choice([-4, 4, -3, 3])  # Randomize the wolf's vertical speed
        # Spawn wolves from the left or right edge based on placement and set the direction and speed
        if placement < 0:
            wolfer = Wolf(canvas=gamecanvas, interval=40, xspeed=random.randint(2, 4), yspeed=yspeedchooser, direction=Direction.EAST)
        elif placement > 0:
            wolfer = Wolf(canvas=gamecanvas, interval=40, xspeed=random.randint(-4, -2), yspeed=yspeedchooser, direction=Direction.WEST)
        # Set the wolf's vertical position randomly within the canvas height
        wolfer.y = random.randint(0, (gamecanvas.winfo_reqheight() - (wolfer.getHeight())))
        wolfer.x = placement  # Position the wolf at the edge
        wolfer.move()  # Start moving the wolf
        wolves.append(wolfer)  # Add the new wolf to the active wolves list
        print(f"There are {len(wolves)} wolves")  # Debugging test
    wolfspawnerID = gamecanvas.after(wolfinterval, wolfspawn)  # Schedule the next spawn event for the wolf after a certain number of seconds

def batspawn():
    global bats, batspawnerTimer
    if len(bats) < batonmap:  # Only spawn if the number of bats is below the limit
        placement = random.choice(ychoices)  # Randomly decide the starting vertical position
        # Spawn bats moving upwards or downwards based on placement and set the direction and speed
        if placement < 0:
            batsie = FlyingBat(canvas=gamecanvas, xspeed=random.choice([3, -3, -4, 4]), yspeed=random.choice([3, 4]), ydir=Direction.DOWN)
        elif placement > 0:
            batsie = FlyingBat(canvas=gamecanvas, xspeed=random.choice([3, -3, -4, 4]), yspeed=random.choice([-3, -4]), ydir=Direction.UP)
        # Set the bat's horizontal position randomly within the canvas width
        batsie.y = placement
        batsie.x = random.randint(0, (gamecanvas.winfo_reqwidth() - (batsie.getWidth())))
        bats.append(batsie)  # Add the new bat to the active bats list
        print(f"There are {len(bats)} bats")  # Debugging test 
    batspawnerTimer = gamecanvas.after(batsinterval, batspawn)  # Schedule the next spawn event every few seconds for bats

def enableattack():
    # Reset the wolf attack cooldown, allowing wolves to attack the player again.
    global wolfhithim
    wolfhithim = False

def enableattackBat():
    # Reset the bat attack cooldown, allowing bats to attack the player again.
    global bathithim
    bathithim = False

    
def WinGame():
    # Handles the logic for when the player wins the game.
    global startgame, playercollideID, wizard
    startgame = False  # Stop the game loop

    # Remove all wolves and bats from the canvas
    for wolf in wolves:
        wolf.kill()
    for bat in bats:
        bat.kill()

    # Cancel all active timers based on the total shards collected to avoid errors
    if thetotalshards >= 0 and thetotalshards < 7:
        gamecanvas.after_cancel(playercollideID)
        gamecanvas.after_cancel(bulletsmovetimer)
        gamecanvas.after_cancel(wolfspawnerID)
        gamecanvas.after_cancel(playermoverID)
        gamecanvas.after_cancel(shardspawnerID)
    elif thetotalshards < 14:
        gamecanvas.after_cancel(playercollideID)
        gamecanvas.after_cancel(bulletsmovetimer)
        gamecanvas.after_cancel(wolfspawnerID)
        gamecanvas.after_cancel(batsmoverID) 
        gamecanvas.after_cancel(shardspawnerID)
        gamecanvas.after_cancel(playermoverID)
        gamecanvas.after_cancel(batspawnerTimer)
    elif thetotalshards >= 14:
        gamecanvas.after_cancel(healthspawnintID)   
        gamecanvas.after_cancel(OrbTimerShootID) 
        gamecanvas.after_cancel(batsmoverID) 
        gamecanvas.after_cancel(wizardspawnerID) 
        gamecanvas.after_cancel(bulletsmovetimer) 
        gamecanvas.after_cancel(playermoverID)
        gamecanvas.after_cancel(wolfspawnerID) 
        gamecanvas.after_cancel(batspawnerTimer)  
        gamecanvas.after_cancel(shardspawnerID) 
        gamecanvas.after_cancel(playercollideID)  

        # Delete all wizards
        for wizar in wizard:
            wizar.deleteWizard()
        wizard = []

    # Display a message box to ask the player if they want to save their high score
    answer = messagebox.askyesno("Icy Guardian", "CONGRATULATIONS! You Have Collected all 21 Ice Shards!\n The Time Machine is now ready! ESCAPE!\nDo you want to save your HighScore?")
    if answer == True:
        saveit() # save it if yes
        messagebox.showinfo ("SAVED!", "Your HighScore will be visible upon loading the game again!")
    elif answer == False:
        exit() # exit the game if no
    exit()
    

def playerhitter():
    # Detects collisions between the player and all of the game entities, like the power-up, shards, wolves, bats, and orbs.
    global playercollideID, wolfonmap, batonmap, healthspawninterval, healthlist, batsinterval, ShardsOnMap, wolves, wolfhithim, healthtracker, startgame, bathithim, heartsonmap, thetotalshards, orbsspawninterval, lowtaperfade, wolfinterval
    # Check for collisions with health power-ups
    for powerup in healthlist:  # Iterate over all active health power-ups
        if (Timmy.right - 35) > (powerup.x) and (Timmy.x + 23) < (powerup.right) and (Timmy.y + 5) < (powerup.bottom) and (Timmy.bottom - 2) > (powerup.y + 5):
            healthtracker += 1  # Cap health at 3
            if healthtracker >= 4 or healthtracker == 3:
                healthtracker = 3
                powerup.healthremove()
            Timmy.setHealth(healthtracker)  # Update health display
            powerup.healthremove()  # Remove power-up from canvas
            healthlist.remove(powerup)  # Remove from active list
            heartsonmap -= 1  # Decrease active power-up count
            break  # Stop checking further collisions
        # check for collisions with shards, and if there is collision, 
    for shard in shards:
        if (Timmy.right - 35) > (shard.x + 12) and (Timmy.x + 23) < (shard.right - 17) and (Timmy.y + 5) < (shard.bottom - 5) and (Timmy.bottom - 2) > (shard.y + 5):
            shards.remove(shard) # remove the shard
            ShardsOnMap = ShardsOnMap - 1 # decrease the number of shards active on the map
            shard.shardremove()
            thetotalshards += 1 # the total number of shards collected
            # Trigger different game events based on shards collected
            if thetotalshards == 7:
                # spawn bats now, move the enemies, and make the mobs spawn faster
                batspawn()
                enemyMover()
                wolfonmap = 6
                healthspawninterval = 12000
                wolfinterval = 2700
            elif thetotalshards == 14:
                # spawn wizards now, move the enemies, and make the mobs spawn faster, and make the game harder
                spawnwizard()
                wolfinterval = 4000
                wolfonmap = 4
                batonmap = 3
                healthspawninterval = 4000
                batsinterval = 3000
            # if there are 21 shards collected, the game has been won, and show the wingame message and function
            elif thetotalshards >= 21:
                WinGame()
            # change the total number of shards collected so far every time
            gamecanvas.itemconfig(lowtaperfade, text=f'Shards Collected: {thetotalshards}')
            pygame.mixer.Sound.play(icecollectsound) # play a collection sound
    # for every wolf, check for detection, and set the attack animation to begin
    for wolf in wolves:
        if (Timmy.right - 35) > (wolf.x + 75) and (Timmy.x + 23) < (wolf.right - 90) and (Timmy.y + 5) < (wolf.bottom - 70) and (Timmy.bottom - 2) > (wolf.y + (wolf.height // 2) + 15):
            if wolfhithim == False:
                wolf.setIndex(0)
                wolf.attack() # attack animation
                healthtracker = healthtracker - 1 # damage the player
                Timmy.health = healthtracker # Timmy's health is now this value
                pygame.mixer.Sound.play(playerhitsound) # play the player being hit sound
                # if the health is 0, end the game
                if healthtracker == 0:
                    endthegame()
                    startgame = False
                    gamecanvas.after_cancel(playercollideID)
                    return
                wolfattackpausetimer = gamecanvas.after(1500, enableattack) #the wolf attack delay timer
            wolfhithim = True
        # check for player-bat collision detection
    for bat in bats:
        if (Timmy.right - 35) > (bat.x + 15) and (Timmy.x + 23) < (bat.right - 15) and (Timmy.y + 5) < (bat.bottom - 20) and (Timmy.bottom - 2) > (bat.y + 15):
            if bathithim == False:
                # if the bat was hit, show the attack animation and take away a heart
                bat.setIndex(0)
                bat.setFollow(False)
                bat.attack()
                healthtracker = healthtracker - 1
                Timmy.health = healthtracker
                pygame.mixer.Sound.play(playerhitsound)
                # if the player is dead, then end the game
                if healthtracker == 0:
                    endthegame()
                    startgame = False
                    gamecanvas.after_cancel(playercollideID)
                    return
                # the bee attack delay timer
                batattackpausetimer = gamecanvas.after(1500, enableattackBat)
            bathithim = True
    # for each orb in the active orbs
    for orb in active_orbs:
        if (Timmy.right - 35) > (orb.x) and (Timmy.x + 23) < (orb.right) and (Timmy.y + 5) < (orb.bottom) and (Timmy.bottom - 2) > (orb.y):
            orb.remove() # remove the orb from the list
            active_orbs.remove(orb)
            healthtracker = healthtracker - 1 # deduct a heart
            Timmy.health = healthtracker
            pygame.mixer.Sound.play(playerhitsound)
            # kill the player and then end the game if the player dies
            if healthtracker == 0:
                endthegame()
                startgame = False
                gamecanvas.after_cancel(playercollideID)
                return
    # restart the playercollision timer every ten seconds
    if startgame == True:
        playercollideID = gamecanvas.after(10, playerhitter)

# end the game function to end the game
def endthegame():
    global startgame, playercollideID, Timmy, wizard
    # code the game over text on screen
    GameOverTextID = gamecanvas.create_text(gamecanvas.winfo_reqwidth() // 2, gamecanvas.winfo_reqheight() * 0.4, text='GAME OVER, YOU DIED', font=('Christmas Shaky', 100), fill='#547820')
    # depending on the total number of shards collected, cancel the adequate timers    
    try: 
        if thetotalshards >= 0 and thetotalshards < 7:
            gamecanvas.after_cancel(playercollideID)
            gamecanvas.after_cancel(bulletsmovetimer)
            gamecanvas.after_cancel(wolfspawnerID)
            gamecanvas.after_cancel(playermoverID)
            gamecanvas.after_cancel(shardspawnerID)
        elif thetotalshards < 14: # if 14 shards or less are collected, cancel the timers
            gamecanvas.after_cancel(playercollideID)
            gamecanvas.after_cancel(bulletsmovetimer)
            gamecanvas.after_cancel(wolfspawnerID)
            gamecanvas.after_cancel(batsmoverID) 
            gamecanvas.after_cancel(shardspawnerID)
            gamecanvas.after_cancel(playermoverID)
            gamecanvas.after_cancel(batspawnerTimer)
        elif thetotalshards >= 14: # if 14 shards or less are collected, cancel the timers
            gamecanvas.after_cancel(healthspawnintID)   
            gamecanvas.after_cancel(OrbTimerShootID) 
            gamecanvas.after_cancel(batsmoverID) 
            gamecanvas.after_cancel(wizardspawnerID) 
            gamecanvas.after_cancel(bulletsmovetimer) 
            gamecanvas.after_cancel(playermoverID)
            gamecanvas.after_cancel(wolfspawnerID) 
            gamecanvas.after_cancel(batspawnerTimer)  
            gamecanvas.after_cancel(shardspawnerID) 
            gamecanvas.after_cancel(playercollideID)  
            for wizar in wizard:
                wizar.endTimers()
    except:
        exit()
    # kill the player and make it unable to move him
    Timmy.setIndex(0)
    Timmy.kill()
    Timmy.endtimer()
    startgame = False
    for wolf in wolves:
        wolf.endtimer()
    # ask the user if they want to quit and save or not and save it
    answer = messagebox.askyesno("Icy Guardian", "You DIED!!!\nDo you want to save your HighScore?")
    if answer == True:
        saveit()
        messagebox.showinfo ("SAVED!", "Your HighScore will be visible upon loading the game again!")
    elif answer == False:
        exit() #  exit the program
    exit()
    
# make the variable that spawns shards on the map
def spawnshards():
    global ShardsOnMap, shardspawnerID
    # if there are more than 4 shards, dont spawn any more
    if ShardsOnMap < 3:
        # hover the shards and spawn them
        shardsp = (IceShard(canvas=gamecanvas, xPos = random.randint(40,1085), yPos = random.randint(35, 585)))
        shardsp.hover(ground=shardsp.bottom)
        #shardrect = gamecanvas.create_rectangle(shardsp.x + 12, shardsp.y + 5, shardsp.right - 17, shardsp.bottom - 5)
        ShardsOnMap += 1 # add one more to the counter
        shards.append(shardsp)
        # spawn one every four seconds
    shardspawnerID = gamecanvas.after(4000, spawnshards)

# make the close option message box function. Code the exit button using an exit function
def close_option():
    answer = messagebox.askyesno("Icy Guardian", "Are you sure you want to exit?")
    if answer == True: # if the user does want to exit, let them exit
        # if they do want to exit, then ask them if they want to save their changes on their way out
        exit()
# make a function that brings back the main window after you X out of the start window
def close_startwindow():
    start_window.withdraw()
    root.deiconify()

# initialize the main window for tkinter
root = Tk()
root.title("Icy Guardian")
gamebg = ImageTk.PhotoImage(Image.open('background.png'))
# position the window on the screen
root.geometry(f'{gamebg.width()}x{gamebg.height()}+{(root.winfo_screenwidth() - gamebg.width()) // 2}+{(root.winfo_screenheight() - gamebg.height()) // 2}')
root.iconphoto(False, PhotoImage(file = 'images_misc/Ice_Shard.png'))
# declare the canvas on the Tk() window and create the background image
gamecanvas = Canvas(root, width=gamebg.width(), height=gamebg.height())
gamecanvas.pack()
gamecanvas.create_image(0,0,image=gamebg, anchor='nw')

# make the parameter code for the start window
START_WINDOW_WIDTH, START_WINDOW_HEIGHT = 550, 200
start_window = Toplevel(padx=10, pady=10, background='#88e3f3')
start_window.title('Icy Guardian Homepage')
start_window.resizable(False, False)
start_window.protocol('WM_DELETE_WINDOW', close_option) # set a protocol for closing the window
start_window.geometry(f'{START_WINDOW_WIDTH}x{START_WINDOW_HEIGHT}+{(root.winfo_screenwidth() - START_WINDOW_WIDTH) // 2}+{(root.winfo_screenheight() - START_WINDOW_HEIGHT) // 2}')
# initially withdraw the main window and show the homepage
start_window.deiconify()
root.withdraw()

keys = {'d': False, 'a': False, 'w': False, 's': False}  # Tracks key states in a dictionary

#initialize all pygame music and sound effect components
pygame.mixer.init()
icecollectsound = pygame.mixer.Sound("LedasLuzta.ogg")
playerhitsound = pygame.mixer.Sound("audio/dmgtaken.wav")
pygame.mixer.music.load("audio/Doom.ogg")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)
root.protocol("WM_DELETE_WINDOW", close_option) # set the close option to the window

# make two lists for the west and east running images and store them in a list
eastimages, westimages = [], []
for counter in range(10):
    eastimages.append(ImageTk.PhotoImage(Image.open(f'Hero-Guy-PNG/_Mode-Gun/02-Run/JK_P_Gun__Run_00{counter}.png')))
    westimages.append(ImageTk.PhotoImage(Image.open(f'Hero-Guy-PNG/_Mode-Gun/02-RunWest/JK_P_Gun__Run_00{counter}.png')))
    
''' 
This is the code for initializing all of the game variables!!
'''
wizardchoices = [12, 233, 454] # wizard y choices
playercollideID = None # player collision timer ID
totalkeystotal = 0 #declare the variable counter for clicking the keys for player movement
orbcanAttack = True # boolean for attack orb delay
wizzsidecounter = 0 # either 1 or 2; which side will the wizard be
# the spawn interval variables that will be changed
healthspawninterval = 15000
batsinterval = 2800
wolfinterval = 1000
bulletsfired = False # varaible for checking if bullets are fired or not
startgame = True # determine if the game can start yet
healthtracker = 3 # tracker variable for health amount
ShardsOnMap = 0 # shard tracker variable
orbsspawninterval = 400 # specify the interval that orbs spawn on to the map
wizardcounter = 0 # wizard counter
wizardchoices = [12, 233, 454] # choices for wizard y values
# variables for amount of each mob and heart on the map
wolfonmap = 7
batonmap = 5
heartsonmap = 0
canshoot = True # boolean for delay of player shooting
bulletsmovetimer = None # bullets timer ID
totalscore = 0
# animal attack delay variables
wolfhithim = False
bathithim = False
# declare all lists to store projectiles and mob enemies, and IDs
bats = [] 
wolves = []
wizard = []
shards = []
healthlist = []
bullets = []
active_orbs = []
batspawnerTimer = None # bat timer ID
# declare the shards counter variable and all of the sorting variables
thetotalshards = 0
counter1, counter2, counter3 = 0, 0, 0

# this is the sorting function to sort in ascending or descending order
def sort_columns(columnID):
    global counter1, counter2, allnames
    # if the first column was clicked (last name column)
    if columnID == 1:
        # initialize the other sort variables back to 0 to reset the ascending order
        counter2 = 0
        
        # if the sort counter is 0, sort the last names in ascending order
        if counter1 == 0:
            sortedload = sorted(allnames, key=lambda x: x['Name'])
            counter1 += 1
        # if the sort counter is 1, sort the last names in descending order
        elif counter1 == 1:
            sortedload = sorted(allnames, key=lambda x: x['Name'], reverse=True)
            counter1 = 0
    elif columnID == 2: # if the second column was clicked (sorting by seatletters)
        # initialize the other sort variables back to 0 to reset the ascending order
        counter1 = 0
        # if the sort counter is 0, sort the seatletters in ascending order
        if counter2 == 0:
            sortedload = sorted(allnames, key=lambda x: int(x['Score']))
            counter2 += 1
        # if the sort counter is 1, sort the seatletters in descending order
        elif counter2 == 1:
            sortedload = sorted(allnames, key=lambda x: int(x['Score']), reverse=True)
            counter2 = 0
     # for every player's in the new loads, sort them according to the allnames list
    for stats in allnames:
        tview_scoreboard.delete(stats['IID'])
    # for every player in the now sorted list, sort them accordingly in the treeview widget simply by outputting the new list
    for stats in sortedload:
        tview_scoreboard.insert('', END, iid=stats['IID'], values=((stats['Name']), (stats['Score'])))
        
# make a function that brings back the main window after you X out of the score Treeview window
def close_score():
    start_window.deiconify()
    scoreboard.withdraw()
    
# variable to store all scores
allnames = []

# view the scoreboard upon clicking the view button
def view_scoreboard():
    global allnames
    start_window.withdraw()
    scoreboard.deiconify()
    root.withdraw()
filename = f'scores.txt'

#the save it function to save high scores to the scores.txt files
def saveit():
    filename = 'scores.txt'
    with open(filename, 'at') as writer:
        writer.write(txtFirst.get() + ', ' + f'{totalscore}' + ', ' + f'{int(len(allnames)) + 1}' + '\n')

# set the score window parameters
SCORE_WIDTH, SCORE_HEIGHT = 390, 490 # set the dimensions of the score window
scoreboard = Toplevel(padx=10, pady=10, bg='#88E3F3')
# set the other parameters of the score window to pretiffy it and originally withdraw it
scoreboard.title('Scoreboard')
scoreboard.resizable(False, False)
scoreboard.protocol('WM_DELETE_WINDOW', close_score)
scoreboard.geometry(f'{SCORE_WIDTH}x{SCORE_WIDTH}+{(root.winfo_screenwidth() - SCORE_WIDTH) // 2}+{(root.winfo_screenheight() - SCORE_HEIGHT) // 2}')
scoreboard.withdraw()

# set the treeview headings and columns
tview_scoreboard = ttk.Treeview(scoreboard, selectmode='browse', columns=('1', '2'), show='headings', height=20, style='mystyle.Treeview')
tview_scoreboard.grid(row=1, column=0, pady=5)
# style the treeview widget
style = ttk.Style()
style.configure('mystyle.Treeview.Heading', font=('Calibri', 10, 'bold'), bg='#88E3F3')
style.configure('mystyle.Treeview', font=('Calibri', 11))

# set the scoreboard headings
scoreboard_headings = ('NAME', 'HIGHSCORE')
columnwidths = [250, 100]
# set the column and headings for each column and set it for the treeview widget, and pass the function to the clicks
for i in range(2):
    tview_scoreboard.column(str(i+1), width=columnwidths[i], anchor='w')
    tview_scoreboard.heading(str(i+1), text=scoreboard_headings[i], anchor='w', command=lambda columnid=i + 1: sort_columns(columnid))
# set the scrollbar for the scoreboard
vscroll_scoreboard = Scrollbar(scoreboard, orient='vertical', command=tview_scoreboard.yview)
vscroll_scoreboard.grid(row=1, column=1, sticky='ns')

#Load Timmy the Hero into the game, and center him on the canvas, as well as load the shards collected number ID
Timmy = Hero(canvas = gamecanvas, eastimages=eastimages, westimages=westimages)
Timmy.x = gamecanvas.winfo_reqwidth() // 2 - 50
Timmy.y =  gamecanvas.winfo_reqheight() // 2 - 50

# shards collected output ID
lowtaperfade = gamecanvas.create_text(20 , 4, font=('Stoneyard', 20), fill='#547820', anchor='nw', text=f'Shards Collected: 0')
# highscore output ID
totalscoreID = gamecanvas.create_text(275 , 4, font=('Stoneyard', 20), fill='#547820', anchor='nw', text=f'SCORE: 0')

# image for the Ice Shard information loading and gridding
imgInfo = Image.open('images_misc/Ice_ShardCOPY.png')
imgInfo1 = ImageTk.PhotoImage(imgInfo.resize((int(imgInfo.width * 0.8), int(imgInfo.height * 0.8)), Image.Resampling.LANCZOS))
# label info initializing and gridding
lblInfo1 = Label(start_window, image=imgInfo1, background='#88E3F3')
lblInfo1.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
# make more labels and grid them
lblFirst = Label(start_window, text='GAMER NAME:', font=font.Font(family='Century Gothic', size=10), width=15, anchor='w', bg='#88e3f3')
lblFirst.grid(row=0, column=1, padx=5, pady=5)
# make the first name entry widget and grid it to the start window
txtFirst = Entry(start_window, font=font.Font(family='Century Gothic', size=10), justify='center', width=25)
txtFirst.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
# make the purhcase button frame for the topview widget
startbuttonsFrame = Frame(start_window, pady=10, bg='#88e3f3')
# make an Ok button and give it the respective command
btnSTART = Button(startbuttonsFrame, text='START', width=10, font=font.Font(family='Century Gothic', size=10), command=checker)
btnSTART.pack(side='left', padx=5)
# make a Clear button and give it the respective command
btnScoreboard = Button(startbuttonsFrame, text='SCOREBOARD', width=15, pady=5, font=font.Font(family='Calibri', size=10, weight='bold'), command=view_scoreboard)
btnScoreboard.pack(side='left', padx=5)
# make a Cancel button and give it the respective command
btnExit = Button(startbuttonsFrame, text='EXIT', width=10, font=font.Font(family='Century Gothic', size=10), command=close_option)
btnExit.pack(side='left', padx=5)
# grid the purchase button frame to the topview widget
startbuttonsFrame.grid(row=1, column=1, columnspan=3)

# the possible choices to choose from for spawing mobs
choices = [-100, gamecanvas.winfo_reqwidth() + 150]
ychoices = [-100, gamecanvas.winfo_reqheight() + 150]

# open the scores file to set the scoreboard treeview
with open(filename, 'r') as reader:
        # init the line
        line = reader.readline().strip('\n').split(',')
        # append all the info to a line var, and then to a dictionnary
        while line != [''] and line != ['\n']:
            original_message = line
            allnames.append({'Name':line[0], 'Score':line[1], 'IID':line[2]})
            line = reader.readline().strip('\n').split(',')
        # for all stats in the dict list, insert it into the treeview
        for stats in allnames:
            # insert the player's information into the treeview object
            tview_scoreboard.insert('', END, iid=stats['IID'], values=(f'{stats["Name"]}', (stats["Score"])))
            
            
# add custom font files with pyglet
pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file('fonts/Christmas_Shaky.ttf')
pyglet.font.add_file('fonts/Stoneyard.ttf')

#bind all mouse AND KEYBOARD EVENTS to the canvas and window
root.bind('<KeyPress>', onkeypress)
root.bind('<ButtonPress>', onbuttonpress)
root.bind('<KeyRelease>', onkeyrelease)

#mainloop the window to keep it going

root.mainloop()
