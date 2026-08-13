
from dataclasses import dataclass, field
from math import ceil, floor
from typing import Literal


SkillType = Literal["Standard","Rare","Unique","Inherited Unique"]


@dataclass
class Skill:
    name: str
    type:SkillType
    trigger: SkillTrigger
    effects: list = field(default_factory=list)
    duration: float = 0.0
    used: bool = False
    remaining: float = 0.0
    active: bool = False

    def check(self, course, runner):
        return not self.used and not self.active and self.trigger.check(course, runner)

    def activate(self, course, runner):
        for effect in self.effects:
            effect.apply(runner)
        self.used = True
        self.active = True
        self.remaining = self.duration

    def update(self, dt):
        if not self.active:
            return

        self.remaining -= dt

        if self.remaining <= 0:
            self.remaining = 0
            self.active = False

####Triggers======================================================

class SkillTrigger:
    def check(self,course,runner):
        raise NotImplementedError
    def __and__(self, other):
        return AndTrigger(self, other)

    def __or__(self, other):
        return OrTrigger(self, other)

    def __invert__(self):
        return NotTrigger(self)

####Portes logiques =======================================

class AndTrigger(SkillTrigger):

    def __init__(self, *triggers):
        self.triggers = triggers

    def check(self, course, runner):
        return all(
            trigger.check(course, runner)
            for trigger in self.triggers
        )


class OrTrigger(SkillTrigger):

    def __init__(self, *triggers):
        self.triggers = triggers

    def check(self, course, runner):
        return any(
            trigger.check(course, runner)
            for trigger in self.triggers
        )


class NotTrigger(SkillTrigger):

    def __init__(self, trigger):
        self.trigger = trigger

    def check(self, course, runner):
        return not self.trigger.check(course, runner)

####Triggers de base=====================================================

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
        return course.track[runner.track_index].curvature == 0

class FinalCornerTrigger(SkillTrigger):
    def check(self,course,runner):
        return course.track[runner.track_index].is_final_corner



    
####Effects==================================================================

class Effect:
    def apply(self,target):
        raise NotImplementedError




@dataclass 
class Velocity(Effect):
    amount:float

    def apply(self,target):
        pass
    def skill_speed(self,speed):
        return speed + self.amount

@dataclass 
class Acceleration(Effect):
    amount:float
    def apply(self,target):
        pass
    def skill_acceleration(self,accel):
        return accel + self.amount
    
@dataclass 
class Recovery(Effect):
    amount:float
    def apply(self,target):
        target.hp += self.amount

