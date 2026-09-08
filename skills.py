
from dataclasses import dataclass, field

from typing import Literal
from trackbuilder import STEP

from random import *
SkillType = Literal["Standard","Rare","Unique","Inherited Unique"]
EARLY_RACE = 0
MID_RACE = 100/3 
LATE_RACE = 200/3 
LAST_SPURT = 500/6


####Triggers======================================================
##############################################################################

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
##############################################################################

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
##############################################################################

@dataclass
class AfterDistanceTrigger(SkillTrigger):
    percentage: float

    def check(self,course,runner):
        return runner.distance >= course.length * (self.percentage/100)
    
@dataclass
class BeforeDistanceTrigger(SkillTrigger):
    percentage: float

    def check(self,course,runner):
        return runner.distance <= course.length * (self.percentage/100)

@dataclass
class BetweenDistanceTrigger(SkillTrigger):
    p1: float
    p2: float

    def check(self,course,runner):
        return BeforeDistanceTrigger(self.p2).check(course,runner) and AfterDistanceTrigger(self.p1).check(course,runner)


@dataclass
class AtMeterDistanceTrigger(SkillTrigger):
    distance:int
    def check(self,course,runner):
        return runner.distance >= self.distance -1 and runner.distance <= self.distance +1


@dataclass
class MeterDistanceRemainingTrigger(SkillTrigger):
    distance:int
    def check(self,course,runner):
        return runner.distance >= course.length - self.distance -1 and runner.distance <= course.length - self.distance + 1 



class EarlyRaceTrigger(SkillTrigger):
    def check(self,course,runner):
        return RandomBeforeDistanceTrigger(MID_RACE).check(course,runner)

class MidRaceTrigger(SkillTrigger):
    def check(self,course,runner):
        return RandomBetweenDistanceTrigger(MID_RACE,LATE_RACE).check(course,runner)

class LateRaceTrigger(SkillTrigger):
    def check(self,course,runner):
        return RandomAfterDistanceTrigger(LATE_RACE).check(course,runner)

class LastSpurtTrigger(SkillTrigger):
    def check(self,course,runner):
        return RandomAfterDistanceTrigger(LAST_SPURT).check(course,runner)


@dataclass
class BeforePositionTrigger(SkillTrigger):
    percentage: float

    def check(self,course,runner):
        position_start = (runner.position - 1) *100 / course.runner_count
        return position_start <= self.percentage

@dataclass
class AfterPositionTrigger(SkillTrigger):
    percentage: float

    def check(self,course,runner):
        position_end = runner.position *100 / course.runner_count
        return position_end >= self.percentage

@dataclass
class BetweenPositionTrigger(SkillTrigger):
    p1: float
    p2: float

    def check(self,course,runner):
        
        position_start = (runner.position - 1) *100 / course.runner_count
        position_end = runner.position * 100 / course.runner_count
        
        return AfterPositionTrigger(self.p1).check(course,runner) and BeforePositionTrigger(self.p2).check(course,runner)

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

class StraightawayTrigger(SkillTrigger):
    def check(self, course, runner):
        return course.track[runner.track_index].curvature == 0

class FinalCornerTrigger(SkillTrigger):
    def check(self,course,runner):
        return course.track[runner.track_index].is_final_corner

class GreatEscapeTrigger(SkillTrigger):
    def check(self,course,runner):
        return runner.style=="escape"

class FrontRunnerTrigger(SkillTrigger):
    def check(self,course,runner):
        return runner.style=="front" or runner.style=="escape"

class PaceChaserTrigger(SkillTrigger):
    def check(self,course,runner):
        return runner.style=="pace"

class LateSurgerTrigger(SkillTrigger):
    def check(self,course,runner):
        return runner.style=="late"

class EndCloserTrigger(SkillTrigger):
    def check(self,course,runner):
        return runner.style=="end"
    
####triggers aleatoires=================================================
##############################################################################
@dataclass
class RandomAfterDistanceTrigger(SkillTrigger):
    percentage:int
    targets:dict = field(default_factory=dict)

    
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            self.targets[runner_id] = uniform(
                self.percentage,
                100
            )
        target = self.targets[runner_id]
        return AfterDistanceTrigger(target).check(course,runner)


        
@dataclass
class RandomBeforeDistanceTrigger(SkillTrigger):
    percentage:int
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            self.targets[runner_id] = uniform(
                0,
                self.percentage
            )
        target = self.targets[runner_id]
        return AfterDistanceTrigger(target).check(course,runner)


    

@dataclass
class RandomBetweenDistanceTrigger(SkillTrigger):
    percent1:int
    percent2:int
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)

        if runner_id not in self.targets:
            self.targets[runner_id] = uniform(
                self.percent1,
                self.percent2
            )
        target = self.targets[runner_id] 
        print(target)
        return AfterDistanceTrigger(target).check(course, runner)

@dataclass
class RandomCornerTrigger(SkillTrigger):
    p1:float =0
    p2:float =100
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            min_distance = course.length * (self.p1/100)
            max_distance = course.length * (self.p2/100)
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
    p2:float =100
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            min_distance = course.length * (self.p1/100)
            max_distance = course.length * (self.p2/100)
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
    p2:float =100
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            min_distance = course.length * (self.p1/100)
            max_distance = course.length * (self.p2/100)
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
    p2:float =100
    targets:dict = field(default_factory=dict)
    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.targets:
            min_distance = course.length * (self.p1/100)
            max_distance = course.length * (self.p2/100)
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

#####triggers compliqués ====================================================
##############################################################################

@dataclass
class OvertakingTrigger(SkillTrigger):
    target : int = 1
    counters: dict = field(default_factory=dict)

    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.counters:
            self.counters[runner_id] = 0

        self.counters[runner_id] += runner.overtakes_this_frame
        return self.counters[runner_id] >= self.target

@dataclass
class OvertakenTrigger(SkillTrigger):
    target : int = 1
    counters: dict = field(default_factory=dict)

    def check(self,course,runner):
        runner_id = id(runner)
        if runner_id not in self.counters:
            self.counters[runner_id] = 0

        self.counters[runner_id] += runner.overtaken_this_frame
        return self.counters[runner_id] >= self.target

@dataclass
class DiffInFrontTrigger(SkillTrigger):
    distance:float
    def check(self,course,runner):
        return runner.diff_infront <= self.distance

@dataclass
class DiffBehindTrigger(SkillTrigger):
    distance:float
    def check(self,course,runner):
        return runner.diff_behind <= self.distance


####Effects==================================================================
##############################################################################

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