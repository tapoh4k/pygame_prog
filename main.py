import random

import pygame as pg

from Player import Player
from Asteroid import Asteroid
from Bullet import Bullet
from Explosion import Explosion
from PowerUps import PowerUp

screen = pg.display.set_mode((1240, 960))
bg = pg.image.load("Images/Background.png")
pg.font.init()
my_font = pg.font.SysFont('Comic Sans MS', 30)
health_text = my_font.render('Жизни: ', True, (255, 0, 0))
score_text = my_font.render('Счет: ', False, (255, 0, 0))

bullets = pg.sprite.Group()
asteroids = pg.sprite.Group()
explosions = pg.sprite.Group()

health = 3
score = 0

power_Ups = ["heal", "armor", "double shot", "slowdown"]
spawnable_power_Ups = []
current_power_Up = None
immunity = False
double_shot = False
slowdown = False

asteroids_multiplier = 1
power_Ups_counter = 0

player = Player((screen.get_width() - screen.get_width() / 2, screen.get_height() - screen.get_height() / 2), 0, 0)
player_copy = None
second = False


def is_cross(a, b):
    ax1, ay1, ax2, ay2 = a[0], a[1], a[2], a[3]
    bx1, by1, bx2, by2 = b[0], b[1], b[2], b[3]

    xa = [ax1, ax2]
    xb = [bx1, bx2]

    ya = [ay1, ay2]
    yb = [by1, by2]

    if max(xa) < min(xb) or max(ya) < min(yb) or min(ya) > max(yb):
        return False

    elif (max(xa) > min(xb)) and (min(xa) < min(xb)):
        return True
    else:
        return True


def blit():
    screen.blit(bg, (0, 0))
    screen.blit(health_text, (150, 50))
    screen.blit(score_text, (900, 50))
    screen.blit(my_font.render(str(health), False, (255, 0, 0)), (260, 50))
    screen.blit(my_font.render(str(score), False, (255, 0, 0)), (975, 50))


def draw(alive, main_player, copy):
    if alive:
        main_player.key_listener()
        main_player.draw(screen)
        if copy is not None:
            copy.draw(screen)
            copy.key_listener()

    asteroids.draw(screen)
    bullets.draw(screen)
    explosions.draw(screen)
    if current_power_Up is not None:
        current_power_Up.draw(screen)


def update(main_player, copy):
    asteroids.update(slowdown)
    bullets.update()
    explosions.update()
    if current_power_Up is not None:
        current_power_Up.update()
    if not main_player.moving:
        main_player.update_speed()
        if copy is not None:
            copy.update_speed()


