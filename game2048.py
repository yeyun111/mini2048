from numpy import random, array, zeros, append, sum, concatenate, copy, ndenumerate, isnan, rot90, nan, int, float
DOWN, RIGHT, UP, LEFT = range(4)

class Game2048:
    def __init__(self):
        self._grid, self._score = zeros(16) + nan, 0
        self._grid[random.choice(16, 2, replace=False)] = random.choice([2]*9+[4], 2, replace=False) # init with 2 tiles
        self._grid = self._grid.reshape((4, 4))  # create 4x4 grid

    @staticmethod
    def _merge_down(grid):
        merge = concatenate((grid, [zeros(4) + nan])) - concatenate(([zeros(4) + nan], grid))  # find the mergable tiles
        merge[2][merge[3]==0], merge[1][merge[2]==0] = nan, nan     # remove redundant 0 by 3 same tiles
        score = sum(grid[merge[:4] == 0])
        grid[merge[:4] == 0], grid[merge[1:] == 0] = grid[merge[:4] == 0] * 2, nan # fill the merged  with new number
        return score

    def _create_tiles(self):
        avail = isnan(self._grid)
        if avail[avail==True].size > 0:
            new_tiles = append(random.choice([20]*9+[40]), zeros(avail[avail==True].size - 1) + nan)
            random.shuffle(new_tiles)
            self._grid[avail] = new_tiles

    def step(self, direction):
        self._grid[self._grid%10==0] /= 10
        merge_v, merge_h, grid_copy = copy(self._grid), copy(rot90(self._grid)), copy(self._grid)
        map(Game2048._merge_down, [merge_v, merge_h])       # try to merge tiles along two directions
        if merge_v[isnan(merge_v)].size is 0 and merge_h[isnan(merge_h)].size is 0:         # Check if game is over
            return False
        self._grid = rot90(self._grid, RIGHT - direction)
        self._grid = array([concatenate((x[isnan(x)], x[~isnan(x)])) for x in self._grid])  # move tiles
        self._grid = rot90(self._grid, -1)
        self._score += Game2048._merge_down(self._grid)                                     # merge tiles
        self._grid = rot90(self._grid, 1)
        self._grid = array([concatenate((x[isnan(x)], x[~isnan(x)])) for x in self._grid])  # move tiles
        self._grid = rot90(self._grid, direction - RIGHT)
        if not ((self._grid == grid_copy) | (isnan(self._grid) & isnan(grid_copy))).all():
            self._create_tiles()
        return True

    def get_grid(self):
        grid = copy(self._grid)
        grid[grid%10==0] /= 10
        return grid

    def get_new_tiles(self):
        grid = zeros((4, 4), int)
        grid[self._grid%10==0] = 1
        return grid

    def get_score(self):
        return self._score
