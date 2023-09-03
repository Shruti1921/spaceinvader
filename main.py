import pygame
import random
import math
from pygame import mixer

#initialize the pygame
pygame.init()

#create the screen
screen=pygame.display.set_mode((800,600))

#Background
background=pygame.image.load('background.png')



#Title and  Icon
pygame.display.set_caption('Space Invaders')
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
playerimg=pygame.image.load('Player.png')
playerX=370
playerY=480
playerX_change=0

#Enemy
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy1.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#Bullet
bulletimg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state='ready'

#Score
score_val=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#Game Over
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score=font.render('Score:'+str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text=over_font.render('GAME OVER',True,(255,255,255))
    screen.blit(over_text,(200,250))


def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletimg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False
#Game Loop
running=True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
             playerX_change=-5   
            if event.key==pygame.K_RIGHT:
                playerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state=='ready':
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0

# checking bouindaries of spaceship
    playerX+=playerX_change 

    if playerX<=0:
        playerX=0 
    elif playerX>=736:
        playerX=736

#Enemy Movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[i]=2000
            bulletY_change=0
            game_over_text()
            break

        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
        
        #Collision
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_sound=mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY=480
            bullet_state='ready'
            score_val+=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)

#Bullet Movement
    if bulletY<=0:
        bulletY=480
        bullet_state='ready'

    if bullet_state=='fire':
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)
    
    pygame.display.update()

