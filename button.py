import pygame
import game_functions as gf
from pygame.sprite import Sprite
import os
from ship import Ship

class Button(Sprite):
    def __init__(self,ai_game,src,center:tuple,button_type:str) :
        super().__init__()
        """ 初始化按钮属性 """
        self.screen = ai_game.screen
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.src = src
        self.button_type = button_type
        # 按键是否按下
        self.button_pressed  = False
        self.button_clicknum = 0
        self.click_button_sound = self.src.sounds['sounds']['clickbutton']
        self.click_button_sound.set_volume(0.2)
        # 创建按钮
        if button_type in["pause","music"] :#两种状态的按钮
            self.images = self.src.images["buttons"][button_type]["button"]
            self.image = self.images[0]
        elif self.button_type in ["ship1", "ship2", "ship3", "ship4","ship5","ship6"]:# 选择船
            self.last_clicktime = 0
            self.selected = False
            self.image =  self.src.images["buttons"][button_type]["button"]
        else:
            self.image =  self.src.images["buttons"][button_type]["button"]
        self.rect = pygame.Rect(0,0,self.image.get_width(), self.image.get_height())  # 创建按钮的碰撞体积(rect矩形)
        self.rect.center= center

    def check_button_pressed(self,mouse_pos = None,ai_game = None):
        """ 检查按钮是否被点击 """
        button_cliked = self.rect.collidepoint(mouse_pos)
        self.button_pressed = button_cliked
        # 首页按钮
        if button_cliked and (not self.stats.game_active) and (not self.stats.is_gameover):
            self.click_button_sound.play()  # 点击按钮音效
            self.button_clicknum += 1
            if self.button_type == "play":  # play按钮
                ai_game.ship = Ship(ai_game,self.src,ai_game.ship_selected.button_type)
                pygame.mixer.music.play(-1)
                # 重置游戏统计信息
                ai_game.stats.reset_stats()
                ai_game.stats.game_active = True
                ai_game.sb.prep_img(text = ai_game.stats.score,loc=(ai_game.screen.get_rect().left,10),fontsize = 30,type = 'score')
                ai_game.sb.prep_img(text = ai_game.stats.ship_level,loc=(ai_game.screen.get_rect().left ,40),fontsize = 30,type = 'level' )
                ai_game.sb.prep_img(text = ai_game.stats.ship_level,loc=(ai_game.screen.get_rect().left ,100),fontsize = 30,type = 'diffcuilty' )
                ai_game.sb.prep_img(text = ai_game.stats.ships_left,loc=(ai_game.screen.get_rect().left ,ai_game.screen.get_rect().bottom),fontsize = 30,type = 'ships_left' )
                #ai_game.sb.prep_ships()
                ai_game.stats.is_boss = False
                ai_game.ship.is_protected = 0
                for button in ai_game.buttons_1:
                        button.button_clicknum = 0 
                # 清除余下的外星人和子弹
                ai_game.aliens.empty()
                ai_game.ship_bullets.empty()
                ai_game.buffs.empty()
                ai_game.boss_bullets.empty()
                ai_game.explosions.empty()
                # 创建一群新的外星人并让飞船居中
                gf.create_fleet(screen = ai_game.screen,settings =  ai_game.settings,stats =  ai_game.stats,src =  ai_game.src,aliens =  ai_game.aliens,warnings = ai_game.warnings)
                ai_game.ship.center_ship()
                pygame.time.set_timer(pygame.USEREVENT + 3, ai_game.settings.BOSS_APPEAR_TIME)
                pygame.time.set_timer(pygame.USEREVENT + 4, ai_game.settings.BOSS_SHOOT_INTERVAL)

            if self.button_type in ["ship1", "ship2", "ship3", "ship4","ship5","ship6"]:
                self.last_clicktime = pygame.time.get_ticks()

        # 局内
        if button_cliked and (self.stats.game_active) and (not self.stats.is_gameover):
            if self.button_type == "pause":  # 暂停按钮
                gf.pause(ai_game)
                self.image =  self.images[self.stats.is_paused]
            
            if self.button_type == "music":  # 背景音乐按钮
                self.image =  self.images[self.stats.music_on]
                if self.stats.music_on:
                    self.stats.music_on = 0
                    pygame.mixer.music.set_volume(0)
                else:
                    self.stats.music_on = 1
                    pygame.mixer.music.set_volume(0.4)
                
                

    def update_button(self):
        if  self.button_type == "pause":  # 暂停按钮
            self.image =  self.images[self.stats.is_paused]
            self.screen.blit(self.image,self.rect)
                




        
