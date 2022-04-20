# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 20:07:52 2021

@author: 49280
"""

import pygame
import math
from random import randint
'''
#gamestart(screen-length,screen-width,player-x,player-y,player-image,background-image,
mode: string with seven digit, enemy-list with 8 elements, item-list with 6 elements,
spells1-bullets-list with 6 elements, spells2-bullets-list with 6 elements,
spells3-bullets-list with 6 elements)

game mode(0000000-9999999):
    1st: have no enemy then 0, if > 0 then number of enemies
    2nd: have no pick-up items then 0, if > 0 then number of items in the screen at the same time
    3rd: have no time limit then 0, if > 0 then how many 10s you have
    4th: extension of 3rd, time limit = 3rd*10s + 4th*10s
    5th: have no score requirement then 0, if > 0 then how many score should get
    6th: extension of 5th, score requirement = 5th + 6th
    7th: if 0 then items will never refresh after an item picked, if >0 then a new item will be added in a random place when another item picked
    For example, 5294921 means a game require (9+2) score in (90+40) seconds, the field have 5 enemies and 2 items, an new item will refresh when another picked

enemy ([0,0,0,0,0,0,0,0]):
    1st and 2nd: minimum and maximum of x(*100), enemy will only appears randomly in this areas, if 1st = 2nd, will not landed randomly.
    3rd and 4th: minimum and maximum of y(*100), enemy will only appears randomly in this areas, if 3rd = 4th, will not landed randomly.
    5th: movement type, 0-never move, 1-horizonal, 2-vertical, 3-diagonal
    6th: max movement speed(*0.05)
    7th: 0-cannot spell, 1-can use spell1, 2-can use spell2, 3-can use spell3, 4-can use 1 and 2, 5-can use all the spells
    8th: image of enemy

spells1-3(3types of bullets)([0,0,0,0,0,0]):
    1st: image of bullets
    2nd: number of bullets in 1 spell
    3rd: speed
    4th: spell type, 0-straightly shoot, 1-draw a circle
    5th: angle range, if there are more than 1 bullets, their angles will be divided into different angles in this range.
    6th: how large the bullets are
    
item ([0,0,0,0,0,0]):
    1st and 2nd: same as enemy
    3rd and 4th: same as enemy
    5th: movement speed
    6th: image of items
    
    

'''



def battlegame(length,width,px,py,pimage,bgimage,gamemode,enemy,item,spells1,spells2,spells3):
    #init for my own testing,if done in outer code, they can be removed
    pygame.init()
    pygame.font.init()
    logo = pygame.image.load("art/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Battle Start")
    #Screen
    screen = pygame.display.set_mode((length,width))
    #If user didn't put a background image(leave a 0), the screen will be a blank white screen
    if bgimage:
        background_image = pygame.image.load(bgimage)
    else:
        screen.fill((255,255,255))
    #Game mode
    gmcode = [0,0,0,0,0,0,0]
    for i in range(0,7):
        gmcode[i] = int(gamemode[i])
    #Player
    px = px
    py = py
    player_image = pygame.image.load(pimage)
    player_speed = length*0.005
    player_statementtext = pygame.font.SysFont('Ariel',30)
    #An effect showing player is immune now
    player_immune_color = 255
    #Set a visible edge
    length*=0.95
    width*=0.95
    #If hp become 0 then die
    player_hp_max = player_hp = 3
    #Statement
    player_dead = False
    running = True 
    playing = True
    #Will not get hurt again in short time after getting hurt
    player_immune_time = 250
    screen.blit(player_image,(px,py))
    
    default_area = 32
    #[0-active,1-x,2-y,3-spelltype,4-movement type,5-movement speed]
    enemy_group = [[0,0,0,0,0,0]]*100
    #[0-active,1-x,2-y,3-angle,4-speed,5-how large,type]
    if spells1[0]:
        bullet1_image = pygame.image.load(spells1[0])
        bullet1_large = spells1[5]
        bullet1_group = [[0,0,0,0.00,0.00,0,0]]*1000
    if spells2[0]:
        bullet2_image = pygame.image.load(spells2[0])
        bullet2_large = spells2[5]
        bullet2_group = [[0,0,0,0.00,0.00,0,0]]*1000
    if spells3[0]:
        bullet3_image = pygame.image.load(spells3[0])
        bullet3_large = spells3[5]
        bullet3_group = [[0,0,0,0.00,0.00,0,0]]*1000
     
    #[0-active,1-horizon(0) or vertical(1),2-x or y,3-image_reminder,4-image_affects,5-movespeed,6-width]
    #beam_group = [[0,0,0,0,0,0,0]]*1000
    #[0-active,1-x,2-y,3-angle,4-speed,5-score earn when pick,6-type]
    item_group = [[0,0,0,0,0,0,0]]*1000
    #load enemies   
    if gmcode[0] > 0:
        enemy_image = pygame.image.load(enemy[7])
        for i in range(0,gmcode[0]):
            #Initialize the position
            enemy_group[i] = [1,100*randint(enemy[0],enemy[1]),100*randint(enemy[2],enemy[3]),enemy[6],enemy[4],randint(1,enemy[5])]
    #load items    
    if gmcode[1] > 0:
        item_image = pygame.image.load(item[5])
        for i in range(0,gmcode[1]):
            #Initialize the position
            #[0-active,1-x,2-y,3-angle,4-speed,5-score earn when pick,6-movement type]
            item_group.insert(i,[1,100*randint(item[0],item[1]),100*randint(item[2],item[3]),randint(0,360),item[4],1,randint(3,6)])
    #time limit
    time_start = time_now = pygame.time.get_ticks()
    time_used = 0
    if gmcode[2] > 0:
        time_limit = 10000*(gmcode[2]+gmcode[3])
    else:
        time_limit = 0
    #score requirement
    score_now = 0
    if gmcode[4] > 0:
        score_require = gmcode[4]+gmcode[5]
    else:
        score_require = 0
    #spelling(how many bullects, where to spawn:x2,y2, speed, how large the bullets are, rotate speed)        
    def spelling1(n,x2,y2,s,area,turning):
        for i in range(0,n):
            angle = i*180/n
            bullet1_group.insert(0,[1,x2,y2,angle,s,area,turning])
        return
    def spelling2(n,x2,y2,s,area,turning):
        for i in range(0,n):
            angle = i*60/n
            bullet1_group.insert(0,[1,x2,y2,angle,s,area,turning])
        return
    def spelling3(n,x2,y2,s,area,turning):
        for i in range(0,n):
            angle = i*10/n
            bullet1_group.insert(0,[1,x2,y2,angle,s,area,turning])
        return
    
    def endgame(text,dead):
        global playing,player_dead
        playing = False
        font_dead = pygame.font.SysFont('Ariel',50)
        font_dead_reason = pygame.font.SysFont("Ariel",30)
        font_dead_again = pygame.font.SysFont("Ariel",30)
        if dead:
            font_dead_render = font_dead.render("Failed!",False,(255,0,0),(0,0,0))
            font_dead_reason_render = font_dead_reason.render(text,False,(255,0,0),(0,0,0))
            font_dead_again_render = font_dead_again.render("Press [Enter] to try again",False,(255,0,0),(0,0,0))
        else:
            font_dead_render = font_dead.render("Well done!",False,(0,255,0),(0,0,0))
            font_dead_reason_render = font_dead_reason.render(text,False,(0,255,0),(0,0,0))
            font_dead_again_render = font_dead_again.render("Press [Enter] to continue",False,(0,255,0),(0,0,0))
        mid = int(width/3)
        lenmid = int(length/3)
        screen.blit(font_dead_render,(lenmid,int(mid-30)))
        screen.blit(font_dead_reason_render,(lenmid-20,int(mid+30)))
        screen.blit(font_dead_again_render,(lenmid-20,int(mid+60)))
        pygame.display.update()
        return False
        
        
    #Start game loop
    while running:
        #Check the key pressed 60 times per second
        pygame.time.Clock().tick(60)
        if playing:
            #Timer records the time used
            time_now = pygame.time.get_ticks()
            time_used = time_now - time_start
            if bgimage:
                screen.blit(background_image,(0,0))
            else:
                screen.fill((255,255,255))
            if player_immune_time:
                pygame.draw.circle(player_image, (255,255,0), (px,py), 40,width=0)
                player_immune_time-=1
            if time_used%200 == 0 and time_used>0:#per 2 seconds
                random_enemy = randint(0,gmcode[0])
                random_enemy_x = enemy_group[random_enemy][1]
                random_enemy_y = enemy_group[random_enemy][2]
                #0-cannot spell, 1-can use spell1, 2-can use spell2, 3-can use spell3, 4-can use 1 and 2, 5-can use all the spells
                if enemy[6] in [1,4,5]:
                    spelling1(spells1[1],random_enemy_x,random_enemy_y,spells1[2],spells1[5],spells1[4])
                    random_enemy = randint(0,gmcode[0])
                    random_enemy_x = enemy_group[random_enemy][1]
                    random_enemy_y = enemy_group[random_enemy][2]
                if enemy[6] in [2,4,5]:
                    spelling2(spells2[1],random_enemy_x,random_enemy_y,spells2[2],spells2[5],spells2[4])
                    random_enemy = randint(0,gmcode[0])
                    random_enemy_x = enemy_group[random_enemy][1]
                    random_enemy_y = enemy_group[random_enemy][2]
                if enemy[6] in [3,5]:
                    spelling3(spells3[1],random_enemy_x,random_enemy_y,spells3[2],spells3[5],spells3[4])
            if time_used >= time_limit :
                if score_now < score_require:
                    player_dead = True
                    playing = endgame(f"You must get {score_require} scores in {time_limit/1000} seconds!",1)
                else:
                    playing = endgame("You survived enough time!",0)
            for i in range(0,50):
                if enemy_group[i][0]:#Move the enemy
                #[0-active,1-x,2-y,3-spelltype,4-movement type,5-movement speed]
                    if enemy_group[i][4]:
                        if enemy_group[i][4] in [1,3,4]:
                            enemy_group[i][1] += enemy_group[i][5]
                        if enemy_group[i][4] in [2,4,5]:
                            enemy_group[i][2] += enemy_group[i][5]
                        if enemy_group[i][4] in [5,6]:
                            enemy_group[i][1] -= enemy_group[i][5]
                        if enemy_group[i][4] in [3,6]:
                            enemy_group[i][2] -= enemy_group[i][5]
                        if enemy_group[i][4] == 1 and (enemy_group[i][1] >= length or enemy_group[i][1] <= 0):
                            enemy_group[i][5] *= -1
                        if enemy_group[i][4] == 2 and (enemy_group[i][2] >= width or enemy_group[i][2] <= 0):
                            enemy_group[i][5] *= -1
                        if (enemy_group[i][4] == 3 and enemy_group[i][2] <= 0 and enemy_group[i][1] < length) or (enemy_group[i][4] == 5 and enemy_group[i][2] < width and enemy_group[i][1] <= 0) or (enemy_group[i][4] == 6 and enemy_group[i][2] == 0 and enemy_group[i][1] == 0): 
                            enemy_group[i][4] = 4#↘
                        if (enemy_group[i][4] == 3 and enemy_group[i][2] > 0 and enemy_group[i][1] >= length) or (enemy_group[i][4] == 4 and enemy_group[i][2] < width and enemy_group[i][1] >= length) or (enemy_group[i][4] == 6 and enemy_group[i][2] <= 0 and enemy_group[i][1] > 0):
                            enemy_group[i][4] = 5#↙
                        if (enemy_group[i][4] == 3 and enemy_group[i][2] == 0 and enemy_group[i][1] == length) or (enemy_group[i][4] == 4 and enemy_group[i][2] == width and enemy_group[i][1] == length) or (enemy_group[i][4] == 5 and enemy_group[i][2] >= width and enemy_group[i][1] > 0):
                            enemy_group[i][4] = 6#↖
                        if (enemy_group[i][4] == 4 and enemy_group[i][2] >= width and enemy_group[i][1] < length) or (enemy_group[i][4] == 5 and enemy_group[i][2] == width and enemy_group[i][1] == 0) or (enemy_group[i][4] == 6 and enemy_group[i][2] > 0 and enemy_group[i][1] <= 0):
                            enemy_group[i][4] = 3#↗
                    screen.blit(enemy_image,(enemy_group[i][1],enemy_group[i][2]))
                    #kill the player when touched
                    if abs(px - enemy_group[i][1])<bullet1_large and abs(py - enemy_group[i][2])<bullet1_large and not player_immune_time:
                        player_hp -= 1
                        if player_hp == 0:
                            player_dead = True
                            playing = endgame("Do not touch the enemies!",1)
                        player_immune_time = 250

                if bullet1_group[i][0]:#Move the bullets
                #[0-active,1-x,2-y,3-angle,4-speed,5-how large,6-type:0-straight,>0-turning]
                    bullet1_group[i][3] += 0.03*bullet1_group[i][6]
                    bullet1_group[i][1] += bullet1_group[i][4]*math.cos(bullet1_group[i][3])
                    bullet1_group[i][2] += bullet1_group[i][4]*math.sin(bullet1_group[i][3])
                    screen.blit(bullet1_image,(bullet1_group[i][1],bullet1_group[i][2]))
                    reason1d = abs(px - bullet1_group[i][1])<bullet1_large and abs(py - bullet1_group[i][2])<bullet1_large and not player_immune_time
                    reason1e = bullet1_group[i][1] <= 0 or bullet1_group[i][1] >= length or bullet1_group[i][2]<=0 or bullet1_group[i][2]>= width
                    if reason1d or reason1e:
                        bullet1_group[i][0] = 0
                        bullet1_group.remove(bullet1_group[i])
                        if reason1d:
                            player_hp -= 1
                            player_immune_time = 250
                            if player_hp == 0:
                                player_dead = True
                                playing = endgame("Do not touch the bullets!",1)
                        
                if bullet2_group[i][0]:#Move the bullets
                    bullet2_group[i][3] += bullet2_group[i][6]
                    bullet2_group[i][1] += bullet2_group[i][4]*math.cos(bullet2_group[i][3])
                    bullet2_group[i][2] += bullet2_group[i][4]*math.sin(bullet2_group[i][3])
                    screen.blit(bullet2_image,(bullet2_group[i][1],bullet2_group[i][2]))
                    reason2d = abs(px - bullet2_group[i][1])<bullet2_large and abs(py - bullet2_group[i][2])<bullet2_large and not player_immune_time
                    reason2e = bullet2_group[i][1] <= 0 or bullet2_group[i][1] >= length or bullet2_group[i][2]<=0 or bullet2_group[i][2]>= width
                    if reason2d or reason2e:
                        bullet2_group[i][0] = 0
                        bullet2_group.remove(bullet2_group[i])
                        if reason2d:
                            player_hp -= 1
                            player_immune_time = 250
                            if player_hp == 0:
                                player_dead = True
                                playing = endgame("Do not touch the bullets!",1)
                if bullet3_group[i][0]:#Move the bullets
                    bullet3_group[i][3] += bullet3_group[i][6]
                    bullet3_group[i][1] += bullet3_group[i][4]*math.cos(bullet3_group[i][3])
                    bullet3_group[i][2] += bullet3_group[i][4]*math.sin(bullet3_group[i][3])
                    screen.blit(bullet3_image,(bullet3_group[i][1],bullet3_group[i][2]))
                    reason3d = abs(px - bullet3_group[i][1])<bullet3_large and abs(py - bullet3_group[i][2])<bullet3_large and not player_immune_time
                    reason3e = bullet3_group[i][1] <= 0 or bullet3_group[i][1] >= length or bullet3_group[i][2]<=0 or bullet3_group[i][2]>= width
                    if reason3d or reason3e:
                        bullet3_group[i][0] = 0
                        bullet3_group.remove(bullet3_group[i])
                        if reason3d:
                            player_hp -= 1
                            player_immune_time = 250
                            if player_hp == 0:
                                player_dead = True
                                playing = endgame("Do not touch the bullets!",1)
                if item_group[i][0] == 1:#Move the items
                       #[0-active,1-x,2-y,3-angle,4-speed,5-score earn when pick,6-movement type]
                    if item_group[i][6]:
                        if item_group[i][6] in [1,3,4]:
                            item_group[i][1] += item_group[i][4]
                        if item_group[i][6] in [2,4,5]:
                            item_group[i][2] += item_group[i][4]
                        if item_group[i][6] in [5,6]:
                            item_group[i][1] -= item_group[i][4]
                        if item_group[i][6] in [3,6]:
                            item_group[i][2] -= item_group[i][4]
                        if item_group[i][6] == 1 and (item_group[i][1] >= length or item_group[i][1] <= 0):
                            item_group[i][4] *= -1
                        if item_group[i][6] == 2 and (item_group[i][2] >= width or item_group[i][2] <= 0):
                            item_group[i][4] *= -1
                        if (item_group[i][6] == 3 and item_group[i][2] <= 0 and item_group[i][1] < length) or (item_group[i][6] == 5 and item_group[i][2] < width and item_group[i][1] <= 0) or (item_group[i][6] == 6 and item_group[i][2] == 0 and item_group[i][1] == 0): 
                            item_group[i][6] = 4#↘
                        if (item_group[i][6] == 3 and item_group[i][2] > 0 and item_group[i][1] >= length) or (item_group[i][6] == 4 and item_group[i][2] < width and item_group[i][1] >= length) or (item_group[i][6] == 6 and item_group[i][2] <= 0 and item_group[i][1] > 0):
                            item_group[i][6] = 5#↙
                        if (item_group[i][6] == 3 and item_group[i][2] == 0 and item_group[i][1] == length) or (item_group[i][6] == 4 and item_group[i][2] == width and item_group[i][1] == length) or (item_group[i][6] == 5 and item_group[i][2] >= width and item_group[i][1] > 0):
                            item_group[i][6] = 6#↖
                        if (item_group[i][6] == 4 and item_group[i][2] >= width and item_group[i][1] < length) or (item_group[i][6] == 5 and item_group[i][2] == width and item_group[i][1] == 0) or (item_group[i][6] == 6 and item_group[i][2] > 0 and item_group[i][1] <= 0):
                            item_group[i][6] = 3#↗
                    screen.blit(item_image,(item_group[i][1],item_group[i][2]))
                    #player touch
                    reasondi = abs(px - item_group[i][1])<default_area and abs(py - item_group[i][2])<default_area
                    if reasondi :
                        score_now+= item_group[i][5]
                        if score_now >= score_require:
                            playing = endgame("You got enough score!",0)
                        item_group[i][0]=0
                        item_group.remove(item_group[i]) 
                        #spawn a new item
                        if gmcode[6]:
                            item_group.insert(0,[1,100*randint(item[0],item[1]),100*randint(item[2],item[3]),randint(0,360),item[4],1,randint(3,6)])
            
            player_hp_rate = player_hp/player_hp_max
            if score_require and time_limit:
                player_statementtext_text =(f"===Life:<{player_hp}/{player_hp_max}>   Score:<{score_now}/{score_require}>    Time:<{(time_limit-time_used)/1000}/{time_limit/1000}> ===")
            if not score_require:
                player_statementtext_text = (f"===Life:<{player_hp}/{player_hp_max}>   Score:<Not required>    Time:<{(time_limit-time_used)/1000}/{time_limit/1000}> ===")
            if not time_limit:
                player_statementtext_text =(f"===Life:<{player_hp}/{player_hp_max}>   Score:<{score_now}/{score_require}>    Time:<∞/∞> ===")
            player_statementtext_render = player_statementtext.render(player_statementtext_text,False,(255*(1-player_hp_rate),255*(player_hp_rate),0),(0,0,0))
            screen.blit(player_statementtext_render,(0,0))
            
            
        for event in pygame.event.get():
        # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
               # change the value to False, to exit the main loop
               running = False
               pygame.quit()
        #get keys player pressing
        keys = pygame.key.get_pressed()
        #enter for respawn or go to next scene
        if keys[pygame.K_RETURN] and playing == False:
            if player_dead:
                #Open the game again
                battlegame(length,width,px,py,pimage,bgimage,gamemode,enemy,item,spells1,spells2,spells3)
                return
            if not player_dead:
                return 1#this function will return 1, standing for victory
                pygame.quit()#This line just for testing, please delete when using!
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and px<length and playing:
            px += player_speed
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and py>0 and playing:
            py -= player_speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and py<width and playing:
            py += player_speed
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and px > 0 and playing:
            px -= player_speed
        
        screen.blit(player_image,(px,py)) 
        
        if player_immune_time:
            if time_used%2 == 0:
                if player_immune_color == 255:
                    player_immune_color = 0
                else:
                    player_immune_color = 255
            pygame.draw.circle(screen, (255,player_immune_color,0), (px+15,py+15), 30,width = 10)
        if playing:
            pygame.display.update()#updates after every pictures on the screen have blited
        
'''    
***An simple example***
battlegame(600,400,300,200,"art/seal32x32.png",0,"5230911",[1,5,1,3,3,1,1,"art/bear32x32walk1.png"],[1,5,1,3,2,"art/fish1fish32x32.png"],["art/bullet32x32.png",2,2,0,0,32],["art/bullet32x32.png",2,2,0,0,32],["art/bullet32x32.png",2,2,0,0,32])
battlegame(600,400,300,200,"art/seal32x32.png",0,"4030001",[1,5,1,3,3,1,5,"art/bear32x32walk1.png"],[1,5,1,3,2,"art/fish1fish32x32.png"],["art/bullet32x32.png",2,2,0,0,32],["art/bullet32x32.png",2,2,0,0,32],["art/bullet32x32.png",2,2,0,0,32])
battlegame(1000,500,900,400,"art/seal32x32.png",0,"9433911",[1,9,1,4,1,5,5,"art/bear32x32walk1.png"],[1,9,1,3,2,"art/fish1fish32x32.png"],["art/bullet32x32.png",8,2,0,0.5,32],["art/bullet32x32.png",16,3,0,0,32],["art/bullet32x32.png",1,5,0,0,32])
battlegame(600,400,300,200,"art/seal32x32.png","art/background600x400.png","4030001",[1,5,1,3,3,1,5,"art/bear32x32walk1.png"],[1,5,1,3,2,"art/fish1fish32x32.png"],["art/bullet32x32.png",2,2,0,0,32],["art/bullet32x32.png",2,2,0,0,32],["art/bullet32x32.png",2,2,0,0,32])

'''         
    
        
            
