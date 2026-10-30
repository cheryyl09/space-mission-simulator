import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

BG = "#071326"
WHITE = "#f3f6ff"
TEAL = "#55e6cf"

EVENTS = [
    ("ASTEROIDS", "Rocks block your route!",
     [("Evade", -12, 0, -8), ("Shield", -20, 0, 5),
      ("Risk it", -3, 0, -25)]),
    ("OXYGEN LEAK", "Oxygen is escaping!",
     [("Repair", -5, 8, 0), ("Seal", 0, -5, 0),
      ("Ignore", 0, -22, 0)]),
    ("ENGINE FAILURE", "The engine is overheating!",
     [("Cool", -8, 0, 5), ("Backup", -18, 0, -5),
      ("Push", -5, 0, -18)]),
    ("SUPPLIES", "A supply capsule is nearby!",
     [("Collect", -5, 15, 8), ("Scan", -2, 5, 0),
      ("Ignore", 0, 0, 0)]),
    ("SOLAR STORM", "Radiation hits your ship!",
     [("Cover", -8, -3, 5), ("Shield", -18, 0, 8),
      ("Fly through", -2, -2, -20)])
]


class MarsGame:
    def __init__(self, root):
        self.root = root
        root.title("Space Mission Simulator - Reach Mars")
        root.geometry("650x680")
        root.configure(bg=BG)

        tk.Label(root, text="🚀 SPACE MISSION: REACH MARS",
                 font=("Arial", 17, "bold"),
                 bg=BG, fg=WHITE).pack(pady=8)

        self.scene = tk.Canvas(root, width=610, height=230,
                               bg=BG, highlightthickness=0)
        self.scene.pack()

        self.stars = [(random.randint(0, 610),
                       random.randint(0, 230))
                      for _ in range(55)]

        self.bars = {}
        for name in ("Fuel", "Oxygen", "Hull", "Progress"):
            row = tk.Frame(root, bg=BG)
            row.pack(fill="x", padx=25, pady=2)
            tk.Label(row, text=name, width=9, anchor="w",
                     bg=BG, fg=WHITE).pack(side="left")
            bar = ttk.Progressbar(row, maximum=100)
            bar.pack(side="left", fill="x", expand=True)
            self.bars[name] = bar

        self.status = tk.Label(root, bg=BG, fg=TEAL,
                               font=("Arial", 11, "bold"))
        self.status.pack(pady=5)

        self.desc = tk.Label(root, bg=BG, fg=WHITE,
                             wraplength=580, font=("Arial", 11))
        self.desc.pack(pady=5)

        self.choices = tk.Frame(root, bg=BG)
        self.choices.pack(fill="x", padx=75)

        self.log = tk.Label(root, bg=BG, fg=TEAL,
                            wraplength=580)
        self.log.pack(pady=5)

        tk.Button(root, text="↻ RESTART MISSION",
                  command=self.restart, bg="#24486a",
                  fg=WHITE, relief="flat").pack(pady=5)

        self.restart()
        self.animate()

    def restart(self):
        if hasattr(self, "timer_id"):
            self.root.after_cancel(self.timer_id)

        self.data = {"Fuel": 100, "Oxygen": 100,
                     "Hull": 100, "Progress": 0}
        self.seconds = 50
        self.turn = 0
        self.over = False
        self.log.config(text="Choose wisely to reach Mars!")
        self.new_event()
        self.update_board()
        self.timer_id = self.root.after(1000, self.tick)

    def update_board(self):
        for name, bar in self.bars.items():
            bar["value"] = self.data[name]
        self.status.config(
            text=f"TIME: {self.seconds}s     EVENT: {self.turn}")

    def new_event(self):
        if self.over:
            return

        self.turn += 1
        for w in self.choices.winfo_children():
            w.destroy()

        title, message, options = random.choice(EVENTS)
        self.desc.config(text=f"{title} — {message}")

        for name, fuel, oxygen, hull in options:
            tk.Button(
                self.choices, text=name,
                command=lambda a=(name, fuel, oxygen, hull):
                    self.choose(a),
                bg="#183554", fg=WHITE,
                relief="flat", pady=5
            ).pack(fill="x", pady=2)

    def choose(self, choice):
        if self.over:
            return

        name, fuel, oxygen, hull = choice
        self.data["Fuel"] += fuel
        self.data["Oxygen"] += oxygen
        self.data["Hull"] += hull
        self.data["Progress"] += random.randint(12, 18)

        result = f"You chose: {name}."

        if random.random() < 0.25:
            damage = random.randint(5, 15)
            self.data["Hull"] -= damage
            result += f" Ship damage: {damage}%!"

        for key in self.data:
            self.data[key] = max(0, min(100, self.data[key]))

        self.log.config(text=result)
        self.update_board()

        if min(self.data[k] for k in ("Fuel", "Oxygen", "Hull")) == 0:
            self.finish("MISSION FAILED: A system has failed!")
        elif self.data["Progress"] >= 100:
            if (self.data["Fuel"] >= 10 and
                    self.data["Oxygen"] >= 10 and
                    self.data["Hull"] >= 25):
                self.finish("SUCCESS! YOU REACHED MARS! 🪐")
            else:
                self.finish("Landing failed: resources too low!")
        else:
            self.new_event()

    def tick(self):
        if self.over:
            return
        self.seconds -= 1
        self.update_board()

        if self.seconds <= 0:
            self.finish("TIME'S UP! Mission failed!")
        else:
            self.timer_id = self.root.after(1000, self.tick)

    def finish(self, message):
        self.over = True
        for w in self.choices.winfo_children():
            w.destroy()
        self.desc.config(text=message)
        self.log.config(text="Press Restart Mission to play again.")
        messagebox.showinfo("Mission Result", message)

    def animate(self):
        c = self.scene
        c.delete("all")

        for i, (x, y) in enumerate(self.stars):
            c.create_oval(x, y, x + 2, y + 2,
                          fill="#8caed8", outline="")
            self.stars[i] = (x - 1 if x > 0 else 610,
                             y if x > 0 else random.randint(0, 230))

        c.create_oval(10, 75, 85, 150, fill="#277ac2", outline="")
        c.create_text(48, 165, text="EARTH", fill=WHITE)
        c.create_oval(525, 75, 600, 150, fill="#c95645", outline="")
        c.create_text(563, 165, text="MARS", fill=WHITE)
        c.create_line(90, 112, 520, 112,
                      fill="#284a70", dash=(4, 5))

        x = 95 + 420 * self.data["Progress"] / 100
        y = 112 + math.sin(self.turn) * 12
        color = "#dce9f8" if self.data["Hull"] > 50 else "#ff657a"

        c.create_polygon(x - 18, y, x - 5, y - 9,
                         x + 18, y, x - 5, y + 9,
                         fill=color, outline=WHITE)
        c.create_oval(x - 2, y - 3, x + 5, y + 3,
                      fill="#55e6cf", outline="")

        c.create_text(305, 25,
                      text=f"JOURNEY: {self.data['Progress']}%",
                      fill=TEAL, font=("Arial", 12, "bold"))

        self.root.after(100, self.animate)


if __name__ == "__main__":
    window = tk.Tk()
    game = MarsGame(window)
    window.mainloop()


