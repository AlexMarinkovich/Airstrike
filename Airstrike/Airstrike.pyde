# READ THIS ########################################################
# game coded by Alexander Marinkovich
# game inspired by "Heavy Weapon"
# version 1.0 - June 16, 2020.
# 1600+ lines

# gameplay features include:
# * 13 unique plane types with custom images
# * realistic physics properties for some weapon types including: gravity acceleration, heat seeking, cluster explosion, aiming trigonometry formulas
# * collision detection using algorithms
# * tank with 4 different types of unique upgrades - spreadshot, firing speed, movement speed, extra live
# * tank can move left and right with keys w and a, and the tank's gun is controlled with the mouse
# * tank ability to nuke all enemies on screen with key s
# * animations including: plane explosions, shadows, nuclear explosions, upgrade notifications during gameplay
# * progression system - planes spawn faster and plane types become harder as time goes on
# * scoreboard with score, lives left, elapsed time, number of nukes, planes destroyed
# * pause feature with spacebar to go for bio breaks

# other features:
# * how to play section, which includes controls and scoreboard explanation
# * hangar - describes all planes and their capabilities
# * game over screen with gameplay statistics

# developer features:
# * adjustable start time
# * toggleable hitboxes to confirm collisions
# * variable based plane configuration (for designing new planes)
# * adjustable weapon upgrades using variable values
# * lists to show all tank bullets, planes, and plane bullets on the screen, which has all their properties including screen position, hp, and more
# * all images for planes, the tank, and titles, as well as fonts are stored in the data folder

# developer notes:
# * tried out the sound library from processing, but there's a known bug that causes sound failure and sound not to play after first run of program, so sound not included in this version (bug from python processing)
# * future features - highscore saving, mission mode (different from survival mode), standalone executable, mobile version

# GLOBAL VARIABLES #######################################

import math
import random

# mode
mode = "menu"

# debugging
hitboxes = False
game_time = 0 # in seconds

# tank
tank_length = 80
tank_height = 60
tank_x = 600
tank_y = 670
floor_y = 700
tank_hp = 5

# tank upgradables
tank_dx = 6
spreadshot = 1
shoot_time = 8 # number of frames in between each shot (adjustable)
upgrade_type = None # used for announcement of an upgrade
upgrade_delay = 300 # used for announcement of an upgrade

# gun
gun_length = 40
gun_x = tank_x
gun_y = tank_y - 25
gun_rotation = 0

# gun bullets
bullets = [] # [x, y, angle]
bullet_diameter = 10
bullet_speed = 15
shoot_delay = shoot_time # counts frames after each shot

# planes
planes = [] # [x, y, x_movement, y_movement, plane_length, plane_height, plane_shoot_delay, plane_shoot_time, plane_hp, plane_color, plane_type, plane_bullet_color, plane_bullet_hp, plane_score]  
plane_spawn_time = 60 # number of frames in between each plane spawning, adjustable in gametime()
plane_spawn_delay = plane_spawn_time # counts frames after each plane spawning
plane_explosions = [] # [x, y, plane explosion delay, plane explosion length, plane explosion height]

# plane bullets
plane_bullets = [] # [x, y, x_movement, y_movement, plane_bullet_diameter, plane_bullet_color, plane_bullet_hp]
nuker_explosions = [] # [x, y, nuker explosion delay]

# nukes
nukes = 0
nuke_chance = 100 # 1 / nuke_chance to get nuke from plane, increases by 50 each time you get a nuke
nuke_delay = 0 # counts frames before you can nuke again
obtain_nuke_delay = 0 # counts frames for the announcement of obtaining a nuke

# game data
counter = 0 # counts frames for game_time
respawn_delay = 0 # counts frames before respawning
score = 0
lives = 2
planes_destroyed = 0
planes_escaped = 0

# hangar
plane_list_number = 0

# how to play
how_to_play_page = 1

# key presses
key_a = False
key_d = False
key_s = False

# SETUP FUNCTIONS #######################################
def setup():
    global impact_font, arial_font, comicsans_font, remaining_tanks, remaining_nukes, airstrike_title, how_to_play_title, hangar_title, game_background, planes_destroyed_image, tank_image, nuker_bullet
    global fly_by_image, fly_by_image_reverse, bomber_image, bomber_image_reverse, armored_bomber_image, armored_bomber_image_reverse, carpet_bomber_image, carpet_bomber_image_reverse, armored_carpet_bomber_image, armored_carpet_bomber_image_reverse
    global heat_seeker_image, heat_seeker_image_reverse, downrush_image, cluster_bomber_image, cluster_bomber_image_reverse, rammer_image, rammer_reverse_image, rammer_downwards_image
    global nuker_image, nuker_reverse_image, minigun_image, minigun_reverse_image, railgun_image, railgun_reverse_image
    
    # screen
    size(1200,750)
    frameRate(60)
    
    # fonts
    impact_font = loadFont("Impact.vlw")
    arial_font = loadFont("Arial.vlw")
    comicsans_font = loadFont("ComicSans.vlw")
    
    # scoreboard
    remaining_tanks = loadImage("TanksRemaining.png")
    remaining_nukes = loadImage("NukesRemaining.png")
    planes_destroyed_image = loadImage("PlanesDestroyed.png")
    
    # titles
    airstrike_title = loadImage("AirstrikeTitle.png")
    how_to_play_title = loadImage("HowToPlayTitle.png")
    hangar_title = loadImage("HangarTitle.png")
    
    # background
    game_background = loadImage("GameBackground.png")
    
    # tank and planes
    tank_image = loadImage("Tank.png")
    fly_by_image = loadImage("FlyBy.png")
    fly_by_image_reverse = loadImage("FlyByReverse.png")
    bomber_image = loadImage("Bomber.png")
    bomber_image_reverse = loadImage("BomberReverse.png")
    armored_bomber_image = loadImage("ArmoredBomber.png")
    armored_bomber_image_reverse = loadImage("ArmoredBomberReverse.png")
    carpet_bomber_image = loadImage("CarpetBomber.png")
    carpet_bomber_image_reverse = loadImage("CarpetBomberReverse.png")
    armored_carpet_bomber_image = loadImage("ArmoredCarpetBomber.png")
    armored_carpet_bomber_image_reverse = loadImage("ArmoredCarpetBomberReverse.png")
    heat_seeker_image = loadImage("HeatSeeker.png")
    heat_seeker_image_reverse = loadImage("HeatSeekerReverse.png")
    downrush_image = loadImage("Downrush.png")
    cluster_bomber_image = loadImage("ClusterBomber.png")
    cluster_bomber_image_reverse = loadImage("ClusterBomberReverse.png")
    rammer_image = loadImage("Rammer.png")
    rammer_reverse_image = loadImage("RammerReverse.png")
    rammer_downwards_image = loadImage("RammerDownwards.png")
    nuker_image = loadImage("Nuker.png")
    nuker_reverse_image = loadImage("NukerReverse.png")
    nuker_bullet = loadImage("NukerBullet.png")
    minigun_image = loadImage("Minigun.png")
    minigun_reverse_image = loadImage("MinigunReverse.png")
    railgun_image = loadImage("Railgun.png")
    railgun_reverse_image = loadImage("RailgunReverse.png")
    
def draw():
    background(100,183,255)
    if mode == "play" or mode == "gameover" or mode == "pause":
        drawbackground()
        drawtank()
        if mode != "pause":
            movetank()
            calcbullets()
            calcplanes()
            calcplanebullets()
        nukerexplosions()
        planeexplosions()
        drawbullets()        
        drawplanes()
        drawplanebullets()
        if mode != "pause":
            movebullets()
            moveplanes()
            moveplanebullets()
        hitboxtank()
        hitboxplanes()
        hitboxplanebullets()
        hitboxfloor()
        outofbounds()
        obtainnuke()
        nuke()
        respawntank()
        gametime()
        upgrades()
        scoreboard()
    if mode == "play":
        crosshair()
    if mode == "pause":
        pausescreen()
    if mode == "gameover":
        gameoverscreen()
    if mode == "menu":
        menuscreen()
    if mode == "howtoplay":
        howtoplayscreen()
    if mode == "hangar":
        hangarscreen()
    
