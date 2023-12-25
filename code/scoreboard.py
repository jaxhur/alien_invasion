import pygame.font
from pygame.sprite import Group
from ship import Ship

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
class Scoreboard:
    """ 显示得分信息 """
    def __init__(self,ai_game,src):
        """ 初始化显示得分涉及的属性 """
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.src = src
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        # 读取最高分
        df = pd.read_csv('./data/history_score.csv')
        self.stats.high_score = df.loc[df['score'].idxmax()]['score']
        # 显示得分
        self.text_color = (78,238,148)
        self.font = pygame.font.Font("./素材/font/2.ttf", 30)
        self.font_deadpage = pygame.font.SysFont("STKaiTi",50)
        # 渲染初始得分图像
        self.prep_img(text = self.stats.score,loc=(self.screen_rect.left ,10),fontsize = 30,type = 'score')
        self.prep_img(text = self.stats.high_score,loc=(self.screen_rect.centerx,0),fontsize = 30,type = 'highscore')
        self.prep_img(text = self.stats.ship_level,loc=(self.screen_rect.left ,40),fontsize = 30,type = 'level' )
        self.prep_img(text = self.stats.ships_left,loc=(self.screen_rect.left ,self.screen_rect.bottom),fontsize = 30,type = 'ships_left' )
        self.prep_img(text = self.stats.diffcuilty,loc=(self.screen_rect.left ,100),fontsize = 30,type = 'diffcuilty' )
        self.prep_score_deadpage()  # 死亡结算
        self.history_score = None

    def prep_img(self,text,loc:tuple,fontsize = 30,type = 'score'):
        """ 渲染初始得分图像 """
        tmp = {'score':"分数:",'highscore':"历史最高分:","level":"等级:","ships_left":"剩余命数:x","diffcuilty":"难度:"}
        if type in ['score','highscore']:
            str = f"{tmp[type]}"+"{:,}".format(round(text,-1) )  # 以10为基本单位
            font = pygame.font.Font("./素材/font/2.ttf", fontsize)
            image = font.render(str,True,self.text_color).convert_alpha() # 记分板背景透明 
            if type == "score":
                self.score_image = image
                self.score_rect = self.score_image.get_rect()
                self.score_rect.left = loc[0]
                self.score_rect.top = loc[1]
            if type == "highscore":
                self.high_score_image = image
                self.high_score_rect = self.high_score_image.get_rect()
                self.high_score_rect.centerx = loc[0]
                self.high_score_rect.top =  loc[1]
        if type in ["level",'ships_left',"diffcuilty"]:
            str = f"{tmp[type]}"+"{:,}".format(text)
            font = pygame.font.Font("./素材/font/2.ttf", fontsize)
            image = font.render(str,True,self.text_color).convert_alpha() # 记分板背景透明 
            if type == "level":
                self.level_image = image
                self.level_rect = self.level_image.get_rect()
                self.level_rect.left = loc[0]
                self.level_rect.top = loc[1]
            if type == "ships_left":
                self.ships_left_image = image
                self.ships_left_rect = self.ships_left_image.get_rect()
                self.ships_left_rect.left = loc[0]
                self.ships_left_rect.bottom = loc[1]
            
            if type == "diffcuilty":
                self.diffcuilty_image = image
                self.diffcuilty_rect = self.diffcuilty_image.get_rect()
                self.diffcuilty_rect.left = loc[0]
                self.diffcuilty_rect.bottom = loc[1]

    def check_high_score(self):
        """ 检查是否出现新的最高分 """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_img(text = self.stats.high_score,loc=(self.screen_rect.centerx,0),fontsize = 40,type = 'highscore')
        
    def show_score(self):
        """ 显示得分 """
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.screen.blit(self.ships_left_image,self.ships_left_rect)
        self.screen.blit(self.diffcuilty_image,self.diffcuilty_rect)


#---------------------------------------------------------------------


    def prep_score_deadpage(self):
        """ 渲染死亡结算本局分数 """
        # 使分数以10为基本单位
        rounded_score = round(self.stats.score,-1)
        score_str = "本局得分: {:,}".format(rounded_score)
        self.score_image_deadpage = self.font_deadpage.render(score_str,True,self.text_color).convert_alpha() # 记分板背景透明
        self.score_rect_deadpage = self.score_image.get_rect()
        self.score_rect_deadpage.left = self.screen.get_rect().centerx - self.screen.get_width()/3
        self.score_rect_deadpage.top = self.screen.get_rect().centery - 150
    


    def prep_high_score_deadpage(self):
        """ 渲染死亡结算最高分 """
        high_score = round(self.stats.high_score,-1)
        high_score_str = f"历史最高分:{high_score:,}"
        self.high_score_image_deadpage = self.font_deadpage.render(high_score_str,True,self.text_color).convert_alpha()  # 记分板背景透明
        # 显示分数
        self.high_score_rect_deadpage = self.score_image.get_rect()
        self.high_score_rect_deadpage.left = self.screen.get_rect().centerx - self.screen.get_width()/3
        self.high_score_rect_deadpage.centery = self.screen.get_rect().centery - 85


    def show_score_on_deadpage(self):
        """ 在结算界面绘制分数 """
        self.screen.blit(self.score_image_deadpage,self.score_rect_deadpage)
        self.screen.blit(self.high_score_image_deadpage,self.high_score_rect_deadpage)
#---------------------------------------------------------------------
    
    def prep_history_score(self):
        """ 最高分以及最近5局分数 """
        df = pd.read_csv('./data/history_score.csv')
        last_5_rows = df.tail(5)
        # 创建图像
        img_size = (300,200)
        img_bg = (255, 255, 255, 0)
        image = Image.new('RGBA', img_size ,img_bg)
        draw = ImageDraw.Draw(image)
        font_size = 20
        font = ImageFont.truetype("./素材/font/2.ttf", font_size)
        font_color = (255, 127, 80,255)  # 完全不透明
        # 最高分
        draw.text((10, 0), f"最高分\t\t{df.columns[0]:^} \t\t\t\t {df.columns[1]:>7} ",fill=font_color, font=font)
        draw.text((10, 25), f"{df.loc[df['score'].idxmax()]['time']:^} {df.loc[df['score'].idxmax()]['score']:>7} ",fill=font_color, font=font)
        # 最近5局
        draw.text((10, 55), f"最近5局\t{df.columns[0]:^} \t\t\t\t {df.columns[1]:>7} ",fill=font_color, font=font)
        text_y = 75
        for _, row in last_5_rows.iterrows():
            text = f"{row['time']:^} {row['score']:>7} "  # 根据实际列名修改
            draw.text((10, text_y), text,fill=font_color, font=font)
            text_y += font_size + 5
 
        # 转换为 Pygame Surface
        image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        pygame_surface = pygame.transform.scale(image,(300,200))  # 调整大小（可选）
        self.history_score = pygame_surface