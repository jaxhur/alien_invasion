from pygame.sprite import Sprite
import pygame
import random 

class Buff(Sprite):
    """ Buff类 """
    def __init__(self,screen,settings,src,buff_type:str):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.src = src
        self.buff_type = buff_type
        self.buff_speed = self.settings.buff_xspeed
        self.sound = self.src.sounds['sounds']["getbuffs"][buff_type]
        #  加载图片
        self.image = self.src.images['buffs'][buff_type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,self.screen.get_rect().width - self.rect.width) # 随机在屏幕上方出现
        self.rect.y = -100
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    
    def buff_action(self,stats):
        """ buff被吃到后一系列动作 """
        self.sound.play()
        # 0:加血buff
        if self.buff_type == "addhp" :
            if stats.ships_left < stats.ship_max: 
                stats.ships_left += 1
        # 1:增加子弹威力buff
        if self.buff_type == "superbullet":
            stats.last_superbullet_time = pygame.time.get_ticks()
            stats.superbullet_remaintime = self.settings.superbullet_DURATION  # 重新获取该buff时，重置该buff实际应该持续时间
            stats.is_super = True
        # 2:双发子弹
        if  self.buff_type == "doublebullet":
            stats.last_doublebullet_time = pygame.time.get_ticks()
            stats.doublebullet_remaintime = self.settings.doublebullet_DURATION  # 重新获取该buff时，重置该buff实际应该持续时间
            stats.is_double = True

        if  self.buff_type == "protect":
            stats.last_protectship_time = pygame.time.get_ticks()
            stats.protect_remaintime = self.settings.protectship_DURATION  # 重新获取该buff时，重置该buff实际应该持续时间
            stats.is_protected = True

    
    def update(self): 
        """ 更新buff坐标 """
        self.y += self.buff_speed
        self.rect.y = self.y

    def draw_buff(self):
        """ 在屏幕上绘制buff """
        self.screen.blit(self.image,self.rect)
