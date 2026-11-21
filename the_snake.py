from random import randint, choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None, border_color=BORDER_COLOR):
        """Инициализирует объект в центре экрана
        с заданным цветом и границы.
        """
        self.position = CENTER_POSITION
        self.body_color = body_color
        self.border_color = border_color

    def draw_cell(self, position):
        """Отрисовывает одну ячейку сетки в указанной позиции."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, self.border_color, rect, 1)

    def draw(self):
        """Отрисовывает объект на экране.

        Вызывает NotImplementedError, если не переопределён.
        """
        raise NotImplementedError(
            'Метод "draw" должен быть реализован в дочерних классах')


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(
            self,
            body_color=APPLE_COLOR,
            border_color=BORDER_COLOR,
            occupied_positions=(
                CENTER_POSITION,
            )):
        """Инициализирует яблоко красным цветом
        и случайной позицией.
        """
        super().__init__(body_color, border_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию яблока
        в пределах игрового поля, гарантируя,
        что она не совпадает с занятыми координатами.
        """
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (x, y)
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на экране,
        используя метод "draw_cell".
        """
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, управляющий логикой
    и отрисовкой змейки.
    """

    def __init__(self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR):
        """Инициализирует змейку:
        цвет, начальную позицию, направление и длину.
        """
        super().__init__(body_color, border_color)
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [CENTER_POSITION]
        self.length = 1

    def draw(self):
        """Отрисовывает все сегменты змейки на экране."""
        for position in self.positions:
            self.draw_cell(position)

    def move(self):
        """Вычисляет новую позицию головы
        и обновляет список сегментов змейки.
        """
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self):
        """Применяет сохранённое направление движения,
        если оно было установлено ранее.

        После применения сбрасывает next_direction в None.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает состояние змейки к начальному.

        Устанавливает случайное направление, сбрасывает позиции и длину.
        """
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.positions = [CENTER_POSITION]
        self.length = 1

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]


def handle_keys(snake):
    """Обрабатывает нажатия клавиатуры
    и определяет следующее направление змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Запускает игровой цикл:
    обрабатывает ввод, обновляет состояние объектов
    и отрисовывает кадр.
    """
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
