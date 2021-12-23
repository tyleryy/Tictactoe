import TicTacToeUI
import gameboard
import socket

def run() -> None:
    '''sets up and runs the tic-tac-toe game with UI'''
    tictactoe1 = gameboard.BoardClass(' ', 'player1', ' ', ' ')
    ClientGame = TicTacToeUI.TicTacToeGUI(tictactoe1)
    ClientGame.client_socket.close()

if __name__ == '__main__':
    run()


