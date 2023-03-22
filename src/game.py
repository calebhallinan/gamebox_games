# Caleb Hallinan
# cph4mb
# Ashton Mann
# arm7fy

# Required Features:
# User Input: Will be able to move the character and be able to shoot/hit another character
# Graphics/Images: We will have background, two characters, cool (different) title screen
# Start Screen: It will include game names, student names (and of course, IDs), and basic game instructions
# Small enough Window: Yep, we'll have it and will not crash your computer

# Optional Requirements:
# 1. Animation (Sprite sheet) - have two characters
# 2. Two Players simultaneously - battle against each other by shooting
# 3. Health meter - will go down if shot or fall off, 10 hits and you lose
# 4. Timer - you have 60 seconds until the game ends and one player will win if it comes to that

# General overview of our game
# Our game will allow two different players to shoot at each other. It's similar to laser tag where players do not die
# when shot. Instead, their health meter decreases when they are shot. The user loses when their health meter runs out
# of health.


# Here is our game!!

import gamebox
import pygame

camera = gamebox.Camera(800, 600)

###############
# Title stuff #
###############

# Indicates whether we have started the game
game_started = False

# instructions on title screen
instructions = '''
    You have one minute to win. 
    Each player has shooting abilities. 
    Controls for each player are listed above.
    Every time you are shot or fall off the platform you lose 10% of your health.

    How to win: shoot your opponent 10 times or have more health
    than your opponent at the end of the minute

    PRESS SPACE TO ENTER THE BATTLE ARENA 
'''
p1_controls = """
    For Kitty:
    Left = A
    Right = D
    Jump = W
    Shoot = Tab
"""
p2_controls = """
    For Megaman:
    Left = Left arrow
    Right = Right arrow
    Jump = Up arrow
    Shoot = ? or /
"""


def draw_title(keys):
    '''Draws all components of the title screen'''
    global game_started

    # contains all boxes we draw
    to_draw = []

    # background for title
    title_background = gamebox.from_image(400, 300, 'game_titlebackground.jpg')
    to_draw.append(title_background)

    # starts the game if any key at all pressed
    if pygame.K_SPACE in keys:
        game_started = True

    # Make the Game Title text
    title_box = gamebox.from_text(400, 30, 'MEGAMAN v. KITTY', 80, 'blue', True)
    to_draw.append(title_box)
    title_box2 = gamebox.from_text(400, 400, 'Greatest Duel of All Time', 80, 'blue', True)
    to_draw.append(title_box2)

    # draw the instructions
    ypos = 150
    for line in instructions.split('\n'):
        to_draw.append(gamebox.from_text(400, ypos, line, 30, 'yellow'))
        ypos += 20

    # draw p1 controls
    p1_ypos = 60
    for line in p1_controls.split('\n'):
        to_draw.append(gamebox.from_text(125, p1_ypos, line, 30, 'red'))
        p1_ypos += 20

    # draw p2 controls
    p2_ypos = 60
    for line in p2_controls.split('\n'):
        to_draw.append(gamebox.from_text(675, p2_ypos, line, 30, 'red'))
        p2_ypos += 20

    # names and computing ids
    names = gamebox.from_text(400, 575, "Ashton Mann - arm7fy | Caleb Hallinan - cph4mb", 30, 'lightblue', True)
    to_draw.append(names)

    # draw all of the things in list
    for box in to_draw:
        camera.draw(box)


##############
# Game Stuff #
##############


# Playable Characters aka kitty and megaman
# megaman
ss_megaman = gamebox.load_sprite_sheet('game_megaman.png', 1, 3)
megaman = gamebox.from_image(camera.x, camera.y, ss_megaman[0])
megaman.scale_by(1.8)
megaman.y = 300
megaman.x = 500

# kitty
ss_kitty = gamebox.load_sprite_sheet('games_kitty.png', 1, 5)
kitty = gamebox.from_image(camera.x, camera.y, ss_kitty[0])
kitty.scale_by(0.7)
kitty.y = 300
kitty.x = 300

# shooting objects
# used a far away coordinate so shoots wouldn't be on screen until need
megaman_shoot = gamebox.from_circle(2500, 2500, "blue", 5)
megaman_shoot_life = 0
kitty_shoot = gamebox.from_circle(2500, 2500, "red", 5)
kitty_shoot_life = 0

# Variables
gravity = 0.75
kitty_right = True  # true if kitty facing right, false if not
megaman_right = False  # true if megaman facing right, false if not
megaman.flip() # starts megaman flipped so he is facing kitty when the game begins
megaman_health = 100  # health for megaman
kitty_health = 100  # health for kitty

# background
background = gamebox.from_image(400, 300, 'game_background3.jpg')
background.scale_by(1.25)

# floor
floor = gamebox.from_color(400, 525, 'lightblue', 540, 50)

