import tkinter as tk
import random

WIDTH = 400
HEIGHT = 400
DELAY = 100
SNAKE_SIZE = 10

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.score = tk.Label(self, text="Score: 0")
        self.score.pack()
        self.snake = [(WIDTH/2, HEIGHT/2)]
        self.direction = "Up"
        self.food = self.create_food()
        self.bind("<Key>", self.on_key_press)
        self.game_loop()

    def create_food(self):
        x = random.randint(0, WIDTH/SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, HEIGHT/SNAKE_SIZE) * SNAKE_SIZE
        self.canvas.create_oval(x, y, x+SNAKE_SIZE, y+SNAKE_SIZE, fill="red")
        return (x, y)

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x+SNAKE_SIZE, y+SNAKE_SIZE, fill="green", tags="snake")

    def move_snake(self):
        x, y = self.snake[0]
        if self.direction == "Up":
            y -= SNAKE_SIZE
        elif self.direction == "Down":
            y += SNAKE_SIZE
        elif self.direction == "Left":
            x -= SNAKE_SIZE
        elif self.direction == "Right":
            x += SNAKE_SIZE

        self.snake.insert(0, (x, y))

        if self.check_collision():
            self.game_over()
            return

        if self.check_food_collision():
            self.score["text"] = "Score: {}".format(int(self.score["text"].split(":")[1]) + 1)
            self.food = self.create_food()
        else:
            self.snake.pop()

        self.draw_snake()

    def check_collision(self):
        x, y = self.snake[0]
        return (
            x < 0 or
            x >= WIDTH or
            y < 0 or
            y >= HEIGHT or
            len(set(self.snake)) != len(self.snake)
        )

    def check_food_collision(self):
        return self.snake[0] == self.food

    def on_key_press(self, event):
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"

    def game_loop(self):
        self.move_snake()
        if not self.check_collision():
            self.after(DELAY, self.game_loop)

    def game_over(self):
        self.canvas.create_text(
            WIDTH/2, HEIGHT/2,
            text="Game Over",
            font=("Helvetica", 24),
            fill="red"
        )

if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
