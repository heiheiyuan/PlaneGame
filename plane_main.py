#! /Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 2018/7/23 09:28
# @Author  : HYY
# @File    : plane_main.py
#


from plane_sprites import *

pygame.init()

# 刷新频率
FRAME_PRE_SEC = 60

# 定义敌机出场事件
CREATE_ENEMY_EVENT = pygame.USEREVENT

# 定义子弹时间
HERO_FIRE_EVENT = pygame.USEREVENT + 1

# 定义敌机出场间隔时长
PER_ENEMY_TIME = 1000

# 子弹发射间隔时长
PER_BULLET_TIME = 100

# 游戏实例
instance = None


class PlaneGame(object):
    """
    飞机大战主游戏入口
    """
    def __init__(self):
        """
        游戏初始化
        """
        # 游戏是否运行
        self.running = False
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_SIZE.size)
        # 创建时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法，创建精灵和精灵组
        self.__create_sprites()
        # 调动定时任务
        PlaneGame.__create_user_event()

    def start_game(self):
        """
        游戏开始
        """
        self.running = True
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

    @staticmethod
    def __create_user_event():
        """
        定时任务
        """
        # 设置敌机出现定时任务
        pygame.time.set_timer(CREATE_ENEMY_EVENT, PER_ENEMY_TIME)

        # 设置子弹发射定时任务
        pygame.time.set_timer(HERO_FIRE_EVENT, PER_BULLET_TIME)

    @staticmethod
    def __stop_user_event():
        """
        取消定时任务
        """
        # 设置敌机出现定时任务
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 0)

        # 设置子弹发射定时任务
        pygame.time.set_timer(HERO_FIRE_EVENT, 0)

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
        self.destroy_enemy_group = pygame.sprite.Group()

        # 英雄组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        self.running_list = [self.bg_group, self.enemy_group, self.destroy_enemy_group, self.hero_group,
                             self.hero.bullet_group]
        # 重新开始游戏
        self.again = Again()
        self.again_group = pygame.sprite.Group(self.again)

        # 结束游戏
        self.quit = Quit()
        self.quit_group = pygame.sprite.Group(self.quit)

        self.stop_list = [self.again_group, self.quit_group]

    def __event_handler(self):
        """
        事件处理
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                self.enemy_group.add(Enemy())
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            # 按下 b 英雄自爆
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                # 集体自爆
                for enemy in self.enemy_group.sprites():
                    enemy.destroied()
        # 检测用户鼠标操作 如果用户按下鼠标左键
        if pygame.mouse.get_pressed()[0]:
            # 获取鼠标坐标
            pos = pygame.mouse.get_pos()
            # 获取结束游戏 重新开始按钮区域坐标
            quit_rect = self.quit.rect
            again_rect = self.again.rect
            if quit_rect.left < pos[0] < quit_rect.right \
                    and quit_rect.top < pos[1] < quit_rect.bottom:
                # 结束游戏
                PlaneGame.__game_over()
            elif again_rect.left < pos[0] < again_rect.right \
                    and again_rect.top < pos[1] < again_rect.bottom:
                print("点击了重新开始")
                # 重新开始游戏
                global instance
                instance = PlaneGame()
                instance.start_game()

        if self.hero.can_destroied:
            self.running = False
        else:
            # 通过pygame.key 获取用户按键
            keys_pressed = pygame.key.get_pressed()

            direct = keys_pressed[pygame.K_RIGHT] - keys_pressed[pygame.K_LEFT]

            self.hero.speed = [direct * 6, 0]

    def __check_collide(self):
        """
        碰撞检测
        """
        # 子弹撞毁敌机
        enemies = pygame.sprite.groupcollide(self.enemy_group, self.hero.bullet_group, False, True).keys()

        for enemy in enemies:
            enemy.life -= 1

            if enemy.life <= 0:
                enemy.add(self.destroy_enemy_group)
                enemy.remove(self.enemy_group)
                enemy.destroied()

        # 敌机撞毁英雄
        hero = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(hero) > 0:
            self.hero.destroied()

    def __update_sprites(self):
        """
        更新精灵组
        """
        if self.running:
            for group in [self.bg_group, self.enemy_group, self.hero_group, self.hero.bullet_group,
                          self.destroy_enemy_group]:
                group.update()
                group.draw(self.screen)
        else:
            # 停止定时任务
            PlaneGame.__stop_user_event()
            # 清空背景等精灵，生成退出游戏重新开始按钮
            for group in self.running_list:
                group.empty()
            for group in self.stop_list:
                group.update()
                group.draw(self.screen)


if __name__ == '__main__':
    # 创建游戏对象
    instance = PlaneGame()
    instance.start_game()
