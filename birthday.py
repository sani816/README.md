import tkinter as tk
import random
import pygame
import threading

class BirthdayCard:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.title("Happy Birthday!")
        self.root.configure(bg="black")

        # Play music in background
        threading.Thread(target=self.play_music, daemon=True).start()

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.confetti = []
        self.create_confetti()

        # Happy Birthday Text
        self.text = self.canvas.create_text(
            self.root.winfo_screenwidth() // 2,
            80,
            text="🎉 Happy Birthday 🎉",
            font=("Comic Sans MS", 48, "bold"),
            fill="deeppink"
        )

        # Cake Drawing
        self.draw_cake()
        self.animate_candles()

        # Cut Cake Button
        self.cut_button = tk.Button(
            self.root, text="Cut the Cake 🎂", font=("Arial", 18),
            command=self.cut_cake, bg="#FF69B4", fg="white", relief="flat"
        )
        self.canvas.create_window(
            self.root.winfo_screenwidth() // 2,
            360,
            window=self.cut_button
        )

        # Surprise Button
        self.surprise_button = tk.Button(
            self.root, text="Click for a Surprise 🎁", font=("Arial", 16),
            command=self.reveal_message, bg="hotpink", fg="white", relief="flat"
        )
        self.canvas.create_window(
            self.root.winfo_screenwidth() // 2,
            800,
            window=self.surprise_button
        )

        self.secret_text = self.canvas.create_text(
            self.root.winfo_screenwidth() // 2,
            600,
            text="",
            font=("Lucida Handwriting", 26, "italic"),
            fill="gold"
        )

        # Exit button
        self.close_button = tk.Button(
            self.root, text="Exit ❌", font=("Arial", 14),
            command=self.root.destroy, bg="red", fg="white", relief="flat"
        )
        self.canvas.create_window(
            self.root.winfo_screenwidth() - 80,
            40,
            window=self.close_button
        )

        self.animate_confetti()

    def play_music(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("Birthday.mp3")
            pygame.mixer.music.play(-1)
        except:
            print("Error: birthday.mp3 not found or failed to play")

    def create_confetti(self):
        colors = ["red", "yellow", "green", "blue", "magenta", "orange", "cyan"]
        for _ in range(100):
            x = random.randint(0, self.root.winfo_screenwidth())
            y = random.randint(0, self.root.winfo_screenheight())
            size = random.randint(5, 10)
            color = random.choice(colors)
            conf = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            self.confetti.append((conf, random.randint(1, 4)))

    def animate_confetti(self):
        for conf, speed in self.confetti:
            self.canvas.move(conf, 0, speed)
            x, y, x2, y2 = self.canvas.coords(conf)
            if y > self.root.winfo_screenheight():
                self.canvas.coords(conf, x, 0, x2, y2 - y)
        self.root.after(50, self.animate_confetti)

    def draw_cake(self):
        self.w = self.root.winfo_screenwidth() // 2
        self.h = 250
        # Cake base
        self.canvas.create_rectangle(self.w - 100, self.h + 100, self.w + 100, self.h + 160, fill="#D2691E", outline="white")
        self.canvas.create_rectangle(self.w - 80, self.h + 40, self.w + 80, self.h + 100, fill="#FFB6C1", outline="white")
        self.canvas.create_rectangle(self.w - 60, self.h - 10, self.w + 60, self.h + 40, fill="#FF69B4", outline="white")

        # Candles
        self.candles = []
        for i in range(-2, 3):
            flame = self.canvas.create_oval(self.w + i*20 - 3, self.h - 20, self.w + i*20 + 3, self.h - 10, fill="orange", outline="")
            self.candles.append(flame)

    def animate_candles(self):
        for flame in self.candles:
            color = random.choice(["orange", "gold", "yellow"])
            self.canvas.itemconfig(flame, fill=color)
        self.root.after(300, self.animate_candles)

    def cut_cake(self):
        # Cake cutting animation
        x = self.w
        line = self.canvas.create_line(x, self.h - 40, x, self.h - 40, fill="white", width=3)
        def animate_cut(y= self.h - 40):
            if y < self.h + 160:
                self.canvas.coords(line, x, self.h - 40, x, y)
                self.root.after(10, lambda: animate_cut(y + 5))
            else:
                self.canvas.itemconfig(self.secret_text, text="Cake is cut! Let's celebrate! 🎊")
        animate_cut()

    def reveal_message(self):
        self.canvas.itemconfig(
            self.secret_text,
            text="Wishing you a magical birthday full of joy, love, and cake! 🎂💖\n"
            ".you are the most important person of my life .\n"
            "i am so lucky to get you.always keep smiling\n"
        )

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = BirthdayCard(root)
    root.mainloop()
