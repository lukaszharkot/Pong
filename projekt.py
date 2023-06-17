import tkinter as tk
import random
from tkinter import messagebox

class ScoreSaver:
    def __init__(self):
        self.file_path = "wyniki.txt"

    def save_score(self, score_a, score_b, difficulty):
        with open(self.file_path, "a") as file:
            file.write(f"{score_a},{score_b},{difficulty}\n")

    def get_previous_results(self):
        results = []
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    score_a, score_b, difficulty = line.strip().split(",")
                    results.append((int(score_a), int(score_b), difficulty))
        except FileNotFoundError:
            pass
        return results
    
class PongGame:
    def __init__(self, master, speed=3):
            self.master = master
            self.master.geometry("800x435")
            self.master.title("Pong")
            # logo_image = tk.PhotoImage(file="logo.png")
            # self.master.iconphoto(True, logo_image)

            self.speed = int(speed)

            self.current_screen = None

            self.score_saver = ScoreSaver()

            self.show_choose_screen()

    def show_choose_screen(self):
        self.clear_screen()
        self.current_screen = ChooseScreen(self.master, self)

    def show_start_screen1(self):
        self.clear_screen()
        self.current_screen = StartScreen1(self.master, self)

    def show_start_screen2(self):
        self.clear_screen()
        self.current_screen = StartScreen2(self.master, self)

    def show_game_screen(self, difficulty, speed = 3):
        self.clear_screen()
        self.current_screen = GameScreen(self.master, self, difficulty, speed)

    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()

class ChooseScreen(tk.Frame):
    def __init__(self, master, pong_game):
        super().__init__(master, width=800, height=400)

        self.canvas = tk.Canvas(self.master, width=600, height=250)
        self.canvas.pack()

        self.background_image = tk.PhotoImage(file="bg.png")
        self.background = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        self.pong_game = pong_game
        self.pack()

        self.start_button = tk.Button(self, text="PvP", command=self.pvp, width=16)
        self.start_button.pack()

        self.start_button = tk.Button(self, text="Komputer", command=self.computer, width=16)
        self.start_button.pack()

        self.results_button = tk.Button(self, text="Poprzednie Wyniki", command=self.show_previous_results, width=16)
        self.results_button.pack()

        self.quit_button = tk.Button(self, text="Wyjdź", command=self.quit, width=16)
        self.quit_button.pack()

        self.score_saver = ScoreSaver()

    def show_previous_results(self):
        results = self.score_saver.get_previous_results()

        if len(results) == 0:
            messagebox.showinfo("Poprzednie Wyniki", "Brak poprzednich wyników.")
        else:
            result_str = "Poprzednie Wyniki:\nNumer Gry / Wynik Gracza 1 - Wynik Gracza 2 / Trudność\n"
            for i, result in enumerate(results, start=1):
                result_str += f"Gra {i}: {result[0]} - {result[1]} (Poziom trudności: {result[2]})\n"
            messagebox.showinfo("Poprzednie Wyniki", result_str)

    def computer(self):
        self.canvas.destroy()
        self.pong_game.show_start_screen1()

    def pvp(self):
        self.canvas.destroy()
        self.pong_game.show_start_screen2()



class StartScreen1(tk.Frame):
    def __init__(self, master, pong_game):
        super().__init__(master, width=800, height=400)

        self.canvas = tk.Canvas(self.master, width=600, height=210)
        self.canvas.pack()

        self.background_image = tk.PhotoImage(file="bg1.png")
        self.background = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        self.pong_game = pong_game
        self.pack()

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Łatwy")

        self.difficulty_label = tk.Label(self, text="Wybierz poziom trudności:")
        self.difficulty_label.pack()

        self.easy_radio = tk.Radiobutton(self, text="Łatwy", variable=self.difficulty_var, value="Łatwy")
        self.easy_radio.pack(anchor="w")

        self.medium_radio = tk.Radiobutton(self, text="Średni", variable=self.difficulty_var, value="Średni")
        self.medium_radio.pack(anchor="w")

        self.hard_radio = tk.Radiobutton(self, text="Trudny", variable=self.difficulty_var, value="Trudny")
        self.hard_radio.pack(anchor="w")

        self.start_button = tk.Button(self, text="Start", command=self.start_game, width=6)
        self.start_button.pack()

        self.back_button = tk.Button(self, text="Powrót", command=self.go_back, width=6)
        self.back_button.pack()

    def start_game(self):
        self.pong_game.difficulty = self.difficulty_var.get()
        print(self.pong_game.difficulty)
        self.canvas.destroy()
        self.pong_game.show_game_screen(self.pong_game.difficulty)

    def go_back(self):
        self.canvas.destroy()
        self.pong_game.show_choose_screen()

