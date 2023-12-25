import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import  game_functions  as gf
from buff import Buff
from effect import Explosion
import random
from load_source import Source
import math
import copy

class AlienInvasion:
    """ 管理游戏资源与行为的类 """
    def __init__(self):
        pygame.init()   
        self.settings = Settings()
        self.stats = GameStats(self)   # 创建一个用于存储游戏统计信息/状态的实例
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))  # 窗口大小
        pygame.display.set_caption('外星人入侵')  # 窗口标题
        self.src = Source(self.screen)  # 导入游戏所有需要的资源（图片、音频）
        pygame.display.set_icon(self.src.images["icon"])  # 窗口图标
        self.sb = Scoreboard(self,self.src)  # 计分板
        self.ship = Ship(self,self.src) # 创建飞船
        self.clock = pygame.time.Clock()  # 帧率设置
        
        # 背景设置
        self.homepage = self.src.images["bgimages"][0]
        self.background_image = self.src.images["bgimages"][random.choice([2,1])]
        self.background_rect = self.background_image.get_rect()
        self.background_y = 0
        # 首页
        ## 标题
        self.title =  self.src.images["title"]
        self.buttons_1 = pygame.sprite.Group()  # 首页按钮编组
        ## play按钮
        self.play_button = Button(self,src = self.src,center = (self.screen.get_rect().centerx,380-50),button_type = "play")
        ## 操作指南按钮
        self.guide_button = Button(self,src = self.src,center = (self.screen.get_rect().centerx - 80,380 ),button_type = "guide")
        self.guide_page = self.src.images['buttons']['guide']['page']

        ## 历史分数
        self.score_button = Button(self,src = self.src,center = (self.screen.get_rect().centerx + 80,380),button_type = "history")
        ## 更换飞机
        self.changeship_button = Button(self,src = self.src,center = (self.screen.get_rect().centerx - 80,380+50),button_type = "changeship")
        ## 开发人员
        self.developer_button = Button(self,src = self.src,center = (self.screen.get_rect().centerx+ 80,380+50),button_type = "developer")
        self.developer_page = self.src.images['buttons']['developer']['page']

        

        
        self.buttons_1.add(self.play_button,self.guide_button,self.developer_button,self.score_button,self.changeship_button )

        ### 更换飞机内部的飞机按钮
        self.ship_buttons = []
        for i in range(len(self.src.images['ships'])):
            self.ship_buttons.append(Button(self,src = self.src,center = (80+50*(i+1),100),button_type = f"ship{i+1}"))
        self.ship_selected = self.ship_buttons[0]

        # 游戏内按钮
        self.buttons_2 = pygame.sprite.Group()
        # 暂停按钮
        self.pause_button = Button(self,src = self.src,center = (self.screen.get_rect().right -50,self.screen.get_rect().bottom - 50),button_type = "pause")

        # 背景音乐按钮
        self.music_button = Button(self,src = self.src,center = (self.screen.get_rect().right -50,self.screen.get_rect().bottom -100),button_type = "music")
        self.buttons_2.add(self.pause_button,self.music_button)

        # 死亡结算画面
        self.enter_deadpage =  self.src.images['deadpage']['enter']
        # 游戏暂停
        self.pause_end_time = 0 
        self.pause_start_time = 0
        self.pause_duration = 0
        self.buff_superbullet_pause_duration = 0
        self.buff_doublebullet_pause_duration = 0
        # BGM
        pygame.mixer.music.load(self.src.sounds['BGMs'][random.choice([0,1])])
        pygame.mixer.music.set_volume(0.3)
        # 音效     
        ## 点击按钮音效
        self.click_button_sound = self.src.sounds['sounds']['clickbutton']
        ## 射击音效
        self.shootsound = self.src.sounds['sounds']['shoot']
        ## 射中外星人音效
        self.bullet_splash_sound = self.src.sounds['sounds']['bullet_alien_collision']
        ## 获得buff音效
        self.getbuff_addhp_sound = self.src.sounds['sounds']['getbuffs']['addhp']
        self.getbuff_doublebullet_sound =self.src.sounds['sounds']['getbuffs']['doublebullet'] 
        self.getbuff_superbullet_sound = self.src.sounds['sounds']['getbuffs']['superbullet']
        self.getbuff_protect_sound = self.src.sounds['sounds']['getbuffs']['protect']
        # buff设置
        self.protectship_image = self.src.images['effects']['protect']

        
        self.boss_bullets = pygame.sprite.Group()  # boss子弹编组
        self.ship_bullets = pygame.sprite.Group()  # 子弹编组
        self.aliens = pygame.sprite.Group()   # 外星人编组
        self.buffs = pygame.sprite.Group()    # buff编组
        self.explosions = pygame.sprite.Group()  # 爆炸特效编组
        self.warnings = pygame.sprite.Group()
        gf.create_fleet(screen=self.screen,settings=self.settings,stats=self.stats,src = self.src,aliens = self.aliens,warnings = self.warnings)
        # 窗口图标
        pygame.display.set_icon(self.src.images["icon"])  # 窗口图标
        
        
    def run_game(self):
        """ 开始游戏循环 """
        while True:
            self._check_events()
            if self.stats.game_active:
                if not self.stats.is_paused:
                    self.ship.update()  # 飞船移动
                    gf.update_buff(screen=self.screen,settings =self.settings,stats = self.stats,
                                   sb= self.sb,src= self.src,ship =self.ship,buffs=self.buffs)
                    gf.update_fleet(screen=self.screen,settings =self.settings,stats = self.stats,
                                    sb= self.sb,src= self.src,ship =self.ship,aliens = self.aliens,
                                    explosions=self.explosions,warnings = self.warnings,bullet_splash_sound=self.bullet_splash_sound)
                    # self.update_bullets()
                    gf.update_bullets(screen=self.screen,settings = self.settings,stats=self.stats,sb=self.sb,src=self.src,
                                      ship = self.ship,aliens=self.aliens,ship_bullets=self.ship_bullets,explosions=self.explosions,
                                      bullet_splash_sound=self.bullet_splash_sound,
                                      boss_bullets =self.boss_bullets,type = "ship")
                    gf.update_bullets(screen=self.screen,settings = self.settings,stats=self.stats,sb=self.sb,src=self.src,
                                      ship = self.ship,aliens=self.aliens,ship_bullets=self.ship_bullets,explosions=self.explosions,
                                      bullet_splash_sound=self.bullet_splash_sound,
                                      boss_bullets =self.boss_bullets,type = "alien")
                    
                    #self.update_boss_bullets()
                    self.explosions.update()
                    self.warnings.update()
            else:
                # 不处于游戏状态，关闭音乐、音效
                pygame.mixer.music.stop()
                self.shootsound.stop()
                # 停止 BOSS 定时器
                pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                pygame.time.set_timer(pygame.USEREVENT + 4, 0)
            self._update_screen()
    
    def _check_events(self):
        """ 
        按键与鼠标事件 
        调用下面的_check_play_button,_check_keydown_events,_check_keyup_events实现监听
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 退出
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: # 按下
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # 抬起
                self.check_keyup_events(event) 

            elif event.type == pygame.MOUSEBUTTONDOWN:  # 点击
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons_1:
                    if button.button_type =="play": # play按钮
                        button.check_button_pressed(mouse_pos,self)
                    else:
                        button.check_button_pressed(mouse_pos)
                for button in self.buttons_2:
                    if button.button_type == "pause":
                        button.check_button_pressed(mouse_pos,self)
                    else:
                        button.check_button_pressed(mouse_pos)
                if self.changeship_button.button_clicknum % 2:
                    for button in self.ship_buttons:
                        button.check_button_pressed(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons_1:
                    button.button_pressed = False
                for button in self.buttons_2:
                    button.button_pressed = False
                for button in self.ship_buttons:
                    button.button_pressed = False
            elif event.type == pygame.USEREVENT + 3:
                self.stats.is_boss = True
            elif event.type == pygame.USEREVENT + 4 and self.stats.is_boss and self.stats.boss_exists:
                gf.fire_bullet(screen=self.screen,settings = self.settings,stats = self.stats,src = self.src,
                               ship = self.ship,aliens = self.aliens,boss_bullets = self.boss_bullets,type = "alien")
                
#---------------------键盘事件------------------
    def _check_keydown_events(self,event):
        """ 响应按下按键 """
        if event.key ==pygame.K_RIGHT:
            self.ship.moving_right =True
        elif event.key ==pygame.K_LEFT:
            self.ship.moving_left =True
        elif event.key ==pygame.K_UP:
            self.ship.moving_up = True
        elif event.key ==pygame.K_DOWN:
            self.ship.moving_down =True
        elif event.key ==pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if not self.stats.is_paused: # 暂停时不能发射子弹
                gf.fire_bullet(screen=self.screen,settings = self.settings,stats = self.stats,src = self.src,
                               ship = self.ship,ship_bullets = self.ship_bullets,type = "ship")
                self.shootsound.play()
        elif event.key == pygame.K_p: # 暂停
            gf.pause(self)
            self.pause_button.update_button()
            
        # 死亡结算后，enter返回主界面
        elif event.key == pygame.K_RETURN:
            self.stats.is_gameover = False

    def check_keyup_events(self,event):
        """ 响应按键松开 """
        if event.key ==pygame.K_RIGHT:
            self.ship.moving_right = False 
        elif event.key ==pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key ==pygame.K_UP:
            self.ship.moving_up = False
        elif event.key ==pygame.K_DOWN:
            self.ship.moving_down = False

# ----------------------------------------------------------------------
    def _update_screen(self):
        """ 更新屏幕上的图像并切换到新屏幕。 """
        # 背景
        #print(self.stats.is_double)
        self.screen.blit(self.homepage, (0, 0))
        # 如果游戏处于非活动状态----首页
        if not self.stats.game_active:
            if self.stats.is_gameover:
                self.sb.prep_score_deadpage()
                self.sb.prep_high_score_deadpage()
                self.sb.show_score_on_deadpage()
                self.screen.blit(self.enter_deadpage,(self.screen.get_rect().centerx - self.enter_deadpage.get_width()/2,self.screen.get_rect().centery +self.screen.get_height()/3 ))
            else:
                self.screen.blit(self.title,(self.screen.get_rect().centerx - 200,self.screen.get_rect().centery - 200))
                # 点击按钮的效果（图片变透明）
                for button in self.buttons_1:
                    if not button.button_pressed:  # 未点击按钮
                        self.screen.blit(button.image,button.rect)
                    else :# 点击按钮
                        img = button.image.copy()
                        img.set_alpha(128)
                        self.screen.blit(img,button.rect)
                # 点击按钮次数
                if self.guide_button.button_clicknum % 2:
                    self.screen.blit(self.guide_page,(self.screen.get_rect().centerx - self.guide_page.get_width()/2,
                                                    self.screen.get_rect().centery + 75))
                if self.developer_button.button_clicknum % 2:
                    self.screen.blit(self.developer_page,(self.screen.get_rect().left ,self.screen.get_rect().top))
                if self.score_button.button_clicknum % 2 and not self.stats.game_active:
                    self.sb.prep_history_score()
                    self.screen.blit(self.sb.history_score,(self.screen.get_rect().centerx - self.sb.history_score.get_width()/2,
                                                        self.screen.get_rect().bottom - self.sb.history_score.get_height()-20))
                # 更换飞机外表
                if self.changeship_button.button_clicknum %2 and not self.stats.game_active:
                    tmp = [button.last_clicktime for button in self.ship_buttons]
                    maxindex = tmp.index(max(tmp))
                    self.ship_selected = self.ship_buttons[maxindex]
                    self.ship_selected.selected = True
                    for button in self.ship_buttons:
                        if button.button_type != self.ship_selected.button_type:
                            button.selected = False
                        self.screen.blit(button.image,button.rect)
                    pygame.draw.rect(self.screen, (0, 255, 0), self.ship_selected.rect, 2)  # 选中的飞机边框为绿色
                    
        if self.stats.game_active: # 游戏开始才开始绘制飞机等对象
            if not self.stats.is_paused:  # 非暂停状态下滚动
                # 背景滚动
                self.background_y += self.settings.background_scroll_speed *(self.stats.diffcuilty/5+4/5)
                if self.background_y > self.settings.screen_height:
                    self.background_y = 0
            # 背景滚动
            self.screen.blit(self.background_image, (0, self.background_y - self.settings.screen_height))
            self.screen.blit(self.background_image, (0, self.background_y))
            self.aliens.draw(self.screen)  # 画出外星人
            self.ship.blitme()  # 画出武装飞机
            self.sb.show_score()
            # 遍历编组bullets中的精灵
            for bullet in self.ship_bullets.sprites():
                bullet.draw_bullet()
            # 绘制buff
            for buff in self.buffs.sprites():
                buff.draw_buff()
            for bullet in self.boss_bullets.sprites():
                bullet.draw_bullet()            
            for button in self.buttons_2:
                self.screen.blit(button.image,button.rect)
            self.explosions.draw(self.screen)
            self.warnings.draw(self.screen)
            # 绘制boss血条
            if  self.stats.is_boss and not(self.stats.is_gameover):
                gf.show_bosshp(self.screen,self.stats,self.aliens)
        # 绘制保护盾
        if self.stats.is_protected and self.stats.game_active:
            self.screen.blit(self.protectship_image,
                             (self.ship.x + (self.ship.image.get_width() - self.protectship_image.get_width()) / 2,
                            self.ship.y +(self.ship.image.get_height() -  self.protectship_image.get_height()) / 2))
        

            
        pygame.display.flip()  #刷新屏幕
        self.clock.tick(144)  # 设置帧率

if __name__ =='__main__':
    ai = AlienInvasion()

    ai.run_game()