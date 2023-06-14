import tkinter as tk
import random

class PongGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=800, height=400, bg="black")
        self.canvas.pack()

        self.direction = random.choice([-1, 1])
        self.bdirection = 1
        self.speed_x = 3
        self.speed_y = 3

        self.score_a = 0
        self.score_b = 0
        self.scoreboard = self.canvas.create_text(400, 50, text="0 : 0", fill="white", font=("Arial", 20))
        self.game_status = self.canvas.create_text(400, 100, text="", fill="white", font=("Arial", 20))

        self.difficulty = tk.StringVar(value="Łatwy")

        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack()

        self.difficulty_label = tk.Label(self.menu_frame, text="Poziom trudności:")
        self.difficulty_label.pack()

        self.start_button = tk.Button(self.menu_frame, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.menu_frame, text="Reset", command=self.reset_game)
        self.reset_button.pack(side=tk.RIGHT)

        self.difficulty_menu = tk.OptionMenu(self.menu_frame, self.difficulty, "Łatwy", "Średni", "Trudny")
        self.difficulty_menu.pack()

        self.create_objects()

    def create_objects(self):
        self.ball = self.canvas.create_oval(395, 195, 405, 205, fill="white")
        self.paddle_a = self.canvas.create_rectangle(10, 150, 30, 250, fill="blue", outline="white", width=4)
        self.paddle_b = self.canvas.create_rectangle(770, 150, 790, 250, fill="red", outline="white", width=4)

    def bind_events(self):
        self.canvas.bind_all("<KeyPress-Up>", self.move_paddle_a_up)
        self.canvas.bind_all("<KeyPress-Down>", self.move_paddle_a_down)

    def start_game(self):
        self.bind_events()
        self.difficulty_menu.config(state="disabled")
        self.start_button.config(state="disabled")
        self.canvas.focus_set()

        self.reset_ball()  # Zresetuj pozycje piłki
        self.move_ball()
        self.move_paddle_b()

        difficulty = self.difficulty.get()
        if difficulty == "Trudny":
            self.speed_x = 5
            self.speed_y = 5
        else:
            self.speed_x = 3
            self.speed_y = 3
    
    def stop_game(self):
        self.canvas.unbind_all("<KeyPress-Up>")
        self.canvas.unbind_all("<KeyPress-Down>")
        self.difficulty_menu.config(state="normal")
        self.start_button.config(state="disabled")

    def is_game_over(self):
        return self.score_a == 5 or self.score_b == 5

    def move_ball(self):
        # Jeśli gra się skończyła, przestań poruszać piłką
        if self.is_game_over():
            return

        ball_pos = self.canvas.coords(self.ball)
        paddle_a_pos = self.canvas.coords(self.paddle_a)
        paddle_b_pos = self.canvas.coords(self.paddle_b)

        # Sprawdź kolizję z górnym i dolnym brzegiem planszy
        if ball_pos[3] >= 400 or ball_pos[1] <= 0:
            self.speed_y *= -1

        # Sprawdź kolizję z paletką A
        if ball_pos[0] <= paddle_a_pos[2] and (self.speed_x * self.direction) < 0:
            if ball_pos[3] >= paddle_a_pos[1] and ball_pos[1] <= paddle_a_pos[3]:
                self.speed_x *= -1

        # Sprawdź kolizję z paletką B
        if ball_pos[2] >= paddle_b_pos[0] and (self.speed_x * self.direction) > 0:
            if ball_pos[3] >= paddle_b_pos[1] and ball_pos[1] <= paddle_b_pos[3]:
                self.speed_x *= -1

        # Jeśli piłka dotknie prawej krawędzi planszy
        if ball_pos[2] >= 800:
            self.score_a += 1
            self.reset_ball()
        # Jeśli piłka dotknie lewej krawędzi planszy
        elif ball_pos[0] <= 0:
            self.score_b += 1
            self.reset_ball()

        self.update_scoreboard()

        if self.is_game_over():
            self.game_over("Gracz 1" if self.score_a == 5 else "Komputer")
        else:
            self.master.after(10, self.move_ball)
            self.canvas.move(self.ball, self.speed_x * self.direction, self.speed_y)

    def reset_ball(self):
        # Jeśli gra się skończyła, zatrzymaj piłkę
        if self.is_game_over():
            return

        self.direction = random.choice([-1, 1])
        ball_pos = self.canvas.coords(self.ball)
        ball_width = ball_pos[2] - ball_pos[0]
        ball_height = ball_pos[3] - ball_pos[1]
        self.canvas.move(self.ball, 400 - ball_width/2 - ball_pos[0], 200 - ball_height/2 - ball_pos[1])

        difficulty = self.difficulty.get()
        if difficulty == "Trudny":
            self.speed_x = 5
            self.speed_y = 5
        else:
            self.speed_x = 3
            self.speed_y = 3

        if self.is_game_over():
            self.stop_game()  # Zatrzymaj grę, jeśli piłka została zresetowana po zakończeniu gry

    def move_paddle_a_up(self, event):
        paddle_a_pos = self.canvas.coords(self.paddle_a)
        if paddle_a_pos[1] > 0:
            self.canvas.move(self.paddle_a, 0, -20)

    def move_paddle_a_down(self, event):
        paddle_a_pos = self.canvas.coords(self.paddle_a)
        if paddle_a_pos[3] < 400:
            self.canvas.move(self.paddle_a, 0, 20)

    def move_paddle_b(self):
        difficulty = self.difficulty.get()
        paddle_b_pos = self.canvas.coords(self.paddle_b)

        if difficulty == "Łatwy":
            if not self.is_game_over():
                if paddle_b_pos[3] >= 400:
                    self.bdirection = -1
                elif paddle_b_pos[1] <= 0:
                    self.bdirection = 1
                self.canvas.move(self.paddle_b, 0, self.bdirection)

        elif difficulty == "Średni":
            # Przeciwnik (paletka B) podąża za piłką
            ball_pos = self.canvas.coords(self.ball)
            if ball_pos[1] < paddle_b_pos[1]:
                self.canvas.move(self.paddle_b, 0, -1)
            elif ball_pos[3] > paddle_b_pos[3]:
                self.canvas.move(self.paddle_b, 0, 1)

        elif difficulty == "Trudny":
            # Przeciwnik (paletka B) podąża za piłką ze zwiększoną prędkością
            ball_pos = self.canvas.coords(self.ball)
            if ball_pos[1] < paddle_b_pos[1]:
                self.canvas.move(self.paddle_b, 0, -2)
            elif ball_pos[3] > paddle_b_pos[3]:
                self.canvas.move(self.paddle_b, 0, 2)

        self.master.after(10, self.move_paddle_b)

    def update_scoreboard(self):
        self.canvas.itemconfig(self.scoreboard, text=f"{self.score_a} : {self.score_b}")

    def game_over(self, winner):
        self.canvas.unbind_all("<KeyPress-Up>")
        self.canvas.unbind_all("<KeyPress-Down>")

        self.canvas.create_text(400, 350, text=f"{winner} wygrywa!", fill="white", font=("Arial", 30))

        self.difficulty_menu.config(state="normal")
        self.start_button.config(state="disabled")

    def reset_game(self):
        self.canvas.delete("all")
        self.create_objects()
        self.bind_events()
        self.start_button.config(state="normal")

        self.direction = random.choice([-1, 1])
        difficulty = self.difficulty.get()
        if difficulty == "Trudny":
            self.speed_x = 5
            self.speed_y = 5
        else:
            self.speed_x = 3
            self.speed_y = 3

        self.score_a = 0
        self.score_b = 0
        self.scoreboard = self.canvas.create_text(400, 50, text="0 : 0", fill="white", font=("Arial", 20))  # Odtwórz tablicę wyników
        self.update_scoreboard()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pong")
    logo_image = tk.PhotoImage(file="logo.png")
    root.iconphoto(True, logo_image)
    game = PongGame(root)
    root.mainloop()