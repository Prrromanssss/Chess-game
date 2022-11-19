import tkinter as tk

from chess_figures import (BLACK, WHITE, Bishop, Board, King, Knight, Pawn,
                           Queen, Rook)


def print_board(act_fig=None):
    condition = '''(act_fig == (row, col) or board.field[act_fig[0]]
                   [act_fig[1]].can_move(board, act_fig[0],
                   act_fig[1], row, col) or board.field[act_fig[0]]
                   [act_fig[1]].can_attack(board, act_fig[0],
                   act_fig[1], row, col)) or (type(board.field[act_fig[0]]
                   [act_fig[1]]) is Pawn and board.field[act_fig[0]]
                   [act_fig[1]].can_taking_pass(board, act_fig[0],
                   act_fig[1], row, col)) or (type(board.field[act_fig[0]]
                   [act_fig[1]]) is King and (board.can_castling7(row, col) or
                   board.can_castling0(row, col)))
                '''
    canvas.delete('all')
    for row in range(8):
        for col in range(8):
            canvas.create_rectangle(
                col * 95, row * 95, 95 + col * 95, 95 + row * 95,
                fill=(
                    '#856247' if (not col % 2 and not row % 2) or
                                 (col % 2 and row % 2)
                    else '#b5a78c')
                if act_fig and (eval(condition) if act_fig != 'all'else 1)
                else (
                    '#b78763' if (not col % 2 and not row % 2) or
                                 (col % 2 and row % 2)
                    else '#eedab5'),
                outline=(
                    '#856247' if (not col % 2 and not row % 2) or
                                 (col % 2 and row % 2)
                    else '#b5a78c')
                if act_fig and (eval(condition) if act_fig != 'all' else 1)
                else (
                    '#b78763' if (not col % 2 and not row % 2) or
                                 (col % 2 and row % 2)
                    else '#eedab5')
                )


def print_figures(board):
    for row in range(8):
        for col in range(8):
            canvas_field[row][col] = canvas.create_text(
                47 + col * 95, 47 + row * 95,
                fill=(
                    'white' if board.get_piece(row, col).get_color() == WHITE
                    else 'black')
                if board.get_piece(row, col)
                else '',
                text=board.cell(row, col) if board.get_piece(row, col) else '',
                font='Helvetica 70 bold'
                )
            coordinates_to_move[row][col] = (47 + col * 95, 47 + row * 95)


def can_promote():
    if (
        not (type(board.field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]])
             is Pawn and arr_of_two_fig[1][0] in [7, 0])
          ):
        return False
    redraw_canvas('all')
    new_widgets_prom[0] = canvas.create_rectangle(
        0, 190, 761, 570,
        fill='white'
        )
    new_widgets_prom[1] = canvas.create_text(
        380, 270,
        fill='black',
        text='Choose the figure to continue.',
        font='Helvetica 40'
        )
    for figure in range(4):
        new_widgets_prom[figure + 2] = canvas.create_text(
            100 + figure * 190, 380,
            text=['\u265B', '\u265C', '\u265D', '\u265E'][figure],
            fill='black', font='Helvetica 150 bold'
            )
    return True


def promote_pawn(event):
    chars = {
        '\u265C': Rook,
        '\u265E': Knight,
        '\u265D': Bishop,
        '\u265B': Queen
        }
    pos_chars = {
        '\u265B': (range(0, 191), range(190, 571)),
        '\u265C': (range(191, 381), range(190, 571)),
        '\u265D': (range(381, 571), range(190, 571)),
        '\u265E': (range(571, 761), range(190, 571))
        }
    new_figure = None
    for pos in pos_chars:
        if event.x in pos_chars[pos][0] and event.y in pos_chars[pos][1]:
            new_figure = chars[pos]
    if not new_figure:
        return False
    board.field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]] = (
        new_figure(board.field[arr_of_two_fig[1][0]]
                              [arr_of_two_fig[1][1]].get_color())
        )
    canvas.delete(canvas_field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]])
    obj = canvas.create_text(
        *coordinates_to_move[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]],
        fill=(
            'white'
            if board.get_piece(arr_of_two_fig[1][0],
                               arr_of_two_fig[1][1]).get_color() == WHITE
            else
            'black'
            ),
        text=board.cell(arr_of_two_fig[1][0], arr_of_two_fig[1][1]),
        font='Helvetica 70 bold'
            )
    canvas_field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]] = obj
    for widget in new_widgets_prom:
        canvas.delete(widget)
    redraw_canvas()
    arr_of_two_fig.clear()
    return True


def castling(row, col, row1, col1):
    if (col1 not in [2, 6]) or (type(board.field[row][col]) is not King):
        return
    if col1 == 6:
        func = 7
    else:
        func = 0
    color = board.field[row][col].get_color()
    if not eval(f'board.castling{func}()'):
        return False
    canvas.coords(
        canvas_field[row][col],
        *coordinates_to_move[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]]
        )
    canvas.coords(
        canvas_field[0 if color == BLACK else 7][func],
        *coordinates_to_move[0 if color == BLACK else 7]
        [5 if func == 7 else 3]
        )
    canvas_field[row1][col1] = canvas_field[row][col]
    canvas_field[row][col] = None
    # canvas_field[row][col], canvas_field[row1][col1] = None,canvas_field[row][col] # noqa

    canvas_field[0 if color == BLACK else 7][5 if func == 7 else 3] = (
        canvas_field[0 if color == BLACK else 7][-1 if func == 7 else 0])
    canvas_field[0 if color == BLACK else 7][-1 if func == 7 else 0] = None

    # canvas_field[0 if color == BLACK else 7][-1 if func == 7 else 0],\
    #     canvas_field[0 if color == BLACK else 7][5 if func == 7 else 3] = None,\ # noqa
    #     canvas_field[0 if color == BLACK else 7][-1 if func == 7 else 0]
    arr_of_two_fig.clear()
    return True


