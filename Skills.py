
from dataclasses import dataclass, field
from math import ceil, floor

@dataclass
class Skill:
    name: str
    trigger: SkillTrigger
    effects: list = field(default_factory=list)
    used: bool = False

    def check(self, course, runner):
        return not self.used and self.trigger.check(course, runner)

    def activate(self, course, runner):
        for effect in self.effects:
            effect.apply( runner)
        self.used = True

    def update(self, dt):
        pass

####Triggers======================================================

class SkillTrigger:
    def check(self,course,runner):
        raise NotImplementedError

@dataclass
class AfterDistanceTrigger(SkillTrigger):
    percentage: float

    def check(self,course,runner):
        return runner.distance >= course.circuit.length * (self.percentage/100)

@dataclass
class BeforeDistanceTrigger(SkillTrigger):
    percentage: float

    def check(self,course,runner):
        return runner.distance <= course.circuit.length * (self.percentage/100)

@dataclass
class BetweenDistanceTrigger(SkillTrigger):
    p1: float
    p2: float

    def check(self,course,runner):
        return runner.distance <= course.circuit.length * (self.p2/100) and runner.distance >= course.circuit.length * (self.p1/100)

@dataclass
class BeforePositionTrigger(SkillTrigger):
    percentage: float

    def check(self,course,runner):
        return runner.position <= ceil(len(course.runners) * (self.percentage/100))


@dataclass
class AfterPositionTrigger(SkillTrigger):
    percentage: float

    def check(self,course,runner):
        return runner.position >= floor(len(course.runners) * (self.percentage/100))

@dataclass
class BetweenPositionTrigger(SkillTrigger):
    p1: float
    p2: float

    def check(self,course,runner):
        return runner.position >= floor(len(course.runners) * (self.p1/100)) and runner.position <= ceil(len(course.runners) * (self.p2/100))

class UphillTrigger(SkillTrigger):
    def check(self, course, runner):
        gradient = course.track[runner.track_index].gradient
        return gradient > 0

class DownhillTrigger(SkillTrigger):
    def check(self, course, runner):
        gradient = course.track[runner.track_index].gradient
        return gradient < 0

class CornerTrigger(SkillTrigger):
    def check(self, course, runner):
        curve = course.track[runner.track_index].curvature
        return curve > 0

class StrightawayTrigger(SkillTrigger):
    def check(self, course, runner):
        curve = course.track[runner.track_index].curvature
        return curve == 0





    
####Effects==================================================================

class Effect:
    def apply(self,target):
        raise NotImplementedError

    def update(self,target,dt):
        pass
    @property
    def expired(self):
        return self.duration <= 0

@dataclass 
class Velocity(Effect):
    amount:float
    duration:float
    def update(self,target,dt):
        self.duration -= dt
    @property
    def expired(self):
        return self.duration <= 0
    def apply(self,target):
        target.active_effects.append(self)
    def skill_speed(self,speed):
        return speed + self.amount

@dataclass 
class Acceleration(Effect):
    amount:float
    duration:float
    def update(self,target,dt):
        self.duration -= dt
    @property
    def expired(self):
        return self.duration <= 0
    def apply(self,target):
        target.active_effects.append(self)
    def skill_acceleration(self,accel):
        return accel + self.amount
    
@dataclass 
class Recovery(Effect):
    amount:float
    def apply(self,target):
        target.hp += self.amount