def keyPressed():
    global mode
    presskey()
    
    # spacebar alternates between play and pause modes
    if mode == "play" and key == " ":
        mode = "pause"
    elif mode == "pause" and key == " ":
        mode = "play"
    
def keyReleased():
    releasekey()

def mousePressed():
    global mode, counter, respawn_delay, game_time, tank_hp, lives, score, nukes, nuke_chance, planes_destroyed, tank_x, tank_y, bullets, planes, plane_bullets, plane_list_number, floor_y, how_to_play_page
    
    #print mouseX, mouseY
    
    if mode == "pause":
        # resume button
        if mouseX >= 400 and mouseX <= 800 and mouseY >= 300 and mouseY <= 380:
            mode = "play"  
        
        # menu button
        elif mouseX >= 400 and mouseX <= 800 and mouseY >= 450 and mouseY <= 530:
            # removes all bullets, planes, and plane bullets
            bullets = []
            planes = []
            plane_bullets = []
            mode = "menu"
    
    elif mode == "gameover":
        # menu button
        if mouseX >= 400 and mouseX <= 800 and mouseY >= 550 and mouseY <= 630:
            # removes all bullets, planes, and plane bullets
            bullets = []
            planes = []
            plane_bullets = []
            mode = "menu"
            
    elif mode == "menu":
        # play button
        if (sqrt((mouseX - 600)**2 + (mouseY - 400)**2)) <= 110:
            mode = "play"
            # resets game variables
            counter = 0
            respawn_delay = 0
            tank_hp = 5
            score = 0
            lives = 2
            game_time = 0
            nukes = 0
            nuke_chance = 100
            planes_destroyed = 0
            tank_x = 600
            tank_y = 670
            floor_y = 700
            
        # hangar button
        elif (sqrt((mouseX - 600)**2 + (mouseY - 650)**2)) <= 75:
            mode = "hangar"
            floor_y = 550
            
        # how to play button
        elif (sqrt((mouseX - 300)**2 + (mouseY - 600)**2)) <= 75:
            mode = "howtoplay"
    
        # quit game button
        elif (sqrt((mouseX - 900)**2 + (mouseY - 600)**2)) <= 75:
            exit()
    
    elif mode == "howtoplay":
        # got it button
        if (sqrt((mouseX - 600)**2 + (mouseY - 650)**2)) <= 75:
            mode = "menu"
            how_to_play_page = 1
        
        # right arrow and left arrow button
        if (sqrt((mouseX - 800)**2 + (mouseY - 650)**2)) <= 50 or (sqrt((mouseX - 400)**2 + (mouseY - 650)**2)) <= 50:
            if how_to_play_page == 1:
                how_to_play_page = 2
            elif how_to_play_page == 2:
                how_to_play_page = 1
            
    elif mode == "hangar":
        # menu button
        if (sqrt((mouseX - 600)**2 + (mouseY - 650)**2)) <= 75:
            mode = "menu"
            plane_list_number = 0
            planes = []
            plane_bullets = []
            
        # right arrow button
        elif (sqrt((mouseX - 800)**2 + (mouseY - 650)**2)) <= 50:
            if plane_list_number != 12:
                plane_list_number += 1
            elif plane_list_number == 12:
                plane_list_number = 0
            planes = []    
        
        # left arrow button
        elif (sqrt((mouseX - 400)**2 + (mouseY - 650)**2)) <= 50:    
            if plane_list_number != 0:
                plane_list_number -= 1
            elif plane_list_number == 0:
                plane_list_number = 12
            planes = []  
        

# FUNCTIONS #######################################

def crosshair():
    noCursor()
    stroke(255,0,0,200)
    strokeWeight(2)
    line(mouseX-10, mouseY, mouseX+10, mouseY)
    line(mouseX, mouseY-10, mouseX, mouseY+10)

def drawbackground():
    image(game_background,0,0)

def drawtank():
    global gun_rotation, gun_x, gun_y
    
    # gun location
    pushMatrix()
    gun_x = tank_x
    gun_y = tank_y - (tank_height/2)
    
    # gun rotation
    translate(gun_x, gun_y)
    if mouseY < gun_y:
        gun_rotation = (atan((mouseX-gun_x) / (float(gun_y-mouseY))))
    if mode == "play":
        rotate(gun_rotation)
    
    # gun design
    stroke(0)
    strokeWeight(6)
    line(0, 0, 0, -gun_length)
    strokeWeight(1)
    popMatrix()
        
    # body
    stroke(0,0)
    fill(0,50)
    ellipse(tank_x, tank_y+25,75,20) # tank shadow
    image(tank_image, tank_x - 39, tank_y - 40) # tank design
    fill(0,255,0)
    textFont(comicsans_font)
    textSize(20)
    textAlign(CENTER,CENTER)
    text(tank_hp, tank_x, tank_y-15)
    
    
    if hitboxes == True:
        stroke(0)
        fill(0,0)
        rect(tank_x - tank_length/2, tank_y - tank_height/2, tank_length, tank_height)
        ellipse(tank_x, tank_y, 1, 1)
        line(0,floor_y,width,floor_y)
    
def movetank():
    global tank_x
    
    if key_a == True and tank_x > tank_length/2 + 20:
        tank_x -= tank_dx
    if key_d == True and tank_x < width - tank_length/2 - 20:
        tank_x += tank_dx

def respawntank():
    global lives, tank_hp, tank_x, tank_y, respawn_delay, plane_spawn_delay, mode
    
    if tank_hp <= 0:
        tank_y = 1500 # off the screen
        if mode == "play":
            respawn_delay += 1 
        
        if respawn_delay == 1:
            # creates explosion for tank
            plane_explosions.append([tank_x, 670, -10, 300, 300]) # [x, y, explosion delay, explosion length, explosion height]
            
        if lives > 0:
            plane_spawn_delay = 60
            
            if respawn_delay == 30:
                for plane in planes:
                    plane[2] *= 10    
                
            if respawn_delay >= 60 and respawn_delay <= 180:
                textFont(impact_font)
                textAlign(CENTER,CENTER)
                textSize(80)
                fill(0)
                text("Get Ready!", 605, 355) # black shadow of text
                fill(0xffFFBB00)
                text("Get Ready!", 600, 350) # orange text
                
            if respawn_delay >= 180 and len(planes) == 0 and len(plane_bullets) == 0:
                lives -= 1
                tank_hp = 5
                tank_x = 600
                tank_y = 670
                respawn_delay = 0
        
        elif lives <= 0:
            if respawn_delay < 240:
                textFont(impact_font)
                textAlign(CENTER,CENTER)
                textSize(80)
                fill(0)
                text("Game Over!", 605, 355) # black shadow of text
                fill(0xffFFBB00)
                text("Game Over!", 600, 350) # orange text
            
            if respawn_delay == 240:
                mode = "gameover"
                
def calcbullets():
    global shoot_delay
    
    shoot_delay -= 1 # counts down shoot_delay for each frame
    if mousePressed:
        if shoot_delay <= 0 and tank_y < 800: # when shoot_delay is 0 (or less), gun can shoot again    
            
            # calculates spreadshot bullets
            for n in range(spreadshot): 
                if n % 2 == 0:
                    n = n * -1
                n = (n+1)/2
                
                # creates bullets
                bullets.append([gun_x - gun_length * cos(gun_rotation + (90 * PI / 180)), # [x, y, angle]
                            gun_y - gun_length * sin(gun_rotation + (90 * PI / 180)),
                            gun_rotation + ((270+5*n)*PI/180)]) 
            
            shoot_delay = shoot_time # resets shoot_delay after each shot
    
