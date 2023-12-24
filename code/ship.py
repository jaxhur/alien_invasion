
from pygame.sprite import Sprite
from copy import deepcopy
class Ship(Sprite):
    """ 管理飞船的类 """
    def __init__(self,ai_game,src,ship_selected = "ship1") :
        # 初始化飞船并设置其初始位置
        super().__init__()
        self.screen  = ai_game.screen
        self.settings = deepcopy(ai_game.settings)
        self.stats = ai_game.stats
        self.screen_rect = ai_game.screen.get_rect()


        # 飞机撞击后会有一段无敌时间
        # 加载飞船图像，并获取其外接矩形
        self.image = src.images['ships'][ship_selected]
        self.rect = self.image.get_rect()
        # 将飞船放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 在飞船属性x中存储float数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 持续移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        """ 根据移动标志调整飞船位置 """
        # 更新飞船而不是rect对象的 x值
        if self.moving_right and self.rect.right < self.screen_rect.right: 
            self.x += self.stats.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.stats.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.stats.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom :
            self.y += self.stats.ship_speed
        # 根据self.x更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """ 在指定位置绘制飞船 """
        self.screen.blit(self.image,self.rect)
    
    def center_ship(self):
        """ 让飞船回到屏幕底部中央 """
        # 让飞机的外接矩形回到屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 让飞机图像回到屏幕底部中央
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


        