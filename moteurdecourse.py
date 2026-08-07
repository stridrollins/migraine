DEFAULT_SPEED = 60     # km/h
DEFAULT_DEAD_SPEED = 50 # km/h
DEFAULT_SPRINT_SPEED = 70 # km/h

DEFAULT_ACCEL = 1     # km/h par seconde

import time

from visualizer import *
from tracklist import *


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
            normal_speed = (DEFAULT_SPEED *0.9 + (runner.speed/20)*0.1  ) 
            sprint_speed = (DEFAULT_SPRINT_SPEED * 0.5 + runner.speed/20 * 0.5)
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



