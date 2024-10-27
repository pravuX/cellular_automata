from random import randint
import pygame
import copy

grid_width = 1200
grid_height = 900
grid_dim = 10

grid_cols = grid_width // grid_dim
grid_rows = grid_height // grid_dim
grid = []


def get_color(neighbors):

    # random stuff that looked good
    base_color = pygame.Color(247, 118, 142)
    h, s, v, a = base_color.hsva

    new_hue = min(h, neighbors * 10)

    base_color.hsva = new_hue, s, v, a
    return base_color

    # varying shade of base color
    # max_neighbors = 9
    # neighbors_complement = max_neighbors - neighbors
    # base_color = pygame.Color(158, 206, 106)
    # factor = min(1.0, neighbors_complement * 0.1)
    # # Create new color by blending towards black based on factor
    # r = base_color.r - base_color.r * factor
    # g = base_color.g - base_color.g * factor
    # b = base_color.b - base_color.b * factor

    # return pygame.Color(int(r), int(g), int(b))


colors = {
    0: pygame.Color(36, 40, 59),
    1: pygame.Color(247, 118, 142),
}


def sum_neighbors(x, y, size, wrap=True):
    """For a given x, y position on the grid, return the accumulated states of the
    8-Neighbors. That would be number of alive neighbors."""
    start = size // 2
    end = start+1
    result = 0
    for j in range(-start, end):
        for i in range(-start, end):
            # if (j == 0 and i == 0):
            #     continue  # skip itself
            if wrap:
                result += grid[(x+i) % grid_cols][(y+j) % grid_rows]
            else:
                if 0 <= (x+i) < grid_cols and 0 <= (y+j) < grid_rows:
                    result += grid[x+i][y+j]
    return result


vote_rule_992 = {  # island
    0:  0,
    1:  0,
    2:  0,
    3:  0,
    4:  0,
    5:  1,
    6:  1,
    7:  1,
    8:  1,
    9:  1,
}

vote_rule_4_over_5 = {  # dying microbe
    0:  0,
    1:  0,
    2:  0,
    3:  0,
    4:  1,
    5:  0,
    6:  1,
    7:  1,
    8:  1,
    9:  1,
}

fredkin = {  # replicator

    0:  0,
    1:  1,
    2:  0,
    3:  1,
    4:  0,
    5:  1,
    6:  0,
    7:  1,
    8:  0,
    9:  1,
}
next_state = fredkin


def draw_grid(screen):
    for row in range(grid_rows):
        for col in range(grid_cols):
            state = grid[col][row]
            color = colors[state] if state == 0 else get_color(
                sum_neighbors(col, row, 3))

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
                nine_sum = sum_neighbors(col, row, 3, wrap=True)
                new_state[col][row] = next_state[nine_sum]
        grid = copy.deepcopy(new_state)

    # pygame.image.save_extended(screen, "result.png")
    pygame.quit()


if __name__ == "__main__":
    main()
