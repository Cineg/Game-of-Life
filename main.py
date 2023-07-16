import pygame
import random


class Board:
    def __init__(self, window: pygame.Surface, grid_size: int) -> None:
        self.window = window
        self.window_width = window.get_width()
        self.window_height = window.get_height()
        self.grid_size = grid_size
        self.square_side = self.window_width / grid_size
        self.board = self._create_board()
        self.play = True

    def draw(self):
        self._update_board()
        for row in self.board:
            for cell in row:
                cell.draw()
                cell.update_state()

    def mouse_click(self, coordinates: tuple):
        x, y = coordinates
        x = int(x // self.square_side)
        y = int(y // self.square_side)

        cell = self.board[x][y]
        cell.mouse_click()

    def stop_play(self):
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

    def _update_board(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                neighbour_count = self._get_neighbour_count(row, col)
                cell = self.board[row][col]
                cell.set_next_state(neighbour_count)

    def _get_neighbour_count(self, row, col):
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

    def draw(self, color: tuple = None):
        if color == None:
            color = self._get_color()

        position = self._calculate_position_in_px(self.square_side_size)
        pygame.draw.rect(window, color, position)

    def update_state(self):
        self.is_alive = self.is_alive_next_turn
        self.is_alive_next_turn = None

    def set_next_state(self, neighbour_count: int):
        if self.is_alive:
            if neighbour_count == 3 or neighbour_count == 2:
                self.is_alive_next_turn = True
            else:
                self.is_alive_next_turn = False

        else:
            if neighbour_count == 3:
                self.is_alive_next_turn = True

    def get_state(self) -> bool:
        return self.is_alive

    def mouse_click(self):
        self.is_alive = True
        self.is_alive_next_turn = None

        color = (0, 255, 0)
        self.draw(color)

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
            return (255, 0, 0)
        if self.is_alive == False and self.is_alive_next_turn == True:
            return (0, 0, 255)
        if self.is_alive == True:
            return (0, 0, 0)

        return (255, 255, 255)


def main(window: pygame.surface):
    clock = pygame.time.Clock()
    board = Board(window, 100)

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
            clock.tick(60)
            board.draw()

        pygame.display.update()


if __name__ == "__main__":
    window_size = (800, 800)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Game of Life")

    pygame.init()
    main(window)
    pygame.quit()
