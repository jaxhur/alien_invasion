import pygame
import random
from alien import Alien
from bullet import Bullet
from buff import Buff
from effect import Explosion,Warning
from copy import deepcopy 
import math

def scale_img(img,ratio=None,size = None):
        """  缩放图片 """
        if ratio is not None:  # 百分比缩放
            target_size = (int(img.get_width() * ratio ),int(img.get_height() * ratio))
            scaled_img = pygame.transform.scale(img,(target_size[0], target_size[1]))
            return scaled_img
        if ratio == None:  # 指定大小
            scaled_img = pygame.transform.scale(img,(size[0], size[1]))
            return scaled_img

def levelup(screen,settings,stats,sb,src,ship):
    levelup_thresholds = deepcopy(settings.levelup_thresholds)
    if stats.ship_level <= settings.ship_levelmax:
        if stats.score >= levelup_thresholds[stats.ship_level-1]:
            stats.ship_level += 1
            stats.ship_speed +=0.5
            stats.ship_max += 1
            stats.ship_hitharm += 2
            ship.image = src.images['ships'][f'ship{stats.ship_level}']
            if stats.ships_left < stats.ship_max:
                stats.ships_left += 1
            sb.prep_img(text = stats.ships_left,loc=(screen.get_rect().left ,screen.get_rect().bottom),fontsize = 30,type = 'ships_left' )
            
            
def diffcuiltyup(screen,settings,stats,sb,src,ship):
    diffcuiltyup_thresholds = deepcopy(settings.diffcuiltyup_thresholds)
    if stats.diffcuilty < settings.diffcuilty_max:
        if stats.boss_down >= diffcuiltyup_thresholds[stats.diffcuilty - 1]:
            stats.diffcuilty += 1
            sb.prep_img(text = stats.diffcuilty,loc=(screen.get_rect().left ,100),fontsize = 30,type = 'diffcuilty' )
            #stats.alien_max += 1
            B = math.exp(-1*stats.diffcuilty/2)+1  # 增加比值
            for key in stats.alien_hp:
                stats.alien_hp[key] = math.ceil(stats.alien_hp[key]*B)
            for key in stats.alien_xspeed:
                stats.alien_xspeed[key] = stats.alien_xspeed[key]*B
            for key in stats.alien_yspeed:
                stats.alien_yspeed[key] = stats.alien_yspeed[key]*B
            for key in stats.alien_xrange:
                stats.alien_xrange[key] = stats.alien_xrange[key]*B
            for key in stats.alien_bullet_xspeed:
                stats.alien_bullet_xspeed[key] = stats.alien_bullet_xspeed[key]*B
            for key in stats.alien_bullet_yspeed:
                stats.alien_bullet_yspeed[key] = stats.alien_bullet_yspeed[key]*B
def pause(ai_game):
    """ 暂停的一系列动作 """
    ai_game.stats.is_paused = not ai_game.stats.is_paused  
    if ai_game.stats.is_paused:  # 暂停
        ai_game.pause_start_time = pygame.time.get_ticks()
        pygame.time.set_timer(pygame.USEREVENT + 3, 0)
        pygame.time.set_timer(pygame.USEREVENT + 4, 0)
        pygame.mixer.music.pause()
    else:  # 结束暂停
        pygame.time.set_timer(pygame.USEREVENT + 3, ai_game.settings.BOSS_APPEAR_TIME)
        pygame.time.set_timer(pygame.USEREVENT + 4, ai_game.settings.BOSS_SHOOT_INTERVAL)
        ai_game.pause_duration = pygame.time.get_ticks() - ai_game.pause_start_time  # 暂停时间
        # 给buff应当持续时间加上暂停时间
        ai_game.stats.superbullet_remaintime += ai_game.pause_duration  
        ai_game.stats.doublebullet_remaintime += ai_game.pause_duration  
        ai_game.stats.protectship_remaintime += ai_game.pause_duration
        pygame.mixer.music.unpause()

