import tkinter as tk
from math import cos, sin


WIDTH = 900
HEIGHT = 700


class TrackVisualizer:

    def __init__(self, course):

        self.course = course

        self.root = tk.Tk()
        self.root.title(course.circuit.name)

        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH,
            height=HEIGHT,
            bg="black"
        )

        self.canvas.pack()


        self.prepare_scale()


        self.draw_track()

        self.draw_marker(
            self.course.track[0],
            "lime"
        )

        self.draw_marker(
            self.course.track[-1],
            "red"
        )


        self.runner_objects = []

        colors = [
            "red",
            "cyan",
            "yellow",
            "green"
        ]

        for i, runner in enumerate(course.runners):

            obj = self.canvas.create_oval(
                0,
                0,
                10,
                10,
                fill=colors[i % len(colors)]
            )

            self.runner_objects.append(obj)



        self.update()


    def prepare_scale(self):

        xs = [p.x for p in self.course.track]
        ys = [p.y for p in self.course.track]


        self.min_x = min(xs)
        self.max_x = max(xs)

        self.min_y = min(ys)
        self.max_y = max(ys)


        width = self.max_x - self.min_x
        height = self.max_y - self.min_y


        self.scale = min(
            WIDTH / width,
            HEIGHT / height
        ) * 0.8



    def transform(self,x,y):

        sx = (
            x - self.min_x
        ) * self.scale + 50


        sy = (
            y - self.min_y
        ) * self.scale + 50


        # tkinter a l'axe Y inversé
        sy = HEIGHT - sy


        return sx, sy



    def draw_track(self):

        points = []

        for p in self.course.track:

            y,x = self.transform(
                p.x,
                p.y
            )

            points.extend(
                [x,y]
            )


        self.canvas.create_line(
            points,
            fill="white",
            width=3
        )



    def update(self):

        for obj, runner in zip(
            self.runner_objects,
            self.course.runners
        ):

            y,x = self.transform(
                runner.x,
                runner.y
            )


            r = 4

            self.canvas.coords(
                obj,
                x-r,
                y-r,
                x+r,
                y+r
            )


        self.root.after(
            16,
            self.update
        )


    def draw_marker(self, point, color, length=20):

        x,y = self.transform(point.x, point.y)

        # direction perpendiculaire à la piste
        dx = cos(point.heading + 3.14159265 / 2)
        dy = -sin(point.heading + 3.14159265 / 2)
        # le signe - vient du fait que Tkinter inverse l'axe Y

        half = length / 2

        self.canvas.create_line(
            y - dy * half,
            x - dx * half,
            y + dy * half,
            x + dx * half,
            fill=color,
            width=3
        )


    def start(self):

        self.root.mainloop()
