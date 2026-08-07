DEFAULT_SPEED = 60/3.6
DEFAULT_DEAD_SPEED = 50/3.6
DEFAULT_SPRINT_SPEED = 70/3.6
DEFAULT_ACCEL = 1/3.6


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


            # Mise à jour de la distance
            runner.distance += current_speed * dt


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
                        runner.name,
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
                    f"({runner.current_speed*3.6:5.1f})"
                )


        self.y += 1

    def calculate_speed(self, runner, dt):

        # Limites de vitesse
        if runner.hp > 0:
            normal_speed = DEFAULT_SPEED + runner.speed/800
            sprint_speed = DEFAULT_SPRINT_SPEED+runner.speed/1000
        else :
            normal_speed = DEFAULT_DEAD_SPEED + runner.speed/1000
            sprint_speed = normal_speed

        # Accélération dépendante du power
        acceleration = DEFAULT_ACCEL * runner.power / 1000


        # Phase 1 : accélération de départ
        if runner.current_speed < normal_speed:
            if runner.current_speed < 50: #accelere 10fois + vite de 0 a 50kmh
                runner.current_speed += acceleration*10*dt
            else:
                runner.current_speed += acceleration * dt #accelere normalement apres

            runner.current_speed = min(
                runner.current_speed,
                normal_speed
            )
            return runner.current_speed

        sprint_start = self.circuit.length * (2/3)

        if runner.distance >= sprint_start:
            runner.current_speed += acceleration * dt
            runner.current_speed = min(
                runner.current_speed,
                sprint_speed
            )
            return runner.current_speed

        runner.current_speed = normal_speed
        return runner.current_speed


s = Runner("Strid",1200,1200,850)
l = Runner("Lilith",1320,950,620)



tokyo = TrackBuilder().build(tokyo_2400)
nakayama = TrackBuilder().build(nakayama_2000)
hanshin = TrackBuilder().build(hanshin_2200)
kyoto = TrackBuilder().build(kyoto_3000)
print(kyoto_3000.length)
print(tokyo_2400.length)
print(hanshin_2200.length)
print(nakayama_2000.length)








Japanesederby = Course(
    tokyo_2400,
    "b",
    [s,l]
)


Satsukisho = Course(
    nakayama_2000,
    "b",
    [s,l]
)


Kikukasho = Course(
    kyoto_3000,
    "b",
    [s,l]
)

Takarazukakinen = Course(
    hanshin_2200,
    "b",
    [s,l]
)


def game_loop():

    Satsukisho.step(1/60)

    visualizer.root.after(
        16,
        game_loop
    )


visualizer = TrackVisualizer(Satsukisho)

game_loop()

visualizer.start()

#print("Results:")
#for position, runner in enumerate(c.results, start=1):
#    print(f"{position}. {runner}")
