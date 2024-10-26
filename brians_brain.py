from random import randint
import pygame
import copy

grid_width = 1200
grid_height = 900
grid_dim = 20

grid_cols = grid_width // grid_dim
grid_rows = grid_height // grid_dim
grid = []


colors = {
    0: pygame.Color(36, 40, 59),
    1: pygame.Color(247, 118, 142),
    2: pygame.Color(140, 67, 81)
}


def sum_neighbors(x, y, size):
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
            if (neighbor_state == 1):
                result += neighbor_state
    return result


def next_state(x, y):
    """Determine next state for a given cell"""
    current_state = grid[x][y]
    no_of_neighbors = sum_neighbors(x, y, 3)
    if current_state == 0:
        if (no_of_neighbors == 2):
            return 1
        return 0  # same state
    if current_state == 1:
        return 2
    if current_state == 2:
        return 0


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
    grid[col][row] = 1


def init_grid():
    for col in range(grid_cols):
        grid.append(list())
        for row in range(grid_rows):
            grid[col].append(randint(0, 2))


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

        draw_grid(screen)

        m_left, _, _ = pygame.mouse.get_pressed()
        if m_left:
            fill(mouse_x, mouse_y)

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
