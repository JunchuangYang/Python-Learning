# -!- coding: utf-8 -!-
#__author__ = 'lenovo'

import random
import  pygame

# 定义屏幕大小的常量
SCREEN_RECT = pygame.Rect(0,0,480,700)
# 刷新帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""
    def __init__(self,image_name,speed=1):

        # 如果父类不是object基类，一定要主动的调用父类的__init__()方法
        # 调用父类的初始化方法
        super().__init__()

        # 定义对象属性，图像，位置，速度
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    # 重写父类的update方法
    def update(self):

        # 在屏幕的垂直方向上移动
        self.rect.y +=self.speed

class BackgroundSprite(GameSprite):

    def __init__(self,is_alt=False):

        super().__init__('./images/background.png')
        if is_alt:
            self.rect.y =self.rect.height

    def update(self):
        super().update()
        # 判断背景是否移出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self):

        # 调用父类方法，创建敌机精灵
        super().__init__("./images/enemy1.png")
        # 指定敌机的初始速度
        self.speed = random.randint(1,3)
        # 指定敌机的初始随机位置
        self.rect.bottom = 0
        self.rect.x = random.randint(0,SCREEN_RECT.width - self.rect.width)

    def update(self):

        # 调用父类方法，保持垂直方向上的飞行
        super().update()
        # 判断飞机是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # kill方法可以将精灵从所有精灵组中移出，精灵就会自动销毁
            self.kill()

    def __del__(self):
        pass

class Hero(GameSprite):
    def __init__(self):
        super().__init__("./images/me1.png",0)
        # 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹精灵组
        self.bullet_groups = pygame.sprite.Group()

    # 英雄在水平方向上移动，通过加减speed来控制英雄的x的值
    def update(self):
        self.rect.x += self.speed

        # 控制英雄不能离开屏幕
        if self.rect.x <0:
            self.rect.x = 0

        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        # 发射三枚子弹，添加三个子弹精灵
        for i in range(0,3):
            bullet = Bullet()

            bullet.rect.bottom = self.rect.y - 20*i
            bullet.rect.centerx = self.rect.centerx

            self.bullet_groups.add(bullet)

class Bullet(GameSprite):
    def __init__(self):
        # 速度设为负值，子弹向上飞行
        super().__init__("./images/bullet1.png",-2)

    def update(self):
        # 调用父类方法，子弹垂直飞行
        super().update()

        # 判断子弹是否飞出屏幕,kill方法，从精灵组中删除
        if self.rect.bottom<0:
            self.kill()





