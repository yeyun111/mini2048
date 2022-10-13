from tkinter import Tk, Label, Frame, BOTH
from tkinter.font import Font
from game2048 import Game2048, UP, DOWN, LEFT, RIGHT, ndenumerate, copy, isnan

key_map = {'Up': UP, 'Down': DOWN, 'Left': LEFT, 'Right': RIGHT}
color_map = {2: ('#776e65', '#eee4da'), 4: ('#776e65', '#ede0c8'), 8: ('#f9f6f2', '#f2b179'), 16: ('#f9f6f2', '#f2b179'),
             32: ('#f9f6f2', '#f67c5f'), 64: ('#f9f6f2', '#f65e3b'), 128:('#f9f6f2', '#edcf72'), 256: ('#f9f6f2', '#edcc61'),
             512: ('#f9f6f2', '#edc850'), 1024: ('#f9f6f2', '#edc53f'), 2048: ('#f9f6f2', '#edc22e'), 'base': '#ccc0b3'}
color_map.update(dict.fromkeys([2**x for x in range(12, 18)], ('#f9f6f2', '#3c3a32')))

def input_listener(event=None, game=None, tk_root=None, labels=None):
    key = '{}'.format(event.keysym)
    if key in key_map and game and labels and tk_root:
        if game.step(key_map[key]):
            grid, new_tiles, score = game.get_grid(), game.get_new_tiles(), int(game.get_score())
            max_tile = int(grid[~isnan(grid)].max())
            tk_root.title('Move tiles to get {}! Score: {}'.format(2048 if max_tile < 2048 else max_tile * 2, score))
            for (i, j), value in ndenumerate(grid):
                text = '{}'.format('' if isnan(grid[i][j]) else int(grid[i][j]))
                font_color = color_map[32][1] if new_tiles[i][j] else color_map['base'] if isnan(value) else color_map[value][0]
                labels[4*i+j].config(text=text, fg=font_color, bg=color_map['base'] if isnan(value) else color_map[value][1])
        else:
            grid, new_tiles, score = game.get_grid(), game.get_new_tiles(), int(game.get_score())
            max_tile = int(grid[~isnan(grid)].max())
            [labels[i].config(text='' if i < 4 or i > 11 else 'GAMEOVER'[i-4], bg=color_map['base']) for i in xrange(16)]
            tk_root.title('Game Over! Tile acheived: {}, Score: {}'.format(max_tile, score))

if __name__ == '__main__':
    game, root, window_size = Game2048(), Tk(), 360
    root.title('Move tiles to get 2048! Score: 0')
    root.geometry('{0}x{0}+111+111'.format(window_size))
    root.config(background='#bbada0')

    grid, labels = game.get_grid(), []
    for (i, j), value in ndenumerate(grid):
        frame = Frame(root, width=window_size//4-2, height=window_size//4-2)
        font = Font(family='Helvetica', weight='bold', size=window_size//15)
        frame.pack_propagate(0)
        frame.place(x=j*window_size//4+1, y=i*window_size//4+1)
        (text, color) = ('', color_map['base']) if isnan(value) else ('{}'.format(int(value)), color_map[value][0])
        label = Label(frame, text=text, font=font, fg=color, bg=color_map['base'] if isnan(value) else color_map[value][1])
        label.pack(fill=BOTH, expand=True)
        labels.append(label)

    root.bind_all('<Key>', lambda event: input_listener(event, game=game, tk_root=root, labels=labels))
    root.mainloop()
