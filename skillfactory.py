from skills import *



EARLY_RACE = 0
MID_RACE = 1/3 
LATE_RACE = 2/3 
LAST_SPURT = 5/6





### VELOCITY ##########################################################
def corner_adept():
    return Skill(
        "Corner Adept",
        "Standard",
        RandomCornerTrigger(MID_RACE, LATE_RACE),
        [Velocity(0.5)],
        duration = 3.0
    )

def professor_of_curvature():
    return Skill(
        "Professor of Curvature",
        "Rare",
        RandomCornerTrigger(MID_RACE,LATE_RACE),
        [Velocity(10)],
        duration = 3.0
    )

def straightaway_adept():
    return Skill(
        "Straightaway Adept",
        "Standard",
        RandomStraightawayTrigger(MID_RACE,LATE_RACE),
        [Velocity(0.5)],
        duration = 3.0
    )

def beeline_burst():
    return Skill(
        "Beeline Burst",
        "Rare",
        RandomStraightawayTrigger(MID_RACE,LATE_RACE),
        [Velocity(1)],
        duration = 3.0
    )

def ramp_up():
    return Skill(
        "Ramp Up",
        "Standard",
        AfterDistanceTrigger(MID_RACE) & OvertakingTrigger(1),
        [Velocity(0.5)],
        duration = 3.0
    )

def its_on():
    return Skill(
        "It's On",
        "Rare",
        AfterDistanceTrigger(MID_RACE) & OvertakingTrigger(1),
        [Velocity(1)],
        duration = 3.0
    )

def homestretch_haste():
    return Skill(
        "Homestretch Haste",
        "Standard",
        AfterDistanceTrigger(LAST_SPURT) & StrightawayTrigger(),
        [Velocity(0.5)],
        duration = 3.0

    )

def in_body_and_mind():
    return Skill(
        "In Body and Mind",
        "Rare",
        AfterDistanceTrigger(LAST_SPURT) & StrightawayTrigger(),
        [Velocity(1)],
        duration = 3.0

    )

def fast_paced():
    return Skill(
        "Fast Paced",
        "Standard",
        FrontRunnerTrigger() & BetweenDistanceTrigger(MID_RACE,LATE_RACE) & BeforePositionTrigger(50),
        [Velocity(0.5)],
        duration = 3.0
    )

def escape_artist():
    return Skill(
        "Escape Artist",
        "Rare",
        FrontRunnerTrigger() & BetweenDistanceTrigger(MID_RACE,LATE_RACE) & BeforePositionTrigger(50),
        [Velocity(1)],
        duration = 3.0
    )

def prepared_to_pass():
    return Skill(
        "Prepared to Pass",
        "Standard",
        PaceChaserTrigger()  & BeforePositionTrigger(50) & FinalCornerTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )

def speed_star():
    return Skill(
        "Speed Star",
        "Rare",
        PaceChaserTrigger() & BeforePositionTrigger(50) & FinalCornerTrigger(),
        [Velocity(1)],
        duration = 3.0
    )

def position_pilfer():
    return Skill(
        "Position Pilfer",
        "Standard",
        LateSurgerTrigger() & BetweenDistanceTrigger(MID_RACE,LATE_RACE) & AfterPositionTrigger(50),
        [Velocity(0.5)],
        duration = 3.0
    )

def fast_and_furious():
    return Skill(
        "Fast & Furious",
        "Rare",
        LateSurgerTrigger() & BetweenDistanceTrigger(MID_RACE,LATE_RACE) & AfterPositionTrigger(50), 
        [Velocity(1)],
        duration = 3.0
    )

def outer_swell():
    return Skill(
        "Outer Swell",
        "Standard",
        LateSurgerTrigger() & FinalCornerTrigger() & OvertakingTrigger(),
        [Velocity(0.5)],
        duration = 3.0

    )

def rising_dragon():
    return Skill(
        "Rising Dragon",
        "Rare",
        LateSurgerTrigger() & FinalCornerTrigger() & OvertakingTrigger(),
        [Velocity(1)],
        duration = 3.0

    )

def masterful_gambit():
    return Skill(
        "Masterful Gambit",
        "Standard",
        EndCloserTrigger() & AfterDistanceTrigger(LAST_SPURT)
    )

def steadfast():
    return Skill(
        "Steadfast",
        "Standard",
        FinalCornerTrigger() & DiffBehindTrigger(1)
        [Velocity(0.5),Acceleration(0.1)]
    )


def unyielding():
    return Skill(
        "Nope",
        "Rare",
        FinalCornerTrigger() & DiffBehindTrigger(1),
        [Velocity(1), Acceleration(0.2)],
        duration = 50.0
    )


### ACCEL #############################################################
def straight_descent():
    return Skill(
        "Straight Descent",
        "Standard",
        RandomDownhillTrigger(),
        [Acceleration(0.2)],
        duration = 3.0
    )

def determined_descent():
    return Skill(
        "Determined Descent",
        "Rare",
        RandomDownhillTrigger(),
        [Acceleration(0.4)],
        duration = 3.0
    )
### RECOVERY #############################################################

### UNIQUE #############################################################
def moving_past_and_beyond():
    return Skill(
        "Moving Past, and Beyond",
        "Unique",
        AfterDistanceTrigger(LATE_RACE) & CornerTrigger() & BetweenPositionTrigger(60,75),
        [Acceleration(40)],
        duration = 3.0
    )

def angling_and_scheming():
    return Skill(
        "Angling and Scheming",
        "Unique",
        AfterDistanceTrigger(LATE_RACE) & CornerTrigger() & BeforePositionTrigger(1),
        [Acceleration(0.4)],
        duration = 3.0
    )
