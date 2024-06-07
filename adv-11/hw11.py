# i=0
# while True:
#     print( i)
#     if i>=10:
#         i=0
#     else:
#         i+=1
######################匯入模組######################
import pygame
import sys
import os
from pygame.locals import *
import random


####################定義函式######################
def bg_update():
    """更新背景"""
    global bg_roll_x
    bg_roll_x = (bg_roll_x - 10) % bg_x  # 背景移動
    screen.blit(img, (bg_roll_x - bg_x, 0))  # 背景圖左移
    screen.blit(img, (bg_roll_x, 0))  # 背景圖接續顯示


# def move_cacti():
#     """移動仙人掌"""
#     global cacti_x, score, cacti_center_x, cacti_center_y,enemy_random
#     cacti_x = (cacti_x - cacti_shift) % (bg_x - 100)  # 仙人掌移動
#     cacti_center_x = cacti_x + img_cacti.get_width() / 2  # 仙人掌中心x位置
#     cacti_center_y = cacti_y + img_cacti.get_height() / 2  # 仙人掌中心y位置
#     screen.blit(img_cacti, (cacti_x, cacti_y))
#     if cacti_x <= 0:
#         score += 1
#         enemy_random=random.randint(0,1)
def move_dinosaur():
    """移動恐龍"""
    global ds_y, jumpState, jumpValue, ds_index, ds_center_x, ds_center_y, fast_deccend
    if bend_down:
        jumpState = False
        ds_y = LIMIT_LOW + 20
    if jumpState and not bend_down:  # 可以起跳
        if ds_y >= LIMIT_LOW:
            jumpValue = -jump_height
        if ds_y <= 0:
            jumpValue = jump_height
        if fast_deccend:
            jumpValue = jump_height + 20
        ds_y += jumpValue
        # 平滑跳躍（可選）
        if jumpValue < 0:
            jumpValue += 1  # 上升速度逐漸減小
        else:
            jumpValue += 1  # 下降速度逐漸增大
        if ds_y >= LIMIT_LOW:
            jumpState = False
            fast_deccend = False
            ds_y = LIMIT_LOW  # 確保恐龍回到地面
    # 計算恐龍圖片編號
    ds_index = (ds_index - 1) % len(ds_show)
    # 計算恐龍中心點
    ds_center_x = ds_x + ds_show[ds_index].get_width() / 2
    ds_center_y = ds_y + ds_show[ds_index].get_height() / 2
    ds_detect_r = min(ds_show[ds_index].get_width(), ds_show[ds_index].get_height()) / 2
    # 繪製恐龍
    screen.blit(ds_show[ds_index], (ds_x, ds_y))


def score_update():
    """更新分數"""
    score_sur = score_font.render(str(score), True, RED)
    screen.blit(score_sur, [10, 10])


def is_hit(x1, y1, x2, y2, r):
    """圓形碰撞偵測"""
    # 原理:兩點距離公式，兩點距離小於半徑，則碰撞
    if ((x1 - x2) ** 2 + (y1 - y2) ** 2) < (r * r):
        return True
    else:
        return False


def game_over():
    """遊戲結束"""
    screen.blit(img_gg, ((bg_x - gg_w) / 2, (bg_y - gg_h) / 2))


# def move_ptera():
#     """移動翼龍"""
#     global ptera_x, ptera_index, score, ptera_center_x, ptera_center_y,enemy_random
#     ptera_x = (ptera_x - ptera_shift) % (bg_x - 100)  # 翼龍移動
#     ptera_index = (ptera_index - 1) % len(img_ptera)
#     ptera_center_x = ptera_x + img_ptera[ptera_index].get_width() / 2
#     ptera_center_y = ptera_y + img_ptera[ptera_index].get_height() / 2
#     screen.blit(img_ptera[ptera_index], (ptera_x, ptera_y))
#     if ptera_x <= 0:
#         score += 1
#         enemy_random=random.randint(0,1)
####################初始化######################
os.chdir(sys.path[0])
pygame.init()
LIMIT_LOW = 140  # 地面高度
PTERA_LIMIT_LOW = 110  # 翼龍高度
clock = pygame.time.Clock()
RED = (255, 0, 0)  # 紅色
enemy_random = 0
####################載入圖片物件######################
img = pygame.image.load("image/bg.png")  # 加載背景
img_dinosaur = [  # 加載恐龍
    pygame.image.load("image/小恐龍1.png"),
    pygame.image.load("image/小恐龍2.png"),
]
img_cacti = pygame.image.load("image/cacti.png")  # 加載仙人掌
img_gg = pygame.image.load("image/gameover.png")  # 加載遊戲結束畫面
# 加載翼龍
img_ptera = [
    pygame.image.load("image/翼龍飛飛1.png"),
    pygame.image.load("image/翼龍飛飛2.png"),
]
img_bend_down = [
    pygame.image.load("image/小恐龍蹲下1.png"),
    pygame.image.load("image/小恐龍蹲下2.png"),
]
bg_x = img.get_width()
bg_y = img.get_height()
bg_roll_x = 0  # 背景圖片滾動位置
######################建立視窗######################
screen = pygame.display.set_mode([bg_x, bg_y])  # 設定窗口
pygame.display.set_caption("Dinosaur")
######################分數物件######################
score = 0  # 分數計數
typeface = pygame.font.get_default_font()
score_font = pygame.font.Font(typeface, 36)
######################恐龍物件######################
ds_x = 50  # 恐龍x位置
ds_y = LIMIT_LOW  # 恐龍y位置
ds_index = 0  # 恐龍圖片編號
jumpState = False  # 跳躍狀態
jumpValue = 0  # 跳躍值
jump_height = 13  # 跳躍高度
ds_center_x = ds_x + img_dinosaur[0].get_width() / 2  # 恐龍中心x位置
ds_center_y = ds_y + img_dinosaur[0].get_height() / 2  # 恐龍中心y位置
ds_detect_r = (
    min(img_dinosaur[0].get_width(), img_dinosaur[0].get_height()) / 2
)  # 恐龍偵測半徑
ds_show = img_dinosaur
bend_down = False
fast_deccend = False


