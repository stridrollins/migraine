from skills import *

#To do : Ramp up & it's on overtake trigger








#### VELOCITY ##########################################################
def corner_adept():
    return Skill(
        "Corner Adept",
        "Standard",
        CornerTrigger(),
        [Velocity(0.25)],
        duration = 3.0
    )

def professor_of_curvature():
    return Skill(
        "Professor of Curvature",
        "Rare",
        CornerTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )


def straightaway_adept():
    return Skill(
        "Straightaway Adept",
        "Standard",
        StrightawayTrigger(),
        [Velocity(0.25)],
        duration = 3.0
    )

def beeline_burst():
    return Skill(
        "Beeline Burst",
        "Rare",
        StrightawayTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )

def ramp_up():
    return Skill(
        "Ramp Up",
        "Standard",
        None,
        [Velocity(0.25)],
        duration = 3.0
    )
def its_on():
    return Skill(
        "It's On",
        "Rare",
        None,
        [Velocity(0.5)],
        duration = 3.5
    )

def homestretch_haste():
    return Skill(
        "Homestretch Haste",
        "Standard",
        AfterDistanceTrigger(100*5/6) & StrightawayTrigger(),
        [Velocity(0.25)],
        duration = 3.5

    )

def in_body_and_mind():
    return Skill(
        "In Body and Mind",
        "Rare",
        AfterDistanceTrigger(100*5/6) & StrightawayTrigger(),
        [Velocity(0.5)],
        duration = 3.5

    )

def fast_paced():
    return Skill(
        "Fast Paced",
        "Standard",
        BeforePositionTrigger(30) & BeforeDistanceTrigger(100*2/3) & AfterDistanceTrigger(100*1/3),
        [Velocity(0.25)],
        duration = 3.5
    )

def escape_artist():
    return Skill(
        "Escape Artist",
        "Rare",
        BeforePositionTrigger(30) & BeforeDistanceTrigger(100*2/3) & AfterDistanceTrigger(100*1/3),
        [Velocity(0.5)],
        duration = 3.5
    )

def prepared_to_pass():
    return Skill(
        "Prepared to Pass",
        "Standard",
        BeforePositionTrigger(50) & AfterDistanceTrigger(100*2/3) & FinalCornerTrigger(),
        [Velocity(0.25)],
        duration = 3.5
    )

def speed_star():
    return Skill(
        "Speed Star",
        "Rare",
        BeforePositionTrigger(50) & AfterDistanceTrigger(100*2/3) & FinalCornerTrigger(),
        [Velocity(0.5)],
        duration = 3.5
    )



### ACCEL #############################################################
def straight_descent():
    return Skill(
        "Straight Descent",
        "Standard",
        DownhillTrigger(),
        [Acceleration(0.2)],
        duration = 3.0
    )
def determined_descent():
    return Skill(
        "Determined Descent",
        "Rare",
        DownhillTrigger(),
        [Acceleration(0.4)],
        duration = 3.0
    )
### RECOVERY #############################################################

################################################################
def moving_past_and_beyond():
    return Skill(
        "Moving Past, and Beyond",
        "Unique",
        AfterDistanceTrigger(66) & CornerTrigger(),
        [Acceleration(0.4)],
        duration = 3.0
    )


