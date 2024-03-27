######################匯入模組######################
import pygame
import sys
import os
import random
####################定義函式######################
def gophers_update():
    global tick,pos,score
    if tick>max_tick:
        new_pos=random.randint(0,5)
        pos=pos6[new_pos]
        tick=0
    else:
        tick+=1
    screen.blit(gopher,(pos[0]-gopher.get_width()/2,pos[1]-gopher.get_height()/2))
def score_update():
    score_sur=score_font.render(str(score),False,red)
    screen.blit(score_sur,(10,10))
def check_click(pos,x_min,y_min,x_max,y_max):
    x_match=x_min<pos[0]<x_max
    y_match=y_min<pos[1]<y_max
    if x_match and y_match:
        return True
    else:
        return False
    screen.blit(gophers,(pos[0]-gophers.get_width()/2,pos[1]-gophers.get_height()/2))
####################初始化######################
os.chdir(sys.path[0])
pygame.init()
blue = (0,0,255)
white=(255,255,255)
black = (0,0,0)
red = (255,0,0)
clock = pygame.time.Clock()
tick = 0
max_tick = 20
bg_img='Gophers_BG_800x600.png'
bg=pygame.image.load(bg_img)
bg_x=bg.get_width()
bg_y=bg.get_height()

######################建立視窗######################
bg_x = 800
bg_y = 600
screen = pygame.display.set_mode([bg_x,bg_y])
pygame.display.set_caption("打地鼠")
######################背景物件######################
# 將背景填滿黑色
######################地鼠物件######################
pos6 = [[195,305],[400,305],[610,305],[195,450],[400,450],[610,450]]

# pos6 = [[200,200],[300,200],[400,200],[200,300],[300,300],[400,300]]
pos = pos6[0] # 外圍記錄圓的位子
gopher = pygame.image.load("Gophers150.png") # 地鼠圖片
gophers=pygame.image.load('Gophers_BG_800x600.png')
######################分數物件######################
score=0
typeface=pygame.font.get_default_font()
score_font=pygame.font.Font(typeface,24)
######################滑鼠物件######################

######################循環偵測######################
while True:
    clock.tick(30)
    mouse_pos=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if check_click(mouse_pos,pos[0]-50,pos[1]-50,pos[0]+50,pos[1]+50):
                tick=max_tick+1
                score+=1
                
    screen.blit(bg,(0,0))

    gophers_update()
    score_update()
    pygame.display.update()