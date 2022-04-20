#!/usr/bin/env python
#
#
#
#
#

# documentation string of this module
"""
Minimal pygame program.
"""
# some informational variables
__author__    = "$Author: DR0ID $"
__version__   = "$Revision: 109 $"
__date__      = "$Date: 2007-04-03 18:00:40 +0200 (Di, 03 Apr 2007) $"
__license__   = ''
__copyright__ = "DR0ID (c) 2007   http://mypage.bluewin.ch/DR0ID"

#----------------------------- actual code --------------------------------

# import the pygame module, so you can use it
import pygame
import math
from random import randint
dead = False
running = True
screen = pygame.display.set_mode((600,400))
#enemies
bear = [0,0]
bear[0] = pygame.image.load("art/bear32x32walk1.png")
bear[1] = pygame.image.load("art/bear32x32walk2.png")
x = y = 0
bear2 = [0,0]
bear2[0] = pygame.image.load("art/bear32x32walk1.png")
bear2[1] = pygame.image.load("art/bear32x32walk2.png")
x2 = y2 = 0
state2 = 1
bullet = pygame.image.load("art/bullet32x32.png")
#[active,x,y,angle,s,large]
bullet_group = [[0,0,0,0.00,0.00,0]]*1000
#[active,statement,horizon or vertical,x or y,beampic1,beampic2,movespeed,area]
beam_group = [[0,0,0,0,0,0,0,0]]*1000
#[active,x,y,angle,s,score,type]
fish_group = [[0,0,0,0,0,0,0]]*1000
#seal
seal = pygame.image.load("art/seal32x32.png")
sealdead = pygame.image.load("art/sealdead32x32.png")
deadtext = pygame.image.load("art/dead.png")
beam1pic1 = pygame.image.load("art/beam32x600.png")
beam1pic2 = pygame.image.load("art/beamlaser32x600.png")
beam2pic1 = pygame.image.load("art/beam600x32.png")
beam2pic2 = pygame.image.load("art/beamlaser600x32.png")
fishtype1 = pygame.image.load("art/fish1fish32x32.png")
#timer
n = [[0,0],[0,0]]
#Total Time 总时间
TimeCounter = 0
#Score fish eaten 分数 吃了多少鱼
ScoreTotal = 0
#circle画圈圈
def spell1(bear2,x2,y2,n,s,area):
    for i in range(0,n):
        angle = i*180/n
        bullet_group.insert(0,[1,x2,y2,angle,s,area])
    return
#straigt自机狙 incompleted
def spell2(bear,x2,y2,x1,y1,s,area):
    dx = x2 - x1
    dy = y2 - y1
    if dx !=0:
        if dy == 0:
            if dx >0:
                angle = 270
            else:
                angle = 90
        else:
            a = math.atan(abs((dy)/(dx)))*180/math.pi
            if dx > 0 and dx > 0:
                angle = 360 - a
            if dx < 0 and dy > 0:
                angle = 180 + a
            if dx < 0 and dy < 0:
                angle = 180 - a
            if dx > 0 and dx < 0:
                angle = a
    else:
        if dy >= 0:
            angle = 180
        else:
            angle = 0
    bullet_group.insert(0,[1,x2,y2,angle,s,area])
    return            
#Beam 激光
def spell3(dirc,n,s,area):
    ty = [0]*n
    g = [[0,0,0,0,0,0,0,0]]*n
    if dirc == 0:
        for i in range(0,n):
            ty[i] = randint(0,370)
            g[i] = [1,0,0,ty[i],beam2pic1,beam2pic2,s,area]
            beam_group.insert(0,g[i])
            
        return
        #hori
    if dirc == 1:
        for i in range(0,n):
            ty[i] = randint(0,570)
            g[i] = [1,0,1,ty[i],beam1pic1,beam1pic2,s,area]
            beam_group.insert(0,g[i])
        return
        #verti
        
def addfish(x,y,angle,s,score):
    fish_group.insert(0,[1,x,y,angle,s,score,0])
    return
        

def deadseal():
    global dead
    dead = True
    screen.fill((255,0,0))  
    screen.blit(bear[0],(x,y))
    screen.blit(bear2[0],(x2,y2))
    screen.blit(sealdead,pygame.mouse.get_pos())
    screen.blit(deadtext,(236,177))
    pygame.display.flip()
    return
         
            
    
