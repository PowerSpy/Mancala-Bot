import sys
from copy import deepcopy

PLAYER_1_PITS = ('A', 'B', 'C', 'D', 'E', 'F')
PLAYER_2_PITS = ('G', 'H', 'I', 'J', 'K', 'L')


OPPOSITE_PIT = {'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K',
                   'F': 'L', 'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D',
                   'K': 'E', 'L': 'F'}


NEXT_PIT = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'L', 'L': 'K', 'K': 'J', 'J': 'I', 'I': 'H', 'H': 'G',
            'G': '2', '2': 'A'}


PIT_LABELS = 'ABCDEF1LKJIHG2'


STARTING_NUMBER_OF_SEEDS = 4  


def main():
    print('''======== Mancala Game ========\n\n\n''')
    input('Press Enter to begin...')

    gameBoard = getNewBoard()
    playerTurn = '1'  

    while True:  
      
        print('\n' * 60)
       
        displayBoard(gameBoard)
        print(playerTurn, type(playerTurn))
        if playerTurn == '2':
            playerMove = bestMove(deepcopy(gameBoard))
            print(f"player2 chose {playerMove}")
        else:
            playerMove = askForPlayerMove(playerTurn, gameBoard)
       
        playerTurn = makeMove(gameBoard, playerTurn, playerMove)

        
        winner = checkForWinner(gameBoard)
        if winner == '1' or winner == '2':
            displayBoard(gameBoard)  
            print('Player ' + winner + ' has won!')
            sys.exit()
        elif winner == 'tie':
            displayBoard(gameBoard)  
            print('There is a tie!')
            sys.exit()


