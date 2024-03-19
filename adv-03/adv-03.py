###################匯入模組###################
import pygame
import sys
import math
import os
import sys
import time
import random
###################初始化####################
os.chdir(sys.path[0])
width = 500
height= 500
pygame.init()
bg_img="snow.jpg"
bg=pygame.image.load(bg_img)
BLACK=(255,255,255)
bg_x=bg.get_width()
bg_y=bg.get_height()
##################定義函式##################
WHITE=(255,255,255)
def check_click(pos,x_mix,y_mix,x_max,y_max):
    x_match=x_mix<pos[0]<x_max
    y_match=y_mix<pos[1]<y_max
    if x_match and y_match:
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.play()
        pygame.mixer.music.fadeout(600000)
        time.sleep(0.1)
        return True
    else:
        return False
def snow_fall():
    """下雪"""
    

    # global x_site,y_site,x_shift,radius
    for snow in snow_list:
        #畫出雪花
        pygame.draw.circle(screen,WHITE,(snow["x_site"],snow ["y_site"]),snow ["radius"])
        #計算雪花下次顯示的座標
        snow["x_site"]+=snow["x_shift"]
        snow["y_site"]+=snow["radius"]
        #如果雪花落出畫面，重新設置
        if snow["y_site"]>bg_y or snow["x_site"]>bg_x:
            snow["y_site"]=random.randint(-bg_y,-1)
            snow["x_site"]=random.randint(0,bg_x)
###################建立視窗及物件###################
#設定窗大小
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Minecraft")
screen=pygame.display.set_mode((bg_x,bg_y))
pygame.display.set_caption("snow")
###################撥放音樂###################
mp3_path="snow-dream.mp3"
pygame.mixer.music.load(mp3_path)
pygame.mixer.music.play()
pygame.mixer.music.fadeout(600000)
pygame.mixer.music.pause()#暫停音樂
###################設定文字###################
typeface=pygame.font.get_default_font()
font=pygame.font.Font(typeface,24)
title=font.render("Start",True,(0,0,0))
tw=title.get_width()
th=title.get_height()
###################設定雪花基本參數###########
snow_list=[]

for i in range(1500):
    x_site=random.randrange(10,bg_x)#雪花圓心位置
    y_site=random.randrange(-bg_y,1000)#雪花圓心位置
    x_shift=random.randint(-5,1)#x軸偏移量
    radius=random.randint(2,4)#半徑和y下降量
    snow_list.append({"x_site":x_site,"y_site":y_site,"x_shift":x_shift,"radius":radius})
    
###################新增fps###################
clock=pygame.time.Clock()
###################建立畫布###################
# bg=pygame.Surface((width,height))
# bg.fill((0,0,0))
###################循環偵測###################
paint=False
cnt=0
while True:
    clock.tick(60)
    mouse_pos=pygame.mouse.get_pos()
    # print(mouse_pos)
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if check_click(mouse_pos,0,0,tw,th):
                paint=not paint
    if cnt>10:
        cnt=0
        x_shift=random.randint(-3,3)
    else:
        cnt+=1
    screen.blit(bg,(0,0))
    screen.blit(title,(0,0))
    if paint:
        title=font.render("Dio",True,BLACK)
        pygame.mixer.music.unpause()
        snow_fall()
        bg_img="snow.jpg"
        bg=pygame.image.load(bg_img)
    else:
        title=font.render("jojo",True,BLACK)
        pygame.mixer.music.pause()
        bg_img="snow.jpg"
        bg=pygame.image.load(bg_img)
    # screen.blit(bg ,(0, 0))
    # screen.blit(title,(0,0))
    pygame.display.update()
