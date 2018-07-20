import pygame

# 窗口大小
SCREEN_SIZE = pygame.Rect(0, 0, 480, 700)

# 刷新频率
FRAME_PRE_SEC = 60


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
        if self.rect.y >= SCREEN_SIZE.height:
            self.rect.y = -self.rect.height