def getNewBoard():
    """Return a dictionary representing a Mancala board in the starting
    state: 4 seeds in each pit and 0 in the stores."""

   
    s = STARTING_NUMBER_OF_SEEDS


    return {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
            'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}


def displayBoard(board):
    """Displays the game board as ASCII-art based on the board
    dictionary."""

    seedAmounts = []
   
    for pit in 'GHIJKL21ABCDEF':
        numSeedsInThisPit = str(board[pit]).rjust(2)
        seedAmounts.append(numSeedsInThisPit)

    print("""
+------+------+--<<<<<-Player 2----+------+------+------+
2      |G     |H     |I     |J     |K     |L     |      1
       |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |
S      |      |      |      |      |      |      |      S
T  {}  +------+------+------+------+------+------+  {}  T
O      |A     |B     |C     |D     |E     |F     |      O
R      |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |      R
E      |      |      |      |      |      |      |      E
+------+------+------+-Player 1->>>>>-----+------+------+

""".format(*seedAmounts))


def askForPlayerMove(playerTurn, board):
    """Asks the player which pit on their side of the board they
    select to sow seeds from. Returns the uppercase letter label of the
    selected pit as a string."""

    while True:  
       
        if playerTurn == '1':
            print('Player 1, choose move: A-F (or QUIT)')
        elif playerTurn == '2':
            print('Player 2, choose move: G-L (or QUIT)')
        response = input('> ').upper().strip()

        
        if response == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        
        if (playerTurn == '1' and response not in PLAYER_1_PITS) or (
            playerTurn == '2' and response not in PLAYER_2_PITS
        ):
            print('Please pick a letter on your side of the board.')
            continue 
        if board.get(response) == 0:
            print('Please pick a non-empty pit.')
            continue  
        return response


def makeMove(board, playerTurn, pit):
    """Modify the board data structure so that the player 1 or 2 in
    turn selected pit as their pit to sow seeds from. Returns either
    '1' or '2' for whose turn it is next."""

    seedsToSow = board[pit]  
    board[pit] = 0  

    while seedsToSow > 0:  
        pit = NEXT_PIT[pit] 
        if (playerTurn == '1' and pit == '2') or (
            playerTurn == '2' and pit == '1'
        ):
            continue  
        board[pit] += 1
        seedsToSow -= 1

   
    if (pit == playerTurn == '1') or (pit == playerTurn == '2'):
        
        return playerTurn

    
    if playerTurn == '1' and pit in PLAYER_1_PITS and board[pit] == 1:
        oppositePit = OPPOSITE_PIT[pit]
        board['1'] += board[oppositePit]
        board[oppositePit] = 0
    elif playerTurn == '2' and pit in PLAYER_2_PITS and board[pit] == 1:
        oppositePit = OPPOSITE_PIT[pit]
        board['2'] += board[oppositePit]
        board[oppositePit] = 0

  
    if playerTurn == '1':
        return '2'
    elif playerTurn == '2':
        return '1'


def checkForWinner(board):

    player1Total = board['A'] + board['B'] + board['C']
    player1Total += board['D'] + board['E'] + board['F']
    player2Total = board['G'] + board['H'] + board['I']
    player2Total += board['J'] + board['K'] + board['L']

    if player1Total == 0:
       
        board['2'] += player2Total
        for pit in PLAYER_2_PITS:
            board[pit] = 0  
    elif player2Total == 0:
        
        board['1'] += player1Total
        for pit in PLAYER_1_PITS:
            board[pit] = 0 
    else:
        return 'no winner' 

   
    if board['1'] > board['2']:
        return '1'
    elif board['2'] > board['1']:
        return '2'
    else:
        return 'tie'

def bestMove(board, playerTurn='2'):
    moves_dict = {}
    initial = board[playerTurn]
    
    # Evaluate each pit that the current player can choose from
    pits = PLAYER_2_PITS if playerTurn == '2' else PLAYER_1_PITS
    for pit in pits:
        board1 = deepcopy(board)
        seedsToSow = board1[pit]  
        if seedsToSow == 0:  # No seeds to sow in this pit, skip it
            continue
        board1[pit] = 0  # Empty the selected pit
        
        # Simulate sowing the seeds
        current_pit = pit
        while seedsToSow > 0:
            current_pit = NEXT_PIT[current_pit]
            # Skip the opponent's store
            if (playerTurn == '1' and current_pit == '2') or (playerTurn == '2' and current_pit == '1'):
                continue
            board1[current_pit] += 1
            seedsToSow -= 1
        
        # Now check if the last seed goes into the player's own store, giving them an extra turn
        if current_pit == playerTurn:
            next_player_turn = playerTurn
        else:
            next_player_turn = '2' if playerTurn == '1' else '1'

        # Evaluate the move for the current player
        best_op_move = ""
        best_op_increase = -1
        op_initial = board1[next_player_turn]
        
        # Evaluate the potential moves of the opponent, to predict their response
        for opponent_pit in PLAYER_1_PITS if next_player_turn == '1' else PLAYER_2_PITS:
            board2 = deepcopy(board1)
            seedsToSow = board2[opponent_pit]
            if seedsToSow == 0:  # No seeds to sow in this pit, skip it
                continue
            board2[opponent_pit] = 0  # Empty the opponent's selected pit

            # Simulate sowing the seeds for the opponent
            current_opponent_pit = opponent_pit
            while seedsToSow > 0:
                current_opponent_pit = NEXT_PIT[current_opponent_pit]
                if (next_player_turn == '1' and current_opponent_pit == '2') or (next_player_turn == '2' and current_opponent_pit == '1'):
                    continue
                board2[current_opponent_pit] += 1
                seedsToSow -= 1
            
            # Evaluate the change in the opponent's score after their move
            diff = board2[next_player_turn] - op_initial
            if diff > best_op_increase:
                best_op_move = opponent_pit
                best_op_increase = diff
        
        # Add more strategic evaluation factors here:
        score = 0
        
        # Factor 1: Maximize own store
        score += board1[playerTurn]
        
        # Factor 2: Minimize opponent's store
        score -= board1[next_player_turn]
        
        # Factor 3: Check if the move leaves the opponent with a bad situation (e.g., forced to move an empty pit)
        # If opponent's pits are empty, they'll have to skip their turn
        if all(board1[pit] == 0 for pit in (PLAYER_1_PITS if next_player_turn == '1' else PLAYER_2_PITS)):
            score += 5  # Reward the player for forcing the opponent into a bad position

        # Factor 4: Ending in your store gives another turn (consider this move as more favorable)
        if current_pit == playerTurn:
            score += 3
        
        # Factor 5: Capture potential - Check if the move leads to capturing seeds from the opponent
        if current_pit in PLAYER_1_PITS if playerTurn == '1' else PLAYER_2_PITS and board1[current_pit] == 1:
            oppositePit = OPPOSITE_PIT.get(current_pit)
            if oppositePit and board1[oppositePit] > 0:
                score += board1[oppositePit]  # Reward capturing seeds
                board1[oppositePit] = 0
        
        moves_dict[pit] = score

    # Find the pit that gives the best score
    best_move = max(moves_dict, key=moves_dict.get)
    print(f"Best move for Player {playerTurn}: {best_move} (Score: {moves_dict[best_move]})")
    return best_move
# def bestMove(board, playerTurn = '2'):
#     moves_dict = {}
#     initial = board[playerTurn]
#     initial_player = playerTurn
#     for pit in ["G", "H", "I", "J", "K", "L"]:
#         start_pit = pit
#         board1 = deepcopy(board)
#         seedsToSow = board1[pit]  
#         board1[pit] = 0  

#         while seedsToSow > 0:  
#             pit = NEXT_PIT[pit] 
#             if (playerTurn == '1' and pit == '2') or (
#                 playerTurn == '2' and pit == '1'
#             ):
#                 continue  
#             board1[pit] += 1
#             seedsToSow -= 1


        
#         if playerTurn == '1' and pit in PLAYER_1_PITS and board1[pit] == 1:
#             oppositePit = OPPOSITE_PIT[pit]
#             board1['1'] += board1[oppositePit]
#             board1[oppositePit] = 0
#         elif playerTurn == '2' and pit in PLAYER_2_PITS and board1[pit] == 1:
#             oppositePit = OPPOSITE_PIT[pit]
#             board1['2'] += board1[oppositePit]
#             board1[oppositePit] = 0


#         if playerTurn == '1':
#             playerTurn = '2'
#         else:
#             playerTurn = '1'
#         best_op_move = ""
#         best_op_increase = -1
#         op_initial = board1[playerTurn]
#         for p in ["A", "B", "C", "D", "E", "F"]:
#             board2 = deepcopy(board1)
#             seedsToSow = board2[p]  
#             board2[p] = 0  

#             while seedsToSow > 0:  
#                 p = NEXT_PIT[p] 
#                 if (playerTurn == '1' and p == '2') or (
#                     playerTurn == '2' and p == '1'
#                 ):
#                     continue  
#                 board2[p] += 1
#                 seedsToSow -= 1


            
#             if playerTurn == '1' and p in PLAYER_1_PITS and board2[p] == 1:
#                 oppositePit = OPPOSITE_PIT[p]
#                 board2['1'] += board2[oppositePit]
#                 board2[oppositePit] = 0
#             elif playerTurn == '2' and p in PLAYER_2_PITS and board2[p] == 1:
#                 oppositePit = OPPOSITE_PIT[p]
#                 board2['2'] += board2[oppositePit]
#                 board2[oppositePit] = 0
#             diff = board2[playerTurn] - op_initial
#             if diff > best_op_increase:
#                 best_op_move = p
#                 best_op_increase = diff
#         moves_dict[start_pit] = board1[playerTurn] - initial - best_op_increase
#     print(max(moves_dict, key = moves_dict.get))
#     return max(moves_dict, key = moves_dict.get)
    

if __name__ == '__main__':
    main()

