import tkinter as tk
from math import cos, sin, pi

from factories import *

WIDTH = 1320
HEIGHT = 800
TRACK_AREA_WIDTH = WIDTH*0.5
TRACK_AREA_HEIGHT = HEIGHT * 0.6

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
        self.draw_ui()
        self.skill_cards = {}
        self.max_skill_cards = 9

        self.prepare_scale()
        self.draw_track()
        self.draw_marker(self.course.track[0], "lime")
        self.draw_marker(self.course.track[-1], "red")


        self.runner_objects = []
        self.runner_texts = []
        
        for i, runner in enumerate(course.runners):
            obj = self.canvas.create_oval(
                0, 0, 0, 0,
                fill=runner.color
            )
            self.runner_objects.append(obj)
           
        self.update()

        

    def draw_ui(self):
    ####zones ==================================
        self.canvas.create_rectangle(
            4,
            4,
            TRACK_AREA_WIDTH,
            TRACK_AREA_HEIGHT,
            outline="gray",
            width=2
        )
        self.canvas.create_rectangle(
                   
            TRACK_AREA_WIDTH,
            4,
            WIDTH*0.75,
            HEIGHT,
            outline="gray",
            width=2
            )
        self.canvas.create_rectangle(
                   
            WIDTH * 0.75,
            4,
            WIDTH,
            HEIGHT,
            outline="gray",
            width=2
            )
    #### Skill Zone===============================
        self.skill_text = self.canvas.create_text(
            TRACK_AREA_WIDTH + 15,
            20,
            anchor="nw",
            fill="yellow",
            font=("Arial", 13, "bold"),
            text=""
        )
        self.skill_frame = tk.Frame(
            self.root,
            bg="gray10"
        )

        self.skill_frame.place(
            x=TRACK_AREA_WIDTH + 10,
            y=10,
            width=WIDTH * 0.25 - 20,
            height=HEIGHT - 20
        )

    #### leaderboards =============================
        self.ranking_text = self.canvas.create_text(
                WIDTH*0.01,
                HEIGHT*0.7,
                anchor="nw",
                fill="white",
                font=("Courier", 12),
                text=""
            )
        self.results_text = self.canvas.create_text(
                WIDTH*0.75+20,
                HEIGHT*0.01,
                anchor="nw",
                fill="lime",
                font=("Courier", 12),
                text=""
            )
        
    def create_skill_card(self, runner, skill, remaining):

        card = tk.Frame(
            self.skill_frame,
            bg="#332f2f",
            bd=2,
            relief="solid"
        )

        card.pack(
            fill="x",
            padx=(180, 5),
            pady=5
        )

        # Nom du runner
        runner_label = tk.Label(
            card,
            text=runner.name,
            bg="#332f2f",
            fg="#555555",
            font=("Arial", 10, "bold")
        )
        runner_label.pack(
            anchor="w",
            padx=8,
            pady=(5, 0)
        )

        # Ligne skill + temps
        skill_line = tk.Frame(
            card,
            bg="#332f2f"
        )
        skill_line.pack(
            fill="x",
            padx=8
        )

        # Nom du skill
        skill_label = tk.Label(
            skill_line,
            text=skill.name,
            bg="#332f2f",
            fg="#555555",
            font=("Arial", 12, "bold")
        )
        skill_label.pack(
            side="left"
        )

        # Temps restant
        time_label = tk.Label(
            skill_line,
            text=f"{remaining:.1f}s",
            bg="#332f2f",
            fg="#555555",
            font=("Courier", 10, "bold")
        )
        time_label.pack(
            side="right"
        )

        # Barre de progression
        progress = tk.Canvas(
            card,
            height=10,
            bg="#332f2f",
            highlightthickness=0
        )
        progress.pack(
            fill="x",
            padx=8,
            pady=(0, 7)
        )

        bar = progress.create_rectangle(
            0, 0, 0, 10,
            fill="#555555",
            outline=""
        )

        return {
            "frame": card,
            "runner_label": runner_label,
            "skill_line": skill_line,
            "skill_label": skill_label,
            "time_label": time_label,
            "progress": progress,
            "bar": bar,
            "duration": skill.duration,
            "runner_color": runner.color,
            "animating": True,


        }


        
    def prepare_scale(self): # = taille
        xs = [p.x for p in self.course.track]
        ys = [p.y for p in self.course.track]
        self.min_x = min(xs)
        self.max_x = max(xs)
        self.min_y = min(ys)
        self.max_y = max(ys)
        width = self.max_x - self.min_x
        height = self.max_y - self.min_y

        

        margin = 20

        available_width = TRACK_AREA_WIDTH - 2 * margin
        available_height = TRACK_AREA_HEIGHT - 2 * margin

        # Après rotation de 90°, largeur et hauteur sont inversées
        self.scale = min(
            available_width / width,
            available_height / height
        ) * 1


    def transform(self, x, y): # = position
    # Centrer les coordonnées autour de l'origine
        x -= (self.min_x + self.max_x) / 2 
        y -= (self.min_y + self.max_y) / 2 

        sx = -y * self.scale + WIDTH * 0.25
        sy = HEIGHT *0.3 - x * self.scale
        return sx, sy


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

        self.update_skill_display()


        self.update_ranking()
        self.update_results()

        if self.course.finished:
            self.return_button.pack(pady=10)
        else:
            self.root.after(16, self.update)



    def update_skill_display(self):

        active_skills = set()

        for runner in self.course.runners:

            for skill, remaining in runner.get_active_skills():
                remaining = skill.remaining
                key = (id(runner), id(skill))

                active_skills.add(key)

                if key not in self.skill_cards:

                    card = self.create_skill_card(
                        runner,
                        skill,
                        remaining
                    )

                    self.skill_cards[key] = card

                    self.animate_skill_in(card)


                card = self.skill_cards[key]

                card["time_label"].config(
                    text=f"{remaining:.1f}s"
                )

                duration = card["duration"]

                if duration > 0:
                    ratio = max(
                        0,
                        min(1, remaining / duration)
                    )
                else:
                    ratio = 0

                width = card["progress"].winfo_width()

                card["progress"].coords(
                    card["bar"],
                    0,
                    0,
                    width * ratio,
                    10
                )

        # Supprimer les skills terminés
        for key in list(self.skill_cards):

            if key not in active_skills:

                card = self.skill_cards.pop(key)

                card["frame"].destroy()

        # Affichage de la pile
        self.update_skill_stack()


    def update_skill_stack(self):

        cards = list(self.skill_cards.values())
        visible_cards = cards[-self.max_skill_cards:]

        for card in cards:

            if card not in visible_cards:
                card["frame"].pack_forget()





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
            if position < len(ranking):
                next_runner = ranking[position]
                gap = next_runner.distance - runner.distance
            else:
                next_runner = None
                gap = 0

            classement += (
                f"{position}. "
                f"{runner.name:<10} | "
                f"{runner.distance:7.1f}m "
                f"({progress:5.1f}%) | "
                #f"{runner.current_speed:5.1f} km/h | "
                #f"{runner.hp:.0f} HP | "
                f"Ecart : {gap:7.1f}"
                
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
        dx = cos(point.heading )
        dy = -sin(point.heading )
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


    def animate_skill_in(self, card):
        frame = card["frame"]

        steps = 15
        interval = 16

        start_padx = 180
        end_padx = 5

        # Couleurs de départ
        start_bg = "#332f2f"
        start_fg = "#555555"

        # Couleurs finales
        final_bg = "#ffeeee"
        final_fg = "#331100"

        runner_color = card["runner_color"]

        def interpolate_color(c1, c2, t):
            c1 = c1.lstrip("#")
            c2 = c2.lstrip("#")

            r1, g1, b1 = (
                int(c1[0:2], 16),
                int(c1[2:4], 16),
                int(c1[4:6], 16)
            )

            r2, g2, b2 = (
                int(c2[0:2], 16),
                int(c2[2:4], 16),
                int(c2[4:6], 16)
            )

            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)

            return f"#{r:02x}{g:02x}{b:02x}"

        def animate(step=0):
            if not frame.winfo_exists():
                return
            t = step / steps

            # Ease-out cubic
            eased = 1 - (1 - t) ** 3

            # =========================
            # Slide depuis la droite
            # =========================

            padx_left = int(
                start_padx +
                (end_padx - start_padx) * eased
            )

            frame.pack_configure(
                padx=(padx_left, 5)
            )

            # =========================
            # Fade du fond
            # =========================

            bg = interpolate_color(
                start_bg,
                final_bg,
                eased
            )

            # =========================
            # Fade du texte
            # =========================

            fg = interpolate_color(
                start_fg,
                final_fg,
                eased
            )

            frame.config(bg=bg)
            card["runner_label"].config(
                bg=bg,
                fg=runner_color
            )

            card["skill_line"].config(
                bg=bg
            )

            card["skill_label"].config(
                bg=bg,
                fg=fg
            )

            card["time_label"].config(
                bg=bg,
                fg=runner_color
            )

            card["progress"].config(
                bg=bg
            )

            card["progress"].itemconfig(
                card["bar"],
                fill=runner_color
            )

            if step < steps:
                frame.after(
                    interval,
                    lambda: animate(step + 1)
                )
            else:
                card["animating"] = False
                frame.pack_configure(padx=(5, 5))

        animate()
