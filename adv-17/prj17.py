######################載入套件######################
import random
from typing import List
import pygame
import sys
import os
from pygame.locals import *


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
        """發射飛彈"""
        if not self.active:
            self.x = x
            self.y = y
            self.active = True

    def move(self):
        """移動飛彈"""
        if self.active:
            self.y -= self.shift
            if self.y < 0:
                self.active = False

    def draw(self, screen):
        """繪製飛彈"""
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
        self.EXP: int = 0  # 爆炸圖片index

    def move(self):
        """移動敵機"""
        if self.active:
            self.y += self.shift
            if self.y > bg_y:  # 當敵機移動到屏幕底部時，標記為非活躍
                self.reset(*create_enemy(), self.shift)

    def draw(self, screen):
        """繪製敵機"""
        if self.active:
            self.burn_shift = (self.burn_shift + 2) % 6  # 火焰的位移
            screen.blit(
                self.burn_img,
                [self.x - self.burn_w / 2, self.y - self.burn_h - self.burn_shift],
            )
            screen.blit(self.image, (self.x - self.wh, self.y - self.hh))  # 繪製敵機

    def reset(self, x, y, image, shift):
        """初始化敵機"""
        self.x = x
        self.y = y
        self.image = image
        self.active = True
        self.shift = shift
        self.wh = image.get_width() // 2
        self.hh = image.get_height() // 2
        self.EXP = 0


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
    ss_invincible = max(0, ss_invincible - 1)  # 更新飛船無敵時間
    if ss_invincible % 2 == 0:
        screen.blit(
            img_burn, [ss_x - burn_w / 2, ss_y + burn_h + burn_shift]
        )  # 飛船火焰
        screen.blit(ss_img, [ss_x - ss_wh, ss_y - ss_hh])  # 飛船本體


def create_enemy():
    """
    建立敵機
    return: 敵機x位置, 敵機y位置, 敵機圖片
    """
    emy_img = random.choice(emy_show)  # 隨機選擇敵機圖片
    emy_wh = emy_img.get_width() // 2  # 敵機寬度一半
    emy_x = random.randint(emy_wh, bg_x - emy_wh)  # 起始x位置
    emy_y = random.randint(-bg_y, -emy_wh)  # 起始y位置
    return emy_x, emy_y, emy_img


def is_hit(x1, y1, x2, y2, r):
    """檢查兩個物件是否碰撞"""
    if ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) < (r * r):
        return True
    else:
        return False


def score_update():
    global score
    score_sur = score_font.render(str(score), True, (255, 0, 0))  # 繪製分數
    screen.blit(score_sur, [10, 10])  # 顯示分數


def draw_explode(enemy: Enemy):
    """繪製爆炸特效"""
    if 0 < enemy.EXP < 6:
        exp_w, exp_h = img_explode[enemy.EXP].get_rect().size
        screen.blit(img_explode[enemy.EXP], [enemy.x - exp_w / 2, enemy.y - exp_h / 2])
        enemy.EXP += 1


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
img_emy_burn = pygame.transform.rotate(img_burn, 180)
# 載入飛彈圖片
img_weapon = pygame.image.load("image/bullet.png")
# 載入敵機圖片
img_enemy = pygame.image.load("image/enemy1.png")
img_enemy2 = pygame.image.load("image/enemy2.png")
# 載入爆炸圖片
img_explode = [
    None,
    pygame.image.load("image/explosion1.png"),
    pygame.image.load("image/explosion2.png"),
    pygame.image.load("image/explosion3.png"),
    pygame.image.load("image/explosion4.png"),
    pygame.image.load("image/explosion5.png"),
]
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
# 碰到敵人之後閃爍霸體時間
ss_invincible = 0  # 飛船無敵時間
burn_shift = 0  # 飛船火焰的位移
burn_w, burn_h = img_burn.get_rect().size  # 飛船火焰的寬度與高度
######################飛彈設定######################
msl_wh = img_weapon.get_width() / 2  # 飛彈寬度一半
msl_hh = img_weapon.get_height() / 2  # 飛彈高度一半
msl_shift = 30  # 飛彈速度
MISSILE_MAX = 10  # 最大飛彈數量
# 飛彈列表, 不可以用[Missile(0, 0, img_weapon, msl_shift)] * MISSILE_MAX
missiles = [Missile(0, 0, img_weapon, msl_shift) for _ in range(MISSILE_MAX)]
msl_cooldown = 0  # 飛彈冷卻時間
msl_cooldown_max = 10  # 飛彈最大冷卻時間（連發間隔）
######################敵機設定######################
emy_show = [img_enemy, img_enemy2]
emy_shift = 5  # 敵機移動速度
emy_list: List[Enemy] = []  # 敵機列表
emy_num = 5  # 敵機數量
for i in range(emy_num):
    emy_list.append(Enemy(*create_enemy(), emy_shift, img_emy_burn))
######################分數設定######################
score = 0  # 分數計數
typeface = pygame.font.get_default_font()
score_font = pygame.font.Font(typeface, 36)
######################音樂設定######################
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
            if event.key == K_SPACE and msl_cooldown == 0:  # 檢查冷卻時間
                for missile in missiles:
                    if not missile.active:  # 尋找一個未激活的飛彈
                        missile.launch(ss_x - msl_wh, ss_y - msl_hh)
                        msl_cooldown = msl_cooldown_max  # 重設冷卻時間
                        break
    roll_bg()  # 捲動背景
    move_starship()  # 飛船移動
    msl_cooldown = max(0, msl_cooldown - 1)  # 更新飛彈冷卻時間
    for missile in missiles:  # 移動和繪製所有飛彈
        missile.move()
        missile.draw(screen)
    for enemy in emy_list:  # 檢查所有敵機
        enemy.move()  # 移動敵機
        enemy.draw(screen)  # 繪製敵機
        draw_explode(enemy)  # 繪製爆炸特效
        for missile in missiles:  # 檢查是否與飛彈碰撞
            if missile.active and is_hit(
                missile.x, missile.y, enemy.x, enemy.y, msl_wh + enemy.wh
            ):
                missile.active = False  # 標記飛彈為非活躍
                enemy.active = False  # 標記敵機為非活躍
                score += 1
                enemy.EXP = 1
                pygame.mixer.music.play()
                break  # 結束檢查其他飛彈，因為已經碰撞
        if not enemy.active and enemy.EXP == 6:  # 如果敵機非活躍
            enemy.reset(*create_enemy(), emy_shift)  # 重設敵機
        if (
            enemy.active
            and is_hit(enemy.x, enemy.y, ss_x, ss_y, enemy.wh + ss_wh)
            and ss_invincible == 0
        ):
            ss_invincible = 40
            score -= 1
    score_update()
    pygame.display.update()
