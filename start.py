# take 5 (w/ sound) - not async
import sys
import time
import pygame
import math

DEFAULT_FOCUS_DURATION = 25.0
DEFAULT_SHORT_BREAK_DURATION = 5.0
DEFAULT_LONG_BREAK_DURATION = 20.0
SECS_IN_MIN = 60 

POMODOROS_IN_SET = 1

def parse_args(argv):
    argc = len(argv)
    if argc > 4:
        raise Exception('Too many arguments')
    return DEFAULT_FOCUS_DURATION if argc < 2 else float(argv[1]),\
           DEFAULT_SHORT_BREAK_DURATION if argc < 3 else float(argv[2]),\
           DEFAULT_LONG_BREAK_DURATION if argc < 4 else float(argv[3])

def start_interval(duration, audio, eps=0.0001):
    timer_duration = math.floor(duration * SECS_IN_MIN)
    last_sec_check_time = -1
    change_text = False
    start_time = time.time()
    while True:
        timer_left = time.time() - start_time
        if timer_left >= timer_duration:
            break
        if timer_left % 1 < eps:
            if timer_left - last_sec_check_time > eps:
                change_text = True
                last_sec_check_time = timer_left
            if change_text:
                print(time.strftime('\r%H:%M:%S', time.gmtime(timer_duration - time.time() + start_time)), end='')
                change_text = False
    print()
    if audio:
        pygame.mixer.music.play()

     
if __name__ == '__main__':
    focus_duration, short_break_duration, long_break_duration = parse_args(sys.argv)
    audio = True
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('uniphone.wav')
    except pygame.error:
        audio = False

    print('Welcome to Pomodoro App!')
    print(f'The following options were chosen: focus duration is {focus_duration}, '
          f'short break duration is {short_break_duration} and long break duration is {long_break_duration}')
    while True:
        for i in range(POMODOROS_IN_SET):
            if i != 0:
                print(f'Break #{i}')
                start_interval(short_break_duration, audio)
            print(f'Pomodoro #{i + 1}')
            start_interval(focus_duration, audio)
        print('Long break!')
        start_interval(long_break_duration, audio)
        if input('Another one? (y/any other key)\n') != 'y':
            print('Good day!') 
            break

