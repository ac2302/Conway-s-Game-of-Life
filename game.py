import pygame

pygame.init()


themes = {
    "nokia": {
        'fg': (0, 0, 0),
        'bg': (50, 100, 50),
        'bo': (50, 100, 50)
    },
    "graph": {
        'fg': (0, 0, 0),
        'bg': (255, 255, 255),
        'bo': (0, 0, 0)
    }
}

colors = themes['nokia']


def new_grid(rows):
    grid = []

    for i in range(rows):
        grid.append([False] * rows)

    return grid


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def move(grid):
    kills = set()
    births = set()

    def get_neighbors(xv, yv):
        nhb = 0

        for i in range(3):
            for j in range(3):
                a1 = (xv - 1) + i
                a2 = (yv - 1) + j

                if (a1, a2) in [(-1, -1), (len(grid), -1), (-1, len(grid)), (len(grid), len(grid))]:
                    pass

                if a1 < 0:
                    a1 = len(grid)-1
                if a1 >= len(grid):
                    a1 = 0

                if a2 < 0:
                    a2 = len(grid)-1
                if a2 >= len(grid):
                    a2 = 0

                if -1 < a1 < len(grid) and -1 < a2 < len(grid):
                    if grid[a1][a2]:
                        nhb += 1

        return nhb

    kill_list = []
    birth_list = []

    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y]:
                neighbors = get_neighbors(x, y) - 1
                # print(neighbors)
                if neighbors < 2 or neighbors > 3:
                    # grid[x][y] = False
                    # print(neighbors)
                    kill_list.append((x, y))
                    kills.add(neighbors)
            else:
                neighbors = get_neighbors(x, y)
                if neighbors == 3 and (x, y) not in birth_list:
                    # print(neighbors, (x, y))
                    birth_list.append((x, y))
                    births.add(neighbors)

    if kill_list:
        for tpl in kill_list:
            x, y = tpl
            grid[x][y] = False

    if birth_list:
        for tpl in birth_list:
            x, y = tpl
            grid[x][y] = True

    # print(bool(kills) or bool(births))
    if not (bool(kills) or bool(births)):
        pygame.display .set_caption("Conway's Game of Life - (Finished)")
        return False

    return True


def draw(win, side, rows, has_border, grid):
    # define gap
    gap = side // rows

    # fill bg
    win.fill(colors.get('bg'))

    # cells
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y]:
                pygame.draw.rect(win, colors.get(
                    'fg'), (x * gap, y * gap, gap, gap))

    # grid
    if has_border:
        for i in range(rows):
            pygame.draw.line(win, colors.get(
                'bo'), (0, i * gap), (side, i * gap))
            for j in range(rows):
                pygame.draw.line(win, colors.get(
                    'bo'), (j * gap, 0), (j * gap, side))

    # update
    pygame.display.update()


def start(side, rows, tps, has_border):
    global colors

    win = pygame.display.set_mode((side, side))
    title = "Conway's Game of Life"
    title_running = ""
    pygame.display.set_caption(
        title + ' ' + title_running + ' ' + f"({tps if (tps != 0) else 'infinite'} TPS)")

    grid = new_grid(rows)
    neighbormap = []
    gap = side // rows

    clock = pygame.time.Clock()
    running = True
    simulating = False
    while running:
        # tick
        if simulating:
            clock.tick(tps)

        # draw
        draw(win, side, rows, has_border, grid)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0] and not simulating:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, side)
                grid[row][col] = True
                # move(grid, neighbormap)
            if pygame.mouse.get_pressed()[2] and not simulating:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, side)
                grid[row][col] = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if simulating:
                        simulating = False
                        # pygame.display.set_caption(
                        #     "Conway's Game of Life (Paused)")
                        title_running = "(Paused)"
                        pygame.display.set_caption(
                            title + ' ' + title_running + ' ' + f"({tps if (tps != 0) else 'infinite'} TPS)")
                    else:
                        simulating = True
                        # pygame.display.set_caption(
                        #     "Conway's Game of Life (Running)")
                        title_running = "(Running)"
                        pygame.display.set_caption(
                            title + ' ' + title_running + ' ' + f"({tps if (tps != 0) else 'infinite'} TPS)")

                if event.key == pygame.K_c:
                    simulating = False
                    grid = new_grid(rows)
                    # pygame.display.set_caption(
                    #     "Conway's Game of Life (Stopped)")
                    title_running = "(Stopped)"
                    pygame.display.set_caption(
                        title + ' ' + title_running + ' ' + f"({tps if (tps != 0) else 'infinite'} TPS)")
                elif event.key == pygame.K_1:
                    colors = themes['nokia']
                elif event.key == pygame.K_2:
                    colors = themes['graph']
                elif event.key == pygame.K_b:
                    has_border = not has_border
                elif (event.key == pygame.K_RIGHT) and not simulating:
                    move(grid)
                elif event.key == pygame.K_UP:
                    tps += 1
                    pygame.display.set_caption(
                        title + ' ' + title_running + ' ' + f"({tps if (tps != 0) else 'infinite'} TPS)")
                elif (event.key == pygame.K_DOWN) and (tps > 0):
                    tps -= 1
                    pygame.display.set_caption(
                        title + ' ' + title_running + ' ' + f"({tps if (tps != 0) else 'infinite'} TPS)")

        # moves
        if simulating:
            simulating = move(grid)

    pygame.quit()
