from random import shuffle,randint
from .validate import validate
def generate(template:dict,template_name:str):
    colors = "bw"
    color = randint(0,1)
    while True:
        squares = [(x, y) for x in range(8) for y in range(8)]
        shuffle(squares)
        board = {}
        for piece, count in template.items():
            if color == 1:
                piece = piece.swapcase()
            board[piece] = [squares.pop() for _ in range(count)]
        fen = [["1" for _ in range(8)] for _ in range(8)]
        for piece, positions in board.items():
            for position in positions:
                fen[position[0]][position[1]] = piece
        for row in range(len(fen)):
            fen[row] = "".join(fen[row])
            for i in range(8,0,-1):
                fen[row]  = fen[row].replace("1"*i,f"{i}")
        fen = "/".join(fen)
        if validate(fen, template_name): break
    if "Draw" in template:
        color = (color+1)%2
    return fen+f" {colors[color]} - - 0 1"