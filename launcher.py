from moteurdecourse import *
 
def create_courses():
    return [
        Course(
            nakayama_2000,
            "b",
            create_runners()
        ),
        Course(
            tokyo_2400,
            "b",
            create_runners()
        ),
        Course(
            kyoto_3000,
            "b",
            create_runners()
        ),
        Course(
            hanshin_2200,
            "b",
            create_runners()
        ),
        Course(
            laumamusume2,
            "a",
            create_runners()
        ),
        Course(
            ibisdash,
            "b",
            create_runners()
        )
    ]

def create_runners():
    return [
        Runner("A",1450,1250,1100),
        Runner("B",1600,1500,710),
        Runner("C",1550,1200,885),
        Runner("D",1490,1400,850)
    ]

def game_loop():
    if course.finished:
        print("Course terminée")
        return
    for _ in range(2): #le nombre est le facteur de vitesse, avec 2 -> ecoulement du temps 2x plus rapide

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
        3000,
        game_loop
    )
    visualizer.start()
    
    if not visualizer.return_to_selection:
        break

