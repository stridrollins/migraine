DEFAULT_SPEED = 60/3.6
DEFAULT_ACCEL = 1/3.6
DEFAULT_SPRINT_SPEED = 70/3.6
from runner import Runner
from circuit import Circuit, Segment
import time


class Course:
    def __init__(self,circuit,conditions,runners):
        self.circuit=circuit
        self.conditions = conditions
        self.runners = runners
        self.finished = False
        self.y = 0
        self.time=0
        self.results =[]#result = tableau position,runner,temps

    def start(self):
        dt = 1 / 60  # 60 mises à jour par seconde

        while not self.finished:
            start = time.perf_counter()

            self.update(dt)
            self.checkfinish()

            elapsed = time.perf_counter() - start
            time.sleep(max(0, dt - elapsed))

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
        normal_speed = DEFAULT_SPEED + runner.speed/800
        sprint_speed = DEFAULT_SPRINT_SPEED+runner.speed/1000

        # Accélération dépendante du power
        acceleration = DEFAULT_ACCEL * runner.power / 100


        # Phase 1 : accélération de départ
        if runner.current_speed < normal_speed:

            runner.current_speed += acceleration * dt

            # limite vitesse normale
            runner.current_speed = min(
                runner.current_speed,
                normal_speed
            )

            return runner.current_speed


        # Phase 2 : sprint final
        sprint_start = self.circuit.length * (2/3)

        if runner.distance >= sprint_start:

            runner.current_speed += acceleration * dt

            # limite sprint
            runner.current_speed = min(
                runner.current_speed,
                sprint_speed
            )

            return runner.current_speed


        # Phase 3 : vitesse stabilisée
        runner.current_speed = normal_speed

        return runner.current_speed


s = Runner("Strid",1200,1200,850)
l = Runner("Lilith",1320,950,620)

nakayama_2000 = Circuit(
    name="Nakayama 2000m",
    location="Nakayama Racecourse",
    length=2000
)

nakayama_2000.segments = [
    Segment(0, 180, "straight"),
    Segment(180, 480, "turn", value=180),
    Segment(480, 900, "straight"),
    Segment(900, 1300, "turn", value=90),
    Segment(1300, 1650, "uphill", value=2.2),
    Segment(1650, 1690, "turn", value=90),
    Segment(1690, 2000, "straight")
]


c = Course(nakayama_2000,"b",[s,l])

c.start()

print("Results:")
for position, runner in enumerate(c.results, start=1):
    print(f"{position}. {runner}")