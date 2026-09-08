import time

from factories import *
from visualizer import *
from moteurdecourse import *


FIXED_DT = 1 / 60
SPEED = 3.0

accumulator = 0
last_time = time.perf_counter()

def game_loop():
    global accumulator
    global last_time

    now = time.perf_counter()

    frame_time = now - last_time
    last_time = now

    frame_time = min(frame_time, 0.25)

    accumulator += frame_time * SPEED

    while accumulator >= FIXED_DT and not course.finished:
        course.step(FIXED_DT)
        accumulator -= FIXED_DT

    visualizer.update()

    if course.finished:
        return

    visualizer.root.after(16, game_loop)



while True:
    courses = create_courses()

    selector = CourseSelector(courses)
    selector.start()

    course = selector.selected

    if course is None:
        break

    visualizer = TrackVisualizer(course)

    accumulator = 0
    last_time = time.perf_counter()

    visualizer.root.after(16, game_loop)

    visualizer.start()

    if not visualizer.return_to_selection:
        break


#strid : satsuki sho
#rogue : derby
#chameau : kikuka
#rogue (faire gagner berserk avec ulti)
#lilith: laumamusume, ibis summer dash

#punis : berserk, sanhiro