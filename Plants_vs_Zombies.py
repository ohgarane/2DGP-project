import time
import pygame
import pico2d

from bullet import Bullet
from flagzombie import Flagzombie
from peashooter import Peashooter
from sun import Sun
from sunflower import Sunflower
from wallnut import Wallnut
from zombie import Zombie

pygame.init()
backgdsize = (1000, 600)
screen = pygame.display.set_mode(backgdsize)
pygame.display.set_caption("plant vs zombie")

sunflowerImg = pygame.image.load('resources/images/sunflower/SunFlower_00.png').convert_alpha()
peashooterImg = pygame.image.load('resources/images/peashooter/Peashooter_00.png').convert_alpha()
wallnutImg = pygame.image.load('resources/images/wall_nut/WallNut_00.png').convert_alpha()
flowerSeed = pygame.image.load('resources/images/cards/card_sunflower.png').convert_alpha()
wallnutSeed = pygame.image.load('resources/images/cards/card_wallnut.png').convert_alpha()
peashooterSeed = pygame.image.load('resources/images/cards/card_peashooter.png').convert_alpha()
bg_img = pygame.image.load('resources/images/screen/background.jpg').convert_alpha()
seedbank_img = pygame.image.load('resources/images/screen/SeedBank.png').convert_alpha()

text = 900
sun_font = pygame.font.SysFont('arial', 25)
sun_num_surface = sun_font.render(str(text), True, (0, 0, 0))

sunFlowerGroup = pygame.sprite.Group()
peashooterGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
zombieGroup = pygame.sprite.Group()
wallnutGroup = pygame.sprite.Group()
sunGroup = pygame.sprite.Group()

GEN_SUN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(GEN_SUN_EVENT, 1000)

GEN_BULLET_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(GEN_BULLET_EVENT, 1000)

GEN_ZOMBIE_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(GEN_ZOMBIE_EVENT, 3000)

GEN_FLAGZOMBIE_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(GEN_FLAGZOMBIE_EVENT, 3000)

choose = 0
clock = pygame.time.Clock()

# 격자 관련 설정
ROWS, COLS = 5, 9
GRID_LEFT, GRID_TOP = 247, 90  # 격자의 시작점 (좌측 상단 좌표)
GRID_RIGHT, GRID_BOTTOM = 964, 559  # 격자의 끝점 (우측 하단 좌표)
CELL_WIDTH = (GRID_RIGHT - GRID_LEFT) / COLS
CELL_HEIGHT = (GRID_BOTTOM - GRID_TOP) / ROWS

def get_grid_center(x, y):
    """
    클릭된 좌표 (x, y)에 해당하는 격자 중심 좌표를 반환합니다.
    """
    col = int((x - GRID_LEFT) // CELL_WIDTH)
    row = int((y - GRID_TOP) // CELL_HEIGHT)
    if 0 <= col < COLS and 0 <= row < ROWS:
        center_x = GRID_LEFT + col * CELL_WIDTH + CELL_WIDTH / 2
        center_y = GRID_TOP + row * CELL_HEIGHT + CELL_HEIGHT / 2
        return center_x, center_y
    return None  # 격자 범위를 벗어난 경우

def main():
    global sun_num_surface, choose, text
    index = 0
    while True:
        clock.tick(20)
        index += 1
        for bullet in bulletGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(bullet, zombie):
                    zombie.energy -= 1
                    bulletGroup.remove(bullet)
        for wallNut in wallnutGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(wallNut, zombie):
                    zombie.ismeetwallnut = True
                    wallNut.zombies.add(zombie)
        for peashooter in peashooterGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(peashooter, zombie):
                    zombie.ismeetwallnut = True
                    peashooter.zombies.add(zombie)
        for sunflower in sunFlowerGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_mask(sunflower, zombie):
                    zombie.ismeetwallnut = True
                    sunflower.zombies.add(zombie)
        screen.blit(bg_img, (0, 0))
        screen.blit(seedbank_img, (250, 0))
        screen.blit(sun_num_surface, (270, 60))

        screen.blit(flowerSeed, (320, 0))
        screen.blit(peashooterSeed, (382, 0))
        screen.blit(wallnutSeed, (446, 0))
        sunFlowerGroup.update(index)
        sunFlowerGroup.draw(screen)
        peashooterGroup.update(index)
        peashooterGroup.draw(screen)
        bulletGroup.update(index)
        bulletGroup.draw(screen)
        zombieGroup.update(index)
        zombieGroup.draw(screen)
        wallnutGroup.update(index)
        wallnutGroup.draw(screen)
        sunGroup.update(index)
        sunGroup.draw(screen)

        (x, y) = pygame.mouse.get_pos()
        if choose == 1:
            screen.blit(sunflowerImg, (x, y))
        elif choose == 2:
            screen.blit(peashooterImg, (x, y))
        elif choose == 3:
            screen.blit(wallnutImg, (x, y))
        for event in pygame.event.get():
            if event.type == GEN_SUN_EVENT:
                for sprite in sunFlowerGroup:
                    now = time.time()
                    if now - sprite.lasttime >= 5:
                        sun = Sun(sprite.rect)
                        sunGroup.add(sun)
                        sprite.lasttime = now

            if event.type == GEN_BULLET_EVENT:
                for sprite in peashooterGroup:
                    bullet = Bullet(sprite.rect, backgdsize)
                    bulletGroup.add(bullet)

            if event.type == GEN_ZOMBIE_EVENT:
                zombie = Zombie()
                zombieGroup.add(zombie)

            if event.type == GEN_FLAGZOMBIE_EVENT:
                flagzombie = Flagzombie()
                zombieGroup.add(flagzombie)

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_key = pygame.mouse.get_pressed()
                if pressed_key[0] == 1:  # 왼쪽 버튼 클릭
                    x, y = pygame.mouse.get_pos()
                    print(x, y)
                    if 320 <= x <= 382 and 0 <= y <= 89 and text >= 50:
                        choose = 1
                    elif 383 <= x < 446 and 0 <= y <= 89 and text >= 100:
                        choose = 2
                    elif 447 <= x < 511 and 0 <= y <= 89 and text >= 50:
                        choose = 3
                    elif GRID_LEFT <= x <= GRID_RIGHT and GRID_TOP <= y <= GRID_BOTTOM:
                        # 격자 범위 안에서 클릭된 경우
                        grid_center = get_grid_center(x, y)
                        if grid_center:
                            grid_x, grid_y = grid_center
                            if choose == 1:
                                current_time = time.time()
                                sunflower = Sunflower(current_time)
                                sunflower.rect.center = (grid_x, grid_y)
                                sunFlowerGroup.add(sunflower)
                                choose = 0
                                text -= 50
                            elif choose == 2:
                                peashooter = Peashooter()
                                peashooter.rect.center = (grid_x, grid_y)
                                peashooterGroup.add(peashooter)
                                choose = 0
                                text -= 100
                            elif choose == 3:
                                wallnut = Wallnut()
                                wallnut.rect.center = (grid_x, grid_y)
                                wallnutGroup.add(wallnut)
                                choose = 0
                                text -= 50
                            sun_num_surface = sun_font.render(str(text), True, (0, 0, 0))
                    for sun in sunGroup:
                        if sun.rect.collidepoint(x, y):
                            sunGroup.remove(sun)
                            text += 50
                            sun_num_surface = sun_font.render(str(text), True, (0, 0, 0))

        pygame.display.update()

if __name__ == '__main__':
    main()