class StartScreen2(tk.Frame):
    def __init__(self, master, pong_game):
        super().__init__(master, width=800, height=400)

        self.canvas = tk.Canvas(self.master, width=600, height=240)
        self.canvas.pack()

        self.background_image = tk.PhotoImage(file="bg2.png")
        self.background = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        self.pong_game = pong_game
        self.pack()

        self.speed_var = tk.StringVar()
        self.speed_var.set("3")

        self.speed_label = tk.Label(self, text="Wybierz prędkość piłki:")
        self.speed_label.pack()

        self.speed_scale = tk.Scale(self, from_= 1, to= 7, orient="horizontal", variable=self.speed_var)
        self.speed_scale.pack()

        self.start_button = tk.Button(self, text="Start", command=self.start_game, width=6)
        self.start_button.pack()

        self.back_button = tk.Button(self, text="Powrót", command=self.go_back, width=6)
        self.back_button.pack()

    def start_game(self):
        self.pong_game.speed = self.speed_var.get()
        print(self.pong_game.speed)
        self.canvas.destroy()
        self.pong_game.show_game_screen("Na siebie", self.pong_game.speed)

    def go_back(self):
        self.canvas.destroy()
        self.pong_game.show_choose_screen()

class GameScreen(tk.Frame):
    def __init__(self, master, pong_game, difficulty = "Na siebie", speed = 3):  # Dodać argument difficulty
        super().__init__(master, width=800, height=400)
        
        self.canvas = tk.Canvas(self.master, width=800, height=400)
        self.canvas.pack()

        self.pong_game = pong_game
        self.pack()

        self.create_background()

        self.direction = random.choice([-1, 1])
        self.bdirection = 1
        self.speed_x = int(speed)
        self.speed_y = int(speed)

        self.score_a = 0
        self.score_b = 0
        self.scoreboard = self.canvas.create_text(400, 50, text="0 : 0", fill="white", font=("Arial", 30))

        # self.menu_frame = tk.Frame(self.master)
        # self.menu_frame.pack()

        self.start_button = tk.Button(self, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)

        self.go_back_button = tk.Button(self, text="Powrót", command=self.go_back)
        self.go_back_button.pack(side=tk.RIGHT)

        self.reset_button = tk.Button(self, text="Reset", command=self.reset_game)
        self.reset_button.pack()

        self.score_saver = ScoreSaver()

        self.poziom = difficulty
        self.difficulty = tk.StringVar(value=self.poziom)

        self.create_objects()

    def create_background(self):
        self.background_image = tk.PhotoImage(file="tlo.png")
        self.background = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

    def create_objects(self):
        self.ball = self.canvas.create_oval(395, 195, 405, 205, fill="white", outline="black", width=1)
        self.paddle_a = self.canvas.create_rectangle(10, 150, 30, 250, fill="blue", outline="black", width=1)
        self.paddle_b = self.canvas.create_rectangle(770, 150, 790, 250, fill="red", outline="black", width=1)

    def bind_events(self):
        if self.poziom == "Na siebie":
            self.canvas.bind_all("<KeyPress-Up>", self.move_paddle_a_up)
            self.canvas.bind_all("<KeyPress-Down>", self.move_paddle_a_down)
            self.canvas.bind_all("<w>", self.move_paddle_b_up)
            self.canvas.bind_all("<s>", self.move_paddle_b_down)
            self.canvas.bind_all("<W>", self.move_paddle_b_up)
            self.canvas.bind_all("<S>", self.move_paddle_b_down)
        else:
            self.canvas.bind_all("<KeyPress-Up>", self.move_paddle_a_up)
            self.canvas.bind_all("<KeyPress-Down>", self.move_paddle_a_down)

    def go_back(self):
        self.stop_game()  # Zatrzymaj gre
        self.canvas.destroy() #Usuń canve
        if self.poziom == "Na siebie":
            self.pong_game.show_start_screen2()  
        else:
            self.pong_game.show_start_screen1()

    def start_game(self):
        self.bind_events()
        self.start_button.config(state="disabled")
        self.canvas.focus_set()

        self.reset_ball()  # Zresetuj pozycje piłki
        self.move_ball() # Rusz piłkę
        self.move_paddle_b() # Rusz paletkę b (Komputer)

        difficulty = self.difficulty.get()
        if difficulty == "Trudny":
            self.speed_x = 5
            self.speed_y = 5

    def stop_game(self):
        self.canvas.unbind_all("<KeyPress-Up>")
        self.canvas.unbind_all("<KeyPress-Down>")
        self.start_button.config(state="disabled")

        if hasattr(self, 'move_ball_id'):
            self.master.after_cancel(self.move_ball_id)  # Usuń zakolejkowaną metode move_ball
            del self.move_ball_id

        if hasattr(self, 'move_paddle_b_id'):
            self.master.after_cancel(self.move_paddle_b_id)  # Usuń zakolejkowaną metodę move_paddle_b
            del self.move_paddle_b_id

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
            if self.poziom == "Na siebie":
                self.game_over("Gracz 1" if self.score_a == 5 else "Gracz 2")
            else:
                self.game_over("Gracz 1" if self.score_a == 5 else "Komputer")
        else:
            self.move_ball_id = self.master.after(10, self.move_ball)
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

    def move_paddle_b_up(self, event):
        paddle_b_pos = self.canvas.coords(self.paddle_b)
        if paddle_b_pos[1] > 0:
            self.canvas.move(self.paddle_b, 0, -20)

    def move_paddle_b_down(self, event):
        paddle_b_pos = self.canvas.coords(self.paddle_b)
        if paddle_b_pos[3] < 400:
            self.canvas.move(self.paddle_b, 0, 20)

    def move_paddle_b(self):
        if self.is_game_over():
            return
        
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

        self.move_paddle_b_id = self.master.after(10, self.move_paddle_b) 

    def update_scoreboard(self):
        self.canvas.itemconfig(self.scoreboard, text=f"{self.score_a} : {self.score_b}")

    def game_over(self, winner):
        if self.poziom == "Na siebie":
            self.canvas.unbind_all("<KeyPress-Up>")
            self.canvas.unbind_all("<KeyPress-Down>")
            self.canvas.unbind_all("<w>")
            self.canvas.unbind_all("<s>")
            self.canvas.unbind_all("<W>")
            self.canvas.unbind_all("<S>")
        else:
            self.canvas.unbind_all("<KeyPress-Up>")
            self.canvas.unbind_all("<KeyPress-Down>")

        self.canvas.create_text(400, 350, text=f"{winner} wygrywa!", fill="white", font=("Arial", 30))

        self.start_button.config(state="disabled")

        self.score_saver.save_score(self.score_a, self.score_b, self.poziom)
    
    def reset_game(self):
        self.canvas.delete("all")
        self.create_background()
        self.create_objects()
        self.bind_events()
        self.stop_game()
        self.start_button.config(state="normal")

        self.direction = random.choice([-1, 1])
        self.score_a = 0
        self.score_b = 0
        self.scoreboard = self.canvas.create_text(400, 50, text="0 : 0", fill="white", font=("Arial", 30)) 
        self.update_scoreboard()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pong")
    logo_image = tk.PhotoImage(file="logo.png")
    root.iconphoto(True, logo_image)
    game = PongGame(root)
    root.mainloop()