from  pygame.sprite import Sprite
class Bullet(Sprite):
    """ 管理飞机发送的子弹的类 """
    def __init__(self,screen,settings,stats,src,ship,alien = None,type = None,is_left = None,is_right =None):
        super().__init__()  # 调用父类中的初始化
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.ship_rect = ship.rect
        self.src = src
        if type == "ship":  # 武装飞机子弹
            self.bullet_direction = self.settings.bullet_direction[type]  # 向上发射
            self.bullet_yspeed = self.settings.bullet_yspeed[type] * self.stats.ship_level
            if not self.stats.is_super:# 普通子弹
                self.bullet_type = "normal"
                self.bullet_damage = self.settings.bullet_damage[type]['normal'] + self.stats.ship_level
                self.image = self.src.images['bullets']['normal']
            if self.stats.is_super:# 强力子弹
                self.bullet_type = "super"
                self.bullet_damage = self.settings.bullet_damage[type]['super'] + self.stats.ship_level
                self.image = self.src.images['bullets']['super']
            # 在(0,0)处创建一个表示子弹的矩形，在设置正确的位置
            self.rect = self.image.get_rect()
            self.rect.bottom = self.ship_rect.top  # 子弹从飞机顶部出现
            self.rect.centerx = self.ship_rect.centerx

            # 双发子弹
            if self.stats.is_double:
                self.bullet_type = "double"
                if is_left:
                    self.rect.centerx = self.ship_rect.centerx - 20
                if is_right:
                    self.rect.centerx = self.ship_rect.centerx + 20


        if type == "alien":  # 外星人子弹
            self.bullet_direction = self.settings.bullet_direction[type]
            self.bullet_xspeed = self.stats.alien_bullet_xspeed[alien.alien_type]
            self.bullet_yspeed = self.stats.alien_bullet_yspeed[alien.alien_type]
            # BOSS子弹
            #if alien.alien_type == "boss":
            self.bullet_type = alien.alien_type
            self.bullet_damage = self.settings.bullet_damage[type][alien.alien_type]
            self.image = src.images['bullets'][alien.alien_type]

            self.rect = self.image.get_rect()
            self.rect.top = alien.image.get_rect().bottom  
            self.rect.centerx = self.ship_rect.centerx # + random.randint(-50,50)

        # 存储用小数表示的子弹位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        
    def update(self):
        """ 改变子弹 """
        # 更新表示子弹位置的小数值
        self.y += self.bullet_yspeed * self.bullet_direction
        # 更新表示子弹的rect位置、
        self.rect.y = self.y
        if self.bullet_type == "boss" :  # boss子弹
            delta_x  = self.ship_rect.x - self.x
            self.x += ((delta_x>0)-(delta_x<0)) * self.bullet_xspeed
            self.rect.x = self.x

    
    def draw_bullet(self):
        """ 在屏幕上绘制子弹 """
        self.screen.blit(self.image,self.rect)