def drawbullets():
    for bullet in bullets:
        # bullet design
        fill(255)
        stroke(255,0,0)
        strokeWeight(2)
        ellipse(bullet[0], bullet[1], bullet_diameter, bullet_diameter)

def movebullets():    
    for bullet in bullets:
        bullet[0] += (cos(bullet[2])) * bullet_speed
        bullet[1] += (sin(bullet[2])) * bullet_speed

def obtainnuke():
    global nukes, obtain_nuke_delay, nuke_chance
    
    if obtain_nuke_delay > 0:
        if mode == "play":
            obtain_nuke_delay -= 1
        
        textFont(impact_font)
        textAlign(CENTER,CENTER)
        textSize(50)
        fill(0,obtain_nuke_delay * 2)
        text("+1 Nuke", 703, 133) # text shadow
        fill(255,187,0,obtain_nuke_delay * 2)
        text("+1 Nuke", 700, 130)
    
    if obtain_nuke_delay == 179:
        nukes += 1
        nuke_chance += 50
        
def nuke():
    global nukes, nuke_delay, score, planes_destroyed, planes, plane_bullets, plane_spawn_delay
    
    # use nuke
    if key_s == True and nukes > 0 and nuke_delay <= 0 and tank_y < 800:
        nuke_delay = 240
    
    if nuke_delay == 240:
        # kills all planes on screen
        for plane in planes:
            score += plane[14]
            planes_destroyed += 1
        planes = []
        plane_bullets = []
        nukes -= 1
    
    if nuke_delay > 0:
        strokeWeight(20)
        stroke(255,0,0,nuke_delay)
        fill(255,nuke_delay)
        rect(0,0,width-1,height-1)
        nuke_delay -= 1
        plane_spawn_delay = 10

def upgrades():
    global spreadshot, shoot_time, tank_dx, lives, upgrade_delay, upgrade_type
    
    # upgrade announcement
    if upgrade_type != None:
        textFont(impact_font)
        textAlign(CENTER,CENTER)
        textSize(30)
        upgrade_delay -= 2
        
        if upgrade_type == "spreadshot":
            fill(0, upgrade_delay)
            text("Spreadshot Upgrade", tank_x+3, 578)
            fill(255,187,0, upgrade_delay)
            text("Spreadshot Upgrade", tank_x, 575)
        
        elif upgrade_type == "shoot_time":
            fill(0, upgrade_delay)
            text("Firing Speed Upgrade", tank_x+3, 578)
            fill(255,187,0, upgrade_delay)
            text("Firing Speed Upgrade", tank_x, 575)   
        
        elif upgrade_type == "tank_dx":
            fill(0, upgrade_delay)
            text("Movement Speed Upgrade", tank_x+3, 578)
            fill(255,187,0, upgrade_delay)
            text("Movement Speed Upgrade", tank_x, 575)    
        
        elif upgrade_type == "lives":
            textSize(50)
            fill(0, upgrade_delay)
            text("+1 Live", 503, 133)
            fill(255,187,0, upgrade_delay)
            text("+1 Live", 500, 130) 
               
        if upgrade_delay <= 0:
            upgrade_type = None
            upgrade_delay = 300
        
    # upgrades
    if game_time == 0:
        spreadshot = 1
        shoot_time = 8
        tank_dx = 6
    
    # spreadshot upgrades
    
    if game_time >= 60 and game_time < 180: # spreadshot = 2, minute 1
        spreadshot = 2
        if game_time == 60:
            upgrade_type = "spreadshot"
            
    elif game_time >= 180 and game_time < 360: # spreadshot = 3, minute 3 
        spreadshot = 3
        if game_time == 180:
            upgrade_type = "spreadshot"
    
    elif game_time >= 360 and game_time < 600: # spreadshot = 4, minute 6
        spreadshot = 4
        if game_time == 360:
            upgrade_type = "spreadshot"
    
    elif game_time >= 600: # spreadshot = 5, minute 10
        spreadshot = 5
        if game_time == 600:
            upgrade_type = "spreadshot"
    
    # shoot_time upgrades
    
    if game_time >= 120 and game_time < 300: # shoot_time = 7, minute 2
        shoot_time = 7
        if game_time == 120:
            upgrade_type = "shoot_time"
    
    elif game_time >= 300 and game_time < 480: # shoot_time = 6, minute 5
        shoot_time = 6
        if game_time == 300:
            upgrade_type = "shoot_time"
    
    elif game_time >= 480: # shoot_time = 5, minute 8
        shoot_time = 5
        if game_time == 480:
            upgrade_type = "shoot_time"
    
    # tank_dx upgrades
    
    if game_time >= 240 and game_time < 420: # tank_dx = 8, minute 4
        tank_dx = 8
        if game_time == 240:
            upgrade_type = "tank_dx"
    
    elif game_time >= 420 and game_time < 540: # tank_dx = 10, minute 7
        tank_dx = 10
        if game_time == 420:
            upgrade_type = "tank_dx"
    
    elif game_time >= 540: # tank_dx = 12, minute 9
        tank_dx = 12
        if game_time == 540:
            upgrade_type = "tank_dx"
    
    # extra live
    if (game_time == 900 or game_time == 960 or game_time == 1020 or game_time == 1080 or game_time == 1140 or game_time == 1200) and counter == 1 and lives < 2: # minutes 15, 16, 17, 18, 19, 20
        lives += 1
        upgrade_type = "lives"
    
