# i=0
# while True:
#     print( i)
#     if i>=10:
#         i=0
#     else:
#         i+=1
#######################匯入模組#####################
import pygame
import sys
import os
from pygame.locals import *
#######################初始化#######################
os.chdir(sys.path[0])
pygame.init()
LIMIT_LOW=140
clock=pygame.time.Clock()
red=(255,0,0)
######################載入圖片物件##################
img=pygame.image.load('image/bg.png')
img_dinosaur=[
    pygame.image.load('image/小恐龍1.png'),
    pygame.image.load('image/小恐龍2.png'),
]
img_cati=pygame.image.load('image/cacti.png')
bg_x=img.get_width()
bg_y=img.get_height()
bg_roll_x=0
#####################分數物件#######################
score=0
typeface=pygame.font.get_default_font()
score_font=pygame.font.Font(typeface,36)
#####################恐龍物件#######################
ds_x=50
ds_y=LIMIT_LOW
ds_index=0
jumpstate=False
jumpvalue=0
jumpheight=13
ds_center_x=ds_x+img_dinosaur[0].get_width()/2
ds_center_y=ds_y+img_dinosaur[0].get_height()/2
ds_detect_r=min(img_dinosaur[0].get_width(),img_dinosaur[0].get_height())/2
#####################仙人掌物件#######################
catci_x=bg_x-100
catci_y=LIMIT_LOW
catci_shift=10
catci_center_x=catci_x+img_cati.get_width()/2
catci_center_y=catci_y+img_cati.get_height()/2
catci_detect_r=max(img_cati.get_width(),img_cati.get_height())/2-15
######################建立視窗######################
screen=pygame.display.set_mode([bg_x,bg_y])
pygame.display.set_caption('Dinosaur')
######################定義函式######################
def bg_update():
    global bg_roll_x
    bg_roll_x=(bg_roll_x-10)%bg_x
    screen.blit(img,(bg_roll_x-bg_x,0))
    screen.blit(img,(bg_roll_x,0))
def move_dinosaur():
    global ds_y,jumpstate,jumpvalue,ds_index
    if jumpstate:
        if ds_y>=LIMIT_LOW:
            jumpvalue=-jumpheight
        if ds_y<=0:
            jumpvalue=jumpheight
        ds_y+=jumpvalue
        jumpvalue+=1
        if ds_y>=LIMIT_LOW:
            jumpstate=False
            ds_y=LIMIT_LOW
    ds_index=(ds_index-1)% len(img_dinosaur)
    ds_center_x=ds_x+img_dinosaur[ds_index].get_width()/2
    ds_center_y=ds_y+img_dinosaur[ds_index].get_height()/2
    screen.blit(img_dinosaur[ds_index],(ds_x,ds_y))
def move_cacti():
    global catci_x,score
    catci_x=(catci_x-catci_shift)%(bg_x-100)
    screen.blit(img_cati,(catci_x,catci_y))
    if catci_x<=0:
        score+=1
def score_update():
    score_sur=score_font.render(str(score),True,red)
    screen.blit(score_sur,[10,10])
def is_hit(x1,y1,x2,y2,r):
    """圓形碰撞偵測"""
    if ((x1-x2)**2+(y1-y2)**2<(r*r)):
        return True
    else:
        return False
######################循環偵測######################
while True:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==KEYDOWN:
            if event.key==pygame.K_SPACE and ds_y<=LIMIT_LOW:
                jumpstate=True
    bg_update()
    move_dinosaur()
    score_update()
    move_cacti()
    pygame.display.update()