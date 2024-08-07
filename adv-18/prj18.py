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
    def __init__(self, x, y, image, shift, burn_img):
        """初始化敵機"""
        self.x = x
        self.y = y
        self.image = image
        self.active = True
        self.shift = shift
        self.wh = image.get_width() // 2
        self.hh = image.get_height() // 2
        self.burn_shift = 0
        self.burn_img = burn_img
        self.burn_w, self.burn_h = burn_img.get_rect().size
        self.EXP: int = 0
        self.hit = False

    def move(self):
        if self.active:
            self.y += self.shift
            if self.y > bg_y:
                self.reset(*create_enemy(), self.shift)

    def draw(self, screen):
        if self.active:
            self.burn_shift = (self.burn_shift + 2) % 6  # 飛船火焰的位移
            screen.blit(
                self.burn_img,
                [self.x - self.burn_w / 2, self.y - self.burn_h - self.burn_shift],
            )  # 飛船火焰
            screen.blit(self.image, (self.x - self.wh, self.y - self.hh))

    def reset(self, x, y, image, shift):
        self.x = x
        self.y = y
        self.image = image
        self.active = True
        self.shift = shift
        self.wh = image.get_width() // 2
        self.hh = image.get_height() // 2
        self.EXP = 0
        self.hit = False


class FastMissile(Missile):
    def __init__(self, x, y, image, shift):
        super().__init__(x, y, image, shift)
        self.shift += 10


class PiercingMissile(Missile):
    def __init__(self, x, y, image, shift):
        super().__init__(x, y, image, shift)


######################定義函式區######################
def roll_bg():
    """捲動背景"""
    global roll_y
    roll_y = (roll_y + 20) % bg_y  # 背景捲動
    screen.blit(img_bg, [0, roll_y - bg_y])  # 上半部
    screen.blit(img_bg, [0, roll_y])  # 下半部


def move_starship():
    """移動飛船"""
    global ss_x, ss_y, ss_wh, ss_hh, ss_img, burn_shift, ss_invincible
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
    ss_invincible = max(0, ss_invincible - 1)
    if ss_invincible % 2 == 0:
        screen.blit(
            img_burn, [ss_x - burn_w / 2, ss_y + burn_h + burn_shift]
        )  # 飛船火焰
        screen.blit(ss_img, [ss_x - ss_wh, ss_y - ss_hh])  # 飛船本體


def create_enemy():
    emy_img = random.choice(emy_show)  # 隨機選擇敵機圖片
    emy_img = img_enemy
    emy_wh = emy_img.get_width() // 2
    emy_x = random.randint(emy_wh, bg_x - emy_wh)
    emy_y = random.randint(-bg_y, -emy_wh)
    return emy_x, emy_y, emy_img


def is_hit(x1, y1, x2, y2, r):
    if ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) < (r * r):
        return True
    else:
        return False


def score_update():
    global score
    score_sur = score_font.render(str(score), True, (255, 0, 0))
    screen.blit(score_sur, [10, 10])


def draw_explode(enemy: Enemy):
    if 0 < enemy.EXP < 6:
        exp_w, exp_h = img_explode[enemy.EXP].get_rect().size
        screen.blit(img_explode[enemy.EXP], [enemy.x - exp_w / 2, enemy.y - exp_h / 2])
        enemy.EXP += 1


def shield_update():
    shield_w = img_shield.get_width() * ss_shield / 100
    shield_h = img_shield.get_height()
    screen.blit(img_shield, [0, bg_y - 40], [0, 0, shield_w, shield_h])


def show_gameover():
    screen.blit(
        img_gg, [bg_x / 2 - img_gg.get_width() / 2, bg_y / 2 - img_gg.get_height / 2]
    )


######################初始化設定######################
os.chdir(sys.path[0])
pygame.init()
clock = pygame.time.Clock()
gameover = False
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
img_emy_burn = pygame.transform.rotate(img_burn, 180)
img_weapon = pygame.image.load("image/bullet.png")
img_enemy = pygame.image.load("image/enemy1.png")
img_enemy2 = pygame.image.load("image/enemy2.png")
img_explode = [
    None,
    pygame.image.load("image/explosion1.png"),
    pygame.image.load("image/explosion2.png"),
    pygame.image.load("image/explosion3.png"),
    pygame.image.load("image/explosion4.png"),
    pygame.image.load("image/explosion5.png"),
]
img_shield = pygame.image.load("image/shield.png")
img_gg = pygame.image.load("image/gameover.png")
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
ss_invincible = 0
ss_shield = 100
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
    emy_list.append(Enemy(*create_enemy(), emy_shift, img_emy_burn))
#################分數設定#################
score = 0
typeface = pygame.font.get_default_font()
score_font = pygame.font.Font(typeface, 36)
#################音樂設定#################
pygame.mixer.music.load("image/hit.mp3")
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
    if gameover:
        show_gameover()
    else:
        roll_bg()  # 捲動背景
        move_starship()  # 飛船移動

        msl_cooldown = max(0, msl_cooldown - 1)
        for missile in missiles:
            missile.move()
            missile.draw(screen)
        for enemy in emy_list:
            enemy.move()
            enemy.draw(screen)
            draw_explode(enemy)
            for missile in missiles:
                if missile.active and is_hit(
                    missile.x, missile.y, enemy.x, enemy.y, msl_wh + enemy.wh
                ):
                    if enemy.hit:
                        break
                    enemy.hit = True
                    if not isinstance(missile, PiercingMissile):
                        missile.active = False
                    enemy.active = False
                    score += 1
                    enemy.EXP = 1
                    pygame.mixer.music.play()
                    break
            if not enemy.active and enemy.EXP == 6:
                enemy.reset(*create_enemy(), emy_shift)
            if (
                enemy.active
                and is_hit(enemy.x, enemy.y, ss_x, ss_y, enemy.wh + ss_wh)
                and ss_invincible == 0
            ):
                ss_invincible = 40
                score -= 1
                ss_shield -= 20
            if ss_shield <= 0:
                gameover = True
                break
        score_update()
        shield_update()

    pygame.display.update()