def gametime():
    global game_time, counter, plane_type, plane_spawn_time
    
    # calculates game time
    if mode == "play":
        counter += 1
    if counter >= 60 and mode == "play":
        counter = 0
        game_time += 1

    # what types of planes spawn at what game time
    if game_time >= 0 and game_time < 20:
        plane_type = random.choice(["Fly By","Bomber"])
        plane_spawn_time = 60
    
    elif game_time >= 20 and game_time < 40:
        plane_type = random.choice(["Fly By","Bomber","Bomber"])
        plane_spawn_time = 40
    
    elif game_time >= 40 and game_time < 60:
        plane_type = random.choice(["Fly By","Bomber","Bomber","Carpet Bomber"])
        plane_spawn_time = 50
    
    elif game_time >= 60 and game_time < 80:
        plane_type = random.choice(["Carpet Bomber","Armored Bomber"])
        plane_spawn_time = 60
    
    elif game_time >= 80 and game_time < 100:
        plane_type = random.choice(["Bomber","Bomber","Heat Seeker"])
        plane_spawn_time = 70
    
    elif game_time >= 100 and game_time < 120:
        plane_type = random.choice(["Armored Carpet Bomber"])
        plane_spawn_time = 70
    
    elif game_time >= 120 and game_time < 140:
        plane_type = random.choice(["Bomber"])
        plane_spawn_time = 20
    
    elif game_time >= 140 and game_time < 160:
        plane_type = random.choice(["Downrush","Armored Bomber","Armored Bomber"])
        plane_spawn_time = 70
    
    elif game_time >= 160 and game_time < 180:
        plane_type = random.choice(["Downrush","Armored Carpet Bomber","Heat Seeker"])
        plane_spawn_time = 50
        
    elif game_time >= 180 and game_time < 200:
        plane_type = random.choice(["Carpet Bomber","Carpet Bomber","Cluster Bomber"])
        plane_spawn_time = 60
        
    elif game_time >= 200 and game_time < 220:
        plane_type = random.choice(["Heat Seeker"])
        plane_spawn_time = 25
    
    elif game_time >= 220 and game_time < 240:
        plane_type = random.choice(["Downrush","Cluster Bomber","Armored Bomber"])
        plane_spawn_time = 50
    
    elif game_time >= 240 and game_time < 260:
        plane_type = random.choice(["Rammer","Armored Carpet Bomber"])
        plane_spawn_time = 60
    
    elif game_time >= 260 and game_time < 280:
        plane_type = random.choice(["Rammer","Carpet Bomber"])
        plane_spawn_time = 25
    
    elif game_time >= 280 and game_time < 300:
        plane_type = random.choice(["Nuker","Cluster Bomber"])
        plane_spawn_time = 100
    
    elif game_time >= 300 and game_time < 320:
        plane_type = random.choice(["Packed Downrush","Rammer","Heat Seeker"])
        plane_spawn_time = 30
    
    elif game_time >= 320 and game_time < 340:
        plane_type = random.choice(["Cluster Bomber","Armored Bomber","Downrush"])
        plane_spawn_time = 45
        
    elif game_time >= 340 and game_time < 360:
        plane_type = random.choice(["Nuker","Minigun"])
        plane_spawn_time = 80
        
    elif game_time >= 360 and game_time < 380:
        plane_type = random.choice(["Heat Seeker"])
        plane_spawn_time = 15
    
    elif game_time >= 380 and game_time < 400:
        plane_type = random.choice(["Packed Downrush","Downrush","Cluster Bomber","Cluster Bomber"])
        plane_spawn_time = 35
    
    elif game_time >= 400 and game_time < 420:
        plane_type = random.choice(["Armored Bomber","Fly By"])
        plane_spawn_time = 12
        
    elif game_time >= 420 and game_time < 440:
        plane_type = random.choice(["Minigun"])
        plane_spawn_time = 50
    
    elif game_time >= 440 and game_time < 460:
        plane_type = random.choice(["Rammer","Rammer","Rammer","Nuker"])
        plane_spawn_time = 40
        
    elif game_time >= 460 and game_time < 480:
        plane_type = random.choice(["Heat Seeker","Heat Seeker","Heat Seeker","Heat Seeker","Rammer"])
        plane_spawn_time = 20
    
    elif game_time >= 480 and game_time < 500:
        plane_type = random.choice(["Armored Carpet Bomber","Armored Carpet Bomber","Railgun"])
        plane_spawn_time = 40
    
    elif game_time >= 500 and game_time < 520:
        plane_type = random.choice(["Cluster Bomber","Cluster Bomber","Packed Downrush"])
        plane_spawn_time = 50
    
    elif game_time >= 520 and game_time < 540:
        plane_type = random.choice(["Minigun"])
        plane_spawn_time = 35
    
    elif game_time >= 540 and game_time < 560:
        plane_type = random.choice(["Nuker","Heat Seeker","Heat Seeker","Heat Seeker"])
        plane_spawn_time = 30
        
    elif game_time >= 560 and game_time < 580:
        plane_type = random.choice(["Rammer","Packed Downrush","Railgun"])
        plane_spawn_time = 30
    
    elif game_time >= 580 and game_time < 600:
        plane_type = random.choice(["Nuker","Minigun","Railgun"])
        plane_spawn_time = 40
    
    # NO MORE UPGRADES FROM HERE
    
    elif game_time >= 600 and game_time < 630:
        plane_type = random.choice(["Heat Seeker","Cluster Bomber","Rammer"])
        plane_spawn_time = 20
    
    elif game_time >= 630 and game_time < 660:
        plane_type = random.choice(["Minigun","Armored Carpet Bomber","Armored Carpet Bomber","Packed Downrush"])
        plane_spawn_time = 30
    
    elif game_time >= 660 and game_time < 690:
        plane_type = random.choice(["Heat Seeker","Rammer","Bomber"])
        plane_spawn_time = 8
    
    elif game_time >= 690 and game_time < 720:
        plane_type = random.choice(["Nuker","Downrush","Cluster Bomber"])
        plane_spawn_time = 30
    
    elif game_time >= 720 and game_time < 750:
        plane_type = random.choice(["Carpet Bomber","Carpet Bomber","Carpet Bomber","Carpet Bomber","Railgun"])
        plane_spawn_time = 10
    
    elif game_time >= 750 and game_time < 780:
        plane_type = random.choice(["Packed Downrush","Minigun","Fly By","Nuker"])
        plane_spawn_time = 25
    
    elif game_time >= 780 and game_time < 810:
        plane_type = random.choice(["Armored Bomber","Armored Bomber","Cluster Bomber","Rammer"])
        plane_spawn_time = 15
    
    elif game_time >= 810 and game_time < 840:
        plane_type = random.choice(["Bomber","Bomber","Carpet Bomber"])
        plane_spawn_time = 3
    
    elif game_time >= 840 and game_time < 870:
        plane_type = random.choice(["Heat Seeker","Minigun"])
        plane_spawn_time = 10
    
    elif game_time >= 870 and game_time < 900:
        plane_type = random.choice(["Nuker","Minigun","Railgun"])
        plane_spawn_time = 25
    
    elif game_time >= 900 and game_time < 960:
        plane_type = random.choice(["Packed Downrush","Cluster Bomber","Heat Seeker","Rammer"])
        plane_spawn_time = 10
    
    elif game_time >= 960 and game_time < 1020:
        plane_type = random.choice(["Carpet Bomber","Carpet Bomber","Nuker","Minigun"])
        plane_spawn_time = 15
    
    elif game_time >= 1020 and game_time < 1080:
        plane_type = random.choice(["Railgun","Cluster Bomber","Rammer"])
        plane_spawn_time = 15
    
    elif game_time >= 1080 and game_time < 1140:
        plane_type = random.choice(["Armored Bomber","Minigun"])
        plane_spawn_time = 8
    
    elif game_time >= 1140 and game_time < 1200:
        plane_type = random.choice(["Nuker","Minigun","Railgun"])
        plane_spawn_time = 20
    
    else:
        plane_type = random.choice(["Fly By","Bomber","Armored Bomber","Carpet Bomber","Armored Carpet Bomber","Heat Seeker","Rammer","Downrush","Packed Downrush","Cluster Bomber","Nuker","Minigun","Railgun"])
        plane_spawn_time = 5
        
