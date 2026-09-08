#determiner si corner/uphill etc

if self.course.track[runner.track_index].curvature != 0:
    corner = True
else:
    corner = False


#skill template

def ():
    return Skill(
        "",
        "Standard",
        ,
        []
    )
def ():
    return Skill(
        "",
        "Rare",
        ,
        []
    )


,
        Runner(
                    "Chameau",
                    1550, 1070, 920,
                    "end",
                    color="orange",
                    skills=[
                        #sonata_of_chamellerie(),
                        end_corners(),
                        daring_strike(),
                        masterful_gambit(),
                        encroaching_shadow(),
                        homestretch_haste(),
                        go_home_specialist()
                       
    
                    ]
                ),
        Runner(
                    "Sanhiro",
                    1570, 1310, 750,
                    "late",
                    color="#5555ff",
                    skills=[
                        late_straightaways(),
                        rising_dragon(),
                        latch_on(),
                        its_on(),
                        position_pilfer(),
                        lie_in_wait()
    
                    ]
                ),
        Runner(
                        "Berserk",
                        1610, 1070, 850,
                        "pace",
                        color="#009900",
                        skills=[
                            steady_gait(),
                            killer_tunes(),
                            all_ive_got(),
                            race_planner(),
                            head_on(),
                            speed_star()
        
                        ]
                    ),
Runner(
                    "Lilith",
                    1720, 1140, 620,
                    "front",
                    color="#ffaaff",
                    skills=[
                        front_straightaways(),
                        escape_artist(),
                        triple_7s(),
                        top_runner(),
                        productive_plan(),
                        taking_the_lead()
    
                    ]
                ),
Runner(
                    "Rogue",
                    1580, 1250, 840,
                    "pace",
                    color="#0033ff",
                    skills=[
                        pace_corners(),
                        come_what_may(),
                        corner_adept(),
                        swinging_maestro(),
                        highlander(),
                        determined_descent()
                    ]
                )
    