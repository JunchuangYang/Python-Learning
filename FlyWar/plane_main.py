# -!- coding: utf-8 -!-
#__author__ = 'lenovo'

import pygame
from  plane_sprites import *

class PlaneGame(object):
    # 飞机大战主游戏
    def __init__(self):
        print("游戏初始化")
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 设置定时器事件 创建敌机 1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        pygame.time.set_timer(HERO_FIRE_EVENT,500)


    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = BackgroundSprite()
        bg2 = BackgroundSprite(True)

        self.back_group = pygame.sprite.Group(bg1,bg2)

        # 创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始...")

        # 游戏循环
        while True:
            # 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__check_collide()
            # 更新精灵组
            self.__update_sprites()
            # 更新显示
            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 使用键盘提供的方法获取键盘按键，返回的是元祖
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else: self.hero.speed = 0


    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullet_groups,self.enemy_group,True,True)

        # 敌机碰到英雄，返回根英雄碰撞的所有敌机列表
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)

        # 判断是否有内容。
        if len(enemies) > 0:

            # 英雄牺牲
            self.hero.kill()

            PlaneGame.__game_over()


    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)


        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullet_groups.update()
        self.hero.bullet_groups.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束...")

        pygame.quit()
        exit()


if __name__ == '__main__':

    # 创建游戏对象
    game = PlaneGame()

    # 启动游戏
    game.start_game()
