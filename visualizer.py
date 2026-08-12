import tkinter as tk
from math import cos, sin, pi

from factories import *

WIDTH = 900
HEIGHT = 700

class CourseSelector:

    def __init__(self, courses):
        self.courses = courses
        self.selected = None
        self.root = tk.Tk()
        self.root.title("Course Selector")
        self.root.geometry("1080x780")
        self.frames = []
        for i in range(2):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)
        for i, course in enumerate(courses):
            self.initframe(i, course)

    def initframe(self, i, course):
        frame = tk.Frame(self.root, bg="gray20", bd=2, relief="solid")
        frame.grid(
            row=i // 2,
            column=i % 2,
            padx=30,
            pady=30,
            sticky="nsew"
        )
        frame.grid_propagate(False)
        label = tk.Label(
            frame,
            text=f"{course.circuit.name}\n{course.circuit.track}",
            font=("Arial", 16),
            fg="white",
            bg="gray20"
        )
        label.pack(expand=True)
        frame.bind("<Button-1>", lambda event, c=course: self.select(c))
        label.bind("<Button-1>", lambda event, c=course: self.select(c))
        self.frames.append(frame)

    def select(self, course):
        self.selected = course
        self.root.destroy()

    def start(self):
        self.root.mainloop()

class TrackVisualizer:

    def __init__(self, course):
        self.course = course
        self.root = tk.Tk()
        self.root.title(course.circuit.name)
        self.return_to_selection = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)


        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH,
            height=HEIGHT,
            bg="black"
        )
        self.canvas.pack()
        self.return_button = tk.Button(
            self.root,
            text="Retour à la sélection",
            font=("Arial", 14),
            command=self.return_to_menu
        )
        self.return_button.pack(pady=10)
        
        self.prepare_scale()
        self.draw_track()
        self.draw_marker(self.course.track[0], "lime")
        self.draw_marker(self.course.track[-1], "red")
        self.runner_objects = []
        self.runner_texts = []
        colors = ["cyan", "pink", "orange", "green"]
        for i, runner in enumerate(course.runners):
            obj = self.canvas.create_oval(
                0, 0, 10, 10,
                fill=colors[i % len(colors)]
            )
            self.runner_objects.append(obj)
        self.ranking_text = self.canvas.create_text(
            20,
            HEIGHT - 250,
            anchor="nw",
            fill="white",
            font=("Courier", 12),
            text=""
        )
        self.results_text = self.canvas.create_text(
            WIDTH - 250,
            20,
            anchor="nw",
            fill="lime",
            font=("Courier", 12),
            text=""
        )

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

    def transform(self, x, y):
        sx = (x - self.min_x) * self.scale + 50
        sy = (y - self.min_y) * self.scale + 50
        sy = HEIGHT - sy
        return sy, sx

    def draw_track(self):
        points = self.course.track
        if len(points) < 2:
            return
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            x1, y1 = self.transform(p1.x, p1.y)
            x2, y2 = self.transform(p2.x, p2.y)
         
            ####Couleurs=======================
            if p1.gradient > 0:
                color = "#FF6600"
            elif p1.gradient < 0:
                color = "#00AA22"
            elif p1.curvature != 0:
                color = "#00AAFF"
            else:
                color = "#FFFFFF"
            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                width=3
            )

    def update(self):
        for obj, runner in zip(
            self.runner_objects,
            self.course.runners
        ):
            x, y = self.transform(
                runner.x,
                runner.y
            )
            self.canvas.coords(
                obj,
                x - 4,
                y - 4,
                x + 4,
                y + 4
            )
        self.update_ranking()
        self.update_results()

        if self.course.finished:
            self.return_button.pack(pady=10)
        else:
            self.root.after(16, self.update)

    def update_ranking(self):
        if self.course.finished:
            ranking = [result[1] for result in self.course.results]
        else:
            ranking = sorted(
                self.course.runners,
                key=lambda r: r.distance,
                reverse=True
            )
        classement = (
            f"Temps : {self.course.time:.2f}s\n"
            "====================\n"
        )
        for position, runner in enumerate(ranking, start=1):
            progress = (
                runner.distance /
                self.course.circuit.length
            ) * 100
            classement += (
                f"{position}. "
                f"{runner.name:<10} "
                f"{runner.distance:7.1f}m "
                f"({progress:5.1f}%) "
                f"{runner.current_speed:5.1f} km/h "
                f"{runner.hp:.0f} HP "
                f"{runner.total_hp_drain:.3f} Total "
                #f"{self.course.track[runner.track_index].curvature}"
                f"\n"
            )
        self.canvas.itemconfig(
            self.ranking_text,
            text=classement
        )

    def update_results(self):
        if not self.course.results:
            return
        texte = (
            "ARRIVEES\n"
            "================\n"
        )
        for position, runner, temps in self.course.results:
            texte += (
                f"{position}. "
                f"{runner.name:<10} "
                f"{temps:6.2f}s\n"
            )
        self.canvas.itemconfig(
            self.results_text,
            text=texte
        )

    def draw_marker(self, point, color, length=20):
        x, y = self.transform(point.x, point.y)
        dy = cos(point.heading + pi / 2)
        dx = -sin(point.heading + pi / 2)
        half = length / 2
        self.canvas.create_line(
            x - dx * half, y - dy * half,
            x + dx * half, y + dy * half,
            fill=color,
            width=3
        )

    def return_to_menu(self):
        self.return_to_selection = True
        self.root.destroy()

    def close(self):
        self.root.destroy()

    def start(self):
        self.root.mainloop()


