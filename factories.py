from runner import Runner
from skills import *
from skillfactory import *
from moteurdecourse import Course
from trackbuilder import *

def create_runners():
    return [
        Runner("Strid",1450,1250,1100,color="cyan",
               skills=[moving_past_and_beyond()]),

        Runner("Chameau", 1420, 1200, 750, color="orange",
               skills=[professor_of_curvature(), 
                       determined_descent(), 
                       beeline_burst()


                       ]
               ),



        Runner("Lilith",1450,1280,1100,color="pink",
               skills=[speed_star(),
                       fast_paced()
                
               ]),

        Runner("Berserk",1350,1350,1100,color="green",
                       skills=[speed_star(),
                               in_body_and_mind(),
                               fast_paced(),
                               homestretch_haste()
                        
                       ])


            
    ]


#ajouter start_heading = 0/90/180 etc








nakayama_2000 = Circuit(
    name="Satsuki Sho",
    track="Nakayama 2000m",
    start_heading= -pi /2,
    geometry=[
        Straight(124),
        Arc(1,100, 180, True),
        Straight(280),
        Arc(2,100, 110, True),
        Straight(150),
        Arc(3,70, 80, True),
        Straight(150),
        Arc(4,120, 31, True),
        Straight(140),
        Arc(5,100, 139, True, 0.0, is_final_corner=True),
        Straight(250)
    ]
)


tokyo_2400 = Circuit(
    name="Japanese Derby",
    track="Tokyo 2400m",
    start_heading= -pi /2,
    geometry=[

        Straight(356),

        Arc(1,200, 85, False),
        Arc(2,150, 95, False),
        Straight(476),

        Arc(3,200, 85, False),
        Arc(4,150, 95, False, is_final_corner=True),
        Straight(200, 2.0),

        Straight(280)
    ]
)
kyoto_3000 = Circuit(
    name="Kikuka Sho",
    track="Kyoto 3000m",
    start_heading=-pi /2 + (15*pi/90),
    geometry=[

        

        Straight(260,1.5),

        Arc(1,110,95,True),
        Straight(120,-1.5),
        Arc(2,110,100,True),
        Straight(500),

        Arc(3,105,165,True),

        Straight(235),
        Straight(260,1.5),
       
        Arc(4,110,95,True),
        Straight(120,-1.5),
        Arc(5,110,100,True, is_final_corner=True),
        Straight(460),


    ]
)
hanshin_2200 = Circuit(
    name="Takarazuka Kinen",
    track="Hanshin 2200m",
    start_heading=-pi/2,
    geometry=[

        Straight(295,-1.0),
        Straight(125,1.0),
        Straight(100),
        Arc(1,134,85,True),
        Arc(2,134,80,True),
        Straight(348),
	    Arc(3,170,75,True),
        Arc(4,280,25,True),
        Arc(5,145,95,True, is_final_corner=True),
        Straight(160,-1.0),
        Straight(125,1.0),
        Straight(83)
    ]
)

laumamusume2 = Circuit(
    name="Lauma Musume Track N°2",
    track = "Nod-Krai Teappot",
    start_heading=pi/2,
    geometry = [
        Straight(10),
        Arc(1,15,20,True),
        Straight(30),
        Arc(2,15,85,True),
        Straight(50,-2.0),
        Arc(3,30,180,False),
        Straight(50),
        Arc(4,60,80,False),
        Straight(30,5.0),
        Straight(2,-7.0),
        Arc(5,10,90,False),
        Straight(20),
        Arc(6,20,30,False),
        Arc(7,60,90,True),
        Straight(40),
        Arc(8,2,90,True),
        Straight(40),
        Arc(9,2,90,True),
        Straight(30),
        Arc(10,2,90,False),
        Straight(25),
        Arc(11,10,50,False),
        Straight(15,2.0),
        Arc(12,5,180,False),
        Straight(35),
        Arc(13,8,50,False),
        Straight(15),
        Arc(14,20,17,True, is_final_corner=True),
        Straight(10)
    ]
)
ibisdash = Circuit(
    name="Ibis Summer Dash",
    track="Niigata 1000m",
    geometry=[Straight(1000,0.0)]
)


def create_courses():
    return [
        Course(
            nakayama_2000,
            "b",
            create_runners()
        ),
        Course(
            tokyo_2400,
            "b",
            create_runners()
        ),
        Course(
            kyoto_3000,
            "b",
            create_runners()
        ),
        Course(
            hanshin_2200,
            "b",
            create_runners()
        ),
        Course(
            laumamusume2,
            "a",
            create_runners()
        ),
        Course(
            ibisdash,
            "b",
            create_runners()
        )
    ]