def calcplanes():
    global plane_spawn_delay
    
    if mode == "play" or mode == "gameover":
        plane_spawn_delay -= 1 # counts down plane_spawn_delay for each frame
    if plane_spawn_delay <= 0 or mode == "hangar": # when plane_spawn_delay is 0 (or less), new plane spawns
        
        plane_x = random.choice([-100,width+100]) # normal plane_x
        plane_y = random.choice([200,250,300]) # normal plane_y
        plane_dy = 0 # normal dy
        plane_bullet_diameter = 16 # normal size
        plane_bullet_color = 255 # normal color
        plane_bullet_hp = 1 # normal hp
        
        if plane_type == "Fly By":
            plane_dx = random.choice([5,6])
            plane_length = 100
            plane_height = 35
            plane_shoot_time = 9000 # wont shoot
            plane_hp = 1
            plane_color = 255
            plane_score = 500
            
        elif plane_type == "Bomber":
            plane_dx = random.choice([3,4])
            plane_length = 120
            plane_height = 45
            plane_shoot_time = 60 
            plane_hp = 1
            plane_color = 255
            plane_score = 1000
            
        elif plane_type == "Armored Bomber":
            plane_dx = random.choice([3,4])
            plane_length = 120
            plane_height = 45
            plane_shoot_time = 60
            plane_hp = 6
            plane_color = 150
            plane_bullet_color = 150
            plane_bullet_hp = 2
            plane_score = 1500
            
        elif plane_type == "Carpet Bomber":
            plane_dx = random.choice([2,3])
            plane_length = 180
            plane_height = 60
            plane_shoot_time = 15
            plane_hp = 3
            plane_color = 255   
            plane_score = 2000
            
        elif plane_type == "Armored Carpet Bomber":
            plane_dx = random.choice([2,3])
            plane_length = 180
            plane_height = 60
            plane_shoot_time = 15
            plane_hp = 10
            plane_color = 150
            plane_bullet_color = 150
            plane_bullet_hp = 2   
            plane_score = 3000
            
        elif plane_type == "Heat Seeker":
            plane_dx = random.choice([5,6])
            plane_length = 120
            plane_height = 45
            plane_shoot_time = 60
            plane_hp = 4
            plane_color = 0xffFFa500
            plane_bullet_color = 0xffFFa500
            plane_score = 2000
            
        elif plane_type == "Rammer":
            plane_dx = 10
            plane_length = 100
            plane_height = 100
            plane_shoot_time = 9000 # wont shoot
            plane_hp = 9
            plane_color = 0xffFFFF00
            plane_score = 3000
            
        elif plane_type == "Downrush" or plane_type == "Packed Downrush":
            plane_y = -50
            plane_dx = 0
            plane_dy = 7
            plane_length = 20
            plane_height = 150
            plane_shoot_time = 9000 # wont shoot
            plane_hp = 4
            plane_color = 0xffFFFF00
            plane_score = 2500
            if plane_type == "Downrush" and mode == "play" or mode == "gameover":
                for n in range(7):
                    planes.append([166 * n + 100, plane_y, plane_dx, plane_dy, plane_length, plane_height, 9000, plane_shoot_time, plane_hp, plane_color, plane_type, plane_bullet_diameter, plane_bullet_color, plane_bullet_hp, plane_score])  
            elif plane_type == "Packed Downrush" and mode == "play":
                for n in range(9):
                    planes.append([125 * n + 100, plane_y, plane_dx, plane_dy, plane_length, plane_height, 9000, plane_shoot_time, plane_hp, plane_color, plane_type, plane_bullet_diameter, plane_bullet_color, plane_bullet_hp, plane_score]) 
        
        elif plane_type == "Cluster Bomber":
            plane_dx = random.choice([5,6,7])
            plane_length = 150
            plane_height = 50
            plane_shoot_time = 60
            plane_hp = 8
            plane_color = 0xff006900
            plane_bullet_color = 0xffFFFF00
            plane_score = 5000
            
        elif plane_type == "Nuker":
            plane_dx = random.choice([4,5])
            plane_length = 250
            plane_height = 40
            plane_shoot_time = 90
            plane_hp = 15
            plane_color = 0xffFF0000
            plane_bullet_color = 0xffFF0000
            plane_bullet_diameter = 40
            plane_bullet_hp = 5
            plane_score = 8000
            
        elif plane_type == "Minigun":
            plane_dx = random.choice([6,7])
            plane_length = 200
            plane_height = 40
            plane_shoot_time = 8
            plane_hp = 8
            plane_color = 50
            plane_bullet_color = 255
            plane_score = 6000
            
        elif plane_type == "Railgun":
            plane_dx = random.choice([3])
            plane_length = 250
            plane_height = 50
            plane_shoot_time = 150
            plane_hp = 20
            plane_color = 50
            plane_bullet_color = 0xffFF0000
            plane_bullet_hp = 10
            plane_score = 8000
                    
        # if planes spawns on right side, it moves left    
        if plane_x > 600 and mode == "play" or mode == "gameover": 
            plane_dx *= -1
                        
        plane_shoot_delay = plane_shoot_time # counts frames after each shot
        
        if plane_type != "Downrush" and plane_type != "Packed Downrush" and mode == "play" or mode == "gameover": # these plane types have specific spawn groups
            planes.append([plane_x, plane_y, plane_dx, plane_dy, plane_length, plane_height, # [x, y, x_movement, y_movement, plane_length, plane_height,
                            plane_shoot_delay, plane_shoot_time, plane_hp, plane_color, plane_type, # plane_shoot_delay, plane_shoot_time, plane_hp, plane_color, plane_type,
                            plane_bullet_diameter, plane_bullet_color, plane_bullet_hp, plane_score]) # plane_bullet_diameter, plane_bullet_color, plane_bullet_hp, plane_score]  
        
        plane_spawn_delay = plane_spawn_time # resets plane_spawn_delay after each plane spawning  
    
    # display in hangar
    if mode == "hangar" and len(planes) == 0:
        plane_x = 600
        plane_y = 300
        if plane_type != "Downrush" and plane_type != "Packed Downrush":
            planes.append([plane_x, plane_y, plane_dx, plane_dy, plane_length, plane_height, plane_shoot_delay, plane_shoot_time, plane_hp, plane_color, plane_type, plane_bullet_diameter, plane_bullet_color, plane_bullet_hp, plane_score])
        elif plane_type == "Downrush":
            for n in range(7):
                planes.append([166 * n + 100, plane_y, plane_dx, plane_dy, plane_length, plane_height, 9000, plane_shoot_time, plane_hp, plane_color, plane_type, plane_bullet_diameter, plane_bullet_color, plane_bullet_hp, plane_score])
        elif plane_type == "Packed Downrush":
            for n in range(9):
                planes.append([125 * n + 100, plane_y, plane_dx, plane_dy, plane_length, plane_height, 9000, plane_shoot_time, plane_hp, plane_color, plane_type, plane_bullet_diameter, plane_bullet_color, plane_bullet_hp, plane_score]) 
        
