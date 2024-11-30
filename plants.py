from pico2d import *
import random
import time

# 상수 정의
PIXELS_TO_METERS = (10.0 / 0.5)  # 10 픽셀이 50cm를 나타냄
SPEED_KMPH = 20.0  # 속도: km/h
SPEED_MPM = (SPEED_KMPH * 1000.0 / 60.0)  # 분당 이동 거리(m)
SPEED_MPS = (SPEED_MPM / 60.0)  # 초당 이동 거리(m)
SPEED_PPS = (SPEED_MPS * PIXELS_TO_METERS)  # 초당 이동 거리(pixel)

ACTION_DURATION = 0.5  # 하나의 액션이 걸리는 시간 (초)
ACTIONS_PER_SECOND = 1.0 / ACTION_DURATION  # 초당 액션 수
ANIMATION_FRAMES = 5  # 액션 당 프레임 수

class Plant:
    def __init__(self, mouse_x, mouse_y):
        # 플랜트 이미지를 로드하고 초기 위치를 설정
        self.image = load_image('resource/plant.png')
        self.x, self.y = int(mouse_x / 100) * 100 + 55, int(mouse_y / 100) * 100 + 50
        self.frame, self.total_frames = 0.0, 0.0
        self.check_time, self.attack_time = time.time(), 0  # 체크 및 공격 타이머 초기화

    def update(self, frame_time):
        # 애니메이션 프레임 업데이트
        self.total_frames += ANIMATION_FRAMES * ACTIONS_PER_SECOND * frame_time
        self.frame = int(self.total_frames + 1) % 8

        # 1초마다 공격 타이머 갱신
        if self.check_time + 1 < time.time():
            self.check_time = time.time()
            self.attack_time += 1

    def draw(self):
        # 현재 프레임의 플랜트를 그리기
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        # 충돌 박스 반환
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        # 충돌 박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb())

class Attack:
    def __init__(self, plant_x, plant_y):
        # 공격 이미지 로드 및 초기 위치 설정
        self.image = load_image('resource/attack.png')
        self.x, self.y = plant_x + 30, plant_y + 10

    def update(self, frame_time):
        # 공격체의 위치를 이동
        distance = SPEED_PPS * frame_time
        self.x += distance

    def draw(self):
        # 공격체 그리기
        self.image.clip_draw(0, 0, 26, 26, self.x, self.y)

    def get_bb(self):
        # 충돌 박스 반환
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw_bb(self):
        # 충돌 박스 그리기 (디버깅용)
        draw_rectangle(*self.get_bb())

class Flower:
    def __init__(self, mouse_x, mouse_y):
        # 플라워 이미지 로드 및 초기 위치 설정
        self.image = load_image('resource/flower.png')
        self.x, self.y = int(mouse_x / 100) * 100 + 55, int(mouse_y / 100) * 100 + 50
        self.frame, self.total_frames = 0.0, 0.0
        self.check_time, self.sun_time = time.time(), 0  # 체크 및 태양 타이머 초기화

    def update(self, frame_time):
        # 애니메이션 프레임 업데이트
        self.total_frames += ANIMATION_FRAMES * ACTIONS_PER_SECOND * frame_time
        self.frame = int(self.total_frames + 1) % 8

        # 1초마다 태양 타이머 갱신
        if self.check_time + 1 < time.time():
            self.check_time = time.time()
            self.sun_time += 1

    def draw(self):
        # 현재 프레임의 플라워 그리기
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        # 충돌 박스 반환
        return self.x - 30, self.y - 30, self.x + 25, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Sun:
    FRAMES_PER_ACTION = 2  # 태양 애니메이션 프레임 수

    def __init__(self):
        # 태양 이미지 로드 및 랜덤 초기 위치 설정
        self.image = load_image('resource/sun.png')
        self.x, self.y = random.randint(100, 1000), random.randint(100, 500)
        self.frame, self.total_frames = 0.0, 0.0

    def update(self, frame_time):
        # 애니메이션 프레임 업데이트
        self.total_frames += Sun.FRAMES_PER_ACTION * ACTIONS_PER_SECOND * frame_time
        self.frame = int(self.total_frames + 1) % 2

    def draw(self):
        # 현재 프레임의 태양 그리기
        self.image.clip_draw(int(self.frame * 100), 0, 100, 100, self.x, self.y)

class Walnut:
    def __init__(self, mouse_x, mouse_y):
        # 월넛 이미지 로드 및 초기 위치 설정
        self.image = load_image('resource/walnut.png')
        self.x, self.y = int(mouse_x / 100) * 100 + 55, int(mouse_y / 100) * 100 + 50
        self.frame, self.total_frames = 0.0, 0.0
        self.life = 1  # 월넛 내구도 초기화

    def update(self, frame_time):
        # 애니메이션 프레임 업데이트
        self.total_frames += ANIMATION_FRAMES * ACTIONS_PER_SECOND * frame_time
        self.frame = int(self.total_frames + 1) % 8

    def draw(self):
        # 현재 프레임의 월넛 그리기
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        # 충돌 박스 반환
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
