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
LIMIT_LOW = 140
clock = pygame.time.Clock()
RED = (255, 0, 0)
######################載入圖片物件##################
img = pygame.image.load("image/bg.png")
img_dinosaur = [
    pygame.image.load("image/小恐龍1.png"),
    pygame.image.load("image/小恐龍2.png"),
]
img_cati = pygame.image.load("image/cacti.png")
img_gg = pygame.image.load("image/gameover.png")
bg_x = img.get_width()
bg_y = img.get_height()
bg_roll_x = 0
#####################分數物件#######################
score = 0
typeface = pygame.font.get_default_font()
score_font = pygame.font.Font(typeface, 36)
#####################恐龍物件#######################
ds_x = 50
ds_y = LIMIT_LOW
ds_index = 0
jumpstate = False
jumpvalue = 0
ds_center_x = ds_x + img_dinosaur[0].get_width() / 2
ds_center_y = ds_y + img_dinosaur[0].get_height() / 2
ds_detect_r = min(img_dinosaur[0].get_width(), img_dinosaur[0].get_height()) / 2
jumpheight = 13
#####################仙人掌物件#######################
catci_x = bg_x - 100
catci_y = LIMIT_LOW
cacti_shift = 10  # 仙人掌移動量
# 障礙物中心x位置
cacti_center_x = catci_x + img_cati.get_width() / 2
# 障礙物中心y位置
cacti_center_y = catci_y + img_cati.get_height() / 2
# 障礙物偵測半徑
cacti_detect_r = max(img_cati.get_width(), img_cati.get_height()) / 2 - 15
######################遊戲結束物件######################
gg = False
gg_w = img_gg.get_width()
gg_h = img_gg.get_height()
######################建立視窗######################
screen = pygame.display.set_mode([bg_x, bg_y])
pygame.display.set_caption("Dinosaur")


######################定義函式######################
def bg_update():
    global bg_roll_x
    bg_roll_x = (bg_roll_x - 10) % bg_x
    screen.blit(img, (bg_roll_x - bg_x, 0))
    screen.blit(img, (bg_roll_x, 0))


def move_dinosaur():
    global ds_y, jumpstate, jumpvalue, ds_index
    if jumpstate:
        if ds_y >= LIMIT_LOW:
            jumpvalue = -jumpheight
        if ds_y <= 0:
            jumpvalue = jumpheight
        ds_y += jumpvalue
        jumpvalue += 1
        if ds_y >= LIMIT_LOW:
            jumpstate = False
            ds_y = LIMIT_LOW
    ds_index = (ds_index - 1) % len(img_dinosaur)
    ds_center_x = ds_x + img_dinosaur[ds_index].get_width() / 2
    ds_center_y = ds_y + img_dinosaur[ds_index].get_height() / 2
    screen.blit(img_dinosaur[ds_index], (ds_x, ds_y))


def move_cacti():
    """移動仙人掌"""
    global catci_x, score
    catci_x = (catci_x - cacti_shift) % (bg_x - 100)
    cacti_center_x = catci_x + img_cati.get_width() / 2  # 仙人掌中心x位置
    cacti_center_y = catci_y + img_cati.get_height() / 2  # 仙人掌中心y位置
    screen.blit(img_cati, (catci_x, catci_y))
    if catci_x <= 0:
        score += 1


def score_update():
    score_sur = score_font.render(str(score), True, RED)
    screen.blit(score_sur, [10, 10])


def is_hit(x1, y1, x2, y2, r):
    if ((x1 - x2) ** 2 + (y1 - y2) ** 2) < (r * r):
        return True
    else:
        return False


def game_over():
    """遊戲結束"""
    screen.blit(img_gg, ((bg_x - gg_w) / 2, (bg_y - gg_h) / 2))


######################循環偵測######################
while True:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE and ds_y <= LIMIT_LOW:
                jumpstate = True
            if event.key == K_RETURN and gg:
                score = 0
                gg = False
                catci_x = bg_x - 100
                ds_y = LIMIT_LOW
                jumpstate = False
    if gg:
        game_over()
    else:
        bg_update()
        move_dinosaur()
        score_update()
        move_cacti()
        gg = is_hit(
            ds_center_x, ds_center_y, cacti_center_x, cacti_center_y, cacti_detect_r
        )
    if is_hit(ds_center_x, ds_center_y, catci_x, catci_y, cacti_detect_r + ds_detect_r):
        print("hit!!!")
    # 畫出碰撞偵測範圍
    pygame.draw.circle(
        screen, RED, (int(catci_x), int(catci_y)), cacti_detect_r + ds_detect_r, 1
    )
    pygame.display.update()
