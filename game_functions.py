import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    ###Respond to keypresses events.###
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    ###Fire a bullet if limit not reached yet.###
    # Erstellt ein neues Geschoss und fügt es zur Gruppe bullets hinzu.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    ###Respond to key releases events.###
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    ###Respond to keypresses and mouse events.###

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    ###Start a new game when the player clicks Play.###
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        # Setzt die Spieleinstellungen zurück.
        ai_settings.initialize_dynamic_settings()

        # Blendet den Mauszeiger aus.
        pygame.mouse.set_visible(False)

        # Setzt die Spielstatistik zurück.
        stats.reset_stats()
        stats.game_active = True

        # Setzt die Bilder der Anzeigetafel zurück.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Leert die Liste der Aliens und Geschosse.
        aliens.empty()
        bullets.empty()

        # Erstellt eine neue Flotte und zentriert das eigene Schiff.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    ###Update images on the screen and flip to the new screen.###

    #  Zeichnet den Bildschirm bei jedem Schleifendurchlauf neu.
    screen.fill(ai_settings.bg_color)
    # Zeichnet alle Geschosse hinter dem Schiff und den Außerirdischen neu.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Zeichnet das Schiff.
    ship.blitme()
    # Zeichnet die Aliens.
    aliens.draw(screen)

    # Zeichnet die Informationen über den Punktestand.
    sb.show_score()

    # Zeichnet die Play-Schalfläche nur bei inaktivem Spiel.
    if not stats.game_active:
        play_button.draw_button()

    # Macht den als letztes gezeichneten Bildschirm sichtbar.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ###Update position of bullets and get rid of the old bullets.###

    # Aktualisiert die Geschosspositionen.
    bullets.update()

    # Entfernt die verschwundenen Geschosse.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ###Respond to bullet-alien collision.###

    # Prüft, ob Geschosse ein Alien getroffen haben. Wenn ja werden Geschoss und Alien entfernt.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Zerstört alle vorhandenen Geschosse und erstellt eine neue Flotte.
        bullets.empty()
        ai_settings.increase_speed()
        # Setzt das Level herauf.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, sb):
    ###Check to see if there's a new high score.###

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


# ========== Aliens ==========

def get_number_aliens_x(ai_settings, alien_width):
    ###Determine the number of aliens that fit in a row.###
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    ###Determine the number of rows of aliens that fit on the screen.###
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    ###Create an alien and place it in the row.###
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    ###Create a full fleet of aliens.###

    # Erstellt ein Alien und ermittelt die Anzahl der Aliens pro Reihe.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Erstellt die Invasionsflotte.
    for row_number in range(number_rows):
        # Erstellt die erste Reihe Aliens.
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    ###Respond appropriately if any aliens have reached an edge.###
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    ###Drop the entire fleet and change the fleets direction.###
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ###Respond to ship being hit by alien.###
    if stats.ships_left > 0:
        # Verringert die Anzahl der verbleibenden eigenen Schiffe.
        stats.ships_left -= 1

        # Aktualisiert die Anzeigetafel.
        sb.prep_ships()

        # Leert die Liste der Aliens und Geschosse.
        aliens.empty()
        bullets.empty()

        # Erstellt eine neue Flotte und zentriert das eigene Schiff.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        # Blendet den Mauszeiger ein.
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ###Check if any aliens have reached the bottom of the screen.###
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Gleiche Reaktion wie bei einer Kollision mit dem Schiff.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ###Check if the fleet is at an edge, and then update the positions of all aliens in the fleet.###
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Prüft auf Kollisionen zwischen Aliens und dem Schiff.
    if pygame.sprite.spritecollideany(ship, aliens):
        #print('Ship hit!!!')
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # Prüft auf Aliens, die den unteren Bildschirmrand erreichen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

