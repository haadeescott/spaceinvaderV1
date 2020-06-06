# space invader project

import turtle
import winsound
import math
import random
import platform


# set up screen
wn=turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("background.gif")
wn.tracer(0)

# register shapes
turtle.register_shape("invader2.gif")
turtle.register_shape("main3.gif")
turtle.register_shape("laser.gif")

# draw border
border_pen=turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pensize(3)

for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# set score to 0
score = 0

# draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-210,250)
scorestring="Score: {}".format(score)
score_pen.write(scorestring, False, align="right", font=("Arial",14, "normal"))
score_pen.hideturtle()

# create player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("main3.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

playerspeed = 15


# choose number of enemies
number_of_enemies = 30
# create an empty list of enemies
enemies = []
#  add enemies to list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

enemy_start_x= -225
enemy_start_y= 250
enemy_number = 0

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader2.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50*enemy_number)
    y = enemy_start_y 
    enemy.setposition(x,y)
    # update the enemy number
    enemy_number += 1
    
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0
    
    
enemyspeed = 0.08


# create players bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("laser.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 0.89

# bullet state
#  2 states
#   ready - ready to fire
#   fire - bullet it firing
bulletstate = "ready"



# create function to enable change of direction
# bind function to a key
def move_left():
    x = player.xcor()
    x -=playerspeed # subtracts playerspeed each time function is called
    if x < -280:
        x = - 280 # to check if border isnt crossed
    player.setx(x)
    
# create function to enable change of direction
# bind function to a key
def move_right():
    x = player.xcor()
    x +=playerspeed # subtracts playerspeed each time function is called
    if x > 280:
        x =  280 # to check if border isnt crossed
    player.setx(x)

def fire_bullet():
    # declare bullet state as global if needed to change
    global bulletstate
    if bulletstate == "ready":
        play_sound("laser.wav")
        bulletstate = "fire"
        # move bullet to above player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

# collision checking
def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance <15:
        return True
    else:
        return False

def play_sound(sound_file, time=0):
    winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    
    # repeat sound
    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time *1000))

# create keyboard bindings
turtle.listen()
turtle.onkeypress(move_left, "Left")
turtle.onkeypress(move_right, "Right")
turtle.onkey(fire_bullet, "space")

# play background music
# play_sound("bg.wav",206)

# main game loop
while True:
    wn.update() # speed up program
    for enemy in enemies:

        # move enemy 
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # move enemy within boundary and back and down 
        if enemy.xcor()>280:
            # move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # change direction
            enemyspeed *=-1
            
        if enemy.xcor()<-280:
            # move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *=-1
            
        
        # check for collision between bullet and enemy
        if isCollision(bullet, enemy):
            play_sound("explosion.wav")
            #  reset bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            
            #  reset enemy
            
            enemy.setposition(0,10000)
            
            # update score
            score+= 10
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.setposition(-210,250)
            score_pen.write(scorestring, False, align="right", font=("Arial",14, "normal"))
        
        if isCollision(player,enemy):
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break
            
    # move bullet
    if bulletstate == "fire":
        y= bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # check to see if bullet has gone to the top
    if bullet.ycor()>275:
        bullet.hideturtle()
        bulletstate = "ready"
        
    


# in python 2 - raw_input
# in python 3 - input
delay = input("Press enter to finish.")