import pygame
import game_functions as gf 

class Source:
    """ 游戏所有的图片、音频资源 """
    def __init__(self,screen):
        # 图片
        self.images = {}
        # 窗口图标
        icon = pygame.image.load('./素材/img/icon.png') 
        # 背景图片
        img0 = pygame.image.load("./素材/img/bg0.png")
        img1 = pygame.image.load("./素材/img/background_1.png")
        img2 = pygame.image.load("./素材/img/background_2.png")
        images = [img0,img1,img2]
        bgimages = []
        for img in  images:
            bgimages.append(pygame.transform.scale(img,(screen.get_width(),screen.get_height())))
        # 标题
        title = gf.scale_img(pygame.image.load('./素材/img/title.png'),size = (400,100))
        # 按钮
        ## play
        play_img=  gf.scale_img(pygame.image.load("./素材/img/button_play.png"),
                                ratio = 0.25)
        ## 指南
        guide_img = gf.scale_img(pygame.image.load("./素材/img/button_guide.png"),
                                ratio = 0.25)
        guide_page = gf.scale_img(pygame.image.load('./素材/img/guide_page.png'),
                                size = (500,330))
        ## 开发者
        developer_img = gf.scale_img(pygame.image.load("./素材/img/button_developer.png"),
                                ratio = 0.25)
        developer_page = gf.scale_img(pygame.image.load('./素材/img/developer.png'),
                                                ratio = 1)
        ## 历史分数
        history_img =  gf.scale_img(pygame.image.load("./素材/img/button_score.png"),
                                ratio = 0.25)
        
        # 更换飞机
        changeship_img = gf.scale_img(pygame.image.load("./素材/img/button_changeship.png"),
                                ratio = 0.25)
        # 背景音乐
        music_on = gf.scale_img(pygame.image.load("./素材/img/button_music_on.png"),
                                ratio = 0.4)
        music_end = gf.scale_img(pygame.image.load("./素材/img/button_music_end.png"),
                                ratio = 0.25)

        # 暂停
        pause = gf.scale_img(pygame.image.load("./素材/img/button_pause/button_pause.png"),
                                ratio =0.5)
        endpause = gf.scale_img(pygame.image.load("./素材/img/button_pause/button_endpause.png"),
                                ratio = 0.5)
        # 武装飞机
        ship1 = gf.scale_img(pygame.image.load('./素材/img/ship_1.png'),ratio=0.4)
        ship2 = gf.scale_img(pygame.image.load('./素材/img/ship_2.png'),ratio=0.4)
        ship3 = gf.scale_img(pygame.image.load('./素材/img/ship_3.png'),ratio=0.4)
        ship4 = gf.scale_img(pygame.image.load('./素材/img/ship_4.png'),ratio=0.4)
        ship5 = gf.scale_img(pygame.image.load('./素材/img/ship_5.png'),ratio=0.4)
        ship6 = gf.scale_img(pygame.image.load('./素材/img/ship_6.png'),ratio=0.4)
        # 子弹
        normalbullet = gf.scale_img(pygame.image.load('./素材/img/bullet_normal.png'),ratio = 1)
        superbullet = gf.scale_img(pygame.image.load('./素材/img/bullet_super.png'),ratio = 1) 
        bossbullet = gf.scale_img(pygame.image.load('./素材/img/bullet_alien_boss.png'),size = (50, 50)) 
        # 外星人
        alien_low = gf.scale_img(pygame.image.load('./素材/img/alien_low.png'),
                                size = (50, 25))
        alien_middle = gf.scale_img(pygame.image.load('./素材/img/alien_middle.png'),
                                size = (75, 35))
        alien_high = gf.scale_img(pygame.image.load('./素材/img/alien_high.png'),
                                size = (100, 50))
        alien_boss = gf.scale_img(pygame.image.load('./素材/img/alien_boss.png'),
                                size = (screen.get_width(), 150))
        
        # buff
        addhp_buff = gf.scale_img(pygame.image.load('./素材/img/buff_addhp.png'),ratio = 0.5)
        superbullet_buff = gf.scale_img(pygame.image.load('./素材/img/buff_superbullet.png'),ratio = 1)
        doublebullet_buff = gf.scale_img(pygame.image.load('./素材/img/buff_doublebullet.png'),ratio = 1)
        protect_buff = gf.scale_img(pygame.image.load('./素材/img/buff_protect.png'),ratio = 0.5)

        # 特效
        ## 爆炸特效
        explosion_image = []
        for i in range(16):  # 一共载入16张图片
            image = pygame.image.load(f'./素材/effect/explosion/e{i+1}.png').convert_alpha()  # 载入图片，返回Surface对象
            explosion_image.append(image)  # 将Surface对象添加到列表中备用

        ## 溅射特效
        splash_image = []
        for i in range(14):  # 一共载入14张图片
            image = gf.scale_img(pygame.image.load(f'./素材/effect/splash/splash{i}.png').convert_alpha(),ratio=0.1)  # 载入图片，返回Surface对象
            splash_image.append(image)  # 将Surface对象添加到列表中备用
        ## 保护盾
        protect_image = gf.scale_img(pygame.image.load('./素材/img/Protection_cover.png').convert_alpha()
                                               ,size = (60,70))
        
        ## 警告
        warning_image = []
        for i in range(2):  
            image = gf.scale_img(pygame.image.load(f'./素材/effect/warning/warning_{i+1}.png').convert_alpha(),ratio=1)  # 载入图片，返回Surface对象
            warning_image.append(image)  # 将Surface对象添加到列表中备用

        #死亡结算
        enter_deadpage = gf.scale_img(pygame.image.load('./素材/img/enter.png'),ratio = 0.3)
        
        self.images.update({"icon":icon,
                            "bgimages":bgimages,
                            "title":title,
                            "buttons":{
                                "play":{"button":play_img},
                                "guide":{"button":guide_img,"page":guide_page},
                                "developer":{"button":developer_img,"page":developer_page},
                                "history":{"button":history_img},
                                "changeship":{"button":changeship_img},
                                "pause":{"button":[pause,endpause]},
                                "ship1":{"button":ship1},
                                "ship2":{"button":ship2},
                                "ship3":{"button":ship3},
                                "ship4":{"button":ship4},
                                "ship5":{"button":ship5},
                                "ship6":{"button":ship6},
                                "music":{"button":[music_on,music_end]}

                            },
                            "ships":{"ship1":ship1,"ship2":ship2,
                                     "ship3":ship3,"ship4":ship4,
                                     "ship5":ship5,"ship6":ship6},
                            "bullets":{
                                "normal":normalbullet,
                                "super":superbullet,
                                "boss":bossbullet
                            },
                            "aliens":{
                                "low":alien_low,
                                "middle":alien_middle,
                                "high":alien_high,
                                "boss":alien_boss
                            },
                            "buffs":{
                                "addhp":addhp_buff,
                                "superbullet":superbullet_buff,
                                "doublebullet":doublebullet_buff,
                                "protect":protect_buff
                            },
                            "effects":{
                                        "explosions":explosion_image,
                                        "splashs":splash_image,
                                        "protect":protect_image,
                                        "warning":warning_image

                            },
                            "deadpage":{
                                "enter":enter_deadpage
                            }
                            })
        
        # 音乐
        self.sounds = {}
        ## music
        ### BGM
        bgm1 = './素材/music/BGM1.mp3'
        bgm2 = './素材/music/BGM2.mp3'
        bgms = [bgm1,bgm2]
        ## 音效
        clickbutton_sound = pygame.mixer.Sound('./素材/sound/clickbutton.mp3')
        clickbutton_sound.set_volume(0.1)
        ## 射击音效
        shootsound = pygame.mixer.Sound('./素材/sound/shoot.wav')  
        shootsound.set_volume(0.05)
        ## 射中外星人音效
        bullet_alien_collisionsound = pygame.mixer.Sound('./素材/sound/bullet_alien_collision.wav')  
        bullet_alien_collisionsound.set_volume(0.2)
        ## 获得buff音效
        getbuff_addhp_sound = pygame.mixer.Sound('./素材/sound/getbuff_addhp.wav')  
        getbuff_doublebullet_sound = pygame.mixer.Sound('./素材/sound/getbuff_doublebullet.wav')  
        getbuff_superbullet_sound = pygame.mixer.Sound('./素材/sound/getbuff_superbullet.wav')
        getbuff_protect_sound = pygame.mixer.Sound('./素材/sound/getbuff_addhp.wav')
        
        getbuff_addhp_sound.set_volume(0.1)
        getbuff_doublebullet_sound.set_volume(0.4)
        getbuff_protect_sound.set_volume(0.1)
        getbuff_superbullet_sound.set_volume(0.1)
        # boss出现音效
        boss_up = pygame.mixer.Sound('./素材/sound/boss_up.MP3')  
        # 失败
        fail = pygame.mixer.Sound('./素材/sound/fail.mp3')
        fail.set_volume(0.2)
        self.sounds.update({"BGMs":bgms,
                           "sounds":{
                               "clickbutton":clickbutton_sound,
                               "shoot":shootsound,
                               "bullet_alien_collision":bullet_alien_collisionsound,
                               "getbuffs":{
                                   "addhp":getbuff_addhp_sound,
                                   "doublebullet":getbuff_doublebullet_sound,
                                   "superbullet":getbuff_superbullet_sound,
                                   "protect":getbuff_protect_sound
                               },
                               "bossup":boss_up,
                               "fail":fail
                           }
            }
        ) 