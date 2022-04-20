# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 17:02:32 2021

@author: 82706
"""

import pygame
import os

def walking(screen):


    pygame.init()
    pygame.key.set_repeat(150, 150) # To make the character keep moving when hold one key,but with 150ms lag
    # screen=pygame.display.set_mode([900,600]) # Set the scale of the screen
    Map = [] #Use list to contain the map image
    House =[]

    class Character(object):
        def __init__(self,Name,Image,Direction,Point,Clock):
            #"name，Direction is player image list，point used to show which move next，times to repeat the animation(Action delay)"
            self.Name=Image
            self.Image=Image
            self.Direction=Direction
            self.Point = Point
            self.Clock = Clock
    class Terrain(object):
        def __init__(self,Image,name):
            self.Image=Image
            self.name=name

    ground = Terrain(pygame.image.load('image/grass1.png').convert_alpha(),"ground")
    # Use to generate the ground
    house1 = pygame.image.load('image/room1.png').convert_alpha()
    house2 = pygame.image.load('image/room2.png').convert_alpha()
    house3 = pygame.image.load('image/room3.png').convert_alpha()
    house4 = pygame.image.load('image/room5.png').convert_alpha()
    Housetype = [house1,house2,house3,house4]
    roof1 =pygame.image.load('image/roof1.png').convert_alpha()
    roof2 =pygame.image.load('image/roof2.png').convert_alpha()
    roof3 =pygame.image.load('image/roof3.png').convert_alpha()
    roof4 =pygame.image.load('image/roof4.png').convert_alpha()
    player = Character('player',
    [
    [pygame.image.load('image/3.png').convert_alpha(),
    pygame.image.load('image/1.png').convert_alpha(),
    pygame.image.load('image/2.png').convert_alpha()],
    [pygame.image.load('image/3.png').convert_alpha(),
    pygame.image.load('image/1.png').convert_alpha(),
    pygame.image.load('image/2.png').convert_alpha()],
    [pygame.image.load('image/left.png').convert_alpha(),
    pygame.image.load('image/left1.png').convert_alpha(),
    pygame.image.load('image/left2.png').convert_alpha()],
    [pygame.image.load('image/right.png').convert_alpha(),
    pygame.image.load('image/right1.png').convert_alpha(),
    pygame.image.load('image/right2.png').convert_alpha()]
    ]
    ,0,0,0)
    pygame.mixer.music.load('image/music.mp3')
    pygame.mixer.music.play(loops=-1)
    Tree = pygame.image.load('image/tree1.png').convert_alpha()
    # load in the trees' image
    for i in range(40):
    #40 is the length of the map, in fact you can put any number here,
    #but that will make the map too big which will be hard to find boundry.
        row=[] # Add the ground by list, add empty list in orderly first.

        for j in range(40): # the width of the map
            row.append([ground,'']) #Add the grass image into the list, '' used to store the name of object
        Map.append(row) # Add the whole list into map list

    Player_location = [8,8] #Set the orignal coordinate of the player
    flower= pygame.image.load('image/flower.png').convert_alpha()
    sand = pygame.image.load('image/sand.png').convert_alpha()
    isaac = pygame.image.load('image/isaac.png').convert_alpha()
    hole = pygame.image.load('image/hole.png').convert_alpha()
    Flower=[]
    Flowertype=[flower,sand,isaac,hole]
    Roof=[]
    Rooftype=[roof1,roof2,roof3,roof4]
    def add_roof(x,y,roofs):
        Roof.append([x,y,roofs])
    add_roof(10,9,0)
    add_roof(20,4,1)
    add_roof(18,15,2)
    add_roof(27,10,3)
    def add_flower(x,y,z):
        Flower.append([x,y,z])
    add_flower(8,6,0)
    add_flower(13,6,0)
    add_flower(8,8,0)
    add_flower(20,9,2)
    add_flower(17,22,0)
    add_flower(17,24,3)
    add_flower(27,16,3)
    add_flower(27,6,3)
    for i in range(5,20):
        add_flower(7,i,1)
    for i in range(7,27):
        add_flower(i,15,1)

    for i in range(20,28,2):
        add_flower(8,i,0)
    for i in range(10,16):
        add_flower(22,i,1)
        add_flower(21,i,1)
    for i in range(16,22):
        add_flower(22,i,1)
    for i in range(20,22):
        add_flower(i,21,1)
    for i in range(20,25,2):
        add_flower(25,i,0)
    def add_tree(location):
        Map[location[0]][location[1]-1][1] = 'tree_image' #put tree image into '' in the list


    for i in range(0,39,2): # because of the tree image has 2 lattice in length and width, so every 2 lattices we put one tree
        for j in range(-1,39,2): # i means from left to right of the screen, j means from top to bottom of the screen
            if j<7 or j >29 or i<8 or i>31:
                add_tree([i,j]) #
    # 7,29,8,31 are the boundry of the map, in order to avoid error like index out of list,
    # we put trees to avoid player walk out of the map
    def add_house(x0,y0,houses):
       House.append([x0,y0,houses])
    add_house(10,9,0)
    add_house(20,4,1)
    add_house(18,15,2)
    add_house(27,10,3)

    talk1=pygame.image.load('image/Thor1.png').convert_alpha()
    talk2=pygame.image.load('image/isaac1.png').convert_alpha()
    talk3=pygame.image.load('image/thor2.png').convert_alpha()
    talk4=pygame.image.load('image/isaac2.png').convert_alpha()
    talks=[talk1,talk2,talk3,talk4]
    pointer=-1
    massage=pygame.image.load('image/welcome.png').convert_alpha()
    massage1=pygame.image.load('image/massage2.png').convert_alpha()
    massage2=pygame.image.load('image/massage3.png').convert_alpha()
    def hitup1():
        for i in House:
            if i[0] in range(4,8) and i[1]==0:
                return False
            elif Player_location[0] in range(21,25) and Player_location[1]==12:
                return False
            elif Player_location[0] in range(28,32) and Player_location[1]==18:
                return False
            elif Player_location[0] in range(19,23) and Player_location[1]==23:
                return False
            elif Player_location[0]==21 and Player_location==13:
                return False
            elif Player_location[1]==30 and Player_location[0] in range(19,21):
                return False
            elif Player_location[1]==22 and Player_location[0] in range(29,31):
                return False
            elif Player_location[1]==12 and Player_location[0] in range(29,31):
                return False

            else:
                return True
    def hitleft1():
         for i in House:
            if i[1] in range(1,5) and i[0]==8:
                return False
            elif Player_location[0]==20 and Player_location[1] in range(8,12):
                return False
            elif Player_location[0]==27 and Player_location[1] in range(15,18):
                return False
            elif Player_location[0]==18 and Player_location[1] in range(19,23):
                return False
            elif Player_location[0]==20 and Player_location[1] in range(12,14):
                return False
            elif Player_location[0]==18 and Player_location[1] in range(27,30):
                return False
            elif Player_location[0]==28 and Player_location[1] in range(19,22):
                 return False
            elif Player_location[0]==28 and Player_location[1] in range(9,12):
                 return False

            else:
                return True
    def hitright1():
         for i in House:
            if i[0]==3 and i[1] in range(1,5):
                return False
            elif Player_location[0]==25 and Player_location[1] in range(8,12):
                return False
            elif Player_location[0]==23 and Player_location[1] in range(19,23):
                return False
            elif Player_location[0]==22 and Player_location[1] in range(12,14):
                return False
            elif Player_location[0]==21 and Player_location[1] in range(27,30):
                return False
            elif Player_location[0]==31 and Player_location[1] in range(19,22):
                 return False
            elif Player_location[0]==31 and Player_location[1] in range(10,12):
                 return False
            else: return True
    def hitdown1():
         for i in House:

            if Player_location[0] in range(11,15) and Player_location[1]==13:
                return False
            elif Player_location[0] in range(28,32) and Player_location[1]==14:
                return False
            elif Player_location[0] in range(19,23) and Player_location[1]==19:
                return False
            elif Player_location[0] in range(19,21) and Player_location[1]==26:
                return False
            elif Player_location[0] in range(29,31) and Player_location[1]==18:
                return False
            elif Player_location[0] in range(29,31) and Player_location[1]==8:
                return False
            else:
                return True










    def refresh(): # This function is to refresh the screen to show elements
        # global screen
        # global ground
        # global house1

    # one lattice in this game will be 60 pixel, so the screen will be 10*15
        for i in range(0,10):
            for j in range(0,15):
                screen.blit((Map[Player_location[0]-7+j][Player_location[1]-5+i][0]).Image,[j*60,i*60])
    #According to the player location to call the ground images which are already put in Map list,
    #Horizontal coordinate-7 because of there are 7 lattices for putting trees,so ground will be put from the left of the screen,
    #ordinate coordinate as well
    #Then the ground will be added line by line
        for i in range(-1,15):#Becuase of the tree is 2 lattices long and wide, so put tree from 1 lattice out of the screen
            for j in range(-1,15):
                if  Map[Player_location[0]-7+j][Player_location[1]-7+i][1] == 'tree_image':
                    screen.blit(Tree,[j*60,(i-1)*60])


        for i in House:
            screen.blit(Housetype[i[2]],[i[0]*60,i[1]*60])

        for i in Flower:
            screen.blit(Flowertype[i[2]],[i[0]*60,i[1]*60])

    # we have already left 'tree_image' this string into Map list, so if is 'tree_image' we put one tree here
        if player.Clock ==0 :
            screen.blit(player.Image[player.Direction][0],[7*60,4*60])
    # Clock=0 means the walking animation is finished, then put the image on the center of the screen
        else:
            player.Clock -=1
            screen.blit(player.Image[player.Direction][1+player.Point%2],[7*60,4*60])
            if player.Clock == 0:
                player.Point +=1
        for i in Roof:
            screen.blit(Rooftype[i[2]],[i[0]*60,i[1]*60])

        if pointer<=3 and pointer!=-1:
            screen.blit(talks[pointer],[420,360])
        if Player_location[0] in range(8,11) and Player_location[1] in range(8,11):
            screen.blit(massage,[0,0])
        if Player_location[0] in range(20,23) and Player_location[1] in range(13,15):
            screen.blit(massage1,[0,0])
        if Player_location[0] in range(18,22) and Player_location[1] in range(26,31):
            screen.blit(massage2,[0,0])
        if Player_location[0] in range(28,32) and Player_location[1] in range(18,22):
            screen.blit(massage2,[0,0])
        if Player_location[0] in range(28,32) and Player_location[1] in range(8,13):
            screen.blit(massage2,[0,0])



    # We set the clock=10 below to show player's full animation by 10times, it's really quick
    # every time colck-1 images like move left foot or right foot will be showed on the screen



    while True:


        refresh()


        pygame.display.flip()

        pygame.time.delay(20)





        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)
    #Move the players
            if event.type==pygame.KEYDOWN and player.Clock == 0: # Clock=0 means, player has finished last animation
                if event.key==pygame.K_w:
                    if player.Direction == 1 and Player_location[1]>8 and hitup1():# To see whether player is at the boundry,if so, it cannot move
                        Player_location[1]-=1
                        for i in House:
                            i[1]+=1
                        for i in Flower:
                            i[1]+=1
                        for i in Roof:
                            i[1]+=1
                      #if player face up and is not reach the top boudry, oridinate coordinate-1(move up)
                    else: #else it remains it direction and no moves
                        player.Direction = 1
                    player.Clock = 10 # Action delay will be set to 10 times, to show the full animation
                elif event.key==pygame.K_a:
                    if player.Direction == 2 and Player_location[0]>8 and hitright1():
                        Player_location[0]-=1
                        for i in House:
                            i[0]+=1
                        for i in Flower:
                            i[0]+=1
                        for i in Roof:
                            i[0]+=1
                    else:
                        player.Direction = 2
                    player.Clock = 10
                elif event.key==pygame.K_s:
                    if player.Direction == 0 and 31>Player_location[1] and hitdown1():
                        Player_location[1]+=1
                        for i in House:
                            i[1]-=1
                        for i in Flower:
                            i[1]-=1
                        for i in Roof:
                            i[1]-=1

                    else:
                        player.Direction = 0
                    player.Clock = 10
                elif event.key==pygame.K_d:
                    if player.Direction == 3 and 31>Player_location[0] and hitleft1():
                        Player_location[0]+=1
                        for i in House:
                            i[0]-=1
                        for i in Flower:
                            i[0]-=1
                        for i in Roof:
                            i[0]-=1

                    else:
                        player.Direction = 3
                    player.Clock = 10
                elif event.key == pygame.K_e:
                    if Player_location[0] in range(20,23) and Player_location[1] in range(13,15):

                        if pointer<=3:
                           pointer+=1
                        else:
                           pointer=-1
                elif event.key== pygame.K_f:
                    if Player_location[0] in range(18,22) and Player_location[1] in range(26,31):
                       return True
                    elif Player_location[0] in range(28,32) and Player_location[1] in range(18,22):
                        return True
                    elif Player_location[0] in range(28,32) and Player_location[1] in range(8,13):
                        return True

                    
                
                    
                
   

                
                
