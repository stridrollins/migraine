from skills import Skill

class Runner:
    def __init__(self, name,speed,power,stamina, skills = None):
        self.name = name
        self.position = 0
        self.speed = speed
        self.power = power
        self.stamina = stamina

        self.skills = skills or []

        self.distance = 0
        self.track_index =0
        self.x =0
        self.y =0
        self.finished = False

        self.current_speed = 0
        self.target_speed = 0

        self.hp  = self.stamina
        self.hp_drain = 0
        self.total_hp_drain = 0

        self.active_effects =[]
        

    def update_skills(self, course, dt):
        for skill in self.skills:
            if skill.check(course, self):
                skill.activate(course, self)
            skill.update(dt)
        for effect in self.active_effects:
            effect.update(self, dt)

            # Suppression des effets terminés
        self.active_effects = [
            effect
            for effect in self.active_effects
            if not effect.expired
        ]
