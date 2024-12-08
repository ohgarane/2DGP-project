from pico2d import *
import time

PIXEL_PER_METER = (10.0 / 0.5)  # 10 pixel 50 cm
RUN_SPEED_KMPH = 25.0  # Km / Hour 속도
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

class Stage:
    def __init__(self):
        self.stage1_image = load_image('resource/stage1.png')
        self.bar_image = load_image('resource/progress_bar.png')
        self.bar_zombie_image = load_image('resource/zombie_bar.png')
        self.font = load_font('resource/ConsolaMalgun.ttf', 17)
        self.state = 'stage1'
        self.check_time = time.time()
        self.zombie_time = 2
        self.bar_time = 0
        self.bar_total_time = 0

    def update(self):
        if self.check_time + 0.5 < time.time():
            self.check_time = time.time()
            self.zombie_time += 0.5
            self.bar_total_time += 0.5

        if self.bar_total_time >= 1:
            self.bar_time += 1
            self.bar_total_time = 0

    def draw(self, sun_point):
        if self.state == 'stage1':
            self.stage1_image.draw(700, 300)
        self.font.draw(20, 504, '%d' % sun_point)
        self.bar_image.clip_draw(0, 0, 300, 60, 1230, 50)
        self.bar_image.clip_draw_to_origin(0, 60, 300 - self.bar_time, 60, 1080, 21)
        self.bar_zombie_image.clip_draw(0, 0, 57, 57, 1370 - self.bar_time, 50)

    def cnt_init(self):
        self.zombie_time, self.bar_time, self.bar_total_time = 2, 0, 0

class Item:
    coin_sound = None
    set_plant_sound = None

    def __init__(self):
        self.select_image = load_image('resource/select_plant.png')
        if self.set_plant_sound is None:
            self.coin_sound = load_wav('resource/coin.wav')
            self.coin_sound.set_volume(32)
        if self.set_plant_sound is None:
            self.set_plant_sound = load_wav('resource/set_plant.wav')
            self.set_plant_sound.set_volume(32)

    def update(self, frame_time):
        pass

    def draw(self, select_plant, mouse_x, mouse_y):
        self.select_image.clip_draw((select_plant - 1) * 100 + 10, 0, 100, 100, mouse_x, mouse_y)
        self.select_image.clip_draw((select_plant - 1) * 100 + 10, 0, 100, 100, 1350, 545)

    def coin(self):
        self.coin_sound.play()

    def plant(self):
        self.set_plant_sound.play()

class Game_End:
    def __init__(self):
        self.plant_image = load_image('resource/end_plant.jpg')
        self.zombie_image = load_image('resource/end_zombie.jpg')
        self.play_bgm = load_music('resource/play.mp3')
        self.plant_bgm = load_music('resource/end_plant.mp3')
        self.zombie_bgm = load_music('resource/end_zombie.mp3')
        self.state = 'play'
        self.play()

    def draw(self):
        if self.state == 'plant':
            self.plant_image.draw(700, 300)
        elif self.state == 'zombie':
            self.zombie_image.draw(700, 300)

    def play(self):
        self.play_bgm.stop()
        self.play_bgm.set_volume(45)
        self.play_bgm.repeat_play()

    def plant(self):
        self.state = 'plant'
        self.play_bgm.stop()
        self.plant_bgm.set_volume(50)
        self.plant_bgm.repeat_play()

    def zombie(self):
        self.state = 'zombie'
        self.play_bgm.stop()
        self.zombie_bgm.set_volume(100)
        self.zombie_bgm.repeat_play()
