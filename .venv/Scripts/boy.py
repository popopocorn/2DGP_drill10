# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *
from state_machine import *
from ball import Ball
import game_world
import game_framework



TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
FRAMES_PER_ACTION = 14

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif right_down(e) or left_up(e):
            boy.action = 2
            boy.face_dir = -1
        elif left_down(e) or right_up(e):
            boy.action = 3
            boy.face_dir = 1


        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        if get_time() - boy.wait_time > 2:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        if boy.face_dir ==1:
            if int(boy.frame) < 5:
                boy.image.clip_draw((int(boy.frame))%5 * 183, 338, 183, 169, boy.x, boy.y, 100, 100)
            elif int(boy.frame) < 10:
                boy.image.clip_draw((int(boy.frame)) % 5 * 183, 169, 183, 169, boy.x, boy.y, 100, 100)
            else:
                boy.image.clip_draw((int(boy.frame)) % 5 * 183, 0, 183, 169, boy.x, boy.y, 100, 100)
        else:
            if int(boy.frame) < 5:
                boy.image.clip_composite_draw((int(boy.frame))%5 * 183, 338, 183, 169,  0, 'h' ,boy.x, boy.y, 100, 100)
            elif int(boy.frame) < 10:
                boy.image.clip_composite_draw((int(boy.frame)) % 5 * 183, 169, 183, 169,  0, 'h', boy.x, boy.y, 100, 100)
            else:
                boy.image.clip_composite_draw((int(boy.frame)) % 5 * 183, 0, 183, 169, 0, 'h', boy.x, boy.y, 100, 100)

class Sleep:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.face_dir = 1
            boy.action = 3
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14


    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 300, 100, 100,
                                          3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 200, 100, 100,
                                          -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = -1, -1, 0

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()


    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        boy.x += boy.dir * RUN_SPEED_PPS*game_framework.frame_time


    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            if int(boy.frame) < 5:
                boy.image.clip_draw((int(boy.frame)) % 5 * 183, 338, 183, 169, boy.x, boy.y, 100, 100)
            elif int(boy.frame) < 10:
                boy.image.clip_draw((int(boy.frame)) % 5 * 183, 169, 183, 169, boy.x, boy.y, 100, 100)
            else:
                boy.image.clip_draw((int(boy.frame)) % 5 * 183, 0, 183, 169, boy.x, boy.y, 100, 100)
        else:
            if int(boy.frame) < 5:
                boy.image.clip_composite_draw((int(boy.frame)) % 5 * 183, 338, 183, 169, 0, 'h', boy.x, boy.y, 100, 100)
            elif int(boy.frame) < 10:
                boy.image.clip_composite_draw((int(boy.frame)) % 5 * 183, 169, 183, 169, 0, 'h', boy.x, boy.y, 100, 100)
            else:
                boy.image.clip_composite_draw((int(boy.frame)) % 5 * 183, 0, 183, 169, 0, 'h', boy.x, boy.y, 100, 100)


class Boy:

    def __init__(self):
        self.frame=0
        self.x, self.y = 400, 150
        self.face_dir = 1
        self.font = load_font("ENCR10B.TTF", 16)
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},

            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x, self.y, f'time:{get_time()}', (255, 255, 0))

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.face_dir * 10)
        game_world.add_object(ball)