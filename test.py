def move(grid, rows, x, y):
    def get_neighbors(xv, yv):
        nhb = 0

        for i in range(3):
            for j in range(3):
                a1 = (xv - 1) + i
                a2 = (yv - 1) + j

                if -1 < a1 < len(grid) and -1 < a2 < len(grid):
                    if grid[a1][a2]:
                        nhb += 1

        return nhb

    return get_neighbors(x, y)


grid = [
    [False, True, False],
    [False, False, False],
    [False, False, False]
]

for i in range(3):
    for j in range(3):
        print(move(grid, 3, i, j), end='\t')
    print()
