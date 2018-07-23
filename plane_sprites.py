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

    @staticmethod
    def image_names(prefix, count):
        images = []

        for i in range(1, count + 1):
            images.append("./images/" + prefix + str(i) + ".png")

        return images


class BackGround(GameSprite):
    """
    背景类
    """

    def __init__(self, is_out=False):
        super().__init__("./images/background.png")
        if is_out:
            self.rect.bottom = 0

    def update(self):
        # 调用父类update
        super().update()
        if self.rect.y >= SCREEN_SIZE.height:
            self.rect.bottom = 0


class PlaneSprite(GameSprite):
    """
    飞机精灵：包括英雄和敌机
    """
    def __init__(self, image_names, destroy_names, life, speed=None, change_rate=0.05):
        image_name = image_names[0]
        super().__init__(image_name, speed=speed)

        # 生命值
        self.life = life

        # 正常图像列表
        self.__life_names = []
        for file in image_names:
            image = pygame.image.load(file)
            self.__life_names.append(image)

        # 被摧毁图像列表
        self.__destroy_names = []
        for file in destroy_names:
            image = pygame.image.load(file)
            self.__destroy_names.append(image)

        # 默认播放生存图片
        self.images = self.__life_names

        # 显示图像索引
        self.show_image_index = 0

        # 图像是否可以被删除
        self.can_destroied = False

        # 是否循环播放
        self.is_loop_show = True

        # 动画切换频率系数
        self.change_rate = change_rate

    def update(self):
        self.update_images()
        super().update()

    def update_images(self):
        """
        更新图像
        """
        pre_index = self.show_image_index
        print("pre_index = %f" % pre_index)

        self.show_image_index += self.change_rate
        count = len(self.images)
        print("count = %d" % count)

        # 判断是否循环播放
        if self.is_loop_show:
            self.show_image_index %= len(self.images)
        elif self.show_image_index > count - 1:
            self.show_image_index = count - 1
            self.can_destroied = True

        current_index = int(self.show_image_index)
        print("current_index = %d" % current_index)

        if pre_index != current_index:
            self.image = self.images[current_index]

    def destroied(self):
        """
        飞机被摧毁
        """
        self.images = self.__destroy_names

        self.show_image_index = 0

        self.is_loop_show = False


class Hero(PlaneSprite):

    def __init__(self):
        # 正常图片
        image_names = GameSprite.image_names("me", 2)
        # 摧毁图片
        destroy_names = GameSprite.image_names("me_destroy_", 4)

        super().__init__(image_names, destroy_names, 0, change_rate=0.15)

        # 设置初始位置
        self.rect.centerx = SCREEN_SIZE.centerx

        self.rect.bottom = SCREEN_SIZE.bottom - 100

        # 创建子弹组
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        """更新"""
        self.update_images()

        # 飞机水平移动
        self.rect.x += self.speed[0]

        # 飞机不可飞出屏幕控制
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_SIZE.right:
            self.rect.right = SCREEN_SIZE.right
        pass

    def fire(self):
        """
        发射子弹:一次可发射多发子弹
        """
        for i in range(0, 1):
            bullet = Bullet()
            # 设置初始子弹位置
            bullet.rect.bottom = self.rect.top - i * 5

            bullet.rect.centerx = self.rect.centerx

            self.bullet_group.add(bullet)


class Bullet(GameSprite):
    """子弹对象"""
    def __init__(self):
        image_name = "./images/bullet1.png"
        super().__init__(image_name, speed=[0, -10])

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


class Enemy(PlaneSprite):
    """
    敌机类
    """

    def __init__(self):
        image_names = ["./images/enemy1.png"]
        destroy_names = GameSprite.image_names("enemy1_down", 4)

        super().__init__(image_names, destroy_names, random.randint(1, 6), [0, random.randint(0, 3)], 0.35)

        self.rect.x = random.randint(0, SCREEN_SIZE.width - self.rect.width)
        self.speed = [0, random.randint(1, 6)]

    def update(self):
        super().update()
        # 当敌机飞出屏幕,移除该对象
        if self.rect.y >= SCREEN_SIZE.height:
            self.kill()

        # 如果敌机已被摧毁
        if self.can_destroied:
            self.kill()

    def __del__(self):
        print("敌机飞出屏幕被被移除了内存 坐标 %s" % self.rect)
