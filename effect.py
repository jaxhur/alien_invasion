import pygame
from pygame.sprite import  Sprite


class Explosion(Sprite):
    
    def __init__(self,src,center = None,alien_type = None,ship = None) -> None:
        super().__init__()
        self.frame_rate = 50  # 爆炸的帧速率
        if alien_type != None:
            size =(150,150)
            if alien_type == "boss": size = (200,200)
        self.explosion_images = [pygame.transform.scale(i,size) for i in src.images['effects']['explosions']]  # 导入所有爆炸图片
        # 初始帧
        self.current_frame_index = 0
        self.image = self.explosion_images[self.current_frame_index]
        self.rect = self.image.get_rect()  
        self.rect.center = center
        self.x = self.rect.x
        self.y = self.rect.y
        self.last_update = pygame.time.get_ticks()  # 获取最近刷新时间

    def update(self):
        now = pygame.time.get_ticks()  # 获取当前时间
        if now - self.last_update > self.frame_rate:  # 本帧与上一帧的时间差达到fram_rate时，显示1帧爆炸图片
            self.last_update = now  # 记录最近刷新时间
            self.current_frame_index += 1  # 帧数+1，这样下次才会调用下一张图片
            if self.current_frame_index == len(self.explosion_images):  # 当爆炸图片到达最后一帧时，爆炸对象自杀(不再占用内存)
                self.kill()
            else:
                self.image = self.explosion_images[self.current_frame_index]  # 指定要显示的爆炸图片(Surface对象)

class Warning(Sprite):
    def __init__(self,src,center = None) -> None:
        super().__init__()
        self.frame_rate = 200
        self.warning_images = src.images['effects']['warning']
        self.current_frame_index = 0
        self.image = self.warning_images[self.current_frame_index]
        self.rect = self.image.get_rect()  
        self.rect.center = center
        self.x = self.rect.x
        self.y = self.rect.y
        self.last_update = pygame.time.get_ticks() 

    def update(self):
        now = pygame.time.get_ticks()  # 获取当前时间
        if now - self.last_update > self.frame_rate:  # 本帧与上一帧的时间差达到fram_rate时，显示1帧爆炸图片
            self.last_update = now  # 记录最近刷新时间
            self.current_frame_index += 1  # 帧数+1，这样下次才会调用下一张图片
            if self.current_frame_index == len(self.warning_images)*5:  # 当爆炸图片到达最后一帧时，爆炸对象自杀(不再占用内存)
                self.kill()
            else:
                self.image = self.warning_images[self.current_frame_index%2]  # 指定要显示的爆炸图片(Surface对象)

# class Splash(Sprite):
#     def __init__(self,src,center):
#         super().__init__()
#         self.frame_rate = 50
#         self.splash_images = src.images['effects']['splashs']
#         self.current_frame_index = 0
#         self.image = self.self.splash_images[self.current_frame_index]
#         self.rect = self.image.get_rect()  
#         self.rect.center = center
#         self.x = self.rect.x
#         self.y = self.rect.y
#         self.last_update = pygame.time.get_ticks()  # 获取最近刷新时间
    
#     def update(self):
#         now = pygame.time.get_ticks()  # 获取当前时间
#         if now - self.last_update > self.frame_rate:  # 本帧与上一帧的时间差达到fram_rate时，显示1帧爆炸图片
#             self.last_update = now  # 记录最近刷新时间
#             self.current_frame_index += 1  # 帧数+1，这样下次才会调用下一张图片
#             if self.current_frame_index == len(self.explosion_images):  # 当爆炸图片到达最后一帧时，爆炸对象自杀(不再占用内存)
#                 self.kill()
#             else:
#                 self.image = self.explosion_images[self.current_frame_index]  # 指定要显示的爆炸图片(Surface对象)


        
