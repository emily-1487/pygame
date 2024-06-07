######################匯入模組######################
import pygame
import sys
import os
from pygame.locals import *
import random
from collections import deque


######################障礙物物件######################
class Obstacle:
    def __init__(self, x: int, y: int, img: list[pygame.Surface], shift: int):
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
    def __init__(self, x: int, y: int, img: list[pygame.Surface], shift: int):
        """初始化障礙物, x: x位置, y: y位置, img: 圖片, shift: 移動量"""
        super().__init__(x, y, img, shift)
        self.detect_r = self.detect_r - 10


####################定義函式######################
def bg_update():
    """更新背景"""
    global bg_roll_x

    bg_roll_x = (bg_roll_x - 10) % bg_x  # 背景移動
    screen.blit(img, (bg_roll_x - bg_x, 0))  # 背景圖左移
    screen.blit(img, (bg_roll_x, 0))  # 背景圖接續顯示


def move_dinosaur():
    """移動恐龍"""
    global ds_y, jumpState, jumpValue, ds_index, ds_center_x, ds_center_y, ds_detect_r, fast_descend

    # 如果恐龍正在蹲下，將跳躍狀態設定為False，強制恐龍回到地面
    if bend_down:
        jumpState = False
        ds_y = LIMIT_LOW + 20

    if jumpState and not bend_down:  # 可以起跳
        if ds_y >= LIMIT_LOW:  # 確保恐龍在地面上才能起跳
            jumpValue = -jump_height
        if ds_y <= 0:  # 確保恐龍在畫面上方時，不會繼續上升
            jumpValue = jump_height
        if fast_descend:  # 如果正在快速下降
            jumpValue = jump_height + 20  # 設置一個較大的下降值以快速回到地面
        ds_y += jumpValue

        # 平滑跳躍（可選）
        if jumpValue < 0:
            jumpValue += 1  # 上升速度逐漸減小
        else:
            jumpValue += 1  # 下降速度逐漸增大

        if ds_y >= LIMIT_LOW:
            jumpState = False
            fast_descend = False  # 確保恐龍回到地面後關閉快速下降狀態
            ds_y = LIMIT_LOW  # 確保恐龍回到地面

    # 計算恐龍圖片編號
    ds_index = (ds_index - 1) % len(ds_show)
    # 計算恐龍中心點
    ds_center_x = ds_x + ds_show[ds_index].get_width() / 2
    ds_center_y = ds_y + ds_show[ds_index].get_height() / 2
    ds_detect_r = (
        min(ds_show[ds_index].get_width(), ds_show[ds_index].get_height()) / 2
    )  # 恐龍偵測半徑
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


def add_enemy_to_queue():
    """隨機選擇一個敵人加入到隊列中"""
    enemy_type = random.choice(["cacti", "ptera"])  # 隨機選擇仙人掌或翼龍
    if len(enemies_queue) < max_enemies:  # 如果隊列中的敵人數量小於最大敵人數量
        enemies_queue.append(enemy_type)  # 將新敵人加入隊列
    # 在畫面右上角顯示目前對列中的敵人縮圖
    for i, enemy in enumerate(enemies_queue):
        # enumerate(enemies_queue)的意思是將enemies_queue中的元素依序取出，並且給予一個編號
        if enemy == "cacti":
            screen.blit(img_cacti, (bg_x - max_enemies * 50 + i * 50, 0))
        elif enemy == "ptera":
            screen.blit(img_ptera[0], (bg_x - max_enemies * 50 + i * 50, 0))


