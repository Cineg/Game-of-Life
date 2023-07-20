import pygame
import random


class Board:
    ANIMATION_COUNTDOWN = 4

    def __init__(self, window: pygame.Surface, grid_size: int) -> None:
        self.window = window
        self.window_width = window.get_width()
        self.window_height = window.get_height()
        self.grid_size = grid_size
        self.square_side = self.window_width / grid_size
        self.board = self._create_board()
        self.play = True
        self.animation_countdown = self.ANIMATION_COUNTDOWN

    def draw(self) -> None:
        self._update_board()
        for row in self.board:
            for cell in row:
                cell.draw()
                if self.animation_countdown == self.ANIMATION_COUNTDOWN:
                    cell.update_state()

    def mouse_click(self, coordinates: tuple) -> None:
        x, y = coordinates
        x = int(x // self.square_side)
        y = int(y // self.square_side)

        cell = self.board[x][y]
        cell.mouse_click()
        self.animation_countdown = self.ANIMATION_COUNTDOWN

    def stop_play(self) -> None:
        self.play = False

    # Private
    def _create_board(self) -> list:
        array = []

        for row in range(self.grid_size):
            arr_row = []
            for col in range(self.grid_size):
                if random.randint(0, 20) > 18:
                    state = True
                else:
                    state = False

                arr_row.append(Cell(self.window, row, col, self.square_side, state))

            array.append(arr_row)
        return array

    def _update_board(self) -> None:
        if self.animation_countdown != 0:
            self.animation_countdown -= 1
            return

        self.animation_countdown = self.ANIMATION_COUNTDOWN

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                neighbour_count = self._get_neighbour_count(row, col)
                cell = self.board[row][col]

                ## Get live cell that will live
                if cell.get_state() and (neighbour_count == 3 or neighbour_count == 2):
                    cell.set_next_state(True)

                ## Get dead cell that will be reborn
                elif not cell.get_state() and neighbour_count == 3:
                    cell.set_next_state(True)

                else:
                    cell.set_next_state(False)

    def _get_neighbour_count(self, row, col) -> int:
        neigbour_count = 0
        for r in range(-1, 2):
            if row + r < 0 or row + r == self.grid_size:
                continue

            for c in range(-1, 2):
                if col + c < 0 or col + c == self.grid_size:
                    continue

                if r == 0 and c == 0:
                    continue

                cell = self.board[row + r][col + c]
                if cell.get_state() == True:
                    neigbour_count += 1

        return neigbour_count


class Cell:
    ANIMATION_DURATION = 3

    def __init__(
        self,
        window: pygame.Surface,
        row: int,
        col: int,
        square_side_size: int,
        is_alive: bool,
    ) -> None:
        self.window = window
        self.row = row
        self.column = col
        self.is_alive = is_alive
        self.is_alive_next_turn = None
        self.square_side_size = square_side_size
        self.current_color = self._get_color()
        self.target_color = self._get_color()
        self.animate_cell = False
        self.animation_duration = 0
        self.animation_buffer = None

    def draw(self) -> None:
        if self.animate_cell:
            self._animate_color(self.current_color, self.target_color)

        else:
            position = self._calculate_position_in_px(self.square_side_size)
            pygame.draw.rect(self.window, self.current_color, position)

    def update_state(self) -> None:
        self.is_alive = self.is_alive_next_turn

    def set_next_state(self, next_turn: bool) -> None:
        if not self.animate_cell:
            self.trigger_animation()

        if self.is_alive_next_turn != None:
            self.animation_buffer = self.is_alive
            self.is_alive = self.is_alive_next_turn

        self.target_color = self._get_color()
        self.is_alive_next_turn = next_turn
        self.current_color = self._get_color()

        if self.animation_buffer != None:
            self.is_alive = self.animation_buffer
            self.animation_buffer = None

    def get_state(self) -> bool:
        return self.is_alive

    def mouse_click(self) -> None:
        self.animate_cell = True
        self.animation_duration = self.ANIMATION_DURATION

        self.current_color = (0, 255, 0)
        self.draw()
        self.target_color = self._get_color()

        self.is_alive = True
        self.is_alive_next_turn = None

    def trigger_animation(self) -> None:
        self.animate_cell = True
        self.animation_duration = self.ANIMATION_DURATION

    # Private
    def _calculate_position_in_px(self, square_side_size) -> tuple:
        """
        Returns position as ( start_row, start_column, width, height ).
        """
        row = self.row * square_side_size
        column = self.column * square_side_size

        return (row, column, square_side_size, square_side_size)

    def _get_color(self) -> tuple:
        if self.is_alive == True and self.is_alive_next_turn == False:
            return (242, 82, 46)
        if self.is_alive == False and self.is_alive_next_turn == True:
            return (66, 39, 242)
        if self.is_alive:
            return (242, 184, 75)

        return (13, 13, 13)

    def _animate_color(self, start_color: tuple, target_color: tuple) -> None:
        progress = self.animation_duration / self.ANIMATION_DURATION
        current_color = self._interpolate_color(start_color, target_color, progress)

        position = self._calculate_position_in_px(self.square_side_size)
        pygame.draw.rect(self.window, current_color, position)

        self.animation_duration -= 1
        if self.animation_duration == 0:
            self.animate_cell = False

    def _interpolate_color(self, start_color, end_color, progress) -> tuple:
        r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)
        return r, g, b


def main(window: pygame.surface) -> None:
    clock = pygame.time.Clock()
    board = Board(window, 80)

    is_mouse_pressed = False

    while board.play == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.stop_play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mouse_pressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_pressed = False

        if is_mouse_pressed == True:
            coordinates = pygame.mouse.get_pos()
            board.mouse_click(coordinates)

        else:
            clock.tick(20)
            board.draw()

        pygame.display.flip()


if __name__ == "__main__":
    window_size = (800, 800)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Game of Life")

    pygame.init()
    main(window)
    pygame.quit()