#-------------------------bullet begin------------------
def fire_bullet(screen,settings,stats,src,ship,ship_bullets=None,aliens = None,boss_bullets=None,type = None):
    """ 创建一颗飞船/外星人子弹,并将其加入编组bullets;alien,boss_bullets只有外星人才用到.bullets只有飞船用;ship都要用"""
    if type == "ship":
        if len(ship_bullets) < settings.bullets_max[type]:
            if stats.is_double:
                bullet_left = Bullet(screen = screen,settings=settings,stats =stats,src=src,ship=ship,is_left=True,type = type)
                bullet_right = Bullet(screen = screen,settings=settings,stats =stats,src=src,ship=ship,is_right=True,type = type)
                ship_bullets.add(bullet_left,bullet_right)
            else:
                new_bullet = Bullet(screen = screen,settings=settings,stats =stats,src=src,ship=ship,type = type)
                ship_bullets.add(new_bullet)  # 加入bullets编组
    if type == "alien":
        if stats.is_boss and stats.boss_exists and (not stats.is_paused):  # BOSS存在
            if len(boss_bullets) < settings.bullets_max[type]:
                boss_sprites = [alien for alien in aliens.sprites() if alien.alien_type == "boss"]
                new_bullet = Bullet(screen = screen,settings=settings,stats =stats,src=src,ship=ship,alien = boss_sprites[0],type = type)
                boss_bullets.add(new_bullet)

def update_bullets(screen,settings,stats,sb,src,ship,aliens,ship_bullets,explosions,bullet_splash_sound,boss_bullets,type = "ship"):
    """ 更新子弹的位置并删除消失的子弹 """
    if type == "ship":
        # 更新编组内子弹的位置
        ship_bullets.update()
        # 子弹到达顶部，则删除
        for bullet in ship_bullets.copy():
            if bullet.rect.bottom <= 0:
                ship_bullets.remove(bullet)
        #print(aliens)
        check_bullet_alien_collisions(screen = screen,settings = settings,stats = stats,sb=sb,src=src,ship = ship,ship_bullets = ship_bullets,
                                      aliens = aliens,explosions = explosions,bullet_splash_sound = bullet_splash_sound)
    
    if type == "alien":
        boss_bullets.update()
        # 删除消失的子弹
        for bullet in boss_bullets.copy():
            if bullet.rect.top > screen.get_rect().height:
                boss_bullets.remove(bullet)

        check_bullet_ship_collisions(screen = screen,settings = settings,stats = stats,sb=sb,src =src,ship = ship,boss_bullets = boss_bullets,
                                     bullet_splash_sound = bullet_splash_sound)

def check_bullet_alien_collisions(screen ,settings,stats,sb,src,ship,ship_bullets,aliens,explosions,bullet_splash_sound):
    """ 响应子弹和外星人碰撞 """
    #print(aliens)
    collisions = pygame.sprite.groupcollide(
            ship_bullets,aliens,True,False#, pygame.sprite.collide_mask
    )  
    if collisions:  # collisions={bullet:aliens},就是一个子弹对应多个外星人精灵
        bullet_splash_sound.play()
        for bullet,hittedaliens in collisions.items():  # 遍历所有被子弹射中的外星人,这边的hittedaliens别命名为aliens会与上面aliens冲突
            for alien in hittedaliens :  
                alien.hp -= bullet.bullet_damage
                if alien.hp <= 0:
                    levelup(screen,settings,stats,sb,src,ship)
                    stats.score += alien.point
                    aliens.remove(alien)
                    if alien.alien_type == "boss": 
                        stats.is_boss = False
                        stats.boss_exists = False
                        stats.boss_down += 1
                        diffcuiltyup(screen =screen,settings=settings,stats=stats,sb = sb,src=src,ship=ship)
                        pygame.time.set_timer(pygame.USEREVENT + 3, settings.BOSS_APPEAR_TIME)
                    explosion = Explosion(src = src,center = alien.rect.center,alien_type = alien.alien_type)  # 实例化爆炸对象，爆炸中心=敌人中心位置
                    explosions.add(explosion)
                    sb.prep_img(text = stats.score,loc=(screen.get_rect().left,10),fontsize = 30,type = 'score')
                    sb.prep_img(text = stats.ship_level,loc=(screen.get_rect().left ,40),fontsize = 30,type = 'level' )
                    sb.check_high_score()

def check_bullet_ship_collisions(screen,settings,stats,sb,src,ship,boss_bullets,bullet_splash_sound):
    """ 相应外星人子弹与飞船碰撞 """
    collisions = pygame.sprite.spritecollide(ship,boss_bullets,False)
    if collisions: # 发生碰撞
        for bullet in collisions:  # 对于每个与飞机相撞的子弹
            if (not stats.is_protected):  #若不处于保护状态
                protect_ship(settings,stats,bullet_splash_sound)
                stats.ships_left -= 1
            sb.prep_img(text = stats.ships_left,loc=(screen.get_rect().left ,screen.get_rect().bottom),fontsize = 30,type = 'ships_left' )
            boss_bullets.remove(bullet)
            if stats.ships_left <= 0:  # 没命了
                stats.game_active = False
                stats.is_gameover = True
                stats.store_score()
                ship.center_ship()
                src.sounds['sounds']['fail'].play()
                pygame.mouse.set_visible(True)
                break
