
from factories import *
from visualizer import *
from moteurdecourse import *



def game_loop():
    if course.finished:
        print("Course terminée")
        return
    for _ in range(50): #le nombre est le facteur de vitesse, avec 2 -> ecoulement du temps 2x plus rapide

        course.step(1/60)

    visualizer.root.after(
        16,
        game_loop
    )

###PROGRAME PRINCIPAL

while True:
    courses = create_courses()
    selector = CourseSelector(courses)
    selector.start()
    course = selector.selected
    if course is None:
        break 
    visualizer=TrackVisualizer(course)
    visualizer.root.after(
        1500,
        game_loop
    )
    visualizer.start()
    
    if not visualizer.return_to_selection:
        break

