from tkinter import Tk, Button, messagebox, font
from functools import partial

aiPlayer = "X"
humanPlayer = "O"
buttonBoard = list()
gameBoard = list(range(9))
root = Tk()
root.title("Tic-Tac-Toe")
fc = 0


def empty_index(board):
    return [i for i in board if type(i) is int]


def winning_combinations(board, player):
    for i in range(0, 9, 3):
        if board[i] == player and board[i + 1] == player and board[i + 2] == player:
            return True
    for i in range(0, 3):
        if board[i] == player and board[i + 3] == player and board[i + 6] == player:
            return True
    if board[0] == player and board[4] == player and board[8] == player:
        return True
    elif board[2] == player and board[4] == player and board[6] == player:
        return True
    else:
        return False


def minimax(newboard, player):
    global fc
    fc += 1
    availablespots = empty_index(newboard)

    if winning_combinations(newboard, humanPlayer):
        return dict(score=-10)
    elif winning_combinations(newboard, aiPlayer):
        return dict(score=10)
    elif len(availablespots) == 0:
        return dict(score=0)

    moves = list()

    for i in range(len(availablespots)):
        move = dict()
        move['index'] = newboard[availablespots[i]]
        newboard[availablespots[i]] = player
        if player == aiPlayer:
            result = minimax(newboard, humanPlayer)
            move['score'] = result['score']
        else:
            result = minimax(newboard, aiPlayer)
            move['score'] = result['score']

        newboard[availablespots[i]] = move['index']
        moves.append(move)

    bestmove = None
    if player == aiPlayer:
        bestscore = -100
        for i in range(len(moves)):
            if moves[i]['score'] > bestscore:
                bestscore = moves[i]['score']
                bestmove = i
    else:
        bestscore = 100
        for i in range(len(moves)):
            if moves[i]['score'] < bestscore:
                bestscore = moves[i]['score']
                bestmove = i

    return moves[bestmove]


def init():
    button = font.Font(family='verdana', size=72, weight='bold')
    for i in range(0, 9):
        buttonBoard.append(Button(root, width=2, font=button, command=partial(buttonpress, i)))

    for i, button in enumerate(buttonBoard):
        button.grid(row=(int(i / 3) + 1), column=(i % 3))


def restart():
    for i in range(0, 9):
        buttonBoard[i].configure(text="")
        gameBoard[i] = i


def buttonpress(num):
    if type(gameBoard[num]) is int:
        buttonBoard[num].configure(text=humanPlayer, activeforeground='Dodger Blue', fg='Dodger Blue')
        gameBoard[num] = humanPlayer

        if winning_combinations(gameBoard, humanPlayer):
            messagebox.showinfo("Human Win", "You Win!")
            restart()

        else:
            aiCounter = minimax(gameBoard, aiPlayer)
            global fc
            print("Calculated", fc, "Times")
            fc = 0
            try:
                buttonBoard[aiCounter['index']].configure(text=aiPlayer, activeforeground='Tomato', fg='Tomato')
                gameBoard[aiCounter['index']] = aiPlayer
            except KeyError:
                messagebox.showerror("Tie", "It's a tie!")
                restart()

            if winning_combinations(gameBoard, aiPlayer):
                messagebox.showerror("AI Win", "You Lose!")
                restart()


init()
root.mainloop()