def create_enemies():
    """隨機決定是否召喚隊列中的敵人"""
    global active_enemies, score, gg, enemies_delay
    enemies_delay = (enemies_delay - 1) % enemies_delay_max  # 敵人出現間隔計數
    if len(enemies_queue) > 0 and enemies_delay == 0:
        enemy_type = enemies_queue.popleft()  # 將隊列中的敵人取出
        if enemy_type == "cacti":
            active_enemies.append(Cacti(bg_x - 100, LIMIT_LOW, [img_cacti], 10))
        elif enemy_type == "ptera":
            active_enemies.append(Ptera(bg_x - 100, PTERA_LIMIT_LOW, img_ptera, 10))
    for enemy in active_enemies:
        enemy.move()
        gg = is_hit(
            ds_center_x,
            ds_center_y,
            enemy.center_x,
            enemy.center_y,
            enemy.detect_r + ds_detect_r,
        )
        if gg:
            break
        if enemy.x <= 0:
            score += 1
            active_enemies.remove(enemy)


####################初始化######################
os.chdir(sys.path[0])
pygame.init()
LIMIT_LOW = 140  # 地面高度
PTERA_LIMIT_LOW = 110  # 翼龍高度
clock = pygame.time.Clock()
RED = (255, 0, 0)  # 紅色
FPS = 20  # 遊戲更新畫面的時間
level_up = False  # 升級狀態

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
jump_height = 15  # 跳躍高度
ds_center_x = ds_x + img_dinosaur[0].get_width() / 2  # 恐龍中心x位置
ds_center_y = ds_y + img_dinosaur[0].get_height() / 2  # 恐龍中心y位置
ds_detect_r = (
    min(img_dinosaur[0].get_width(), img_dinosaur[0].get_height()) / 2
)  # 恐龍偵測半徑
ds_show = img_dinosaur
bend_down = False  # 蹲下狀態
fast_descend = False  # 快速下降狀態

######################遊戲結束物件######################
gg = False  # 遊戲結束
gg_w = img_gg.get_width()  # 遊戲結束圖片寬度
gg_h = img_gg.get_height()  # 遊戲結束圖片高度

######################敵人出現隊列######################
max_enemies = 3  # 最大敵人數量，可以根據需要修改這個值，總共可以放幾個敵人在隊列中
enemies_queue = deque(maxlen=max_enemies)  # 使用deque來創建一個有最大長度的隊列
active_enemies = []
enemies_delay = 0  # 敵人出現間隔計數
enemies_delay_max = 30  # 敵人出現間隔計數最大值

######################循環偵測######################
while True:
    clock.tick(FPS)

    if score % 5 == 0 and score != 0 and not level_up:
        # 每得到5分，敵人出現間隔減少1，20為最小間隔
        enemies_delay_max = max(20, enemies_delay_max - 1)
        if enemies_delay_max == 20:
            # 如果敵人出現間隔已經最小，則遊戲更新畫面的時間加快
            FPS += 10
        level_up = True  # 避免重複升級
    elif score % 5 != 0:
        level_up = False  # 重置升級狀態

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and ds_y <= LIMIT_LOW:  # 判斷恐龍是否在地上
                jumpState = True  # 開啟跳躍狀態
            elif event.key == K_DOWN:
                if jumpState:  # 如果恐龍在跳躍狀態
                    fast_descend = True  # 開啟快速下降狀態
                else:
                    bend_down = True  # 開啟蹲下狀態
                    ds_show = img_bend_down  # 切換蹲下圖片
            if event.key == K_RETURN and gg:
                score = 0
                gg = False
                ds_y = LIMIT_LOW
                jumpState = False
                active_enemies.clear()
                FPS = 20

        if event.type == KEYUP:
            if event.key == K_DOWN:
                fast_descend = False  # 關閉快速下降狀態
                if ds_y >= LIMIT_LOW:  # 如果恐龍在地上
                    bend_down = False  # 關閉蹲下狀態
                    ds_show = img_dinosaur  # 切換恐龍圖片
                    ds_y = LIMIT_LOW  # 確保恐龍回到地面

    if gg:
        game_over()
    else:
        bg_update()
        move_dinosaur()
        score_update()
        add_enemy_to_queue()
        create_enemies()
    pygame.display.update()