#-------------------------bullet end------------------


# ------------------------外星人begin---------------
def create_alien(screen,settings,stats,src,aliens,warnings):
    """ 创建一个外星人 """
    stats.boss_exists = any(alien.alien_type == "boss" for alien in aliens)
    if not stats.is_boss and (not stats.boss_exists):  # 非BOSS战
        alien_type = random.choice(["low","middle","high"])
        x = random.randint(0, screen.get_rect().width - 50)  # 随机出现在屏幕顶部
        alien = Alien(screen,settings,stats,src = src,alien_x_init=x,alien_type=alien_type)
        aliens.add(alien)
    else: # BOSS战状态
        if (not stats.boss_exists):
            alien_type = "boss"
            x = screen.get_rect().x
            warning = Warning(src = src,center = (screen.get_rect().centerx,screen.get_rect().centery-screen.get_height()/3))  # 实例化爆炸对象，爆炸中心=敌人中心位置
            warnings.add(warning)
            src.sounds['sounds']['bossup'].play()
            alien = Alien(screen,settings,stats,src = src,alien_x_init=x,alien_type=alien_type)
            aliens.add(alien)
            pygame.time.set_timer(pygame.USEREVENT + 3, 0)


def create_fleet(screen,settings,stats,src,aliens,warnings):
    """ 开始的时候，创建一个外星人群 """
    while (len(aliens) < stats.alien_max) and(not stats.is_boss) :
        create_alien(screen = screen,settings = settings,stats = stats,src = src,aliens = aliens,warnings=warnings)

def update_fleet(screen,settings,stats,sb,src,ship,aliens,explosions,warnings,bullet_splash_sound):
    """ 删除屏外外星人，检测外星人与飞机碰撞 """
    # 检测外星人是否到达边缘，到达x运动边缘改变方向，到达底部则从精灵组删除
    for alien in aliens.sprites():
        alien.check_edges()
        if alien.y > screen.get_height(): # 外星人飞出底部，则从精灵组中删除
            aliens.remove(alien)
    aliens.update()
    check_ship_alien_collisions(screen=screen,settings = settings,stats = stats,sb=sb,src = src,ship= ship,aliens = aliens,explosions=explosions,warnings = warnings,bullet_splash_sound= bullet_splash_sound)

def check_ship_alien_collisions(screen,settings,stats,sb,src,ship,aliens,explosions,warnings,bullet_splash_sound):
    """ 检查外星人/飞船之间的碰撞 """
    alien_hitted = pygame.sprite.spritecollide(ship,aliens,False)#, pygame.sprite.collide_mask)
    if pygame.sprite.spritecollide(ship,aliens,False):  # 外星人\飞船碰撞后，不删除外星人
        if (not stats.is_protected):  # 不处于保护状态，则相应被撞
            ship_hit(screen = screen,stats=stats,settings = settings,sb =sb,src = src,ship = ship,aliens =aliens,alien_hitted=alien_hitted,explosions=explosions)
            protect_ship(settings,stats,bullet_splash_sound)
            
        else:
            # print("保护阶段",ai_game.protectship_remaintime)
            pass
    if pygame.time.get_ticks() - stats.last_protectship_time > stats.protectship_remaintime:
        stats.is_protected = False
    # 外星人数减少时进行创建
    if len(aliens) < stats.alien_max and(not stats.is_boss):
        create_alien(screen = screen,settings = settings,stats = stats,src = src,aliens = aliens,warnings = warnings)
    if stats.is_boss and (not stats.boss_exists):
        create_alien(screen = screen,settings = settings,stats = stats,src = src,aliens = aliens,warnings = warnings)


def ship_hit(screen,stats,settings,sb,src,ship,aliens,alien_hitted,explosions):
    """ 响应飞船被外星人撞到 """
    stats.ships_left -= 1
    sb.prep_img(text = stats.ships_left,loc=(screen.get_rect().left ,screen.get_rect().bottom),fontsize = 30,type = 'ships_left' )
    for alien in alien_hitted:
        alien.hp -= stats.ship_hitharm
        if alien.hp <=0:
            stats.score += alien.point
            levelup(screen,settings,stats,sb,src,ship)
            sb.prep_img(text = stats.score,loc=(screen.get_rect().left,10),fontsize = 30,type = 'score')
            sb.prep_img(text = stats.ship_level,loc=(screen.get_rect().left ,40),fontsize = 30,type = 'level' )
            aliens.remove(alien)
            if alien.alien_type == "boss": 
                stats.is_boss = False
                stats.boss_exists = False
                stats.boss_down += 1
                pygame.time.set_timer(pygame.USEREVENT + 3, settings.BOSS_APPEAR_TIME)
                diffcuiltyup(screen =screen,settings=settings,stats=stats,sb = sb,src=src,ship=ship)
            explosion = Explosion(src = src,center = alien.rect.center,alien_type = alien.alien_type)  # 实例化爆炸对象，爆炸中心=敌人中心位置
            explosions.add(explosion)
    #sb.prep_ships()
    if stats.ships_left <= 0: # 没命了，游戏非激活状态，鼠标可视
        stats.game_active = False
        stats.is_gameover = True
        ship.center_ship()
        stats.store_score()
        src.sounds['sounds']['fail'].play()
        pygame.mouse.set_visible(True)

