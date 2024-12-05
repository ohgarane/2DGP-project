import random
import json
import os
import time
from pico2d import *

import game_framework
import title_state
from plants import *
from zombies import *
from stage import *

name = "MainState"

# 전역 객체 선언
stage, item, game_end_manager = None, None, None
plant_objects, projectile_objects = None, None
flower_objects, sun_objects = None, None
walnut_objects = None
zombie_objects = None

# 선택 상태 상수
NOT_SELECTED, SELECT_PLANT, SELECT_FLOWER, SELECT_WALNUT = 0, 1, 2, 3

mouse_pos_x, mouse_pos_y = 0, 0  # 마우스 위치
sun_points = 500  # 태양 포인트 초기값
selected_plant = NOT_SELECTED  # 현재 선택된 식물
grid_status = [[0 for _ in range(5)] for _ in range(8)]  # 그리드 상태 (0: 빈 공간)

def enter():
    """
    메인 스테이트 진입 시 객체 초기화
    """
    global stage, item, game_end_manager
    global plant_objects, flower_objects, walnut_objects, zombie_objects
    global projectile_objects, sun_objects

    # 객체 초기화
    stage = Stage()
    item = Item()
    game_end_manager = Game_End()
    plant_objects = []
    projectile_objects = []
    flower_objects = []
    sun_objects = []
    walnut_objects = []
    zombie_objects = []

def exit():
    """
    메인 스테이트 종료 시 객체 삭제
    """
    global stage, item, game_end_manager
    global plant_objects, flower_objects, walnut_objects, zombie_objects
    global projectile_objects, sun_objects

    del stage
    del item
    del game_end_manager
    del plant_objects
    del projectile_objects
    del flower_objects
    del sun_objects
    del walnut_objects
    del zombie_objects

def pause():
    pass

def resume():
    pass

def select_space():
    """
    현재 마우스 위치에 식물을 심는 공간을 선택
    """
    global grid_status, item, selected_plant
    global mouse_pos_x, mouse_pos_y

    item.plant()
    grid_x, grid_y = mouse_pos_x - 200, mouse_pos_y - 100
    grid_status[int(grid_x / 100)][int(grid_y / 100)] = 1
    selected_plant = NOT_SELECTED

def select_item():
    """
    사용자 인터페이스에서 선택된 아이템을 처리
    """
    global mouse_pos_x, selected_plant

    if 100 < mouse_pos_x < 155:
        selected_plant = SELECT_PLANT
    elif 160 < mouse_pos_x < 210:
        selected_plant = SELECT_FLOWER
    elif 215 < mouse_pos_x < 260:
        selected_plant = SELECT_WALNUT

def select_sun():
    """
    태양을 선택하여 포인트를 추가
    """
    global item, sun_objects, sun_points

    item.coin()
    if sun_objects:
        sun_points += len(sun_objects) * 10
        sun_objects.clear()

def handle_mouse_click():
    """
    마우스 클릭 이벤트 처리
    """
    global plant_objects, flower_objects, walnut_objects
    global mouse_pos_x, mouse_pos_y, selected_plant, grid_status, sun_points

    if 210 < mouse_pos_x < 1000 and 110 < mouse_pos_y < 600:  # 그리드 내부 클릭
        grid_x, grid_y = mouse_pos_x - 200, mouse_pos_y - 100
        if grid_status[int(grid_x / 100)][int(grid_y / 100)] == 0:
            # 선택된 식물 배치
            if selected_plant == SELECT_PLANT and sun_points >= 100:
                sun_points -= 100
                new_plant = Plant(mouse_pos_x, 599 - mouse_pos_y)
                plant_objects.append(new_plant)
                select_space()
            elif selected_plant == SELECT_FLOWER and sun_points >= 50:
                sun_points -= 50
                new_flower = Flower(mouse_pos_x, 599 - mouse_pos_y)
                flower_objects.append(new_flower)
                select_space()
            elif selected_plant == SELECT_WALNUT and sun_points >= 50:
                sun_points -= 50
                new_walnut = Walnut(mouse_pos_x, 599 - mouse_pos_y)
                walnut_objects.append(new_walnut)
                select_space()
    elif 100 < mouse_pos_x < 580 and 0 < mouse_pos_y < 80:
        select_item()
    elif 25 < mouse_pos_x < 75 and 20 < mouse_pos_y < 65:
        select_sun()

def spawn_zombie():
    """
    새로운 좀비를 생성하여 리스트에 추가
    """
    global stage, zombie_objects
    if stage.bar_time < 70:  # 게임 초반
        if stage.zombie_time >= 3:
            new_zombie = Zombie()
            zombie_objects.append(new_zombie)
            stage.zombie_time = 0  # 좀비 생성 후 초기화
    elif 200 < stage.bar_time:  # 게임 후반
        if stage.zombie_time >= 0.5:
            new_zombie = Zombie()
            zombie_objects.append(new_zombie)
            stage.zombie_time = 0  # 좀비 생성 후 초기화
    else:  # 중간 난이도
        if stage.zombie_time >= 1:
            new_zombie = Zombie()
            zombie_objects.append(new_zombie)
            stage.zombie_time = 0  # 좀비 생성 후 초기화

