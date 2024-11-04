import pygame
import random

# 필요한 클래스들 (예시로 Zombie만 추가)
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('resources/zombie/Zombie_0.png').convert_alpha()  # 좀비 이미지
        self.rect = self.image.get_rect()
        self.rect.x = 1000  # 화면 오른쪽 끝에서 시작
        self.rect.y = random.randint(90, 540)  # y좌표는 랜덤으로 설정 (게임판에 적당히 맞게)
        self.speed = 2  # 좀비 이동 속도

    def update(self):
        self.rect.x -= self.speed  # 왼쪽으로 이동
        if self.rect.x < 0:  # 화면 왼쪽 끝에 도달하면 삭제
            self.kill()

# 초기화
pygame.init()
backgdsize = (1000, 600)
screen = pygame.display.set_mode(backgdsize)
pygame.display.set_caption("Plant vs Zombie")

# 그룹 생성
zombieGroup = pygame.sprite.Group()

# 타이머 이벤트 설정 (좀비 생성)
GEN_ZOMBIE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(GEN_ZOMBIE_EVENT, 3000)  # 3초마다 좀비 생성

clock = pygame.time.Clock()

def main():
    global zombieGroup

    while True:
        clock.tick(20)  # FPS 설정 (20으로 설정)

        screen.fill((255, 255, 255))  # 배경색을 흰색으로 설정

        # 좀비 그룹 업데이트 및 그리기
        zombieGroup.update()
        zombieGroup.draw(screen)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == GEN_ZOMBIE_EVENT:
                # 좀비 생성
                zombie = Zombie()
                zombieGroup.add(zombie)

        pygame.display.update()

if __name__ == '__main__':
    main()