def redraw_canvas(figure=None):
    print_board(act_fig=figure)
    print_figures(board)
    pass


def main(event):
    global flag_for_action
    flag_for_redraw = True
    if len(list(filter(lambda x: sum(map(lambda z: 1,
                filter(lambda y: type(y) is King, x))),
            board.field))) <= 1:
        return
    if flag_for_action:
        if promote_pawn(event):
            flag_for_action = False
        return
    for row in range(len(coordinates_of_field)):
        for col in range(len(coordinates_of_field[row])):
            if (
                event.x in coordinates_of_field[row][col][0] and
                event.y in coordinates_of_field[row][col][1]
              ):
                arr_of_two_fig.append((row, col))
    if not arr_of_two_fig:
        return
    if board.field[arr_of_two_fig[0][0]][arr_of_two_fig[0][1]] is not None:
        redraw_canvas(arr_of_two_fig[0])
    if board.field[arr_of_two_fig[0][0]][arr_of_two_fig[0][1]] is None:
        arr_of_two_fig.clear()
        return
    if len(arr_of_two_fig) == 2:
        redraw_canvas()
        if (
            board.field[arr_of_two_fig[0][0]][arr_of_two_fig[0][1]] is not None
            and board.field[arr_of_two_fig[1][0]]
                           [arr_of_two_fig[1][1]] is not None
            and board.field[arr_of_two_fig[0][0]]
                           [arr_of_two_fig[0][1]].get_color()
                == board.field[arr_of_two_fig[1][0]]
                              [arr_of_two_fig[1][1]].get_color()
              ):
            arr_of_two_fig[0] = arr_of_two_fig[1]
            redraw_canvas(arr_of_two_fig[0])
            del arr_of_two_fig[-1]
            return
        flag_for_end = False
        if (
            type(board.field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]])
                is King
                ):
            flag_for_end = True
            color = (
                board.field[arr_of_two_fig[1][0]]
                           [arr_of_two_fig[1][1]].get_color()
                )
        if castling(*arr_of_two_fig[0], *arr_of_two_fig[1]):
            return
        if board.move_piece(*arr_of_two_fig[0], *arr_of_two_fig[1]):
            if can_promote():
                flag_for_action, flag_for_redraw = True, False
            if (
                canvas_field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]]
                    is not None
                    ):
                (
                    canvas.delete(canvas_field[arr_of_two_fig[1][0]]
                                  [arr_of_two_fig[1][1]])
                                )
                if flag_for_redraw:
                    redraw_canvas()
            if (
                type(board.field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]])
                is Pawn
                    and arr_of_two_fig[1][1] != arr_of_two_fig[0][1] and
                    canvas_field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]]
                    is None
                   ):
                if flag_for_redraw:
                    redraw_canvas()
                canvas.delete(
                    canvas_field[board.pass_figure[0]][board.pass_figure[1]]
                    )
                canvas_field[board.pass_figure[0]][board.pass_figure[1]] = None
            canvas.coords(
                canvas_field[arr_of_two_fig[0][0]][arr_of_two_fig[0][1]],
                *coordinates_to_move[arr_of_two_fig[1][0]]
                                    [arr_of_two_fig[1][1]]
                )
            if flag_for_end:
                redraw_canvas('all')
                canvas.create_rectangle(0, 190, 760, 570, fill='white')
                canvas.create_text(
                    370, 380,
                    text=f"{'Whites' if color == BLACK else 'Blacks'} won!",
                    fill='black',
                    font='Helvetica 70 bold',
                    justify=tk.CENTER
                )
            canvas_field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]] = (
                canvas_field[arr_of_two_fig[0][0]][arr_of_two_fig[0][1]]
                )
            canvas_field[arr_of_two_fig[0][0]][arr_of_two_fig[0][1]] = None
            # canvas_field[arr_of_two_fig[0][0]][arr_of_two_fig[0][1]], \
            #     canvas_field[arr_of_two_fig[1][0]][arr_of_two_fig[1][1]] = None, \ # noqa
            #     canvas_field[arr_of_two_fig[0][0]][arr_of_two_fig[0][1]]
        if not flag_for_action:
            arr_of_two_fig.clear()


flag_for_action = False
new_widgets_prom = [None] * 6
coordinates_to_move = [[None] * 8 for _ in range(8)]
canvas_field = [[None] * 8 for _ in range(8)]
coordinates_of_field, arr_of_two_fig = [[] * 8 for i in range(8)], []
for i in range(8):
    for j in range(8):
        coordinates_of_field[i].append(
            (range(j * 95 + 1 if j else 0, 96 + j * 95),
             range(i * 95, 96 + i * 95))
            )


if __name__ == '__main__':
    win = tk.Tk()
    win.title('Chess')
    win.iconphoto(False, tk.PhotoImage(file='media/icon.png'))
    win.geometry('761x760+350+0')
    canvas = tk.Canvas(win, width=761, height=760, bd=0, highlightthickness=0)
    board = Board()
    canvas.pack()
    canvas.bind_all("<Button-1>", main)
    print_board()
    print_figures(board)
    win.mainloop()
