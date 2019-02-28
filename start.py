# take 7 - async (w/ blocking)
import sys
sys.path.insert(0, './blocker')
import time
import math

import pygame

import blocker
import config

DEFAULT_FOCUS_DURATION = 25.0
DEFAULT_SHORT_BREAK_DURATION = 5.0
DEFAULT_LONG_BREAK_DURATION = 30.0

POMODOROS_IN_SET = 4

SECS_IN_MIN = 60

def parse_args(argv):
    argc = len(argv)
    if argc > 4:
        raise Exception('Too many arguments')
    return DEFAULT_FOCUS_DURATION if argc < 2 else float(argv[1]),\
           DEFAULT_SHORT_BREAK_DURATION if argc < 3 else float(argv[2]),\
           DEFAULT_LONG_BREAK_DURATION if argc < 4 else float(argv[3])

def start_interval(duration, audio):
    for i in range(int(duration * SECS_IN_MIN), -1, -1):
        print(time.strftime('\r%H:%M:%S', time.gmtime(i)), end='')    
        time.sleep(1)
    print()
    if audio:
        pygame.mixer.music.play()

def start_pomodoro(duration, audio, block, number):
    print(f"Pomodoro #{number}")
    if block:
        blocker.block()
    start_interval(duration, audio)
    pomodoro_ended = time.time()
    input("Have you ended? (Press ENTER)")
    overtime = time.time() - pomodoro_ended
    if block:
        blocker.unblock()
    return overtime / SECS_IN_MIN

def start_break(duration, long_duration, audio, number):
    long_break = number == POMODOROS_IN_SET
    print(f"Break #{number}" if not long_break else f"Long break!")
    if duration <= 0:
        print("You're studying too hard! Have a break already!")
        return
    start_interval(duration if not long_break else long_duration, audio)

if __name__ == '__main__':
    focus_duration, short_break_duration, long_break_duration = parse_args(sys.argv)
    audio = True
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('uniphone.wav')
    except pygame.error:
        audio = False
    # damn
    block = True
    # try:
    #    blocker.block()
    #    blocker.unblock()
    # except FileNotFoundError:
    #    block = False
    # need to change that var names...
    blocked = config.load_configuration()

    print('Welcome to Pomodoro App!')
    print(f'The following options were chosen: focus duration is {focus_duration}, '
          f'short break duration is {short_break_duration} and long break duration is {long_break_duration}')
    while True:
        for i in range(POMODOROS_IN_SET):
            overtime = start_pomodoro(focus_duration, audio, block, i + 1)
            start_break(short_break_duration - overtime, long_break_duration - overtime, audio, i + 1) 
        if input('Another one? (y/any other key)\n') != 'y':
            print('Good day!') 
            if blocked:
                blocker.block()
            break

