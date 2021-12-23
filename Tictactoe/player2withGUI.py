import TicTacToeUI
import gameboard

def run() -> None:
    '''sets up and runs the tic-tac-toe game with UI'''

    tictactoe2 = gameboard.BoardClass(' ' , ' ', 'player2', ' ')
    server_game = TicTacToeUI.TicTacToeGUI(tictactoe2)
    server_game.host_socket.close()
    

if __name__ == "__main__":
    run()