def show_bosshp(screen,stats,aliens):
    boss = [alien for alien in aliens if alien.alien_type == "boss"]

    bar_width,bar_height= 300, 20 #血条大小
    bar_x,bar_y = (screen.get_width() - bar_width) // 2,50  # 血条位置
    # 血条框
    border_width, border_height= bar_width+2,bar_height+2
    border_x,border_y = bar_x ,bar_y -1
    border_size = 3
    border_color = (205,155 ,29, 255) 
        
    frame_surface = pygame.Surface((border_width, border_height), pygame.SRCALPHA)
    # 绘制血条框
    pygame.draw.rect(frame_surface, border_color , (0, 0, border_width,border_height), border_size,border_radius=bar_height // 2)
    screen.blit(frame_surface, (border_x, border_y))

    # 绘制Boss血条
    health_percentage = boss[0].hp / stats.alien_hp['boss']
    health_bar_width = int(bar_width * health_percentage)
    pygame.draw.rect(screen, (255,0,0), (bar_x, bar_y, health_bar_width, bar_height),border_radius=bar_height // 2)

    # 绘制当前血量数字
    font = pygame.font.Font(None, 36)   
    text = font.render(str(int(boss[0].hp)), True, (34,165,152))
    text_rect = text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
    screen.blit(text, text_rect)
    

# ------------------------外星人end----------------
        
# -----------------------buff begin------------------
def create_buff(screen,settings,src,buffs):
    """ 创建一个buff """
    # 根据概率生成buff
    buff_type = random.choices(settings.buff_types, weights=settings.buffs_prob)[0]
    buff = Buff(screen=screen,settings=settings,src=src,buff_type = buff_type)
    buffs.add(buff)

def update_buff(screen,settings,stats,sb,src,ship,buffs):
    """ 更新buff """
    # 到达底部，删除buff
    for buff in buffs:
        if buff.rect.top >= screen.get_height():
            buffs.remove(buff)

    # 检测buff与武装飞机是否碰撞
    obtain_buff = pygame.sprite.spritecollide(ship, buffs, False) # buff碰撞后，不删除buff
    if obtain_buff:
        for buff in obtain_buff:
            buff.buff_action(stats)
        #sb.prep_ships()
        sb.prep_img(text = stats.ships_left,loc=(screen.get_rect().left ,screen.get_rect().bottom),fontsize = 30,type = 'ships_left' )
        buffs.remove(obtain_buff)
    
    # 更新buff状态：
    if pygame.time.get_ticks() - stats.last_superbullet_time > stats.superbullet_remaintime :
        stats.is_super = False
    if pygame.time.get_ticks() - stats.last_doublebullet_time > stats.doublebullet_remaintime :
        stats.is_double = False
    if pygame.time.get_ticks() - stats.last_protectship_time > stats.protectship_remaintime:
        stats.is_protected = False


    # 如果没有buff，则创建一个（各种buff）
    if len(buffs) == 0:
        # 循环以2，3，5秒的间隔在屏幕上方出现一个sprite
        if pygame.time.get_ticks() - stats.last_buff_time >= stats.buffs_intervals[0]:
            create_buff(screen = screen,settings = settings,src=src,buffs = buffs)  # 创建buff
            stats.last_buff_time = pygame.time.get_ticks()  # 记录创建buff的时刻
            stats.buffs_intervals.pop(0)
            if len(stats.buffs_intervals) == 0: # 如果间隔列表为空，重新填充
                stats.buffs_intervals = settings.buffs_intervals.copy()
    buffs.update()  # 更新buff坐标
# -----------------------buff end------------------
    
def protect_ship(settings,stats,bullet_splash_sound,):
    """ 保护飞机的一系列动作 """
    bullet_splash_sound.play()
    stats.is_protected = True
    stats.last_protectship_time = pygame.time.get_ticks()
    stats.protectship_remaintime = settings.protectship_DURATION