def update_objects():
    """
    객체 상태를 업데이트
    """
    global plant_objects, flower_objects, walnut_objects, zombie_objects
    global projectile_objects, sun_objects

    for plant in plant_objects:
        if plant.attack_time == 2:
            new_attack = Attack(plant.x, plant.y)
            projectile_objects.append(new_attack)
            plant.attack_time = 0
    for flower in flower_objects:
        if flower.sun_time == 3:
            new_sun = Sun()
            sun_objects.append(new_sun)
            flower.sun_time = 0

def remove_objects():
    """
    화면 밖으로 벗어난 객체를 삭제
    """
    global projectile_objects, zombie_objects

    zombie_objects = [zombie for zombie in zombie_objects if zombie.x >= 0 and zombie.state != zombie.END]
    projectile_objects = [attack for attack in projectile_objects if attack.x <= 1400]

def remove_plant(x, y):
    """
    그리드에서 특정 위치의 식물을 제거
    """
    global grid_status
    grid_x, grid_y = (x - 55) // 100 - 2, 4 - (y - 50) // 100
    if 0 <= grid_x < len(grid_status) and 0 <= grid_y < len(grid_status[0]):
        grid_status[int(grid_x)][int(grid_y)] = 0

def handle_collisions():
    """
    모든 객체의 충돌 처리
    """
    global plant_objects, flower_objects, walnut_objects, zombie_objects, projectile_objects

    for zombie in zombie_objects:
        for plant in plant_objects:
            if collide(zombie, plant):
                remove_plant(plant.x, plant.y)
                plant_objects.remove(plant)
                zombie.state = zombie.ATTACK
        for flower in flower_objects:
            if collide(zombie, flower):
                remove_plant(flower.x, flower.y)
                flower_objects.remove(flower)
                zombie.state = zombie.ATTACK
        for walnut in walnut_objects:
            if collide(zombie, walnut):
                if zombie.state == zombie.WALK:
                    if walnut.life > 0:
                        walnut.life -= 1
                    else:
                        remove_plant(walnut.x, walnut.y)
                        walnut_objects.remove(walnut)
                zombie.state = zombie.ATTACK
        for attack in projectile_objects:
            if collide(attack, zombie):
                zombie.life -= 1
                if zombie.life <= 0:
                    zombie.state = zombie.DIE
                projectile_objects.remove(attack)

def game_end_check():
    """
    게임 종료 조건 확인
    """
    global game_end_manager, stage, zombie_objects

    if stage.bar_time >= 270:
        game_end_manager.plant()
    for zombie in zombie_objects:
        if zombie.x < 0:
            game_end_manager.zombie()

def handle_events(frame_time):
    """
    이벤트 처리
    """
    global mouse_pos_x, mouse_pos_y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_MOUSEMOTION:
            mouse_pos_x, mouse_pos_y = event.x, event.y
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            handle_mouse_click()

def update(frame_time):
    """
    게임 로직 업데이트
    """
    global stage, item, game_end_manager

    if game_end_manager.state == 'play':
        stage.update()
        item.update(frame_time)
        for plant in plant_objects:
            plant.update(frame_time)
        for attack in projectile_objects:
            attack.update(frame_time)
        for flower in flower_objects:
            flower.update(frame_time)
        for sun in sun_objects:
            sun.update(frame_time)
        for walnut in walnut_objects:
            walnut.update(frame_time)
        for zombie in zombie_objects:
            zombie.update(frame_time)

        game_end_check()
        spawn_zombie()  # 좀비 생성
        update_objects()  # 객체 상태 업데이트
        remove_objects()  # 객체 삭제
        handle_collisions()  # 충돌 처리

def draw(frame_time):
    """
    화면 그리기
    """
    global stage, item, game_end_manager
    global plant_objects, flower_objects, walnut_objects, zombie_objects
    global projectile_objects, sun_objects, selected_plant, sun_points, mouse_pos_x, mouse_pos_y

    clear_canvas()
    if game_end_manager.state == 'play':
        stage.draw(sun_points)
        for plant in plant_objects:
            plant.draw()
        for flower in flower_objects:
            flower.draw()
        for walnut in walnut_objects:
            walnut.draw()
        for zombie in zombie_objects:
            zombie.draw()
        item.draw(selected_plant, mouse_pos_x, 600 - mouse_pos_y)
        for attack in projectile_objects:
            attack.draw()
        for sun in sun_objects:
            sun.draw()
    else:
        game_end_manager.draw()
    update_canvas()
