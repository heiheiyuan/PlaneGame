import sys, pygame

# 初始化

pygame.init()

# 创建游戏窗口
"""
- resolution 指定屏幕的 宽 和 高，默认创建的窗口大小和屏幕大小一致
- flags 参数指定屏幕的附加选项，例如是否全屏等等，默认不需要传递
- depth 参数表示颜色的位数，默认自动匹配
"""
size = width, height = 480, 700

screen = pygame.display.set_mode(size)

# 绘制背景图像

# 加载图像
bg = pygame.image.load("./images/background.png")

# 1> 加载图像
hero = pygame.image.load("./images/me1.png")

# 定义英雄初始化位置
hero_rect = hero.get_rect()
hero_rect.x = 100
hero_rect.y = 500
print(hero_rect.width, hero_rect.height)
print(hero_rect.x, hero_rect.y)
speed = [0, -6]

# 获取时钟
clock = pygame.time.Clock()

while 1:
    # 设置刷新频率
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("退出游戏。。。")
            pygame.quit()
            sys.exit()

    hero_rect = hero_rect.move(speed)

    if hero_rect.y < - 126:
        hero_rect.y = 700

    # 绘制在屏幕
    screen.blit(bg, (0, 0))
    # 2> 绘制在屏幕
    screen.blit(hero, hero_rect)

    pygame.display.update()

