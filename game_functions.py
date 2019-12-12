import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien
import _thread


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    """按键按下"""
    if event.key == pygame.K_RIGHT:
        # 飞船右移
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE and stats.game_active:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_LSHIFT:
        ai_settings.auto_fire = not ai_settings.auto_fire
        if ai_settings.auto_fire:
            _thread.start_new_thread(thread_auto_fire, (ai_settings, screen, ship, bullets))
    elif event.key == pygame.K_SPACE and not stats.game_active:
        game_restart(ai_settings, stats, sb, ship)
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        sys.exit()


def thread_auto_fire(ai_settings, screen, ship, bullets):
    """自动发射子弹线程"""
    while ai_settings.auto_fire:
        fire_bullet(ai_settings, screen, ship, bullets)
        sleep(.1)


def game_restart(ai_settings, stats, sb, ship):
    """开始游戏"""
    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    ai_settings.initialize_dynamic_settings()
    # 放置飞船
    stats.ships_left -= 1
    ship.center_ship()
    # 重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    # 隐藏光标
    pygame.mouse.set_visible(False)


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果子弹没有达到限制，就发射一颗子弹"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, stats, ship):
    """按键抬起"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, stats, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, mouse_x, mouse_y):
    """检测玩家是否点击开始按钮"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        game_restart(ai_settings, stats, sb, ship)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕"""
    screen.fill(ai_settings.bg_color)
    sb.show_score()
    # 重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    for alien in aliens.sprites():
        alien.blitme()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中外星人
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹与外星人碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        stats.level += 1
        sb.prep_level()


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 外星人间距为一个外星人宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    number_row = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建多行外星人
    for row_number in range(number_row):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新外星人位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_alines_bottom(ai_settings, stats, screen, ship, aliens, bullets)
    # 检测外星人和飞船是否相撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """检测是否有外星人到达屏幕边缘"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将外星人下移并改变其平移方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """飞船相撞"""
    if stats.ships_left > 0:
        # 创建新的飞船
        stats.ships_left -= 1
        ship.center_ship()
        # 更新记分牌
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        # 创建新的外星人和飞船
        create_fleet(ai_settings, screen, ship, aliens)
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_alines_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检测是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """检查最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
