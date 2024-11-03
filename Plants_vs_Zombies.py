import time
import pygame

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

bg_img = pygame.image.load('resources/screen/background.jpg').convert_alpha()


def main():

        # 총알과 좀비의 충돌 처리

        # 벽돌과 좀비의 충돌 처리

        # 피셔터와 좀비의 충돌 처리

        # 해바라기와 좀비의 충돌 처리

        # 화면에 배경과 UI 표시

        # 씨앗 카드 이미지 표시

        # 각 스프라이트 업데이트 및 화면에 그리기

        # 마우스 클릭으로 선택된 씨앗 표시

        # 해바라기에서 태양 생성

        # 피셔터에서 총알 생성

        # 일반 좀비 생성
        while True:
            screen.blit(bg_img, (0, 0))  # Draw the background image
            pygame.display.update()  # Update the display

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        pass
if __name__ == '__main__':
    main()
