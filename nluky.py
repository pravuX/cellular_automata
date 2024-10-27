from random import randint
import pygame
import copy

grid_width = 1920
grid_height = 1080
grid_dim = 10

grid_cols = grid_width // grid_dim
grid_rows = grid_height // grid_dim
grid = []

# Cooties is NLUKY 72223; Faders is NLUKY 72222; and RainZha is NLUKY 72322
# Life is NLUKY 03323; and Brain is NLUKY 12299
# for more info see https://www.fourmilab.ch/cellab/classic/manual/chap4.html

N = 5  # = 0 for Life
L = 1
U = 2
K = 9  # = 9 For Brain
Y = 9  # = 9 "   "


colors = {
    0: pygame.Color(36, 40, 59),
    1: pygame.Color(247, 118, 142),
    2: pygame.Color(140, 67, 81)
}


def get_colors(state):

    # transition from red to green
    # offset_state = state - 1  # relative to R0 (state - 2 + 1)
    # base_color = pygame.Color(140, 67, 81)
    # base_color.g = int(255 * offset_state / N)
    # return base_color

    # varying shade of base color and
    # more smooth transition between refractory states
    offset_state = N - state  # relative to R0 (state - 2 + 1)
    base_color = pygame.Color(140, 67, 81)
    factor = min(1.0, offset_state * 0.1)
    # Create new color by blending towards black based on factor
    r = base_color.r + base_color.r * factor
    g = base_color.g + base_color.g * factor
    b = base_color.b + base_color.b * factor

    return pygame.Color(int(r), int(g), int(b))


def sum_neighbors(x, y, size=3):
    """For a given x, y position on the grid, return the accumulated states of the
    8-Neighbors. That would be number of on neighbors."""
    start = size // 2
    end = start+1
    result = 0
    for j in range(-start, end):
        for i in range(-start, end):
            if (j == 0 and i == 0):
                continue  # skip itself
            neighbor_state = grid[(x+i) % grid_cols][(y+j) % grid_rows]
            if (neighbor_state == 1):  # sum only "on" cells
                result += neighbor_state
    return result


def next_refractory(current_refractory_state):
    state = current_refractory_state - 2  # origin at 0
    if state == N - 1:  # highest state
        return 0
    return current_refractory_state + 1


def next_state(x, y):
    cell = grid[x][y]
    eight_sum = sum_neighbors(x, y)
    new_state = cell

    if cell == 0:
        if L <= eight_sum <= U:
            new_state = 1
        else:
            new_state = 0
    elif cell == 1:
        if K <= eight_sum <= Y:
            new_state = 1
        else:
            if (N > 0):  # there are refractory states
                new_state = 2
            else:
                new_state = 0
    elif cell >= 2:
        new_state = next_refractory(cell)

    return new_state


def draw_grid(screen):
    for row in range(grid_rows):
        for col in range(grid_cols):
            state = grid[col][row]
            color = get_colors(state) if state >= 2 else colors[state]

            sqr_x = col * grid_dim
            sqr_y = row * grid_dim
            sqr = pygame.Rect(sqr_x, sqr_y, grid_dim, grid_dim)
            pygame.draw.rect(screen, color, sqr)
            # pygame.draw.rect(screen, colors[0], sqr, 1)


def fill(mouse_x, mouse_y):
    col = mouse_x // grid_dim
    row = mouse_y // grid_dim
    grid[col][row] = (grid[col][row] + 1) % (N + 2)  # 0 to N+1


def init_grid():
    for col in range(grid_cols):
        grid.append(list())
        for row in range(grid_rows):
            grid[col].append(randint(0, N+1))


def fill_grid(val=0, r=False):
    for col in range(grid_cols):
        for row in range(grid_rows):
            if r:
                grid[col][row] = randint(0, N+1)
            else:
                grid[col][row] = val


def main():
    global grid

    pygame.init()

    screen = pygame.display.set_mode((grid_width, grid_height))
    clock = pygame.time.Clock()
    running = True
    pause = True
    fps = 1000

    init_grid()

    while running:
        clock.tick(fps)
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False
            if keys[pygame.K_p]:
                pause = not pause
            if keys[pygame.K_r]:
                fill_grid(r=True)
            if keys[pygame.K_c]:
                fill_grid()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_left, _, _ = pygame.mouse.get_pressed()
                if m_left:
                    fill(mouse_x, mouse_y)

        draw_grid(screen)

        pygame.display.flip()

        if pause:
            continue

        new_state = copy.deepcopy(grid)
        for row in range(0, grid_rows):
            for col in range(0, grid_cols):
                new_state[col][row] = next_state(col, row)
        grid = new_state[:]

    # pygame.image.save_extended(screen, "result.png")
    pygame.quit()


if __name__ == "__main__":
    main()
