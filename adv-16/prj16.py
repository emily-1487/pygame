######################載入套件######################
import pygame
import sys
import os
import random
from pygame.locals import *
from typing import List


######################物件類別######################
class Missile:
    def __init__(self, x, y, image, shift):
        """初始化飛彈"""
        self.x = x
        self.y = y
        self.image = image
        self.active = False
        self.shift = shift

    def launch(self, x, y):
        if not self.active:
            self.x = x
            self.y = y
            self.active = True

    def move(self):
        if self.active:
            self.y -= self.shift
            if self.y < 0:
                self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, image, shift):
        """初始化敵機"""
        self.x = x
        self.y = y
        self.image = image
        self.active = True
        self.shift = shift
        self.wh = image.get_width() // 2
        self.hh = image.get_height() // 2

    def move(self):
        if self.active:
            self.y += self.shift
            if self.y > bg_y:
                self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x - self.wh, self.y - self.hh))

    def reset(self, x, y, image, shift):
        self.x = x
        self.y = y
        self.image = image
        self.active = True
        self.shift = shift
        self.wh = image.get_width() // 2
        self.hh = image.get_height() // 2


######################定義函式區######################
def roll_bg():
    """捲動背景"""
    global roll_y
    roll_y = (roll_y + 20) % bg_y  # 背景捲動
    screen.blit(img_bg, [0, roll_y - bg_y])  # 上半部
    screen.blit(img_bg, [0, roll_y])  # 下半部


def move_starship():
    """移動飛船"""
    global ss_x, ss_y, ss_wh, ss_hh, ss_img, burn_shift
    key = pygame.key.get_pressed()
    ss_img = img_sship[0]
    if key[pygame.K_UP]:
        ss_y -= 20
    if key[pygame.K_DOWN]:
        ss_y += 20
    if key[pygame.K_LEFT]:
        ss_x -= 20
        ss_img = img_sship[1]
    if key[pygame.K_RIGHT]:
        ss_x += 20
        ss_img = img_sship[2]
    ss_hh = ss_img.get_height() / 2
    ss_wh = ss_img.get_width() / 2
    if ss_y < ss_hh:  # 飛船上邊界
        ss_y = ss_hh
    if ss_y > bg_y - ss_hh:  # 飛船下邊界
        ss_y = bg_y - ss_hh
    if ss_x < ss_wh:  # 飛船左邊界
        ss_x = ss_wh
    if ss_x > bg_x - ss_wh:  # 飛船右邊界
        ss_x = bg_x - ss_wh
    burn_shift = (burn_shift + 2) % 6  # 飛船火焰的位移
    screen.blit(img_burn, [ss_x - burn_w / 2, ss_y + burn_h + burn_shift])  # 飛船火焰
    screen.blit(ss_img, [ss_x - ss_wh, ss_y - ss_hh])  # 飛船本體


def create_enemy():
    emy_img = random.choice(emy_show)  # 隨機選擇敵機圖片
    emy_img = img_enemy
    emy_wh = emy_img.get_width() // 2
    emy_x = random.randint(emy_wh, bg_x - emy_wh)
    emy_y = random.randint(-bg_y, -emy_wh)
    return emy_x, emy_y, emy_img


######################初始化設定######################
os.chdir(sys.path[0])
pygame.init()
clock = pygame.time.Clock()
######################載入圖片######################
# 載入背景圖片
img_bg = pygame.image.load("image/space.png")
# 載入飛船圖片
img_sship = [
    pygame.image.load("image/fighter_M.png"),
    pygame.image.load("image/fighter_L.png"),
    pygame.image.load("image/fighter_R.png"),
]
# 載入飛船火焰
img_burn = pygame.image.load("image/starship_burner.png")
img_weapon = pygame.image.load("image/bullet.png")
img_enemy = pygame.image.load("image/enemy1.png")
img_enemy2 = pygame.image.load("image/enemy2.png")
######################遊戲視窗設定######################
bg_x = img_bg.get_width()  # 背景圖片寬度
bg_y = img_bg.get_height()  # 背景圖片高度
bg_size = (bg_x, bg_y)  # 背景圖片大小
pygame.display.set_caption("Galaxy Lancer")
screen = pygame.display.set_mode(bg_size)
roll_y = 0
######################玩家設定######################
ss_x = bg_x / 2  # 飛船x位置
ss_y = bg_y / 2  # 飛船y位置
ss_wh = img_sship[0].get_width() / 2  # 飛船寬度一半
ss_hh = img_sship[0].get_height() / 2  # 飛船高度一半
ss_img = img_sship[0]  # 飛船圖片
burn_shift = 0  # 飛船火焰的位移
burn_w, burn_h = img_burn.get_rect().size  # 飛船火焰的寬度與高度
######################飛彈設定######################
msl_wh = img_weapon.get_width() / 2
msl_hh = img_weapon.get_height() / 2
msl_shift = 30
MISSLE_MAX = 10
missiles = [Missile(0, 0, img_weapon, msl_shift) for _ in range(MISSLE_MAX)]
msl_cooldown = 0
msl_cooldown_max = 1
######################敵機設定######################
emy_show = [img_enemy, img_enemy2]
emy_shift = 5  # 敵機移動速度
emy_list: List[Enemy] = []  # 敵機列表
emy_num = 5  # 敵機數量
for i in range(emy_num):
    emy_list.append(Enemy(*create_enemy(), emy_shift))
######################主程式######################
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_F1:
                screen = pygame.display.set_mode(bg_size, FULLSCREEN)
            elif event.key == K_ESCAPE:
                screen = pygame.display.set_mode(bg_size)
            if event.key == K_SPACE and msl_cooldown == 0:
                for missile in missiles:
                    if not missile.active:
                        missile.launch(ss_x - msl_wh, ss_y - msl_hh)
                        msl_cooldown = msl_cooldown_max
                        break
                missile.launch(ss_x - msl_wh, ss_y - msl_hh)
    roll_bg()  # 捲動背景
    move_starship()  # 飛船移動
    msl_cooldown = max(0, msl_cooldown - 1)
    for missile in missiles:
        missile.move()
        missile.draw(screen)
    for enemy in emy_list:
        enemy.move()
        enemy.draw(screen)
        if not enemy.active:
            enemy.reset(*create_enemy(), emy_shift)

    pygame.display.update()
