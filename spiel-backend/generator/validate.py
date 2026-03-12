import chess
import chess.syzygy
tablebase = chess.syzygy.open_tablebase("syzygy/")
def dist(a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))
def tb_legal(fen: str):
    board = chess.Board(fen)
    if not board.is_valid():
        return False
    board.push(chess.Move.null())
    illegal = board.is_check()
    board.pop()

    return not illegal
def count_draw_moves(board, tb):
    count = 0

    for move in board.legal_moves:
        board.push(move)
        try:
            if tb.probe_wdl(board) == 0:
                count += 1
        finally:
            board.pop()

    return count

def validate(fen:str,template_name:str):
    if not tb_legal(fen): return False
    match template_name:
        #case "King and Pawn": return await validate_king_pawn(board)
        #case "Ladder Mate": return await validate_rook_mate(board)
        #case "Mate with Rook": return await validate_rook_mate(board)
        #case "Mate with Queen": return await validate_queen_mate(board)
        case "king_and_pawn_draw": return validate_opposition(fen)
    return False

def validate_king_pawn(board:dict) -> bool:
    if "p" in board: return dist(board["p"][0], board["k"][0]) == dist(board["p"][0], board["K"][0])
    if "P" in board: return dist(board["P"][0], board["k"][0]) == dist(board["P"][0], board["K"][0])
    return False
def validate_rook_mate(board:dict) -> bool:
        if "r" in board: return all(k[x] != r[x] for k in board["K"] for r in board["r"] for x in range(len(k)))
        if "R" in board: return all(k[x] != r[x] for k in board["k"] for r in board["R"] for x in range(len(k)))
        return False
def validate_queen_mate(board:dict) -> bool:
    if "Q" in board: return all(k[x] != q[x] and abs(k[0]-q[0])!=abs(k[1]-q[1]) for k in board["K"] for q in board["Q"] for x in range(len(k)))
    return False
def validate_opposition(fen):
    dtz = tablebase.probe_dtz(chess.Board(fen))
    if not dtz and count_draw_moves(chess.Board(fen), tablebase) <= 2:
        return True
    return False