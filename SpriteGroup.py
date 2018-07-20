from plane_sprites import *

# 初始化pygame
pygame.init()

# 创建游戏窗口
size = width, height = 400, 700

screen = pygame.display.set_mode(size)

# 创建敌机
enemy1 = GameSprite("./images/enemy1.png", [100, 0], [0, 2])
enemy2 = GameSprite("./images/enemy1.png", [200, 0], [0, 4])
enemy3 = GameSprite("./images/enemy1.png", [300, 0], [0, 6])

# 加载图像
bg = pygame.image.load("./images/background.png")

# 1> 加载图像
hero = pygame.image.load("./images/me1.png")

# 定义英雄初始化位置
hero_rect = hero.get_rect()
hero_rect.x = 100
hero_rect.y = 500
speed = [0, -2]
# 添加至精灵组

enemy_group = pygame.sprite.Group(enemy1, enemy2, enemy3)

# 时钟对象
clock = pygame.time.Clock()

# 循环部分
while 1:
    clock.tick(60)
    # 监听程序退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("游戏退出。。。。")
            pygame.quit()
            exit()

    hero_rect = hero_rect.move(speed)

    if hero_rect.y < - 126:
        hero_rect.y = 700

    # 绘制在屏幕
    screen.blit(bg, (0, 0))
    # 2> 绘制在屏幕
    screen.blit(hero, hero_rect)

    # 敌机组移动和绘制
    enemy_group.update()
    enemy_group.draw(screen)

    # 刷新界面
    pygame.display.update()
