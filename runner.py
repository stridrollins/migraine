
class Runner:
    def __init__(self, name,speed,power,stamina):
        self.name = name
        self.position = 0
        self.speed = speed
        self.power = power
        self.stamina = stamina
        self.skills = []
        self.distance = 0
        self.finished = False
        self.current_speed = 0

    def update_skills(self, course, dt):

        for skill in self.skills:

            if not skill.used and skill.check(course):
                skill.activate()

            skill.update(dt)

