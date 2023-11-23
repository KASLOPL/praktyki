import AI

def test_best_move_1():
    board = ["X","","O","X","","O","","",""]

    assert AI.MiniMaxAI().get_best_move(board, "X") == 7

def test_best_move_2():
    board = ["X","","O","X","","O","","",""]

    assert AI.MiniMaxAI().get_best_move(board, "O") == 9