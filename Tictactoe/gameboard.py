class BoardClass():
    '''A public interface connecting users, the tic-tac-toe game, and the data surrounding them.

    Attributes:
        _players_username (str): the username of the player the class describes
        username_last_turn (str): the username of the player who made the last move
        wins (int): the number of wins the player the class belongs to has
        losses (int): the number of losses the player the class belongs to has
        ties (int): the number of ties the player the class belongs to has

    '''
    def __init__ (self, players_username: str, player1: str, player2: str, last_turn: str) -> None:
        '''Make a BoardClass

        Args:
            players_username: the username of the player the class describes
            username_last_turn: the username of the player who made the last move
            wins: the number of wins the player the class belongs to has
            losses: the number of losses the player the class belongs to has
            ties: the number of ties the player the class belongs to has
        '''

        self._players_username = players_username
        self._player1 = player1
        self._player2 = player2
        self._username_last_turn = last_turn
        self._wins = 0
        self._losses = 0
        self._ties = 0
        self._board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    def updateGamesPlayed(self) -> int:
        '''keeps track of how many games have been played

            Returns:
                the sum of wins, losses, and ties a player has had
        '''
        return self._wins + self._losses + self._ties

    def get_board(self):
        return self._board

    def setlastturn(self, lastmove: str) -> None:
        self._username_last_turn = lastmove
    
    def getlastturn(self):
        return self._username_last_turn

    def set_player1(self, name: str):
        self._player1 = name
    
    def get_player1(self):
        return self._player1
    
    def set_player2(self, name: str):
        self._player2 = name
    
    def get_player2(self):
        return self._player2

    def setUsername(self, name: str):
        self._players_username = name

    def getUsername(self):
        return self._players_username

    def resetGameBoard(self) -> None:
        self._board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        
    def updateGameBoard(self, entry: int, move_type: str) -> int:
        self._board[entry] = move_type.upper()
        return entry
    
    def isWinner(self) -> bool:
        #returns False if there is a tie
        #returns True if one player wins
        if self._players_username == self._player2:
            #check rows
            for row in range(3):
                if self._board[3*row:3+3*row].count('O') == 3 or self._board[3*row:3+3*row].count('X') == 3:
                    if self._username_last_turn == self._player2:
                        self._wins += 1
                    else:
                        self._losses += 1
                    
                    return True
            #check columns
            for column in range(3):
                if self._board[column] == self._board[column+3] == self._board[column+6] and self._board[column] != ' ':
                    if self._username_last_turn == self._player2:
                        self._wins += 1
                    else:
                        self._losses += 1
                    
                    return True
            #check diagonals
            if (self._board[0] == self._board[4] == self._board[8] or self._board[2] == self._board[4] == self._board[6]) and self._board[4] != ' ':
                if self._username_last_turn == self._player2:
                    self._wins += 1
                else:
                    self._losses += 1

                return True
        else:
            #check rows
            for row in range(3):
                if self._board[3*row:3+3*row].count('X') == 3 or self._board[3*row:3+3*row].count('O') == 3:
                    if self._username_last_turn == self._player2:
                        self._losses += 1
                    else:
                        self._wins += 1
                    
                    return True
            #check columns
            for column in range(3):
                if self._board[column] == self._board[column+3] == self._board[column+6] and self._board[column] != ' ':
                    if self._username_last_turn == self._player2:
                        self._losses += 1
                    else:
                        self._wins += 1
                    
                    return True
            #check diagonals
            if (self._board[0] == self._board[4] == self._board[8] or self._board[2] == self._board[4] == self._board[6]) and self._board[4] != ' ':
                if self._username_last_turn == self._player2:
                    self._losses += 1
                else:
                    self._wins += 1

                return True
        return False

    def boardIsFull(self) -> bool:
        if ' ' in self._board:
            return False
        else:
            self._ties += 1
        return True

    def printStats(self):
        return f'''\nStats: \n
Username: {self._players_username} 
Last Move: {self._username_last_turn} 
Games Played: {self.updateGamesPlayed()} 
Wins: {self._wins} 
Losses: {self._losses} 
Ties: {self._ties} \n'''

