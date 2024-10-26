from random import randint
import pygame

grid_width = 800
grid_height = 600
grid_dim = 10

grid_cols = grid_width // grid_dim
grid_rows = grid_height // grid_dim
grid = []

colors = {
    1: pygame.Color(255, 255, 255),
    0: pygame.Color(0, 0, 0),
}

rule_30 = {
    "111":  0,
    "110":  0,
    "101":  0,
    "100":  1,
    "011":  1,
    "010":  1,
    "001":  1,
    "000":  0,
}

rule_90 = {
    "111":  0,
    "110":  1,
    "101":  0,
    "100":  1,
    "011":  1,
    "010":  0,
    "001":  1,
    "000":  0,
}


rule_110 = {
    "111":  0,
    "110":  1,
    "101":  1,
    "100":  0,
    "011":  1,
    "010":  1,
    "001":  1,
    "000":  0,
}

rule_150 = {
    "111":  1,
    "110":  0,
    "101":  0,
    "100":  1,
    "011":  0,
    "010":  1,
    "001":  1,
    "000":  0,
}


rule_190 = {
    "111":  1,
    "110":  0,
    "101":  1,
    "100":  1,
    "011":  1,
    "010":  1,
    "001":  1,
    "000":  0,
}

rule_182 = {
    "111":  1,
    "110":  0,
    "101":  1,
    "100":  1,

    "011":  0,
    "010":  1,
    "001":  1,
    "000":  0,
}

rule_220 = {
    "111":  1,
    "110":  1,
    "101":  0,
    "100":  1,

    "011":  1,
    "010":  1,
    "001":  0,
    "000":  0,
}

new_state = rule_30


def draw_grid(screen):
    for row in range(grid_rows):
        for col in range(grid_cols):
            state = grid[col][row]
            color = colors[state]
            sqr_x = col * grid_dim
            sqr_y = row * grid_dim
            sqr = pygame.Rect(sqr_x, sqr_y, grid_dim, grid_dim)
            if state == 1:
                n_h, n_s, n_v, n_a = color.hsva
                n_h = row % 360
                n_s = 28.5
                n_v = 96.5
                color.hsva = n_h, n_s, n_v, n_a
                # gray scale
                # color.r = row % 255
                # color.g = row % 255
                # color.b = row % 255
            pygame.draw.rect(screen, color, sqr)
            # if state == 1:
            #     pygame.draw.rect(screen, "black", sqr, 1)


def main():
    global grid

    pygame.init()

    screen = pygame.display.set_mode((grid_width, grid_height))
    clock = pygame.time.Clock()
    running = True
    fps = 1000

    for col in range(grid_cols):
        grid.append(list())
        for row in range(grid_rows):
            # if row == 0:
            #     grid[col].append(randint(0, 1))
            # else:
            #     grid[col].append(0)
            # if (col % (grid_cols // 8) == 0 and col != 0):
            #     grid[col].append(1)
            # else:
            #     grid[col].append(0)

            grid[col].append(0)
    # place only one point on the middle of the first row
    grid[grid_cols // 2][0] = 1

    for row in range(0, grid_rows - 1):
        for col in range(0, grid_cols):
            pattern = ""
            start = col
            end = start + 3
            mid = (start + end - 1) // 2
            # non wrapping
            if (end <= grid_cols):
                for i in range(start, end):
                    pattern += str(grid[i][row])
                if pattern:
                    grid[mid][row+1] = new_state[pattern]
            # wrapping
            # for i in range(start, end):
            #     pattern += str(grid[i % grid_cols][row])
            # if pattern:
            #     grid[mid % grid_cols][row+1] = new_state[pattern]

    while running:
        clock.tick(fps)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False

        draw_grid(screen)

        pygame.display.flip()

    # pygame.image.save_extended(screen, "result.png")
    pygame.quit()


if __name__ == "__main__":
    main()
