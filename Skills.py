
from dataclasses import dataclass, field
from math import ceil, floor
from typing import Literal
from trackbuilder import STEP

from random import *
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
        return runner.distance >= course.circuit.length * (self.percentage)

@dataclass
class BeforeDistanceTrigger(SkillTrigger):
    percentage: float

    def check(self,course,runner):
        return runner.distance <= course.circuit.length * (self.percentage)

@dataclass
class BetweenDistanceTrigger(SkillTrigger):
    p1: float
    p2: float

    def check(self,course,runner):
        return runner.distance <= course.circuit.length * (self.p2) and runner.distance >= course.circuit.length * (self.p1)

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

class GreatEscapeTrigger(SkillTrigger):
    def checkk(self,course,runner):
        return runner.style=="escape"

class FrontRunnerTrigger(SkillTrigger):
    def check(self,course,runner):
        return runner.style=="front" or runner.style=="escape"

class PaceChaserTrigger(SkillTrigger):
    def check(self,course,runner):
        return runner.style=="pace"

class LateSurgherTrigger(SkillTrigger):
    def check(self,course,runner):
        return runner.style=="late"

class EndCloserTrigger(SkillTrigger):
    def check(self,course,runner):
        return runner.style=="end"
    
####triggers aleatoires=================================================
@dataclass
class RandomCornerTrigger(SkillTrigger):
    p1:float =0
    p2:float =1
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            min_distance = course.length * (self.p1)
            max_distance = course.length * (self.p2)
            eligible_points = [
                index
                for index in course.corner_points
                if min_distance <= index * STEP <= max_distance
            ]
            if not eligible_points:
                return False
            self.targets[runner_id] = choice(eligible_points)
        target = self.targets[runner_id]

        return runner.track_index >= target

@dataclass
class RandomStraightawayTrigger(SkillTrigger):
    p1:float =0
    p2:float =1
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            min_distance = course.length * (self.p1)
            max_distance = course.length * (self.p2)
            eligible_points = [
                index
                for index in course.straightaway_points
                if min_distance <= index * STEP <= max_distance
            ]
            if not eligible_points:
                return False
            self.targets[runner_id] = choice(eligible_points)
        target = self.targets[runner_id]
        return runner.track_index >= target

@dataclass
class RandomUphillTrigger(SkillTrigger):
    p1:float =0
    p2:float =1
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            min_distance = course.length * (self.p1)
            max_distance = course.length * (self.p2)
            eligible_points = [
                index
                for index in course.uphill_points
                if min_distance <= index * STEP <= max_distance
            ]
            if not eligible_points:
                return False
            self.targets[runner_id] = choice(eligible_points)
        target = self.targets[runner_id]
        return runner.track_index >= target

@dataclass
class RandomDownhillTrigger(SkillTrigger):
    p1:float =0
    p2:float =1
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            min_distance = course.length * (self.p1)
            max_distance = course.length * (self.p2)
            eligible_points = [
                index
                for index in course.downhill_points
                if min_distance <= index * STEP <= max_distance
            ]
            if not eligible_points:
                return False
            self.targets[runner_id] = choice(eligible_points)
        target = self.targets[runner_id]
        return runner.track_index >= target
#####triggers compliqués ===============================

@dataclass
class OvertakingTrigger(SkillTrigger):
    target : int
    counters: dict = field(default_factory=dict)

    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.counters:
            self.counters[runner_id] = 0

        self.counters[runner_id] += runner.overtakes_this_frame
        return self.counters[runner_id] >= self.target

@dataclass
class OvertakenTrigger(SkillTrigger):
    target : int
    counters: dict = field(default_factory=dict)

    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.counters:
            self.counters[runner_id] = 0

        self.counters[runner_id] += runner.overtaken_this_frame
        return self.counters[runner_id] >= self.target
    
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

