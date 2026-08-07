DEFAULT_SPEED = 60     # km/h
DEFAULT_DEAD_SPEED = 50 # km/h
DEFAULT_SPRINT_SPEED = 70 # km/h

DEFAULT_ACCEL = 1     # km/h par seconde



from runner import Runner
from visualizer import TrackVisualizer
import time

from tracklist import tokyo_2400,nakayama_2000,kyoto_3000,hanshin_2200
from trackbuilder import (
    Circuit,
    TrackBuilder,
    Straight,
    Arc,
    Slope,
    STEP
)


class Course:
    def __init__(self,circuit,conditions,runners):
        self.circuit=circuit
        self.conditions = conditions
        self.runners = runners
        self.finished = False
        self.y = 0
        self.time=0
        self.results =[]#result = tableau position,runner,temps
        builder = TrackBuilder()
        self.track=builder.build(circuit)
        print(
            "Circuit chargé :",
            self.circuit.name,
            self.circuit.length,
            "m"
        )
    def start(self):
        dt = 1 / 60  # 60 mises à jour par seconde

        while not self.finished:
            start = time.perf_counter()

            self.update(dt)
            self.checkfinish()

            elapsed = time.perf_counter() - start
            time.sleep(max(0, dt - elapsed))


    def step(self,dt):

        self.update(dt)
        self.checkfinish()



    def checkfinish(self):
        if len(self.results) == len(self.runners):
            self.finished = True  

    def update(self, dt):
        self.time += dt

        for runner in self.runners:

            # Si le coureur a terminé, on ne le met plus à jour
            if runner.finished:
                continue

            # Calcul de la vitesse actuelle
            # À remplacer plus tard par la gestion puissance/endurance/segments
            current_speed = self.calculate_speed(runner, dt)


          

            speed_ms = current_speed / 3.6

            runner.distance += speed_ms * dt



            runner.track_index = min(
                int(runner.distance / STEP),
                len(self.track) - 1
            )

            point = self.track[runner.track_index]

            runner.x = point.x
            runner.y = point.y






            # Vérification de l'arrivée
            if runner.distance >= self.circuit.length:
                runner.distance = self.circuit.length
                runner.finished = True

                self.results.append(
                    (
                        len(self.results) + 1,
                        runner,
                        self.time
                    )
                )


        # Classement temporaire pendant la course
        ranking = sorted(
            self.runners,
            key=lambda r: r.distance,
            reverse=True
        )


        # Affichage toutes les secondes
        if self.y % 60 == 0:
            print("\n====================")
            print(f"Temps : {self.time:.2f}s")
            print("====================")

            for position, runner in enumerate(ranking, start=1):
                progress = (runner.distance / self.circuit.length) * 100

                print(
                    f"{position}. "
                    f"{runner.name:<10} "
                    f"{runner.distance:7.1f}m "
                    f"({progress:5.1f}%)"
                    f"({runner.current_speed:5.1f})"
                )
        self.y += 1



    def calculate_speed(self, runner, dt):

        if runner.hp > 0:
            normal_speed = DEFAULT_SPEED + runner.speed / 800
            sprint_speed = DEFAULT_SPRINT_SPEED + runner.speed / 1000
        else:
            normal_speed = DEFAULT_DEAD_SPEED + runner.speed / 1000
            sprint_speed = normal_speed

        acceleration = DEFAULT_ACCEL * runner.power / 1000

        target_speed = normal_speed

        if runner.distance >= self.circuit.length * 2 / 3 and runner.hp > 0:
            target_speed = sprint_speed

        if runner.current_speed < target_speed:
            if runner.current_speed < 40:
                runner.current_speed += acceleration*5*dt
            runner.current_speed = min(
                runner.current_speed + acceleration * dt,
                target_speed
            )
        else:
            runner.current_speed = max(
                runner.current_speed - acceleration * dt,
                target_speed
            )

        runner.hp = max(
            0,
            runner.hp - (runner.current_speed / 1200*120) * dt
        )

        return runner.current_speed
#Speed/Power/Stamina
s = Runner("Strid",1500,1300,1100)
l = Runner("Lilith",2100,1900,725)
c = Runner("Chameau",1850,1200,950)
b = Runner("Berserk",1850,1500,850)

Japanesederby = Course(
    tokyo_2400,
    "b",
    [s,l,c,b]
)

Satsukisho = Course(
    nakayama_2000,
    "b",
    [s,l,c,b]
)

Kikukasho = Course(
    kyoto_3000,
    "b",
    [s,l,c,b]
)

Takarazukakinen = Course(
    hanshin_2200,
    "b",
    [s,l,c,b]
)

courses = [Satsukisho,Japanesederby,Kikukasho,Takarazukakinen]


course = courses[3]







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


visualizer = TrackVisualizer(course)

game_loop()







visualizer.start()

#print("Results:")
#for position, runner in enumerate(c.results, start=1):
#    print(f"{position}. {runner}")
