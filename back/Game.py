import flet as ft
import time
import random

from flet.core.types import TextAlign


class SnakeGame:
    def __init__(self, container):
        self.container = container
        self.snake_body = []
        self.snake_movement_state = [True, False, False, False]  # Right, Left, Down, Up
        self.food = None
        self.score = 0
        self.score_board = None
        self.game_area = None
        self.outer_container = None
        self.DEFAULT_PIXEL = 40
        self.initialize_game()

    def initialize_game(self):
        # Initialize snake
        left_padding = self.DEFAULT_PIXEL * 6
        top_padding = self.DEFAULT_PIXEL * 4

        for _ in range(3):
            self.snake_body.append(self.create_square(left_padding, top_padding, "white"))
            left_padding -= self.DEFAULT_PIXEL

        # Initialize food
        self.food = self.create_square(self.DEFAULT_PIXEL * 10, self.DEFAULT_PIXEL * 8, "red")

        # Initialize scoreboard
        self.score_board = ft.Text(value=f"Your Score: {self.score}", size=self.DEFAULT_PIXEL * 1.2, opacity=0.5, text_align=TextAlign.CENTER)

        # Create game area
        self.game_area = ft.Container(
            content=ft.Stack(controls=[self.food] + self.snake_body),
            width=self.DEFAULT_PIXEL * 28,
            height=self.DEFAULT_PIXEL * 11,
            bgcolor=ft.colors.BLACK,
            border_radius=10,
            alignment=ft.alignment.center
        )

        # Create outer container
        self.outer_container = ft.Container(
            content=ft.Column([self.score_board, self.game_area], alignment=ft.MainAxisAlignment.CENTER),
            width=self.DEFAULT_PIXEL * 30,
            height=self.DEFAULT_PIXEL * 14,
            bgcolor=ft.colors.CYAN_900,
            border_radius=10,
            alignment=ft.alignment.center
        )

        # Add to container
        self.container.controls.clear()
        self.container.controls.append(self.outer_container)
        self.container.update()

        # Set keyboard listener
        self.container.page.on_keyboard_event = self.on_keyboard

        # Start game loop
        self.run_game()

    def create_square(self, left_padding, top_padding, color):
        return ft.Container(
            width=self.DEFAULT_PIXEL,
            height=self.DEFAULT_PIXEL,
            bgcolor=color,
            left=left_padding,
            top=top_padding
        )

    def on_keyboard(self, e):
        if e.key == "D" and not self.snake_movement_state[1]:
            self.snake_movement_state[:] = [True, False, False, False]
        elif e.key == "A" and not self.snake_movement_state[0]:
            self.snake_movement_state[:] = [False, True, False, False]
        elif e.key == "S" and not self.snake_movement_state[3]:
            self.snake_movement_state[:] = [False, False, True, False]
        elif e.key == "W" and not self.snake_movement_state[2]:
            self.snake_movement_state[:] = [False, False, False, True]

    def run_game(self):
        while True:
            # Check collision with food
            if self.snake_body[0].top == self.food.top and self.snake_body[0].left == self.food.left:
                self.food.top = random.randint(0, 11) * self.DEFAULT_PIXEL
                self.food.left = random.randint(0, 15) * self.DEFAULT_PIXEL

                # Add new segment to the end of the snake
                last_segment = self.snake_body[-1]
                new_segment = self.create_square(last_segment.left, last_segment.top, "white")
                self.snake_body.append(new_segment)
                self.game_area.content.controls.append(new_segment)

                self.score += 1
                self.score_board.value = f"Your Score: {self.score}"

            # Move the snake body
            for x in range(len(self.snake_body) - 1, 0, -1):
                self.snake_body[x].left = self.snake_body[x - 1].left
                self.snake_body[x].top = self.snake_body[x - 1].top

            # Update snake head position
            if self.snake_movement_state[0]:
                self.snake_body[0].left += self.DEFAULT_PIXEL
            elif self.snake_movement_state[1]:
                self.snake_body[0].left -= self.DEFAULT_PIXEL
            elif self.snake_movement_state[2]:
                self.snake_body[0].top += self.DEFAULT_PIXEL
            elif self.snake_movement_state[3]:
                self.snake_body[0].top -= self.DEFAULT_PIXEL

            # Check wall collisions
            if (
                self.snake_body[0].left < 0 or
                self.snake_body[0].top < 0 or
                self.snake_body[0].left >= self.game_area.width or
                self.snake_body[0].top >= self.game_area.height
            ):
                break

            # Check self-collision
            for segment in self.snake_body[1:]:
                if self.snake_body[0].left == segment.left and self.snake_body[0].top == segment.top:
                    # Exit the game loop if the snake collides with itself
                    self.score_board.value = "Game Over!"
                    self.container.update()
                    return

            self.container.update()
            time.sleep(0.25)

        # Game Over
        self.score_board.value = "Game Over!"
        self.container.update()