def movearound(s,bear2,x2,y2,state2):
        if state2 == 1:
            x2-=s
            y2-=s
            if x2 <= 0 and y2 > 0:
                state2 = 2
            if x2 <= 0 and y2 <= 0:
                state2 = 4
            if x2 > 0 and y2 <= 0:
                state2 = 3
            lst = [x2,y2,state2]
            return lst
        if state2 == 2:
            x2+=s
            y2-=s
            if x2 >= 570 and y2 > 0:
                state2 = 1
            if x2 >= 0 and y2 <= 0:
                state2 = 4
            if x2 > 570 and y2 <= 0:
                state2 = 3
            lst = [x2,y2,state2]
            return lst
        if state2 == 3:
            x2-=s
            y2+=s
            if x2 <= 0 and y2 >= 0:
                state2 = 4
            if x2 <=0 and y2> 370:
                state2 = 2
            if x2 > 0 and y2>370:
                state2 = 1
            lst = [x2,y2,state2]
            return lst
        if state2 == 4:
            x2+=s
            y2+=s
            if x2 > 570 and y2 <=0:
                state2 = 1
            if x2 > 570 and y2 >= 0:
                state2 = 3
            if x2 < 570 and y2 > 370:
                state2 = 2
            lst = [x2,y2,state2]
            return lst
        
# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    global x,y,x2,y2,state2,dead,running,bullet_group,n,beam_group,TimeCounter,ScoreTotal,fish_group
    # load and set the logo
    logo = pygame.image.load("art/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Seal Protection")

    z = m = 0
    # create a surface on screen that has the size of 600 x 400
    screen.blit(bear[0],(0,0))
    screen.blit(bear2[0],(600,400))
    screen.blit(seal,(300,200))
    pygame.display.flip()
    # define a variable to control the main loop
    screen.fill((255,255,255))
    s = 0.05
    
    # main loop
    while running :
        TimeCounter += 1
        if z <= 50:
            z += 1
        else:
            z = 0
            n[0][0] += 1
            n[1][0] += 1
            #for i in range(0,100):
                #n[i][0] += 1
            if m == 0:
                m += 1
            else:
                m -= 1
        if n[0][0] >= 10:
            if not dead and ScoreTotal >= 2:     
                spell1(bear2,x2,y2,8,s,32)
            n[0][0] = 0
        if n[1][0] >= 2:
            n[1][0] = 0
            if not dead and ScoreTotal >= 1:
                spell2(bear,x,y,pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],0.4,32)
            if not dead:
                sp = 0.01*randint(-10,10)
                dirc = randint(0,1)
                if ScoreTotal >= 5:
                    spell3(dirc,3,sp,32)
                
        if TimeCounter == 100:
            i1 = randint(100,500)
            i2 = randint(100,300)
            addfish(i1, i2, randint(0,360), 0.02 * randint(-10,10), 1)
        # event handling, gets all event from the eventqueue
        if not dead:
            for i in range(10):
                if x< 570 and y<=0:
                    x+=s
                if y<370 and x >= 570:
                    y+=s
                if y>=370 and x>0:
                    x-=s
                if y>0 and x<=0:
                    y-=s
                
                screen.fill((255,255,255))
                screen.blit(bear[m],(x,y))
                x2 = movearound(s,bear2,x2,y2,state2)[0]
                y2 = movearound(s,bear2,x2,y2,state2)[1]
                state2 = movearound(s,bear2,x2,y2,state2)[2]
                screen.blit(bear2[m],(x2,y2))                
                screen.blit(seal,pygame.mouse.get_pos())
                for i in range(0,600):
                    if bullet_group[i][0] == 1:#Move the bullet
                        bullet_group[i][1] += bullet_group[i][4]*math.cos(bullet_group[i][3])
                        bullet_group[i][2] += bullet_group[i][4]*math.sin(bullet_group[i][3])
                        screen.blit(bullet,(bullet_group[i][1],bullet_group[i][2]))
                        if abs(pygame.mouse.get_pos()[0] - bullet_group[i][1])<bullet_group[i][5] and abs(pygame.mouse.get_pos()[1] - bullet_group[i][2])<bullet_group[i][5]:
                            bullet_group[i][0] = 0
                            bullet_group.remove(bullet_group[i])
                            deadseal()
                        if bullet_group[i][1] <= 0 or bullet_group[i][1] >= 600 or bullet_group[i][2]<=0 or bullet_group[i][2]>= 400:
                            bullet_group[i][0] = 0
                            bullet_group.remove(bullet_group[i])
                    if beam_group[i][0] == 1:#active
                        beam_group[i][3] += beam_group[i][6]#Move the beam
                        #[0-active,1-remind or kill,2-horizon or vertical,3-x or y,4-beampic1,5-beampic2,6-movespeed,7-area,width]
                        if beam_group[i][1] < 1000:#remind
                            if beam_group[i][2] == 0:
                                screen.blit(beam_group[i][4],(0,beam_group[i][3]))
                            else:
                                screen.blit(beam_group[i][4],(beam_group[i][3],0))
                            beam_group[i][1] += 1
                        if beam_group[i][1] >= 1000:#kill
                            if beam_group[i][2] == 0:
                                beam_group[i][3] += beam_group[i][6]
                                screen.blit(beam_group[i][5],(0,beam_group[i][3]))
                                if abs(pygame.mouse.get_pos()[1] - beam_group[i][3])<beam_group[i][7]:
                                    beam_group[i][0] = 0
                                    beam_group.remove(beam_group[i])
                                    deadseal()
                            else:
                                screen.blit(beam_group[i][5],(beam_group[i][3],0))
                                if abs(pygame.mouse.get_pos()[0] - beam_group[i][3])<beam_group[i][7]:
                                    beam_group[i][0] = 0
                                    beam_group.remove(beam_group[i])
                                    deadseal() 
                            beam_group[i][1] += 1
                        if beam_group[i][1] >= 2000:#Remove
                            beam_group[i][0] = 0
                            beam_group.remove(beam_group[i])
                    if fish_group[i][0] == 1:#Move the fish
                    #[0-active,1-x,2-y,3-angle,4-speed,5-score,6-type]
                        fish_group[i][1] += fish_group[i][4]*math.cos(fish_group[i][3])
                        fish_group[i][2] += fish_group[i][4]*math.sin(fish_group[i][3])
                        screen.blit(fishtype1,(fish_group[i][1],fish_group[i][2]))
                        reason1 = abs(pygame.mouse.get_pos()[0] - fish_group[i][1])<32 and abs(pygame.mouse.get_pos()[1] - fish_group[i][2])<32
                        reason2 = fish_group[i][1] <= 0 or fish_group[i][1] >= 600 or fish_group[i][2]<=0 or fish_group[i][2]>= 400
                        if reason1 or reason2:
                            if reason1:
                                ScoreTotal += fish_group[i][5]
                                if ScoreTotal%10 == 0:
                                    s += 0.05
                            fish_group[i][0]=0
                            fish_group.remove(fish_group[i])
                            addfish(randint(100,500), randint(100,300), randint(0,360), 0.02 * randint(-10,10), 1)
                            
                if not dead:
                    pygame.display.flip()
                #Dead
                if (abs(pygame.mouse.get_pos()[0]-x) <=32 and abs(pygame.mouse.get_pos()[1] - y) <= 32) or (abs(pygame.mouse.get_pos()[0]-x2) <=32 and abs(pygame.mouse.get_pos()[1] - y2) <= 32):
                    deadseal()
        for event in pygame.event.get():
                # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                pygame.quit()
        keys = pygame.key.get_pressed()  #检查按键是按下
        if keys[pygame.K_RETURN] and dead == True:
            dead = False
            screen.blit(seal,(300,200))
            bullet_group = [[0,0,0,0.00,0.00,0]]*1000
            beam_group = [[0,0,0,0,0,0,0,0]]*1000
            fish_group = [[0,0,0,0,0,0,0]]*1000
            n = [[0,0],[0,0]]
            x = y = x2 = y2 = 0
            z = 0
            s = 0.05
            TimeCounter = 0
            ScoreTotal = 0
            pygame.display.flip()
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()