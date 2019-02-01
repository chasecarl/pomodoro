# take 2 - not async
import sys
import time

DEFAULT_FOCUS_DURATION = 25.0
DEFAULT_SHORT_BREAK_DURATION = 5.0
DEFAULT_LONG_BREAK_DURATION = 20.0

POMODOROS_IN_SET = 4

def parse_args(argv):
    argc = len(argv)
    if argc > 4:
        raise Exception('Too many arguments')
    return DEFAULT_FOCUS_DURATION if argc < 2 else float(argv[1]),\
           DEFAULT_SHORT_BREAK_DURATION if argc < 3 else float(argv[2]),\
           DEFAULT_LONG_BREAK_DURATION if argc < 4 else float(argv[3])

def start_interval(duration):
    duration_time_secs = duration * 60
    start_time = time.time()
    while time.time() - start_time < duration_time_secs:
        print(time.strftime('\r%H:%M:%S', time.gmtime(duration_time_secs - time.time() + start_time)), end='')
    print()

     
if __name__ == '__main__':
    focus_duration, short_break_duration, long_break_duration = parse_args(sys.argv)
    pom_break = False

    print('Welcome to Pomodoro App!')
    print(f'The following options were chosen: focus duration is {focus_duration}, '
              f'short break duration is {short_break_duration} and long break duration is {long_break_duration}')
    while True:
        for i in range(POMODOROS_IN_SET):
            if i != 0:
                print(f'Break #{i}')
                start_interval(short_break_duration)
            print(f'Pomodoro #{i + 1}')
            start_interval(focus_duration)
        print('Long break!')
        start_interval(long_break_duration)
        if input('Another one? (y/any other key)\n') != 'y':
            print('Good day!') 
            break

