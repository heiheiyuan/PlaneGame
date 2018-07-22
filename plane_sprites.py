import pygame
import random

# 窗口大小
SCREEN_SIZE = pygame.Rect(0, 0, 480, 700)


class GameSprite(pygame.sprite.Sprite):
    """
    游戏精灵基类
    """

    def __init__(self, image_name, location=None, speed=None):
        # 调用父类初始化方法
        super().__init__()

        # 加载图像
        self.image = pygame.image.load(image_name)

        # 获取图像尺寸
        self.rect = self.image.get_rect()

        # 记录速度
        if speed is None:
            speed = [0, 1]
        self.speed = speed

        # 记录初始位置
        if location is None:
            location = [0, 0]
        self.rect.x = location[0]
        self.rect.y = location[1]

    def update(self):
        self.rect = self.rect.move(self.speed)


class BackGround(GameSprite):
    """
    背景类
    """

    def __init__(self, is_out=False):
        if is_out:
            super().__init__("./images/background.png", [0, -SCREEN_SIZE.height])
        else:
            super().__init__("./images/background.png")

    def update(self):
        # 调用父类update
        super().update()
        if self.rect.y >= SCREEN_SIZE.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """
    敌机类
    """

    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.rect.x = random.randint(0, SCREEN_SIZE.width - self.rect.width)
        self.speed = [0, random.randint(1, 6)]

    def update(self):
        super().update()
        # 当敌机飞出屏幕,移除该对象
        if self.rect.y >= SCREEN_SIZE.height:
            self.kill()

    def __del__(self):
        print("敌机飞出屏幕 被杀掉了 坐标 %s" % self.rect)
