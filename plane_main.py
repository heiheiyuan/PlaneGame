from plane_sprites import *
pygame.init()

# 刷新频率
FRAME_PRE_SEC = 60

# 定义敌机出场事件
CREATE_ENEMY_EVENT = pygame.USEREVENT

# 定义敌机出场间隔时长
PER_ENEMY_TIME = 1000


class PlaneGame(object):
    """
    飞机大战主游戏入口
    """

    def __init__(self):
        """
        游戏初始化
        """
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_SIZE.size)
        # 创建时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法，创建精灵和精灵组
        self.__create_sprites()
        # 设置定时器事件
        pygame.time.set_timer(CREATE_ENEMY_EVENT, PER_ENEMY_TIME)

    def start_game(self):
        """
        游戏开始
        """
        while 1:
            # 设置刷新频率
            self.clock.tick(FRAME_PRE_SEC)

            # 事件监听
            self.__event_handler()

            # 碰撞检测
            self.__check_collide()

            # 更新精灵组
            self.__update_sprites()

            # 刷新界面
            pygame.display.update()


    @staticmethod
    def __game_over():
        """
        游戏结束
        """

        print("游戏结束")

        pygame.quit()

        exit()

    def __create_sprites(self):
        """
        创建游戏精灵和精灵组
        """
        # 背景组
        bg1 = BackGround()
        bg2 = BackGround(True)
        self.bg_group = pygame.sprite.Group(bg1, bg2)

        # 敌机组
        self.enemy_group = pygame.sprite.Group()

        # 英雄组
        hero_rect = pygame.image.load("./images/me1.png").get_rect()
        hero = GameSprite("./images/me1.png", [(SCREEN_SIZE.width - hero_rect.width) / 2,
                                               SCREEN_SIZE.height - hero_rect.height - 30], [0, 0])
        self.hero_group = pygame.sprite.Group(hero)

    def __event_handler(self):
        """
        事件处理
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                self.enemy_group.add(Enemy())

    def __check_collide(self):
        """
        碰撞检测
        """
        pass

    def __update_sprites(self):
        """
        更新精灵组
        """
        for group in [self.bg_group, self.enemy_group, self.hero_group]:
            group.update()
            group.draw(self.screen)
        pass


if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()
    # 开始游戏
    game.start_game()
