from skills import *



EARLY_RACE = 0
MID_RACE = 1/3 
LATE_RACE = 2/3 
LAST_SPURT = 5/6




### VELOCITY ###############################################################################################################################
############################################################################################################################################
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
        EndCloserTrigger() & AfterDistanceTrigger(LAST_SPURT),
        [Velocity(0.5)],
        duration=3.0
    )

def sturm_und_drang():
    return Skill(
        "Sturm Und Drang",
        "Rare",
        EndCloserTrigger() & AfterDistanceTrigger(LAST_SPURT),
        [Velocity(1)],
        duration=3.0
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



def up_tempo():
    return Skill(
        "Up-Tempo",
        "Standard",
        BetweenDistanceTrigger(MID_RACE,LATE_RACE),
        [Velocity(0.5)],
        duration = 3.0
    )
def killer_tunes():
    return Skill(
        "Killer Tunes",
        "Rare",
        BetweenDistanceTrigger(MID_RACE,LATE_RACE),
        [Velocity(1)],
        duration = 3.0
    )




### STYLE VELOCITY ###############################################################################################################################
############################################################################################################################################





def front_corners():
    return Skill(
        "Front Runner Corners",
        "Standard",
        FrontRunnerTrigger() & RandomCornerTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )

def pace_corners():
    return Skill(
        "Pace Chaser Corners",
        "Standard",
        PaceChaserTrigger() & RandomCornerTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )
def late_corners():
    return Skill(
        "Late Surger Corners",
        "Standard",
        LateSurgerTrigger() & RandomCornerTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )
def end_corners():
    return Skill(
        "End Closer Corners",
        "Standard",
        EndCloserTrigger() & RandomCornerTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )

def front_straightaways():
    return Skill(
        "Front Runner Straightaways",
        "Standard",
        FrontRunnerTrigger() & RandomStraightawayTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )

def pace_straightaways():
    return Skill(
        "Pace Chaser Straightaways",
        "Standard",
        PaceChaserTrigger() & RandomStraightawayTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )
def late_straightaways():
    return Skill(
        "Late Surger Straightaways",
        "Standard",
        LateSurgerTrigger() & RandomStraightawayTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )
def end_straightaways():
    return Skill(
        "End Closer Straightaways",
        "Standard",
        EndCloserTrigger() & RandomStraightawayTrigger(),
        [Velocity(0.5)],
        duration = 3.0
    )




















### ACCEL ##################################################################################################################################
############################################################################################################################################



def corner_acceleration():
    return Skill(
        "Corner Acceleration",
        "Standard",
        RandomCornerTrigger(),
        [Acceleration(0.2)],
        duration = 3.0
    )
def corner_connoisseur():
    return Skill(
        "Corner Connoisseur",
        "Rare",
        RandomCornerTrigger(),
        [Acceleration(0.4)],
        duration = 3.0
    )

def straightaway_acceleration():
    return Skill(
        "Straightaway Acceleration",
        "Standard",
        RandomStraightawayTrigger(),
        [Acceleration(0.2)],
        duration = 3.0
    )

def rushing_gale():
    return Skill(
        "Rushing Gale",
        "Rare",
        RandomStraightawayTrigger(),
        [Acceleration(0.4)],
        duration = 3.0
    )

def highlander():
    return Skill(
        "Highlander",
        "Standard",
        UphillTrigger(),
        [Acceleration(0.2)],
        duration=3.0
    )

def early_lead():
    return Skill(
        "Early Lead",
        "Standard",
        AfterDistanceTrigger(0),
        [Acceleration(0.2)],
        duration=1.5
    )

def taking_the_lead():
    return Skill(
        "Taking the Lead",
        "Rare",
        AfterDistanceTrigger(0),
        [Acceleration(0.4)],
        duration = 1.5
    )


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


### RECOVERY ###############################################################################################################################
############################################################################################################################################



def corner_recovery():
    return Skill(
        "Corner Recovery",
        "Standard",
        RandomCornerTrigger(),
        [Recovery(25)]
    )

def swinging_maestro():
    return Skill(
        "Swinging Maestro",
        "Rare",
        RandomCornerTrigger(),
        [Recovery(100)]
    )

def straightaway_recovery():
    return Skill(
        "Corner Recovery",
        "Standard",
        RandomStraightawayTrigger(),
        [Recovery(25)]
    )

def breath_of_fresh_air():
    return Skill(
        "Breath Of Fresh Air",
        "Rare",
        RandomStraightawayTrigger(),
        [Recovery(100)]
    )






### ULTIMATE ###############################################################################################################################
############################################################################################################################################



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


def this_dance_is_for_vittoria():
    return Skill(
        "This Dance is for Vittoria !",
        "Unique",
        AfterDistanceTrigger(LAST_SPURT) & (OvertakingTrigger() | OvertakenTrigger()),
        [Velocity(2)],
        duration=5.0
    )

def anchors_aweigh():
    return Skill(
        "Anchors Aweigh",
        "Unique",
        AfterDistanceTrigger(50) & AfterPositionTrigger(0.75),
        [Velocity(1.5)],
        duration=7.5
    )

### CHANTIER ###############################################################################################################################
############################################################################################################################################