######################障礙物物件######################
class Obstacle:
    def __init__(self, x, y, img: list[pygame.Surface], shift):
        self.x = x
        self.y = y
        self.img = img
        self.shift = shift
        self.center_x = x + img[0].get_width() / 2
        self.center_y = y + img[0].get_height() / 2
        self.detect_r = max(img[0].get_width(), img[0].get_height()) / 2
        self.index = 0

    def initial(self):
        self.x = bg_x - 100
        self.center_x = self.x + self.img[0].get_width() / 2
        self.center_y = self.y + self.img[0].get_height() / 2
        self.index = 0

    def move(self):
        self.x = (self.x - self.shift) % (bg_x - 100)
        self.index = (self.index - 1) % len(self.img)
        self.center_x = self.x + self.img[self.index].get_width() / 2
        self.center_y = self.y + self.img[self.index].get_height() / 2
        screen.blit(self.img[self.index], (self.x, self.y))


class Cacti(Obstacle):
    def __init__(self, x: int, y: int, img: list[pygame.Surface], shift: int):
        """初始化障礙物, x: x位置, y: y位置, img: 圖片, shift: 移動量"""
        super().__init__(x, y, img, shift)
        self.detect_r = self.detect_r - 15


class Ptera(Obstacle):
    def __init__(self, x: int, y: int, img: list, shift: int):
        """初始化障礙物, x: x位置, y: y位置, img: 圖片, shift: 移動量"""
        super().__init__(x, y, img, shift)
        self.detect_r = self.detect_r - 10


######################仙人掌物件######################
# cacti_x = bg_x - 100  # 障礙物x位置
# cacti_y = LIMIT_LOW  # 障礙物y位置
# cacti_shift = 10  # 仙人掌移動量
# cacti_center_x = cacti_x + img_cacti.get_width() / 2  # 障礙物中心x位置
# cacti_center_y = cacti_y + img_cacti.get_height() / 2  # 障礙物中心y位置
# cacti_detect_r = max(img_cacti.get_width(), img_cacti.get_height()) / 2 - 15  # 障礙物偵測半徑
cacti = Cacti(bg_x - 100, LIMIT_LOW, [img_cacti], 10)
######################遊戲結束物件######################
gg = False  # 遊戲結束
gg_w = img_gg.get_width()  # 遊戲結束圖片寬度
gg_h = img_gg.get_height()  # 遊戲結束圖片高度
######################翼龍物件######################
# ptera_x = bg_x - 100  # 障礙物x位置
# ptera_y = PTERA_LIMIT_LOW  # 障礙物y位置
# ptera_index = 0  # 翼龍圖片編號
# ptera_shift = 10  # 翼龍移動量
# ptera_center_x = ptera_x + img_ptera[0].get_width() / 2  # 翼龍中心x位置
# ptera_center_y = ptera_y + img_ptera[0].get_height() / 2  # 翼龍中心y位置
# ptera_detect_r = max(img_ptera[0].get_width(), img_ptera[0].get_height()) / 2 - 10  # 翼龍偵測半徑
ptera = Ptera(bg_x - 100, PTERA_LIMIT_LOW, img_ptera, 10)
######################循環偵測######################
while True:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and ds_y <= LIMIT_LOW:  # 判斷恐龍是否在地上
                jumpState = True  # 開啟跳躍狀態
            elif event.key == K_DOWN:
                if jumpState:
                    fast_deccend = True
                else:
                    bend_down = True
                    ds_show = img_bend_down
            if event.key == K_RETURN and gg:
                score = 0
                gg = False
                # cacti_x = bg_x - 100
                # ptera_x = bg_x - 100
                ds_y = LIMIT_LOW
                jumpState = False
                cacti.initial()
                ptera.initial()
        if event.type == KEYUP:
            if event.key == K_DOWN:
                bend_down = False
                ds_show = img_dinosaur
                ds_y = LIMIT_LOW
    if gg:
        game_over()
    else:
        bg_update()
        # move_cacti()
        move_dinosaur()
        score_update()
        if cacti.x <= 0 or ptera.x <= 0:
            score += 1
            # move_cacti()
            # gg=is_hit(ds_center_x, ds_center_y, cacti_center_x, cacti_center_y, cacti_detect_r + ds_detect_r)
            ptera.move()
            gg = is_hit(
                ds_center_x,
                ds_center_y,
                ptera.center_x,
                ptera.center_y,
                ptera.detect_r + ds_detect_r,
            )
        # if enemy_random==0:
        #     move_cacti()
        #     gg = is_hit(ds_center_x, ds_center_y, cacti_center_x, cacti_center_y, cacti_detect_r + ds_detect_r)
        # else:
        #     move_ptera()
        #     gg = is_hit(ds_center_x, ds_center_y, ptera_center_x, ptera_center_y, ptera_detect_r + ds_detect_r)
    pygame.display.update()
