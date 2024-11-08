import pygame
import random
import time

# 초기화
pygame.init()
backgdsize = (1000, 600)
screen = pygame.display.set_mode(backgdsize)
pygame.display.set_caption("Plant vs Zombie")

# 이미지 로드
bg_img = pygame.image.load('resources/screen/background.jpg').convert_alpha()
sunflowerImg = pygame.image.load('resources/sunflower/SunFlower_00.png').convert_alpha()
peashooterImg = pygame.image.load('resources/peashooter/Peashooter_00.png').convert_alpha()

# Sun 클래스
class Sun(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('resources/sun/Sun_1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.lasttime = time.time()

    def update(self):
        pass  # 햇살은 고정 위치에 남음

# Sunflower 클래스
class Sunflower(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = sunflowerImg
        self.rect = self.image.get_rect()
        self.rect.x = 200  # 기본 위치
        self.rect.y = 100
        self.lasttime = time.time()

    def update(self):
        pass  # 동작 없음

# Bullet 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('resources/bullet/Bullet_1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midleft = position
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > backgdsize[0]:  # 화면을 벗어나면 삭제
            self.kill()

# Peashooter 클래스
class Peashooter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = peashooterImg
        self.rect = self.image.get_rect()
        self.rect.x = 300  # 기본 위치
        self.rect.y = 200
        self.lasttime = time.time()

    def update(self):
        pass  # 동작 없음

# Zombie 클래스
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('resources/zombie/Zombie_0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = backgdsize[0]  # 화면 오른쪽 끝에서 시작
        self.rect.y = random.randint(100, 500)
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:  # 화면 왼쪽 끝에 도달하면 삭제
            self.kill()

# 그룹 설정
sunFlowerGroup = pygame.sprite.Group()
peashooterGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
zombieGroup = pygame.sprite.Group()
sunGroup = pygame.sprite.Group()

# 이벤트 타이머
GEN_SUN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(GEN_SUN_EVENT, 5000)  # 5초마다 햇살 생성

GEN_BULLET_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(GEN_BULLET_EVENT, 1000)  # 1초마다 총알 생성

GEN_ZOMBIE_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(GEN_ZOMBIE_EVENT, 3000)  # 3초마다 좀비 생성

# 메인 루프
def main():
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)
        screen.blit(bg_img, (0, 0))  # 배경 그리기

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == GEN_SUN_EVENT:
                for sunflower in sunFlowerGroup:
                    sun = Sun(sunflower.rect.center)
                    sunGroup.add(sun)

            if event.type == GEN_BULLET_EVENT:
                for peashooter in peashooterGroup:
                    bullet = Bullet(peashooter.rect.midright)
                    bulletGroup.add(bullet)

            if event.type == GEN_ZOMBIE_EVENT:
                zombie = Zombie()
                zombieGroup.add(zombie)

        # 그룹 업데이트 및 그리기
        sunFlowerGroup.update()
        sunFlowerGroup.draw(screen)

        peashooterGroup.update()
        peashooterGroup.draw(screen)

        bulletGroup.update()
        bulletGroup.draw(screen)

        zombieGroup.update()
        zombieGroup.draw(screen)

        sunGroup.update()
        sunGroup.draw(screen)

        pygame.display.update()

if __name__ == '__main__':
    sunflower = Sunflower()
    sunFlowerGroup.add(sunflower)

    peashooter = Peashooter()
    peashooterGroup.add(peashooter)

    main()
