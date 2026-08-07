from dataclasses import dataclass
from math import sin, cos, pi, radians


STEP = 2.0


@dataclass
class Straight:
    length: float


@dataclass
class Arc:
    radius: float
    angle: float
    clockwise: bool


@dataclass
class Slope:
    length: float
    gradient: float


Geometry = Straight | Arc | Slope


@dataclass
class Circuit:
    name: str
    track:str
    geometry: list[Geometry]
    length: float = 0


@dataclass
class TrackPoint:
    x: float
    y: float
    heading: float
    gradient: float
    curvature: float



class TrackBuilder:

    def build(self, circuit):

        x = 0.0
        y = 0.0

        heading = radians(90)

        distance = 0

        points = [
            TrackPoint(
                x=x,
                y=y,
                heading=heading,
                gradient=0,
                curvature=0
            )
        ]


        for part in circuit.geometry:


            if isinstance(part, (Straight, Slope)):

                n = int(part.length / STEP)

                gradient = (
                    part.gradient
                    if isinstance(part, Slope)
                    else 0
                )


                for _ in range(n):

                    x += STEP * cos(heading)
                    y += STEP * sin(heading)

                    distance += STEP

                    points.append(
                        TrackPoint(
                            x=x,
                            y=y,
                            heading=heading,
                            gradient=gradient,
                            curvature=0
                        )
                    )


            elif isinstance(part, Arc):

                direction = -1 if part.clockwise else 1

                arc = radians(part.angle)

                n = int(abs(part.radius * arc) / STEP)

                dtheta = direction * abs(arc) / n


                cx = x - direction * part.radius * sin(heading)
                cy = y + direction * part.radius * cos(heading)


                theta = heading - direction * pi / 2


                for _ in range(n):

                    theta += dtheta

                    x = cx + part.radius * cos(theta)
                    y = cy + part.radius * sin(theta)

                    heading += dtheta

                    distance += STEP

                    points.append(
                        TrackPoint(
                            x=x,
                            y=y,
                            heading=heading,
                            gradient=0,
                            curvature=1 / part.radius
                        )
                    )


        circuit.length = distance

        return points
