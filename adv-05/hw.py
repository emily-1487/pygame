######################匯入模組######################
import pygame
import sys
import os
import random
####################定義函式######################
def gophers_update():
    global tick,pos,score,times#使用全域變數
    if tick>max_tick:
        new_pos=random.randint(0,5)
        pos=pos6[new_pos]
        tick=0
        times+=1#次數加一
    else:
        tick+=1
    screen.blit(gopher1,(pos[0]-gopher1.get_width()/2,pos[1]-gopher1.get_height()/2))
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
def times_update():
    """更新次數"""
    times_sur=times_font.render(str(times),True,red)#次數文字渲染
    #將次數文字貼到視窗的右上角
    screen.blit(times_sur,(bg_x-times_sur.get_width()-10,10))
def game_over():
    """遊戲結束"""
    screen.fill(black)
    end_sur=score_font.render(f"Game over~Your Score is:{score}",False,red)
    screen.blit(end_sur,(bg_x/2-end_sur.get_width()/2,bg_y/2-end_sur.get_height()/2))
def mouse_update():
    global hammer, hammer_tick
    if hammer == ham1:
        if hammer_tick > hammer_max_tick:
            hammer = ham2
            hammer_tick = 0
        else:
            hammer_tick += 1
# 讓鎚子的中心點在滑鼠的位置
    screen.blit(hammer, (mouse_pos[0] - 15, mouse_pos[1] - 15)) 
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
######################次數物件######################
times=0#次數計數
times_max=5#地鼠出現最大次數
typeface=pygame.font.get_default_font()
times_font=pygame.font.Font(typeface,24)
######################地鼠物件######################
pos6 = [[195,305],[400,305],[610,305],[195,450],[400,450],[610,450]]

# pos6 = [[200,200],[300,200],[400,200],[200,300],[300,300],[400,300]]
pos = pos6[0] # 外圍記錄圓的位子
gopher1 = pygame.image.load("胖虎.jpg") # 地鼠圖片
gophers=pygame.image.load('Gophers_BG_800x600.png')
######################分數物件######################
score=0
typeface=pygame.font.get_default_font()
score_font=pygame.font.Font(typeface,24)
######################滑鼠物件######################
pygame.mouse.set_visible(False)
ham1 = pygame.image.load("Hammer1.png")  # 鎚子圖片
ham2 = pygame.image.load("Hammer2.png")  # 鎚子圖片
hammer = ham2  # 設定目前要顯示的鎚子圖片
hammer_tick = 0 # 計數器目前值
hammer_max_tick = 5 # 設定計數器最大值
######################循環偵測######################
while True:
    clock.tick(30)
    mouse_pos=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            hammer=ham1
            if check_click(mouse_pos,pos[0]-50,pos[1]-50,pos[0]+50,pos[1]+50):
                tick=max_tick+1
                score+=1

    if times>=times_max:
        game_over()
    else:          
        screen.blit(bg,(0,0))
        gophers_update()
        pygame.draw.circle(screen,blue,mouse_pos,10)
        score_update()
        pygame.display.update()
        times_update()
        mouse_update()  
    pygame.display.update()