from trackbuilder import *
from runner import *


nakayama_2000 = Circuit(
    name="Satsuki Sho",
    track="Nakayama 2000m",
    geometry=[

        Straight(124),

        Arc(100, 180, True),

        Straight(280),

        Arc(100, 110, True),

        Slope(150, 2.2),

        Arc(70, 80, True),

        Straight(150),

        Arc(120, 31, True),

        Straight(140),

        Arc(100, 139, True),

        Straight(250)
    ]
)

tokyo_2400 = Circuit(
    name="Japanese Derby",
    track="Tokyo 2400m",
    geometry=[

        Straight(356),

        Arc(200, 85, False),
        Arc(150, 95, False),
        Straight(476),

        Arc(200, 85, False),
        Arc(150, 95, False),
        Slope(200, 2.0),

        Straight(280)
    ]
)
kyoto_3000 = Circuit(
    name="Kikuka Sho",
    track="Kyoto 3000m",
    geometry=[

        

        Slope(260,1.5),

        Arc(110,95,True),
        Slope(120,-1.5),
        Arc(110,100,True),
        Straight(500),

        Arc(105,165,True),

        Straight(235),
        Slope(260,1.5),
       
        Arc(110,95,True),
        Slope(120,-1.5),
        Arc(110,100,True),
        Straight(460),


    ]
)
hanshin_2200 = Circuit(
    name="Takarazuka Kinen",
    track="Hanshin 2200m",
    geometry=[

        Slope(295,-1.0),
        Slope(125,1.0),
        Straight(100),
        Arc(134,85,True),
        Arc(134,80,True),
        Straight(348),
	    Arc(170,75,True),
        Arc(280,25,True),
        Arc(145,95,True),
        Slope(160,-1.0),
        Slope(125,1.0),
        Straight(83)
    ]
)

laumamusume2 = Circuit(
    name="Lauma Musume Track N°2",
    track = "Nod-Krai Teappot",
    geometry = [
        Straight(10),
        Arc(15,20,True),
        Straight(30),
        Arc(15,85,True),
        Slope(50,-2.0),
        Arc(30,180,False),
        Straight(50),
        Arc(60,80,False),
        Slope(30,5.0),
        Slope(2,-7.0),
        Arc(10,90,False),
        Straight(20),
        Arc(20,30,False),
        Arc(60,90,True),
        Straight(40),
        Arc(2,90,True),
        Straight(40),
        Arc(2,90,True),
        Straight(30),
        Arc(2,90,False),
        Straight(25),
        Arc(10,50,False),
        Slope(15,2.0),
        Arc(5,180,False),
        Straight(35),
        Arc(8,50,False),
        Straight(15),
        Arc(20,17,True),
        Straight(10)


    ]
)
ibisdash = Circuit(
    name="Ibis Summer Dash",
    track="Niigata 1000m",
    geometry=[Straight(1000)]
)







if __name__ == "__main__":
    tokyo = TrackBuilder().build(tokyo_2400)
    nakayama = TrackBuilder().build(nakayama_2000)
    hanshin = TrackBuilder().build(hanshin_2200)
    kyoto = TrackBuilder().build(kyoto_3000)
    lauma = TrackBuilder().build(laumamusume2)


    print(kyoto_3000.length)
    print(tokyo_2400.length)
    print(hanshin_2200.length)
    print(nakayama_2000.length)
    print(laumamusume2.length)