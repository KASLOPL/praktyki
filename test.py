import AI

def test_best_move_1():
    board = ["X","","O","X","","O","","",""]

    assert AI.MiniMaxAI().get_best_move(board, "X") == 7

def test_best_move_2():
    board = ["X","","O","X","","O","","",""]

    assert AI.MiniMaxAI().get_best_move(board, "O") == 9 or 7

def test_is_board_full_1():
    board = ["X","X","O","X","O","O","O","O","X"]

    assert AI.MiniMaxAI().is_board_full(board)

def test_is_board_full_2():
    board = ["X","X","","X","O","O","O","O","X"]

    assert not AI.MiniMaxAI().is_board_full(board)

def test_get_winner1():
    board = ["X","","O","X","","O","X","",""]

    assert AI.MiniMaxAI().get_winner(board) == "X"

def test_get_winner2():
    board = ["X","","O","X","","O","","","O"]

    assert AI.MiniMaxAI().get_winner(board) == "O"