from skills import *

def corner_adept():
    return Skill(
        "Corner Adept",
        CornerTrigger(),
        [Velocity(0.15, 3)]
    )


def straight_descent():
    return Skill(
        "Downhill Adept",
        DownhillTrigger(),
        [Acceleration(0.4, 3)]
    )