def play():
    global player, player_copy, second, health, score, asteroids, asteroids_multiplier, spawnable_power_Ups,\
        current_power_Up, power_Ups_counter, immunity, double_shot, slowdown
    clock = pg.time.Clock()

    tick_counter = 0
    score_counter = 0
    power_up_timer = 0
    death_timer = 0
    immunity_timer = 0
    double_shot_timer = 0
    slowdown_timer = 0
    alive = True
    player.shielded = True

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if alive and not double_shot:
                        bullets.add(Bullet((player.rect.centerx, player.rect.centery), player.angle))
                    elif alive and double_shot:
                        bullets.add(Bullet((player.rect.centerx - 10, player.rect.centery), player.angle))
                        bullets.add(Bullet((player.rect.centerx + 10, player.rect.centery), player.angle))
                if event.key == pg.K_r:
                    player = Player((screen.get_width() - screen.get_width() / 2, screen.get_height() - 80), 0, 0)
                    alive = True
                    health = 3
                    score = 0
                    asteroids = pg.sprite.Group()
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    player.end_rotation()
                if event.key == pg.K_UP:
                    player.moving = False

        if tick_counter == 20:
            asteroids.add(Asteroid((random.randrange(0, screen.get_width() - 50), 0), 180))
            tick_counter = 0

        if power_up_timer == 500 and current_power_Up is None:
            current_power_Up = PowerUp(spawnable_power_Ups[random.randrange(0, len(spawnable_power_Ups))],
                                       (random.randrange(0, screen.get_width() - 50), 0), 0)

        if score_counter == 100 and alive:
            score += 1
            score_counter = 0

        update(player, player_copy)

        if player.rect.centerx >= screen.get_width() - 45 and not second:
            player_copy = Player((0 - (screen.get_width() - player.rect.centerx) - 45, player.rect.centery),
                                 player.angle, player.speed)
            player_copy.angle = player.angle
            second = True
        if player.rect.centerx <= 45 and not second:
            player_copy = Player((screen.get_width() + (screen.get_width() - player.rect.centerx) + 45,
                                  player.rect.centery), player.angle, player.speed)
            player_copy.angle = player.angle
            second = True
        if player.rect.centery >= screen.get_height() - 45 and not second:
            player_copy = Player((player.rect.centerx, 0 - (screen.get_height() - player.rect.centery) - 45),
                                 player.angle, player.speed)
            player_copy.angle = player.angle
            second = True
        if player.rect.centery <= 45 and not second:
            player_copy = Player((player.rect.centerx, screen.get_height()
                                  + (screen.get_height() - player.rect.centery) + 45), player.angle, player.speed)
            player_copy.angle = player.angle
            second = True
        if not screen.get_rect().colliderect(player.rect):
            player = player_copy
            player_copy = None
            second = False

        blit()
        draw(alive, player, player_copy)

        if current_power_Up is not None:
            if current_power_Up.alive() and pg.sprite.collide_rect(player, current_power_Up):
                if current_power_Up.apply_power() == "heal":
                    health += 1
                elif current_power_Up.apply_power() == "shield":
                    immunity = True
                    player.shielded = True
                elif current_power_Up.apply_power() == "double shot":
                    double_shot = True
                elif current_power_Up.apply_power() == "slowdown":
                    slowdown = True

        for asteroid in asteroids:
            if len(bullets) != 0:
                for bullet in bullets:
                    if pg.sprite.collide_rect(bullet, asteroid):
                        explosions.add(Explosion(asteroid.rect))
                        asteroid.kill()
                        bullet.kill()
                        score += 15
            if alive:
                if pg.sprite.collide_rect(player, asteroid):
                    explosions.add(Explosion(asteroid.rect))
                    asteroid.kill()
                    if not immunity:
                        if health == 1:
                            health = 0
                            player.kill()
                            alive = False
                            second = False
                        else:
                            health -= 1

        if not alive:
            death_timer += 1
        if death_timer == 100:
            asteroids = pg.sprite.Group()
            player = Player(
                (screen.get_width() - screen.get_width() / 2, screen.get_height() - screen.get_height() / 2), 0, 0)
            logo()
            done = True

        if immunity_timer == 500:
            immunity = False
            player.shielded = False
            immunity_timer = 0
        if double_shot_timer == 1000:
            double_shot = False
            double_shot_timer = 0
        if slowdown_timer == 500:
            slowdown = False
            slowdown_timer = 0

        pg.display.flip()

        tick_counter += 1
        score_counter += 1
        if immunity:
            immunity_timer += 1
        if double_shot:
            double_shot_timer += 1
        if slowdown:
            slowdown_timer += 1
        asteroids_multiplier = score // 150 + 1
        if score >= 200:
            power_up_timer += 1
        if score // 200 > power_Ups_counter:
            spawnable_power_Ups.append(power_Ups[power_Ups_counter])
            power_Ups_counter += 1

        clock.tick(60)


def logo():
    clock = pg.time.Clock()

    asteroids_timer = 0
    global asteroids, health, score
    done = False
    while not done:
        logo_image = pg.image.load("Images/Logo.jpg")
        screen.blit(bg, (0, 0))
        if asteroids_timer == 30:
            if len(asteroids) < 30:
                asteroids.add(Asteroid((screen.get_width() - 50, random.randrange(0, screen.get_height())), 90))
                asteroids_timer = 0
        asteroids.update()
        asteroids.draw(screen)

        screen.blit(health_text, (150, 50))
        screen.blit(score_text, (900, 50))
        screen.blit(my_font.render(str(health), False, (255, 0, 0)), (260, 50))
        screen.blit(my_font.render(str(score), False, (255, 0, 0)), (975, 50))
        screen.blit(logo_image, (364, 355))
        text = my_font.render('Нажмите чтобы начать игру', True, (0, 255, 0))
        screen.blit(text, (415, screen.get_height() / 2 + 150))

        if pg.mouse.get_pressed()[0]:
            asteroids = pg.sprite.Group()
            health = 3
            score = 0
            play()
            done = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        asteroids_timer += 1
        pg.display.flip()
        clock.tick(60)


def main():
    logo()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
