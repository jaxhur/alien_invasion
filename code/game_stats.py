import pandas as pd
import datetime
from  copy import deepcopy,copy
class GameStats:
    """ 跟踪游戏的统计信息 """
    def __init__(self,ai_game):
        """ 初始化统计信息 """
        self.settings = deepcopy(ai_game.settings)
        self.high_score = 0  # 最高得分
        self.reset_stats()

    def reset_stats(self):
        """ 初始化在游戏运行期间可能变化的统计信息 """
        self.ships_left = deepcopy(self.settings.ship_max)- 2  # 可用的飞船数，也就是命数
        self.score = 0  # 局内分数
        self.music_on = 1
        # 游戏一开始处于非活动状态
        self.game_active = False
        self.is_paused = False
        self.is_gameover = False
        self.is_boss = False
        self.boss_exists = False

        # 游戏难度
        self.boss_down = 0
        self.diffcuilty = deepcopy(self.settings.diffcuilty)
        self.alien_max = deepcopy(self.settings.alien_max)

        # 飞船数值
        self.ship_level = 1
        self.ship_hitharm = deepcopy(self.settings.ship_hitharm) # 飞机撞击伤害
        self.ship_speed = deepcopy(self.settings.ship_speed)  # 飞机速度
        self.ship_max = deepcopy(self.settings.ship_max) # 飞机最大血量


        # 飞机状态
        self.is_super = False
        self.is_double = False
        self.is_protected = False
        self.last_buff_time = 0 # 上次生成一个buff的时刻
        self.last_superbullet_time = 0    # 上次获取buff时刻
        self.last_doublebullet_time = 0
        self.last_protectship_time = 0  
        self.buffs_intervals = copy(self.settings.buffs_intervals)  # buff出现间隔(毫秒)
        self.superbullet_remaintime = copy(self.settings.superbullet_DURATION)  # buff应当持续的时间（包括暂停时间），初始没有暂停时就是等于DURATION这个创数
        self.doublebullet_remaintime = copy(self.settings.doublebullet_DURATION)
        self.protectship_remaintime =copy(self.settings.protectship_DURATION)

        # 外星人数值
        self.alien_hp = deepcopy(self.settings.alien_hp)
        self.alien_point = deepcopy(self.settings.alien_point)
        self.alien_xspeed = deepcopy(self.settings.alien_xspeed)
        self.alien_yspeed = deepcopy(self.settings.alien_yspeed)
        self.alien_xrange = deepcopy(self.settings.alien_xrange)
        self.alien_bullet_xspeed = deepcopy(self.settings.bullet_xspeed["alien"])
        self.alien_bullet_yspeed = deepcopy(self.settings.bullet_yspeed["alien"])
    


    def store_score(self):
        """ 游戏结束时存储分数 """
        df = pd.read_csv("./data/history_score.csv")
        now = datetime.datetime.now()
        current_time = now.strftime("%Y/%m/%d %H:%M:%S")
        new_row = {"time":current_time,"score":self.score}
        df = pd.concat([df,pd.DataFrame([new_row])],ignore_index = True)
        df.to_csv("./data/history_score.csv",index = False)
        print(f"已向文件中追加一行数据：[{current_time}, {self.score}]")
        

