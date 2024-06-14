import pygame
import random

# 初始化Pygame
pygame.init()

# 设置屏幕大小和标题
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("蛋仔派对")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# 定义蛋仔类
class Egg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("egg.png").convert()  # 蛋仔图片
        self.image.set_colorkey(WHITE)  # 设置白色为透明色
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(screen_height - self.rect.height)

    def update(self):
        pass


# 定义玩家得分
score = 0

# 创建精灵组
all_sprites = pygame.sprite.Group()
eggs = pygame.sprite.Group()

# 创建蛋仔
for _ in range(10):
    egg = Egg()
    all_sprites.add(egg)
    eggs.add(egg)

# 游戏循环
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 处理鼠标点击事件
            pos = pygame.mouse.get_pos()
            clicked_sprites = [
                sprite for sprite in eggs if sprite.rect.collidepoint(pos)
            ]
            for egg in clicked_sprites:
                egg.kill()
                score += 1

    all_sprites.update()
    all_sprites.draw(screen)

    # 显示得分
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
