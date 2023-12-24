from pygame.sprite import Sprite
import random
from  copy import deepcopy
import math 
class Alien(Sprite):
    """ 表示单个外星人的类 """
    def __init__(self,screen,settings,stats,alien_x_init,src,alien_type = "low"):
        """初始化外星人并设置其初始位置 """
        super().__init__()
        self.screen = screen
        self.settings = deepcopy(settings)
        self.stats = stats
        self.src = src
        self.direction = random.choice([1,-1])  # 左右方向
        self.alien_type = alien_type  # 设置外星人种类
        self.alien_x_init = alien_x_init  # 该外星人出现时的初始x坐标
        self.image = self.src.images['aliens'][alien_type]

        # 外星人属性
        self.hp = self.stats.alien_hp[alien_type]
        self.point = self.stats.alien_point[alien_type]
        self.alien_xspeed = self.stats.alien_xspeed[alien_type] #+ random.uniform(-self.stats.alien_xspeed[alien_type],0.1)
        self.alien_yspeed = self.stats.alien_yspeed[alien_type] #+ random.uniform(0,0.1)
        self.alien_xrange = self.stats.alien_xrange[alien_type] #+  random.uniform(-self.stats.alien_xrange[alien_type],0.1)

        # 加载外星人图像并设置其rect属性
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕上左上角附近
        self.rect.x = alien_x_init
        self.rect.y = -100

        # 存储外星人精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    
    def check_edges(self):
        """ 如果外星人碰到运动边缘,就返回True """
        screen_rect = self.screen.get_rect()    
        # 边缘的定义如下
        if (self.rect.right >= min(screen_rect.right + 100,self.alien_x_init + self.alien_xrange/2)) or (self.rect.left <= max(0-50,self.alien_x_init - self.alien_xrange/2)):
            self.direction *= -1

    def update(self):
        """ 更新外星人坐标 """
        self.x += (self.alien_xspeed * self.direction)
        self.rect.x = self.x
        if not (self.alien_type == "boss"): # 非boss
            self.y += (self.alien_yspeed )
            self.rect.y = self.y
        else: # boss
            if self.rect.top < self.screen.get_rect().top + 50:
                self.y += (self.alien_yspeed)
                self.rect.y = self.y