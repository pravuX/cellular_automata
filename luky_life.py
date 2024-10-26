from random import randint
import pygame
import copy

grid_width = 1200
grid_height = 900
grid_dim = 20

grid_cols = grid_width // grid_dim
grid_rows = grid_height // grid_dim
grid = []


def get_refractory_color(refractory_state):
    """Return color intensity based on the number of neighbors."""
    ...
    # base_color = pygame.Color(247, 118, 142)
    # effect = 0.045
    #
    # # Calculate brightness factor
    # factor = min(1.0, neighbors * effect)
    #
    # # Create new color by blending towards black based on factor
    # r = base_color.r - base_color.r * factor
    # g = base_color.g + (255 - base_color.g) * factor  # blend towards white
    # b = base_color.b - base_color.b * factor
    #
    # return pygame.Color(int(r), int(g), int(b))


colors = {
    0: pygame.Color(36, 40, 59),
    1: pygame.Color(247, 118, 142),
    2: pygame.Color(140, 67, 81)
}


def sum_neighbors(x, y, size=3):
    """For a given x, y position on the grid, return the accumulated states of the
    8-Neighbors. That would be number of alive neighbors."""
    start = size // 2
    end = start+1
    result = 0
    for j in range(-start, end):
        for i in range(-start, end):
            if (j == 0 and i == 0):
                continue  # skip itself
            result += grid[(x+i) % grid_cols][(y+j) % grid_rows]
    return result


# Life = 3323
L = 3
U = 3
K = 2
Y = 3


def life_next_state(x, y):
    """Determine next state for a given cell according to the rules of Conway's Game of Life"""
    cell = grid[x][y]
    eight_sum = sum_neighbors(x, y)

    if cell == 0 and L <= eight_sum <= U:
        return 1
    if cell == 1 and not (K <= eight_sum <= Y):
        return 0
    return cell


def draw_grid(screen):
    for row in range(grid_rows):
        for col in range(grid_cols):
            state = grid[col][row]
            color = colors[state]

            sqr_x = col * grid_dim
            sqr_y = row * grid_dim
            sqr = pygame.Rect(sqr_x, sqr_y, grid_dim, grid_dim)
            pygame.draw.rect(screen, color, sqr)
            # pygame.draw.rect(screen, colors[0], sqr, 1)


def fill(mouse_x, mouse_y):
    col = mouse_x // grid_dim
    row = mouse_y // grid_dim
    grid[col][row] = (grid[col][row] + 1) % 2


def init_grid():
    for col in range(grid_cols):
        grid.append(list())
        for row in range(grid_rows):
            grid[col].append(randint(0, 1))


def fill_grid(val=0, r=False):
    for col in range(grid_cols):
        for row in range(grid_rows):
            if r:
                grid[col][row] = randint(0, 1)
            else:
                grid[col][row] = val


def main():
    global grid

    pygame.init()

    screen = pygame.display.set_mode((grid_width, grid_height))
    clock = pygame.time.Clock()
    running = True
    pause = True
    fps = 15

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
                new_state[col][row] = life_next_state(col, row)
        grid = new_state[:]

    # pygame.image.save_extended(screen, "result.png")
    pygame.quit()


if __name__ == "__main__":
    main()