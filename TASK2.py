def print_board(board):
    print(board[1] + '|' + board[2] + '|' + board[3])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[7] + '|' + board[8] + '|' + board[9])
    print("\n")


def space_is_free(position):
    return board[position] == ' '


def insert_letter(letter, position):
    if space_is_free(position):
        board[position] = letter
        print_board(board)
        if check_draw():
            print("Draw!")
            exit()
        if check_for_win():
            if letter == 'X':
                print("Bot wins!")
                exit()
            else:
                print("Player wins!")
                exit()
    else:
        print("Can't insert there!")
        position = int(input("Please enter new position: "))
        insert_letter(letter, position)


def check_for_win():
    win_conditions = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  
        (1, 5, 9), (3, 5, 7)              
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != ' ':
            return True
    return False


def check_which_mark_won(mark):
    win_conditions = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  
        (1, 5, 9), (3, 5, 7)              
    ]
    for condition in win_conditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            return True
    return False


def check_draw():
    return all(space != ' ' for space in board.values())


def player_move():
    position = int(input("Enter the position for 'O': "))
    insert_letter(player, position)


def comp_move():
    best_score = -float('inf')
    best_move = 0
    for key in board.keys():
        if board[key] == ' ':
            board[key] = bot
            score = minimax(board, 0, False, -float('inf'), float('inf'))
            board[key] = ' '
            if score > best_score:
                best_score = score
                best_move = key

    insert_letter(bot, best_move)


def minimax(board, depth, is_maximizing, alpha, beta):
    if check_which_mark_won(bot):
        return 1
    elif check_which_mark_won(player):
        return -1
    elif check_draw():
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for key in board.keys():
            if board[key] == ' ':
                board[key] = bot
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[key] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for key in board.keys():
            if board[key] == ' ':
                board[key] = player
                eval = minimax(board, depth + 1, True, alpha, beta)
                board[key] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval


board = {1: ' ', 2: ' ', 3: ' ',
         4: ' ', 5: ' ', 6: ' ',
         7: ' ', 8: ' ', 9: ' '}

print_board(board)
print("Computer goes first! Good luck.")
print("Positions are as follow:")
print("1, 2, 3 ")
print("4, 5, 6 ")
print("7, 8, 9 ")
print("\n")

player = 'O'
bot = 'X'

while not check_for_win():
    comp_move()
    if check_for_win():
        break
    if check_draw():
        print("Draw!")
        break
    player_move()
    if check_for_win():
        break
    if check_draw():
        print("Draw!")
        break
