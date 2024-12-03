from pico2d import *
import random

class Zombie:
    PIXEL_PER_METER = (10.0 / 0.5)           # 10 pixel 50 cm
    RUN_SPEED_KMPH = 10.0                    # Km / Hour 속도
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    WALK_FRAMES = 22
    ATTACK_FRAMES = 21
    DIE_FRAMES = 10

    WALK, ATTACK, DIE, END = 1, 2, 3, 4

    def __init__(self):
        self.walk_images = [load_image(f"C:\\Users\\USER\\Desktop\\2DGP-project\\resources\\images\\zombie\\Zombie_{i}.png") for i in range(self.WALK_FRAMES)]
        self.attack_images = [load_image(f"C:\\Users\\USER\\Desktop\\2DGP-project\\resources\\images\\zombie\\ZombieAttack_{i}.png") for i in range(self.ATTACK_FRAMES)]
        self.die_images = [load_image(f"C:\\Users\\USER\\Desktop\\2DGP-project\\resources\\images\\zombie\\ZombieDie_{i}.png") for i in range(self.DIE_FRAMES)]

        self.x, self.y = 1400, (random.randint(0, 4) * 100) + 60
        self.speed, self.life = 0, 4
        self.attack_time = 0.0
        self.state = self.WALK
        self.walk_frame = 0
        self.attack_frame = 0
        self.die_frame = 0
        self.total_frames = 0.0

    def update(self, frame_time):
        distance = self.RUN_SPEED_PPS * frame_time
        self.total_frames += self.ACTION_PER_TIME * frame_time

        if self.state == self.WALK:
            self.walk_frame = int(self.total_frames * self.WALK_FRAMES) % self.WALK_FRAMES
            self.x -= distance if self.speed == 0 else distance / self.speed
        elif self.state == self.ATTACK:
            self.attack_frame = int(self.total_frames * self.ATTACK_FRAMES) % self.ATTACK_FRAMES
            self.attack_time += frame_time
            if self.attack_time >= 1.0:
                self.attack_time = 0.0
                self.state = self.WALK
        elif self.state == self.DIE:
            self.die_frame = int(self.total_frames * self.DIE_FRAMES) % self.DIE_FRAMES
            if self.die_frame == self.DIE_FRAMES - 1:
                self.state = self.END

    def draw(self):
        if self.state == self.WALK:
            self.walk_images[self.walk_frame].draw(self.x, self.y)
        elif self.state == self.ATTACK:
            self.attack_images[self.attack_frame].draw(self.x, self.y)
        elif self.state == self.DIE:
            self.die_images[self.die_frame].draw(self.x, self.y)

    def attack(self):
        if self.life <= 1:
            self.state = self.DIE
        else:
            self.state = self.ATTACK
            self.life -= 1

    def get_bb(self):
        return self.x - 15, self.y - 55, self.x + 35, self.y + 25

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


# 충돌 감지 함수
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b or right_a < left_b or top_a < bottom_b or bottom_a > top_b:
        return False
    return True


