#coding=utf-8
#__author__ = 'lenovo'

import pygame

# 游戏初始化
pygame.init()

# 创建游戏窗口 480*700,set_mode 返回的结果游戏主窗口
screen = pygame.display.set_mode((480,700))

# 绘制背景图片

# 1.加载图像数据
bg = pygame.image.load("./images/background.png")
# 2. blit 绘制图像
screen.blit(bg,(0,0))


# 绘制英雄图像
hero = pygame.image.load("./images/me1.png")
screen.blit(hero,(150,300))


# 可以在所有绘制工作完成之后，统一调用update方法
pygame.display.update()

# 创建时钟对象
clock = pygame.time.Clock()

# 定义rect，指定记录飞机的初始位置
hero_rect = pygame.Rect(150,300,102,126)

# 游戏循环-》意味着游戏正常开始
while True:

    # 可以指定循环体内部的代码执行的帧率
    clock.tick(60)

    # 事件监听
    for event in pygame.event.get():
        # 判断用户是否点击了关闭按钮
        if event.type == pygame.QUIT:
            print("退出游戏...")

            # quit方法卸载所有模块
            pygame.quit()

            # 直接退出系统
            exit()


    # 修改飞机的位置
    hero_rect.y-=1

    # 判断飞机的位置
    if hero_rect.y+hero_rect.height <=0:
        hero_rect.y = 700

    # 调用blit犯法绘制图像
    screen.blit(bg,(0,0))
    screen.blit(hero,hero_rect)

    #调用update方法更新显示
    pygame.display.update()


pygame.quit()
