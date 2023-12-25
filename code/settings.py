class Settings:
    def __init__(self):
        """ 初始化游戏静态设置 """
        # 屏幕设置
        self.screen_width = 500
        self.screen_height = 750
        # 背景滚动速度
        self.background_scroll_speed = 1
        # 初始难度
        self.diffcuilty = 1
        self.diffcuilty_max = 6
        self.diffcuiltyup_thresholds = [2,4,8,12,15]
        # 飞船设置
        self.ship_max = 5
        self.ship_speed = 5
        self.ship_hitharm = 6
        self.ship_levelmax = 5
        self.levelup_thresholds =  [100, 500, 1000, 2000, 3000]
        # 子弹设置
        self.bullet_direction = {"ship":-1,"alien":1}
        self.bullet_xspeed = {"ship":0,"alien":{"boss":1}}
        self.bullet_yspeed = {"ship":2,"alien":{"boss":1.5}}
        self.bullet_damage = {"ship":{"normal":1,"super":2},"alien":{"boss":1}}
        self.bullets_max = {"ship":100,"alien":50} # 存储最大子弹数

        # 外星人设置
        self.alien_max = 3  # 最多能显示的外星人数
        self.alien_hp = {"low":2,"middle":5,"high":10,"boss":150}
        self.alien_point = {"low":10,"middle":30,"high":50,"boss":200}
        self.alien_xspeed = {"low":1.5,"middle":1,"high":0.5,"boss":0}
        self.alien_yspeed = {"low":0.8,"middle":0.5,"high":0.3,"boss":0.5}
        self.alien_xrange = {"low":self.screen_width,"middle":self.screen_width/5*3,
                             "high":self.screen_width/5*2,"boss":0}
        # BOSS设置
        self.BOSS_APPEAR_TIME = 15000   # BOSS出现时间
        self.BOSS_SHOOT_INTERVAL = 3000  # BOSS发射子弹间隔
        # buff设置
        self.buff_types = ["addhp","superbullet","doublebullet",'protect'] # 加血，威力，子弹数
        self.buffs_prob = [0.2,0.25,0.25,0.3]
        self.buff_xspeed = 1.5
        self.buffs_intervals = [2000,2000,1000]  # buff出现间隔(毫秒)
        self.superbullet_DURATION = 6000  # 常数DURATION：增加威力buff有效时间6000毫秒（不包括暂停时间）
        self.doublebullet_DURATION = 6000  #  双发buff持续6000毫秒
        self.protectship_DURATION = 2000  #  保护buff持续2000毫秒