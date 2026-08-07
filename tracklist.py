from trackbuilder import *



nakayama_2000 = Circuit(
    
    name="Satsuki Sho",
    track="Nakayama 2000m",
    geometry=[

        Straight(124),

        Arc(
            radius=100,
            angle=180,
            clockwise=False
        ),

        Straight(280),

        Arc(
            radius=100,
            angle=110,
            clockwise=False
        ),

        Slope(
            length=150,
            gradient=2.2
        ),

        Arc(radius=70,
            angle=80,
            clockwise=False
        ),

        # Ligne du fond (outer)
        Straight(150),

        Arc(radius=120,
            angle=31,
            clockwise=False
        ),
        Straight(140),

        Arc(radius=100,
            angle =139,
            clockwise=False),

        Straight(250)
    ]
)
tokyo_2400 = Circuit(
    track="Tokyo 2400m",
    name="Japanese Derby",
    geometry=[

        # ligne droite avant le premier virage
        Straight(360),

        # grand virage
        Arc(
            radius=172,
            angle=180,
            clockwise=False
        ),

        # longue ligne opposée
        Straight(480),

        # dernier virage
        Arc(
            radius=172,
            angle=180,
            clockwise=False
        ),

        # montée finale
        Slope(
            length=200,
            gradient=2.0
        ),

        # ligne droite finale
        Straight(280)
    ]
)
kyoto_3000 = Circuit(
    name="Kikuka Sho",
    track="Kyoto 3000m",
    geometry=[

        Straight(106),

        Slope(100,1.5),

        Arc(200,180,False),

        Straight(330),

        Arc(200,180,False),

        Straight(230),

        Slope(100,1.5),
        Arc(200,180,False),


        Straight(250)
    ]
)
hanshin_2200 = Circuit(
    name="Takarazuka Kinen",
    track="Hanshin 2200m",
    geometry=[

        Straight(360),

        Arc(172,195,False),

        Straight(470),

        Arc(110,165,False),

        Slope(180,2.0),

        Straight(290)
    ]
)



if __name__ == "__main__":
    tokyo = TrackBuilder().build(tokyo_2400)
    nakayama = TrackBuilder().build(nakayama_2000)
    hanshin = TrackBuilder().build(hanshin_2200)
    kyoto = TrackBuilder().build(kyoto_3000)
    print(kyoto_3000.length)
    print(tokyo_2400.length)
    print(hanshin_2200.length)
    print(nakayama_2000.length)