# stage
stage = gamebox.from_image(400, 400, 'game_stage.png')
stage.scale_by(1.6)

# list for scenery
scenery = [background, stage]

# list for obstacles to allow them not to go through
obstacles = [floor]

# to cycle images for animation
tick_count = 0


def move_megaman(keys):
    """moves megaman, tells megaman no to off screen, makes megaman"""
    global tick_count
    global megaman_right
    global megaman_health

    # movement to the right
    if pygame.K_RIGHT in keys and megaman_right == False:
        megaman_right = True
        megaman.flip()
    if pygame.K_RIGHT in keys and megaman_right:
        megaman.x += 5

        # animation using sprite sheet
        megaman.image = ss_megaman[tick_count // 8 % len(ss_megaman)]
        tick_count += 1
        megaman.move_speed()

    # movement left
    if pygame.K_LEFT in keys and megaman_right:
        megaman_right = False
        megaman.flip()
    if pygame.K_LEFT in keys and megaman_right == False:
        megaman.x -= 5

        # animation using sprite sheet
        megaman.image = ss_megaman[tick_count // 8 % len(ss_megaman)]
        tick_count += 1
        megaman.move_speed()

    # movement up and makes them touch ground before jumping again
    if pygame.K_UP in keys:
        for obstacle in obstacles:
            if megaman.bottom_touches(obstacle):
                megaman.speedy = -12

    # gravity and move speed
    megaman.speedy += gravity
    megaman.move_speed()

    # need to land on floor
    for obstacle in obstacles:
        megaman.move_to_stop_overlapping(obstacle)

    # reset person if they touch screen
    if megaman.y > 600 or megaman.y < 0 or megaman.x < 0 or megaman.x > 800:
        megaman.y = 300
        megaman.x = 500
        megaman_health -= 10

    camera.draw(megaman)


def move_kitty(keys):
    """makes kitty, moves kitty, tells kitty when to die"""
    global tick_count
    global kitty_right
    global kitty_health

    # movement to the right
    if pygame.K_d in keys and kitty_right == False:
        kitty_right = True
        kitty.flip()
    if pygame.K_d in keys and kitty_right:
        kitty.x += 5

        # animation using sprite sheet
        kitty.image = ss_kitty[tick_count // 5 % len(ss_megaman)]
        tick_count += 1
        kitty.move_speed()

    # movement to the left
    if pygame.K_a in keys and kitty_right:
        kitty_right = False
        kitty.flip()
    if pygame.K_a in keys and kitty_right == False:
        kitty.x -= 5

        # animation using sprite sheet
        kitty.image = ss_kitty[tick_count // 5 % len(ss_megaman)]
        tick_count += 1
        kitty.move_speed()

    # movement up
    if pygame.K_w in keys:
        for obstacle in obstacles:
            if kitty.bottom_touches(obstacle):
                kitty.speedy = -12

    # gravity and moving
    kitty.speedy += gravity
    kitty.move_speed()

    # need to land on floor
    for obstacle in obstacles:
        kitty.move_to_stop_overlapping(obstacle)

    # reset person if they touch screen
    if kitty.y > 600 or kitty.y < 0 or kitty.x < 0 or kitty.x > 800:
        kitty.y = 300
        kitty.x = 300
        kitty_health -= 10

    camera.draw(kitty)


# helps with making megaman have only one shot on screen at a time
megaman_shoot_alive = True

def shooting_megaman(keys):
    """allows megaman to shoot"""
    global kitty_health
    global megaman_shoot_life
    global megaman_shoot
    global megaman_shoot_alive

    # shoots to the left
    if pygame.K_SLASH in keys and megaman_shoot_life > 30 and megaman_right == False and megaman_shoot_alive:
        megaman_shoot.center = megaman.center
        megaman_shoot.speedx = -15
        megaman_shoot_alive = False

    # shoot to the right
    if pygame.K_SLASH in keys and megaman_shoot_life > 30 and megaman_right and megaman_shoot_alive:
        megaman_shoot.center = megaman.center
        megaman_shoot.speedx = 15
        megaman_shoot_alive = False

    # other player takes damage
    if megaman_shoot.touches(kitty):
        kitty_health -= 10
        megaman_shoot.move(3000, 3000)
        megaman_shoot_alive = True

    # resets megamans shot if it goes offscreen
    if megaman_shoot.x < 0 or megaman_shoot.x > 800:
        megaman_shoot.move(3000, 3000)
        megaman_shoot_alive = True

    camera.draw(megaman_shoot)
    megaman_shoot.move_speed()
    megaman_shoot_life += 1


# helps with allowing kitty to have only one shot on screen
kitty_shoot_alive = True

def shooting_kitty(keys):
    """allows kitty to shoot"""
    global megaman_health
    global kitty_shoot_life
    global kitty_shoot
    global kitty_shoot_alive

    # shoots to the left
    if pygame.K_TAB in keys and kitty_shoot_life > 30 and kitty_right == False and kitty_shoot_alive:
        kitty_shoot.center = kitty.center
        kitty_shoot.speedx = -15
        kitty_shoot_alive = False

    # shoots to the right
    if pygame.K_TAB in keys and kitty_shoot_life > 30 and kitty_right and kitty_shoot_alive:
        kitty_shoot.center = kitty.center
        kitty_shoot.speedx = 15
        kitty_shoot_alive = False

    # other player takes damage
    if kitty_shoot.touches(megaman):
        megaman_health -= 10
        kitty_shoot.move(3000, 3000)
        kitty_shoot_alive = True

    # puts kitties shot far away until shot again
    if kitty_shoot.x < 0 or kitty_shoot.x > 800:
        kitty_shoot.move(3000, 3000)
        kitty_shoot_alive = True

    camera.draw(kitty_shoot)
    kitty_shoot.move_speed()
    kitty_shoot_life += 1


def draw_scenery():
    """has the camera draw every box in our scene"""
    for box in scenery:
        camera.draw(box)


# variables for timer to work and count down during the game
ticks = 0
seconds = 60

def timer():
    """creates a timer and draws it"""
    global ticks
    global seconds
    ticks += 1
    if ticks % 30 == 0 and seconds > 0:
        seconds -= 1
    camera.draw("Time Remaining: " + str(seconds), 30, 'black', 400, 75)


# to help determine if the game has ended or not
end_game1 = False

def end_game(keys):
    """ends game after 60 seconds have passed, tells which player wins"""
    global game_started
    global end_game1
    global seconds
    global megaman_health
    global kitty_health

    # condition for ending the game
    if seconds == 0 or megaman_health == 0 or kitty_health == 0:
        end_game1 = True

    # if health is equal
    if megaman_health == kitty_health and end_game1:
        camera.draw("It's a tie!!!", 40, 'yellow', 400, 215)
        camera.draw("To Restart Press R", 30, 'yellow', 400, 275)

    # if megaman has more health than kitty
    if megaman_health > kitty_health and end_game1:
        camera.draw("Megaman Wins!!!", 40, 'yellow', 400, 215)
        camera.draw("To Restart Press R", 30, 'yellow', 400, 275)

    # if kitty has more health than megaman
    if megaman_health < kitty_health and end_game1:
        camera.draw("Kitty Wins!!!", 40, 'yellow', 400, 215)
        camera.draw("To Restart Press R", 30, 'yellow', 400, 275)

    # to reset and go back to title screen
    if pygame.K_r in keys and end_game1:
        end_game1 = False
        game_started = False
        seconds = 60
        megaman_health = 100
        kitty_health = 100

        # reset megaman
        megaman.y = 300
        megaman.x = 500

        # reset kitty
        kitty.y = 300
        kitty.x = 300
        keys.clear()


def draw_megaman_healthmeter(keys):
    """draws the health meter for megaman as well as make them change if they are hit"""
    camera.draw('Megaman Health', 20, 'black', 740, 25)
    if megaman_health == 100:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    elif megaman_health == 90:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    elif megaman_health == 80:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    elif megaman_health == 70:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    elif megaman_health == 60:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    elif megaman_health == 50:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    elif megaman_health == 40:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    elif megaman_health == 30:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    elif megaman_health == 20:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    elif megaman_health == 10:
        megaman_healthmeter = gamebox.from_color(750, 150, 'red', 30, megaman_health * 2)
        camera.draw(megaman_healthmeter)
    else:
        end_game(keys)


def draw_kitty_healthmeter(keys):
    """draws the health meter for kitty as well as make them change if they are hit"""
    camera.draw('Kitty Health', 20, 'black', 60, 25)
    if kitty_health == 100:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    elif kitty_health == 90:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    elif kitty_health == 80:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    elif kitty_health == 70:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    elif kitty_health == 60:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    elif kitty_health == 50:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    elif kitty_health == 40:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    elif kitty_health == 30:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    elif kitty_health == 20:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    elif kitty_health == 10:
        kitty_healthmeter = gamebox.from_color(50, 150, 'red', 30, kitty_health * 2)
        camera.draw(kitty_healthmeter)
    else:
        end_game(keys)


def tick(keys):
    """has all the important stuff"""
    camera.clear("black")
    if not game_started:
        draw_title(keys)
    else:
        draw_scenery()
        move_megaman(keys)
        move_kitty(keys)
        shooting_megaman(keys)
        shooting_kitty(keys)
        timer()
        draw_megaman_healthmeter(keys)
        draw_kitty_healthmeter(keys)
        end_game(keys)

    camera.display()


gamebox.timer_loop(30, tick)
