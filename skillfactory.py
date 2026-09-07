from skills import *


# ==================================================================================================
# CONSTANTES
# ==================================================================================================

EARLY_RACE = 0
MID_RACE = 33.333333
LATE_RACE = 66.666667
LAST_SPURT = 83.333333

WEAK_SPEED = 0.2
STANDARD_SPEED = 0.5
RARE_SPEED = 1

WEAK_ACCELERATION = 0.1
STANDARD_ACCELERATION = 0.2
RARE_ACCELERATION = 0.4

WEAK_RECOVERY = 10
STANDARD_RECOVERY = 25
RARE_RECOVERY = 100

UNIQUE_SPEED = 2.5
UNIQUE_ACCELERATION = 1
UNIQUE_RECOVERY = 250

SHORT_DURATION = 4.8
STANDARD_DURATION = 6.0
UNIQUE_DURATION = 10.0


### VELOCITY ###############################################################################################################################
############################################################################################################################################

def corner_adept():
    return Skill(
        "Corner Adept",
        "Standard",
        RandomCornerTrigger(MID_RACE, LATE_RACE),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def professor_of_curvature():
    return Skill(
        "Professor of Curvature",
        "Rare",
        RandomCornerTrigger(MID_RACE, LATE_RACE),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def straightaway_adept():
    return Skill(
        "Straightaway Adept",
        "Standard",
        RandomStraightawayTrigger(MID_RACE, LATE_RACE),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def beeline_burst():
    return Skill(
        "Beeline Burst",
        "Rare",
        RandomStraightawayTrigger(MID_RACE, LATE_RACE),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def ramp_up():
    return Skill(
        "Ramp Up",
        "Standard",
        AfterDistanceTrigger(MID_RACE) & OvertakingTrigger(1),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def its_on():
    return Skill(
        "It's On",
        "Rare",
        AfterDistanceTrigger(MID_RACE) & OvertakingTrigger(1),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def homestretch_haste():
    return Skill(
        "Homestretch Haste",
        "Standard",
        AfterDistanceTrigger(LAST_SPURT) & StraightawayTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def in_body_and_mind():
    return Skill(
        "In Body and Mind",
        "Rare",
        AfterDistanceTrigger(LAST_SPURT) & StraightawayTrigger(),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def fast_paced():
    return Skill(
        "Fast Paced",
        "Standard",
        FrontRunnerTrigger() & BetweenDistanceTrigger(MID_RACE, LATE_RACE) & BeforePositionTrigger(50),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def escape_artist():
    return Skill(
        "Escape Artist",
        "Rare",
        FrontRunnerTrigger() & BetweenDistanceTrigger(MID_RACE, LATE_RACE) & BeforePositionTrigger(50),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def leaders_pride():
    return Skill(
        "Leader's Pride",
        "Standard",
        BetweenDistanceTrigger(5, LATE_RACE) & (OvertakingTrigger() | OvertakenTrigger()),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def top_runner():
    return Skill(
        "Top Runner",
        "Rare",
        BetweenDistanceTrigger(5, LATE_RACE) & (OvertakingTrigger() | OvertakenTrigger()),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def prepared_to_pass():
    return Skill(
        "Prepared to Pass",
        "Standard",
        PaceChaserTrigger() & BeforePositionTrigger(50) & FinalCornerTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def speed_star():
    return Skill(
        "Speed Star",
        "Rare",
        PaceChaserTrigger() & BeforePositionTrigger(50) & FinalCornerTrigger(),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def position_pilfer():
    return Skill(
        "Position Pilfer",
        "Standard",
        LateSurgerTrigger() & BetweenDistanceTrigger(MID_RACE, LATE_RACE) & AfterPositionTrigger(50),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def fast_and_furious():
    return Skill(
        "Fast & Furious",
        "Rare",
        LateSurgerTrigger() & BetweenDistanceTrigger(MID_RACE, LATE_RACE) & AfterPositionTrigger(50),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def outer_swell():
    return Skill(
        "Outer Swell",
        "Standard",
        LateSurgerTrigger() & FinalCornerTrigger() & OvertakingTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def rising_dragon():
    return Skill(
        "Rising Dragon",
        "Rare",
        LateSurgerTrigger() & FinalCornerTrigger() & OvertakingTrigger(),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def masterful_gambit():
    return Skill(
        "Masterful Gambit",
        "Standard",
        EndCloserTrigger() & AfterDistanceTrigger(LAST_SPURT),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def sturm_und_drang():
    return Skill(
        "Sturm Und Drang",
        "Rare",
        EndCloserTrigger() & AfterDistanceTrigger(LAST_SPURT),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def steadfast():
    return Skill(
        "Steadfast",
        "Standard",
        FinalCornerTrigger() & DiffBehindTrigger(1),
        [Velocity(STANDARD_SPEED), Acceleration(WEAK_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def unyielding():
    return Skill(
        "Unyielding",
        "Rare",
        FinalCornerTrigger() & DiffBehindTrigger(1),
        [Velocity(RARE_SPEED), Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def productive_plan():
    return Skill(
        "Productive Plan",
        "Standard",
        RandomBetweenDistanceTrigger(100 / 6, MID_RACE) & BeforePositionTrigger(50),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def mile_maven():
    return Skill(
        "Mile Maven",
        "Rare",
        RandomBetweenDistanceTrigger(100 / 6, MID_RACE) & BeforePositionTrigger(50),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def up_tempo():
    return Skill(
        "Up-Tempo",
        "Standard",
        BetweenDistanceTrigger(MID_RACE, LATE_RACE),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def killer_tunes():
    return Skill(
        "Killer Tunes",
        "Rare",
        BetweenDistanceTrigger(MID_RACE, LATE_RACE),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def early_start():
    return Skill(
        "Early Start",
        "Standard",
        MidRaceTrigger() & AfterPositionTrigger(50) & EndCloserTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def daring_strike():
    return Skill(
        "Daring Strike",
        "Rare",
        MidRaceTrigger() & AfterPositionTrigger(50) & EndCloserTrigger(),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def _1500000cc():
    return Skill(
        "1,500,000 CC",
        "Standard",
        RandomUphillTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def _15000000cc():
    return Skill(
        "15,000,000 CC",
        "Rare",
        RandomUphillTrigger(),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def fearless():
    return Skill(
        "Fearless",
        "Standard",
        RandomAfterDistanceTrigger(50) & LateSurgerTrigger() & BetweenPositionTrigger(30, 80),
        [Velocity(STANDARD_SPEED), Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def dauntless():
    return Skill(
        "Dauntless",
        "Rare",
        RandomAfterDistanceTrigger(50) & LateSurgerTrigger() & BetweenPositionTrigger(30, 80),
        [Velocity(RARE_SPEED), Acceleration(RARE_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def full_throttle():
    return Skill(
        "Full Throttle",
        "Standard",
        MidRaceTrigger() & LateSurgerTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def keep_going():
    return Skill(
        "Keep Going !",
        "Rare",
        MidRaceTrigger() & LateSurgerTrigger(),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def latch_on():
    return Skill(
        "Latch On",
        "Standard",
        (PaceChaserTrigger() | LateSurgerTrigger()) & AfterDistanceTrigger(50) & OvertakingTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def hot_pursuit():
    return Skill(
        "Hot Pursuit",
        "Rare",
        (PaceChaserTrigger() | LateSurgerTrigger()) & AfterDistanceTrigger(50) & OvertakingTrigger(),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


def steady_gait():
    return Skill(
        "Steady Gait",
        "Standard",
        PaceChaserTrigger() & RandomBetweenDistanceTrigger(50, LATE_RACE),
        [Velocity(WEAK_SPEED), Acceleration(WEAK_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def solid_strike():
    return Skill(
        "Solid Strike",
        "Rare",
        PaceChaserTrigger() & RandomBetweenDistanceTrigger(50, LATE_RACE),
        [Velocity(STANDARD_SPEED), Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def all_ive_got():
    return Skill(
        "All I've Got",
        "Standard",
        StraightawayTrigger() & LastSpurtTrigger() & BetweenPositionTrigger(20, 60),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def come_what_may():
    return Skill(
        "Come What May",
        "Rare",
        StraightawayTrigger() & LastSpurtTrigger() & BetweenPositionTrigger(20, 60),
        [Velocity(RARE_SPEED)],
        duration=STANDARD_DURATION
    )


### STYLE VELOCITY #########################################################################################################################
############################################################################################################################################

def front_corners():
    return Skill(
        "Front Runner Corners",
        "Standard",
        FrontRunnerTrigger() & RandomCornerTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def pace_corners():
    return Skill(
        "Pace Chaser Corners",
        "Standard",
        PaceChaserTrigger() & RandomCornerTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def late_corners():
    return Skill(
        "Late Surger Corners",
        "Standard",
        LateSurgerTrigger() & RandomCornerTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def end_corners():
    return Skill(
        "End Closer Corners",
        "Standard",
        EndCloserTrigger() & RandomCornerTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def front_straightaways():
    return Skill(
        "Front Runner Straightaways",
        "Standard",
        FrontRunnerTrigger() & RandomStraightawayTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def pace_straightaways():
    return Skill(
        "Pace Chaser Straightaways",
        "Standard",
        PaceChaserTrigger() & RandomStraightawayTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def late_straightaways():
    return Skill(
        "Late Surger Straightaways",
        "Standard",
        LateSurgerTrigger() & RandomStraightawayTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


def end_straightaways():
    return Skill(
        "End Closer Straightaways",
        "Standard",
        EndCloserTrigger() & RandomStraightawayTrigger(),
        [Velocity(STANDARD_SPEED)],
        duration=STANDARD_DURATION
    )


### ACCEL ##################################################################################################################################
############################################################################################################################################

def corner_acceleration():
    return Skill(
        "Corner Acceleration",
        "Standard",
        RandomCornerTrigger(),
        [Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def corner_connoisseur():
    return Skill(
        "Corner Connoisseur",
        "Rare",
        RandomCornerTrigger(),
        [Acceleration(RARE_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def straightaway_acceleration():
    return Skill(
        "Straightaway Acceleration",
        "Standard",
        RandomStraightawayTrigger(),
        [Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def rushing_gale():
    return Skill(
        "Rushing Gale",
        "Rare",
        RandomStraightawayTrigger(),
        [Acceleration(RARE_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def nimble_navigator():
    return Skill(
        "Nimble Navigator",
        "Standard",
        LateRaceTrigger() & DiffInFrontTrigger(1),
        [Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def no_stopping_me():
    return Skill(
        "No Stopping Me",
        "Rare",
        LateRaceTrigger() & DiffInFrontTrigger(1),
        [Acceleration(RARE_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def highlander():
    return Skill(
        "Highlander",
        "Standard",
        UphillTrigger(),
        [Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def early_lead():
    return Skill(
        "Early Lead",
        "Standard",
        AfterDistanceTrigger(0),
        [Acceleration(STANDARD_ACCELERATION)],
        duration=SHORT_DURATION
    )


def taking_the_lead():
    return Skill(
        "Taking the Lead",
        "Rare",
        AfterDistanceTrigger(0),
        [Acceleration(RARE_ACCELERATION)],
        duration=SHORT_DURATION
    )


def straight_descent():
    return Skill(
        "Straight Descent",
        "Standard",
        RandomDownhillTrigger(),
        [Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def determined_descent():
    return Skill(
        "Determined Descent",
        "Rare",
        RandomDownhillTrigger(),
        [Acceleration(RARE_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def head_on():
    return Skill(
        "Head-On",
        "Standard",
        PaceChaserTrigger() & RandomBetweenDistanceTrigger(LATE_RACE, LAST_SPURT),
        [Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def neck_and_neck():
    return Skill(
        "Neck and Neck",
        "Rare",
        PaceChaserTrigger() & RandomBetweenDistanceTrigger(LATE_RACE, LAST_SPURT),
        [Acceleration(RARE_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def slick_surge():
    return Skill(
        "Slick Surge",
        "Standard",
        LateSurgerTrigger() & LateRaceTrigger(),
        [Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def on_your_left():
    return Skill(
        "On Your Left !",
        "Rare",
        LateSurgerTrigger() & LateRaceTrigger(),
        [Acceleration(RARE_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def straightaway_spurt():
    return Skill(
        "Straightaway Spurt",
        "Standard",
        LateRaceTrigger() & StraightawayTrigger(),
        [Acceleration(STANDARD_ACCELERATION)],
        duration=STANDARD_DURATION
    )


def encroaching_shadow():
    return Skill(
        "Encroaching Shadow",
        "Rare",
        LateRaceTrigger() & StraightawayTrigger(),
        [Acceleration(RARE_ACCELERATION)],
        duration=STANDARD_DURATION
    )


### RECOVERY ###############################################################################################################################
############################################################################################################################################

def corner_recovery():
    return Skill(
        "Corner Recovery",
        "Standard",
        RandomCornerTrigger(),
        [Recovery(STANDARD_RECOVERY)]
    )


def swinging_maestro():
    return Skill(
        "Swinging Maestro",
        "Rare",
        RandomCornerTrigger(),
        [Recovery(RARE_RECOVERY)]
    )


def straightaway_recovery():
    return Skill(
        "Straightaway Recovery",
        "Standard",
        RandomStraightawayTrigger(),
        [Recovery(STANDARD_RECOVERY)]
    )


def breath_of_fresh_air():
    return Skill(
        "Breath Of Fresh Air",
        "Rare",
        RandomStraightawayTrigger(),
        [Recovery(RARE_RECOVERY)]
    )


def preferred_position():
    return Skill(
        "Preferred Position",
        "Standard",
        PaceChaserTrigger() & BeforePositionTrigger(50) & RandomBetweenDistanceTrigger(MID_RACE, LATE_RACE),
        [Recovery(STANDARD_RECOVERY)]
    )


def race_planner():
    return Skill(
        "Race Planner",
        "Rare",
        PaceChaserTrigger() & BeforePositionTrigger(50) & RandomBetweenDistanceTrigger(MID_RACE, LATE_RACE),
        [Recovery(RARE_RECOVERY)]
    )


def be_still():
    return Skill(
        "Be Still",
        "Standard",
        LateSurgerTrigger() & MidRaceTrigger() & AfterPositionTrigger(50),
        [Recovery(STANDARD_RECOVERY)]
    )


def lie_in_wait():
    return Skill(
        "Lie In Wait",
        "Rare",
        LateSurgerTrigger() & MidRaceTrigger() & AfterPositionTrigger(50),
        [Recovery(RARE_RECOVERY)]
    )


def after_school_stroll():
    return Skill(
        "After School Stroll",
        "Standard",
        RandomDownhillTrigger(),
        [Recovery(STANDARD_RECOVERY)]
    )


def go_home_specialist():
    return Skill(
        "Go Home Specialist",
        "Rare",
        RandomDownhillTrigger(),
        [Recovery(RARE_RECOVERY)]
    )


def triple_7s():
    return Skill(
        "Triple 7s",
        "Standard",
        MeterDistanceRemainingTrigger(777),
        [Recovery(STANDARD_RECOVERY)]
    )


### ULTIMATE ###############################################################################################################################
############################################################################################################################################

def moving_past_and_beyond():
    return Skill(
        "Moving Past, and Beyond",
        "Unique",
        AfterDistanceTrigger(LATE_RACE) & CornerTrigger() & BetweenPositionTrigger(60, 75),
        [Acceleration(UNIQUE_ACCELERATION)],
        duration=UNIQUE_DURATION
    )


def angling_and_scheming():
    return Skill(
        "Angling and Scheming",
        "Unique",
        AfterDistanceTrigger(LATE_RACE) & CornerTrigger() & BeforePositionTrigger(1),
        [Acceleration(UNIQUE_ACCELERATION)],
        duration=UNIQUE_DURATION
    )


def this_dance_is_for_vittoria():
    return Skill(
        "This Dance is for Vittoria !",
        "Unique",
        AfterDistanceTrigger(LAST_SPURT) & (OvertakingTrigger() | OvertakenTrigger()),
        [Velocity(UNIQUE_SPEED)],
        duration=UNIQUE_DURATION
    )


def anchors_aweigh():
    return Skill(
        "Anchors Aweigh",
        "Unique",
        AfterDistanceTrigger(50) & AfterPositionTrigger(75),
        [Velocity(UNIQUE_SPEED)],
        duration=UNIQUE_DURATION
    )