def drawplanes():
    for plane in planes:
        # plane design
        
        if hitboxes == True:
            fill(plane[9])    
            fill(0,0)
            stroke(0)
            strokeWeight(1)
            rect(plane[0] - (plane[4]/2), plane[1] - (plane[5]/2), plane[4], plane[5])
            ellipse(plane[0], plane[1], 1, 1)
        
        # plane shadow
        stroke(0,0)
        fill(0,15)
        ellipse(plane[0], floor_y-5, plane[4]/3*2, 10)
        
        # plane images
        if plane[10] == "Fly By":
            if plane[2] > 0:
                image(fly_by_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
            elif plane[2] < 0:
                image(fly_by_image_reverse, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
        
        elif plane[10] == "Bomber":
            if plane[2] > 0:
                image(bomber_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
            elif plane[2] < 0:
                image(bomber_image_reverse, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
        
        elif plane[10] == "Carpet Bomber":
            if plane[2] > 0:
                image(carpet_bomber_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
            elif plane[2] < 0:
                image(carpet_bomber_image_reverse, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
        
        elif plane[10] == "Armored Bomber":
            if plane[2] > 0:
                image(armored_bomber_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
            elif plane[2] < 0:
                image(armored_bomber_image_reverse, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
        
        elif plane[10] == "Heat Seeker":
            if plane[2] > 0:
                image(heat_seeker_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
            elif plane[2] < 0:
                image(heat_seeker_image_reverse, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
        
        elif plane[10] == "Armored Carpet Bomber":
            if plane[2] > 0:
                image(armored_carpet_bomber_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
            elif plane[2] < 0:
                image(armored_carpet_bomber_image_reverse, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
        
        elif plane[10] == "Downrush" or plane[10] == "Packed Downrush":
            image(downrush_image, plane[0] - (plane[4]/2) - 20, plane[1] - (plane[5]/2))
        
        elif plane[10] == "Cluster Bomber":
            if plane[2] > 0:
                image(cluster_bomber_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2)-10)
            elif plane[2] < 0:
                image(cluster_bomber_image_reverse, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2)-10)
        
        elif plane[10] == "Rammer":
            if plane[2] > 0:
                image(rammer_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
            elif plane[2] < 0:
                image(rammer_reverse_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
            elif plane[2] == 0:
                image(rammer_downwards_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2))
        
        elif plane[10] == "Nuker":
            if plane[2] > 0:
                image(nuker_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2)-30)
            elif plane[2] < 0:
                image(nuker_reverse_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2)-30)
        
        elif plane[10] == "Minigun":
            if plane[2] > 0:
                image(minigun_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2)-20)
            elif plane[2] < 0:
                image(minigun_reverse_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2)-20)
      
        elif plane[10] == "Railgun":
            if plane[2] > 0:
                image(railgun_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2)-50)
            elif plane[2] < 0:
                image(railgun_reverse_image, plane[0] - (plane[4]/2), plane[1] - (plane[5]/2)-50)                   
                                                                                
def moveplanes():
    for plane in planes:
        plane[0] += plane[2]
        plane[1] += plane[3]
    
        if plane[10] == "Rammer":
            if (plane[2] > 0 and plane[0] > tank_x) or (plane[2] < 0 and plane[0] < tank_x):
                plane[2] = 0
                plane[3] = 10
                    
def calcplanebullets():    
    for plane in planes:
        plane[6] -= 1 # plane_shoot_delay counter
        if plane[6] <= 0: # if plane_shoot_delay is zero, plane shoots
            plane_bullet_dx = plane[2]/2
            plane_bullet_dy = 2
            
            if plane[10] == "Nuker": # makes nuker bullets fall slower
                plane_bullet_dy = 1
            
            if plane[10] == "Minigun":
                s = 8
            elif plane[10] == "Railgun":
                s = 20
            if plane[10] == "Minigun" or plane[10] == "Railgun": # makes minigun and railgun aim towards tank
                plane_bullet_dx = (cos(atan((tank_x-plane[0]) / (float(plane[1]+(plane[5]/2)-tank_y)))+90*PI/180)) * s
                plane_bullet_dy = (sin(atan((tank_x-plane[0]) / (float(plane[1]+(plane[5]/2)-tank_y)))+90*PI/180)) * s
            
            
            plane_bullets.append([plane[0], plane[1]+(plane[5]/2), plane_bullet_dx, plane_bullet_dy, # [x, y, dx, dy, 
                                  plane[10], plane[11], plane[12], plane[13]]) # plane_type, plane_bullet_diameter, plane_bullet_color, plane_bullet_hp]
            plane[6] = plane[7] # resets plane_shoot_delay after each shot   
 
def drawplanebullets():
    for plane_bullet in plane_bullets:
        if plane_bullet[4] != "Nuker":
            # plane bullet design
            fill(plane_bullet[6])
            stroke(0)
            strokeWeight(2)
            ellipse(plane_bullet[0], plane_bullet[1], plane_bullet[5], plane_bullet[5])
        
        if plane_bullet[4] == "Nuker":
            image(nuker_bullet, plane_bullet[0]-20, plane_bullet[1]-20)
            
def moveplanebullets():
    for plane_bullet in plane_bullets:
        plane_bullet[0] += plane_bullet[2]
        plane_bullet[1] += plane_bullet[3]
        
        if plane_bullet[4] != "Minigun" and plane_bullet[4] != "Railgun":
            plane_bullet[3] += 0.1
        
        if plane_bullet[4] == "Heat Seeker": # makes heat seeker plane bullets fly towards the tank when nearby
            if (sqrt((plane_bullet[0] - tank_x)**2 + (plane_bullet[1] - tank_y)**2)) < 300:
                plane_bullet[2] += ((plane_bullet[0] - tank_x) * -1) / 500.0

def nukerexplosions():
    # explosion design
    for nuker_explosion in nuker_explosions:
        fill(0,0)
        strokeWeight(20)
        stroke(255,0,0)
        ellipse(nuker_explosion[0], nuker_explosion[1], nuker_explosion[2]*90, nuker_explosion[2]*8)
        if mode != "pause":
            nuker_explosion[2] += 1
    
        if nuker_explosion[2] >= 30:
            nuker_explosions.remove(nuker_explosion)

def planeexplosions():
    # explosions design
    for plane_explosion in plane_explosions:
        fill(255,200,0)
        strokeWeight(10)
        stroke(255,128,0)
        ellipse(plane_explosion[0], plane_explosion[1], plane_explosion[2]*5 + plane_explosion[3]/2, plane_explosion[2]*5 + plane_explosion[4]/2)
        if mode != "pause":
            plane_explosion[2] += 1
        
        if plane_explosion[2] >= 10:
            plane_explosions.remove(plane_explosion)
        
        
def hitboxtank(): # reaction of a plane bullet hitting the tank
    global tank_hp
    
    # checks if a plane bullet collides with a tank
    for plane_bullet in plane_bullets: 
        if tank_x+(tank_length/2) >= plane_bullet[0]-(plane_bullet[5]/2) and tank_x-(tank_length/2) <= plane_bullet[0]+(plane_bullet[5]/2):
            if tank_y+(tank_height/2) >= plane_bullet[1]-(plane_bullet[5]/2) and tank_y-(tank_height/2) <= plane_bullet[1]+(plane_bullet[5]/2): 
                if plane_bullet[4] == "Nuker" or plane_bullet[4] == "Railgun":
                    tank_hp = 0
                    if plane_bullet[4] == "Nuker":
                        nuker_explosions.append([plane_bullet[0], plane_bullet[1], 0]) # [x, y, nuker explosion delay]
                else:
                    tank_hp -= 1
                plane_bullets.remove(plane_bullet)
    
    # checks if a plane collides with a tank             
    for plane in planes:
        if tank_x+(tank_length/2) >= plane[0]-(plane[4]/2) and tank_x-(tank_length/2) <= plane[0]+(plane[4]/2):
            if tank_y+(tank_height/2) >= plane[1]-(plane[5]/2) and tank_y-(tank_height/2) <= plane[1]+(plane[5]/2):  
                planes.remove(plane)
                tank_hp -= 1
                plane_explosions.append([plane[0], plane[1], 0, plane[4], plane[5]]) # [x, y, plane explosion delay, plane explosion length, plane explosion height]
                
def hitboxplanes(): # reaction of bullet hitting a plane
    global planes_destroyed, score, obtain_nuke_delay
    
    for bullet in bullets:
        for plane in planes:
            if bullet[0]+(bullet_diameter/2) >= plane[0]-(plane[4]/2) and bullet[0]-(bullet_diameter/2) <= plane[0]+(plane[4]/2):
                if bullet[1]+(bullet_diameter/2) >= plane[1]-(plane[5]/2) and bullet[1]-(bullet_diameter/2) <= plane[1]+(plane[5]/2): 
                    plane[8] -= 1
                    if plane[8] <= 0:
                        planes.remove(plane)
                        planes_destroyed += 1
                        score += plane[14]
                        plane_explosions.append([plane[0], plane[1], 0, plane[4], plane[5]]) # [x, y, plane explosion delay, plane explosion length, plane explosion height]
                        if nukes < 3 and random.randint(1,nuke_chance) == 1:
                            obtain_nuke_delay = 180
                    if bullet in bullets:
                        bullets.remove(bullet)                    
                                                            
def hitboxplanebullets(): # reaction of bullet hitting a plane bullet
    for bullet in bullets:
        for plane_bullet in plane_bullets:
            if bullet[0]+(bullet_diameter/2) >= plane_bullet[0]-(plane_bullet[5]/2) and bullet[0]-(bullet_diameter/2) <= plane_bullet[0]+(plane_bullet[5]/2): 
                if bullet[1]+(bullet_diameter/2) >= plane_bullet[1]-(plane_bullet[5]/2) and bullet[1]-(bullet_diameter/2) <= plane_bullet[1]+(plane_bullet[5]/2): 
                    plane_bullet[7] -= 1
                    if plane_bullet[7] <= 0:
                        plane_bullets.remove(plane_bullet)
                    if bullet in bullets:
                        bullets.remove(bullet)

def hitboxfloor(): # reaction of a bullet, plane bullet, or plane crashing into the floor
    global tank_hp, planes_escaped
    
    # checks if a bullet collides with the floor
    for bullet in bullets:
        if bullet[1]+(bullet_diameter/2) >= floor_y:
            bullets.remove(bullet)
    
    # checks if a plane collides with the floor
    for plane in planes:
        if plane[1]+(plane[5]/2) >= floor_y:
            planes.remove(plane)
            plane_explosions.append([plane[0], plane[1], 0, plane[4], plane[5]]) # [x, y, plane explosion delay, plane explosion length, plane explosion height]
            if mode == "play" and tank_y < 800:
                planes_escaped += 1
            
                
    # checks if a plane bullet collides with the floor
    for plane_bullet in plane_bullets:
        if plane_bullet[3] > 0: # checks if plane bullet is going downwards
            if plane_bullet[1]+(plane_bullet[5]/2) >= floor_y:
                if plane_bullet[4] == "Nuker":
                    tank_hp = 0
                    nuker_explosions.append([plane_bullet[0], plane_bullet[1], 0]) # [x, y, nuker explosion delay]
                if plane_bullet[4] == "Cluster Bomber": 
                    for n in range(4):
                        plane_bullets.append([plane_bullet[0], plane_bullet[1], -6+(4*n), -4, "Cluster Frags", 16, 0xff006900, 1]) # [x, y, x_movement, y_movement, plane_type, plane bullet diameter, plane bullet color, plane_bullet_hp]
                plane_bullets.remove(plane_bullet)
            
                                    
def outofbounds(): # deletes bullets and planes that are outside the screen
    global planes_escaped
    
    # checks if a bullet is out of bounds
    for bullet in bullets:
        if bullet[0] < -10 or bullet[0] > width+10 or bullet[1] < -10 or bullet[1] > height+10:
            bullets.remove(bullet)
    
    # checks if a plane is out of bounds
    for plane in planes:
        if plane[0] < -100 or plane[0] > width+100 or plane[1] < -100 or plane[1] > height+100:
            planes.remove(plane)
            if mode == "play" and tank_y < 800:
                planes_escaped += 1
            
    # checks if a plane bullet is out of bounds
    for plane_bullet in plane_bullets:
        if plane_bullet[0] < -(plane_bullet[5]/2) or plane_bullet[0] > width+(plane_bullet[5]/2) or plane_bullet[1] < -(plane_bullet[5]/2) or plane_bullet[1] > height+(plane_bullet[5]/2):
            plane_bullets.remove(plane_bullet) 
        
def scoreboard():
    stroke(0xffFFBB00)
    strokeWeight(4)
    fill(0,200)
    rect(300,30,600,40)
    fill(0xffFFBB00)
    textFont(comicsans_font)
    textAlign(CENTER,CENTER)
    textSize(25)
    
    # score
    text(score, 382, 50)
    line(460,30,460,70)
    
    # lives left
    for n in range(lives):
        image(remaining_tanks, 475 + 32*n, 36)
    line(550,30,550,70)
    
    # survival time clock
    text(game_time / 600, 570, 50) # game time in minutes tens column
    text(game_time / 60 % 10, 585, 50) # game time in minutes ones column
    text(":", 600, 50)
    text(game_time / 10 % 6, 615, 50) # game time in seconds tens column
    text(game_time % 10, 630, 50) # game time in seconds ones column
    line(650,30,650,70)
    
    # nukes left
    for n in range(nukes):
        image(remaining_nukes, 665 + 32*n, 36)
    line(770,30,770,70) 
    
    # planes destroyed
    image(planes_destroyed_image, 780, 36)
    textSize(20)
    text(planes_destroyed, 870, 50)
    
def pausescreen():
    global mode
    
    strokeWeight(0)
    fill(0,150)
    rect(0,0,width,height)
    
    textFont(impact_font)
    textSize(100)
    fill(0)
    text("Game Paused",605,155)
    fill(0xffFFBB00)
    text("Game Paused",600,150)
    
    # resume button
    stroke(0xffFFBB00)
    strokeWeight(5)
    fill(0,100)
    rect(400,300,400,80)
    fill(0xffFFBB00)
    textFont(impact_font)
    textSize(40)
    text("Resume",600,335)
    textSize(20)
    text("(Spacebar)",600,365)
    
    # menu button
    stroke(0xffFFBB00)
    strokeWeight(5)
    fill(0,100)
    rect(400,450,400,80)
    fill(0xffFFBB00)
    textSize(40)
    text("Menu",600,490)
    
    # button cursor change
    if mouseX >= 400 and mouseX <= 800 and mouseY >= 300 and mouseY <= 380:
        cursor(HAND)   
    elif mouseX >= 400 and mouseX <= 800 and mouseY >= 450 and mouseY <= 530:
        cursor(HAND)        
    else:
        cursor(ARROW)
    
def gameoverscreen():
    global mode, total_score
    
    stroke(0xffFFBB00)
    strokeWeight(5)
    fill(0,200)
    rect(400,100,400,100)
    rect(400,225,400,300)
    
    # menu button
    rect(400,550,400,80)
    fill(0xffFFBB00)
    textFont(impact_font)
    textSize(40)
    text("Menu",600,590)
    if mouseX >= 400 and mouseX <= 800 and mouseY >= 550 and mouseY <= 630:
        cursor(HAND)
    else:
        cursor(ARROW)
        
    textAlign(CENTER,CENTER)
    textSize(50)
    text("Game Over",600,140)
    textSize(30)
    text("Survival Mode",600,175)
    
    # game data
    textAlign(LEFT,CENTER)
    textSize(25)
    text("Survival Time:",420,260)
    text("Survival Bonus:",420,300)
    text("Planes Destroyed:",420,340)
    text("Plane Score:",420,380)
    text("Kill Percentage:",420,420)
    line(400,450,800,450)
    textSize(35)
    text("Total Score:",420,485)
    
    textSize(25)
    textAlign(RIGHT,CENTER)
    
    # survival time
    text(game_time / 600, 720, 260) # game time in minutes tens column
    text(game_time / 60 % 10, 735, 260) # game time in minutes ones column
    text(":", 746, 258)
    text(game_time / 10 % 6, 765, 260) # game time in seconds tens column
    text(game_time % 10, 780, 260) # game time in seconds ones column
    
    # survival bonus
    survival_bonus = game_time / 60 * 10000
    text(survival_bonus, 780, 300)
    
    # planes destroyed
    text(planes_destroyed,780,340)
    
    # plane score
    text(score,780,380)
    
    # kill percentage
    if planes_destroyed + planes_escaped > 0: # prevents division by 0
        text(planes_destroyed / (planes_destroyed + planes_escaped + 0.0) * 100,780,420)
    else:
        text(0,780,420)
    
    # total score
    total_score = score + survival_bonus
    textSize(35)
    text(total_score, 780, 485)
    
def menuscreen():
    global mode
    
    # title
    strokeWeight(0)
    fill(0,200)
    rect(0,0,1200,170)
    strokeWeight(8)
    line(0,170,1200,170)
    image(airstrike_title, 310, 10)
    
    # play button
    stroke(255,187,0)
    strokeWeight(8)
    fill(0,200)
    ellipse(600,400,220,220)
    fill(255,187,0)
    textFont(impact_font)
    textAlign(CENTER,CENTER)
    textSize(70)
    text("Play",600,400)
    
    # hangar button
    strokeWeight(6)
    fill(0,200)
    ellipse(600,650,150,150)
    fill(255,187,0)
    textSize(25)
    text("Hangar",600,650)
    
    # how to play button
    fill(0,200)
    ellipse(300,600,150,150)
    fill(255,187,0)
    text("How to Play",300,600)
    
    # quit game button
    fill(0,200)
    ellipse(900,600,150,150)
    fill(255,187,0)
    text("Quit Game",900,600)
    
    # button cursor change
    if (sqrt((mouseX - 600)**2 + (mouseY - 400)**2)) <= 110:
        cursor(HAND)
    elif (sqrt((mouseX - 300)**2 + (mouseY - 600)**2)) <= 75:
        cursor(HAND)
    elif (sqrt((mouseX - 600)**2 + (mouseY - 650)**2)) <= 75:
        cursor(HAND)
    elif (sqrt((mouseX - 900)**2 + (mouseY - 600)**2)) <= 75:
        cursor(HAND)        
    else:
        cursor(ARROW)

def howtoplayscreen():
    # title
    strokeWeight(0)
    fill(0,200)
    rect(0,0,1200,170)
    strokeWeight(8)
    line(0,170,1200,170)
    image(how_to_play_title, 210, 15)
    
    # got it button
    strokeWeight(6)
    ellipse(600,650,150,150)
    fill(255,187,0)
    textFont(impact_font)
    textAlign(CENTER,CENTER)
    textSize(40)
    text("Got It",600,650)
    
    # arrow buttons
    strokeWeight(5)
    fill(0,200)
    ellipse(800,650,100,100)
    ellipse(400,650,100,100)
    fill(255,187,0)
    triangle(790,630,790,670,820,650)
    triangle(410,630,410,670,380,650)
    
    if (sqrt((mouseX - 600)**2 + (mouseY - 650)**2)) <= 75:
        cursor(HAND)
    elif (sqrt((mouseX - 800)**2 + (mouseY - 650)**2)) <= 50:
        cursor(HAND)
    elif (sqrt((mouseX - 400)**2 + (mouseY - 650)**2)) <= 50:
        cursor(HAND)           
    else:
        cursor(ARROW)
    
    # how to play
    fill(0,200)
    textFont(comicsans_font)
    if how_to_play_page == 1:
        textSize(30)
        text("1. Use keys w and a to move your tank right and left.",600,220)
        text("2. Use your mouse to aim and shoot bullets to planes.",600,290)
        text("3. Use key s to activate a nuke, which destroys all planes on the screen.",600,360)
        text("Nukes have a chance to be obtained by destroying a plane.",600,400)
        text("4. Press the spacebar to pause.",600,470)
        text("5. Survive and destroy planes for as long as possible to get the highest score.",600,540)
    
    elif how_to_play_page == 2:
        textSize(25)
        text("Score",380,265)
        text("Lives\nLeft",500,280)
        text("Time",600,265)
        text("Nukes\nLeft",710,280)
        text("Planes\nDestroyed",835,280)
        
        global score, lives, game_time, nukes, planes_destroyed
        score = 256000
        lives = 1
        game_time = 261
        nukes = 2
        planes_destroyed = 67
        
        pushMatrix()
        translate(0,170)
        scoreboard()
        popMatrix()
        
def hangarscreen():
    global planes, plane_type, plane_list_number
    
    # display of the plane
    plane_list = ["Fly By","Bomber","Carpet Bomber","Armored Bomber","Heat Seeker","Armored Carpet Bomber","Downrush","Cluster Bomber","Rammer","Packed Downrush","Nuker","Minigun","Railgun"]
    plane_type = plane_list[plane_list_number]
    calcplanes()
    drawplanes()
    calcplanebullets()
    drawplanebullets()
    moveplanebullets()
    nukerexplosions()
    hitboxfloor()
    
    # title
    strokeWeight(0)
    stroke(255,187,0)
    fill(0,200)
    rect(0,0,1200,170)
    strokeWeight(8)
    line(0,170,1200,170)
    image(hangar_title, 380, 15)
    
    # menu button
    strokeWeight(6)
    ellipse(600,650,150,150)
    fill(255,187,0)
    textFont(impact_font)
    textAlign(CENTER,CENTER)
    textSize(40)
    text("Menu",600,650)
    
    # arrow buttons
    strokeWeight(5)
    fill(0,200)
    ellipse(800,650,100,100)
    ellipse(400,650,100,100)
    fill(255,187,0)
    triangle(790,630,790,670,820,650)
    triangle(410,630,410,670,380,650)
    
    # button cursor change
    if (sqrt((mouseX - 600)**2 + (mouseY - 650)**2)) <= 75:
        cursor(HAND)   
    elif (sqrt((mouseX - 800)**2 + (mouseY - 650)**2)) <= 50:
        cursor(HAND)
    elif (sqrt((mouseX - 400)**2 + (mouseY - 650)**2)) <= 50:
        cursor(HAND)      
    else:
        cursor(ARROW)
    
    # plane name
    fill(0)
    textSize(40)
    text(planes[0][10],600,planes[0][1]-(planes[0][5]/2)-30)
    
    # plane stats
    fill(0,200)
    strokeWeight(5)
    stroke(255,187,0)
    rect(-10,200,210,375)
    fill(255,187,0)
    line(0,245,200,245)
    textSize(30)
    text("Plane Stats",95,225)
    textFont(comicsans_font)
    textAlign(LEFT,CENTER)
    textSize(20)
    text("HP:",10,270)
    text("Fire Rate:",10,300)
    text("Score:",10,330)
    line(0,355,200,355)
    textAlign(RIGHT,CENTER)
    
    # hp
    text(planes[0][8],190,270)
    
    # fire rate
    if planes[0][7] < 1000:
        text(1 / (planes[0][7] / 60.0),190,300)
    if planes[0][7] >= 1000:
        text("Never",190,300)
    
    # score
    text(planes[0][14],190,330)
    
    # special ability
    textAlign(LEFT,TOP)
    text("Special Ability:",10,367)
    if planes[0][10] == "Fly By" or planes[0][10] == "Bomber" or planes[0][10] == "Carpet Bomber" or planes[0][10] == "Armored Bomber" or planes[0][10] == "Armored Carpet Bomber" or planes[0][10] == "Downrush" or planes[0][10] == "Packed Downrush":
        text("None",10,395)
    elif planes[0][10] == "Heat Seeker":
        text("This plane's bombs\nseek out the tank\nwhen nearby.",10,395)
    elif planes[0][10] == "Cluster Bomber":
        text("This plane's bombs\nexplode into 4\nbombs when hitting\nthe ground.",10,395)
    elif planes[0][10] == "Rammer":
        text("This plane dives\ndownwards when\nabove the tank.",10,395)
    elif planes[0][10] == "Nuker":
        text("This plane's bombs\nexplode the tank\non impact anywhere.",10,395)
    elif planes[0][10] == "Minigun":
        text("This plane has\nperfect accuracy\nand is the fastest\nshooting plane.",10,395)    
    elif planes[0][10] == "Railgun":
        text("This plane has\nperfect accuracy\nand destroys the\ntank in one shot.",10,395)    
    line(0,505,200,505)
    
    # danger level
    textAlign(LEFT,CENTER)
    text("Danger Level:",10,525)
    if planes[0][10] == "Fly By":
        fill(255,255,255)
        text("None",10,550)
    if planes[0][10] == "Bomber":
        fill(255,255,128)
        text("Very Low",10,550)
    if planes[0][10] == "Carpet Bomber" or planes[0][10] == "Armored Bomber":
        fill(255,255,0)
        text("Low",10,550)
    if planes[0][10] == "Armored Carpet Bomber" or planes[0][10] == "Downrush" or planes[0][10] == "Heat Seeker":
        fill(255,128,0)
        text("Medium",10,550)
    if planes[0][10] == "Cluster Bomber" or planes[0][10] == "Rammer" or planes[0][10] == "Packed Downrush":
        fill(255,50,50)
        text("High",10,550)
    if planes[0][10] == "Nuker" or planes[0][10] == "Minigun" or planes[0][10] == "Railgun":
        fill(225,0,0)
        text("Very High",10,550)
    
# KEY PRESSES #######################################

def presskey():
    
    global key_a, key_d, key_s
    
    if key == "a":
        key_a = True
    if key == "d":
        key_d = True
    if key == "s":
        key_s = True
    
def releasekey():
    global key_a, key_d, key_s
    
    if key == "a":
        key_a = False
    if key == "d":
        key_d = False
    if key == "s":
        key_s = False

    
