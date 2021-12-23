import gameboard as gm
import tkinter
import socket

class TicTacToeGUI():

    my_board = 0
    master = 0
    results = ' '
    username = ' '
    player1 = ' '
    player2 = ' '
    last_turn = ' '
    letter = ' '

    port_number = ' '
    host_socket = ' '
    client_socket = ' '

    Buttons = []
    disabled_buttons = []

    def __init__(self, BoardClass: gm.BoardClass):

        self.my_board = BoardClass

        self.username = 0
        self.player1 = 0
        self.player2 = 0
        self.last_turn = 0
        self.current_turn = ' '

        self.isReceiver = False
        self.isMover = False
        
        self.create_canvas()
        self.make_grid()
        self.tk_vars()
        self.build_board()
        self.player_username_Entry()
        self.submit_button()
        self.turn_button()
        self.turn_label()
        self.results_display()
        self.play_again_button()
        self.quit_button()
        self.port_Entry()
        self.host_Entry()
        self.connected_label()
        self.run_game()

    def tk_vars(self) -> None:
        self.results = tkinter.StringVar()
        self.connect = tkinter.StringVar()
        self.username = tkinter.StringVar()
        self.username.set(self.my_board.getUsername())
        self.player1 = tkinter.StringVar()
        self.player1.set(self.my_board.get_player1())
        self.player2 = tkinter.StringVar()
        self.player2.set(self.my_board.get_player2())
        self.last_turn = tkinter.StringVar()
        self.last_turn.set(self.my_board.getlastturn())
        self.current_turn = tkinter.StringVar()
        self.host_number = tkinter.StringVar()
        self.port_number = tkinter.StringVar()

    #board side and gui side
    def create_canvas(self) -> None:
        self.master = tkinter.Tk()
        self.master.title('Tic-Tac-Toe')
        self.master.geometry('600x600')
        self.master.configure(background='pink')

    def make_grid(self) -> None:
        for x in range(5):
            self.master.grid_rowconfigure(x, weight=1)
            for y in range(3):
                self.master.grid_columnconfigure(y, weight=1)

    def tictactoe_spot(self, x: int, y: int) -> tkinter.Button:

        button = tkinter.Button(self.master, text= ' ', command = lambda: self.make_move(x,y))
        button.grid(column = y, row = x,sticky = 'nesw')
        return button

    def connected_label(self):
        self.connect_label = tkinter.Label(self.master, textvariable=self.connect, width = 10)
        self.connect_label.grid(column=1, row=4, sticky = 'ew')

    def build_board(self) -> None:
        for y in range(3):
            for x in range(3):
                self.Buttons.append(self.tictactoe_spot(y,x))
        self.disable_Board()

    def set_letter(self):
        #if player1
        if self.username.get() == self.player1.get():
            self.letter = 'X'
        elif self.username.get() == self.player2.get():
            self.letter = 'O'

    def set_last_turn(self, input: int) -> None:
        #set last turn for both front and back end boards
        self.last_turn.set(input)
        self.my_board.setlastturn(self.last_turn.get())
#current_turn, last_turn, isMover, isReceiver

#fix the states of both players
    def make_move(self, row: int, col: int, event=None) -> None:
        if self.username.get() == self.current_turn.get():
            print(self.username.get())
            print(self.current_turn.get())
            self.set_letter()
            entry = (row*3) + col
            print(1)
            self.updateGUIBoard(entry, self.letter)
            print(2)
            self.disable_Board()
            self.master.update()
            self.client_socket.send(bytes(str(entry),'utf-8'))
            if self.username.get() == self.player1.get():
                self.current_turn.set(self.player2.get())
                self.set_last_turn(self.player1.get())
            elif self.username.get() == self.player2.get():
                self.current_turn.set(self.player1.get())
                self.set_last_turn(self.player2.get())
            if not self.check_game():
                self.end_state()
                self.repeat_game(self.client_socket)
                return
            
        self.receive_state()

    def receive_state(self) -> None:
        if self.username.get() != self.current_turn.get():
            self.disable_Board()
            self.results.set('Waiting for move')
            self.master.update()
            move = self.client_socket.recv(1024).decode('ascii')
            
            #check letter of player
            other_letter = ' '
            if self.username.get() == self.player1.get():
                other_letter = 'O'
            if self.username.get() == self.player2.get():
                other_letter = 'X'
            print(3)
            self.updateGUIBoard(int(move), other_letter)
            print(4)
            self.results.set('Enter Move')
            if self.username.get() == self.player1.get():
                self.current_turn.set(self.player1.get())
                self.set_last_turn(self.player2.get())
            elif self.username.get() == self.player2.get():
                self.current_turn.set(self.player2.get())
                self.set_last_turn(self.player1.get())
            if not self.check_game():
                self.end_state()
                self.repeat_game(self.client_socket)
                return
            self.reable_Board()
    

    def end_state(self) -> None:
        self.disable_Board()
        if self.username.get() == self.player1.get():
            self.quit['state'] = 'normal'
            self.play_again['state'] = 'normal'
        

    def check_game(self) -> bool:
        if self.my_board.isWinner():
            if self.username.get() == self.player1.get():
                self.results.set(f'{self.my_board.getlastturn()} is the winner!\nPlay Again?')
            elif self.username.get() == self.player2.get():
                self.results.set(f'{self.my_board.getlastturn()} is the winner!')
            return False
        if self.my_board.boardIsFull():
            if self.username.get() == self.player1.get():
                self.results.set('Game is tied\nPlay Again?')
            if self.username.get() == self.player2.get():
                self.results.set('Game is tied')
            return False
        return True

    def repeat_game(self, socket: socket) -> bool:

    #player 2 receives response
    #player 1 sends response via buttons
        if self.username.get() == self.player2.get():

            self.master.update()
            request = socket.recv(1024).decode('ascii')

            if request == 'Play Again':
            
                self.results.set(f'{request}\nGame is Reset')
                self.my_board.resetGameBoard()
                self.disabled_buttons.clear()
                for moves in range(len(self.my_board.get_board())):
                    self.Buttons[moves].configure(text = self.my_board.get_board()[moves])
                    self.Buttons[moves]['state'] = 'normal'
                self.quit['state'] = 'disabled'
                self.play_again['state'] = 'disabled'
                self.set_last_turn(self.player1.get())
                self.current_turn.set(self.player1.get())
                self.receive_state()
                return True
            elif request == 'Fun Times':
                self.results.set(f'{request}\nGame has ended\n{self.my_board.printStats()}')
                socket.close()
                #print stats
                return False

    def updateGUIBoard(self, move: int, letter: str):
        self.my_board.updateGameBoard(move, letter)
        print(self.my_board.get_board())
        for moves in range(len(self.my_board.get_board())):
            self.Buttons[moves].configure(text = self.my_board.get_board()[moves])
        self.Buttons[move]['state'] = 'disabled'
        self.disabled_buttons.append(move)

    def disable_Board(self):
        for tiles in self.Buttons:
            tiles['state'] = 'disabled'
    
    def reable_Board(self):
        for tiles in self.Buttons:
            tiles['state'] = 'normal'
        for disabled_tiles in self.disabled_buttons:
            self.Buttons[disabled_tiles]['state'] = 'disabled'

    def turn_button(self) -> None:
        self.turnDisplay = tkinter.Label(self.master, textvariable=self.current_turn, width = 10)
        self.turnDisplay.grid(column=2, row = 4, sticky = 'nwe')

    def turn_label(self) -> None:
        self.turnlabel = tkinter.Label(self.master, text = "Current Turn", width = 10)
        self.turnlabel.grid(column=2, row=3, sticky = 's')

    def player_username_Entry(self) -> None:
        self.username.set('Enter Username')
        self.nameInput = tkinter.Entry(self.master, textvariable=self.username, width = 7)
        
        self.nameInput.grid(row=3, column=0, sticky = 'we')
        self.nameInput['state'] = 'disabled'
    
    def submit_button(self) -> None:
        self.submit_username = tkinter.Button(self.master, text = 'Submit', command=self.submit_vars)
        self.submit_username.grid(row = 4, column = 0, sticky = 's')

    def display_stats(self) -> None:
        #lastturn and Stats
        self.results.set(self.my_board.printStats())

#runs when clicking SUBMIT button
    def submit_vars(self, event = None) -> None:

        if self.results.get() == 'Enter Username' or self.results.get() == 'Enter Valid Username':
       
            #username
            if self.username.get() != 'Enter Username':

                #determines if class is player 1 or player 2
                if self.player1.get() == 'player1':
                    self.player1.set(self.username.get())
                    self.my_board.set_player1(self.player1.get())
                if self.player2.get() == 'player2':
                    self.player2.set(self.username.get())
                    self.my_board.set_player2(self.player2.get())
        
                #set player1 as last_turn on the first move
                self.set_last_turn(self.player1.get())

                self.my_board.setUsername(self.username.get())

                self.nameInput['state'] = 'disabled'
                if self.my_board.getUsername() == self.player2.get():
                    self.client_socket, self.host_socket = self.build_server(self.get_host(), self.get_port())
                    self.player1.set(self.exchange_usernames(self.client_socket))
                    self.my_board.set_player1(self.player1.get())
                    self.current_turn.set(self.player1.get())
                    self.submit_username['state'] = 'disabled'

                   
                    #puts player 2 in receive state
                    self.receive_state()


                if self.my_board.getUsername() == self.player1.get():
                    self.client_socket = self.build_client(self.get_host(), self.get_port())

                    self.player2.set(self.exchange_usernames(self.client_socket))
                    self.my_board.set_player2(self.player2.get())
                    self.current_turn.set(self.player1.get())
                    self.submit_username['state'] = 'disabled'
                    self.reable_Board()
            else:
                self.results.set('Enter Valid Username')

        elif self.results.get() == 'Please Enter: \nHost\nPort' or self.results.get() == 'Invalid host and port entry. Try Again.':

            self.host_number.get().strip()
            self.port_number.get().strip()

   
            try:
                if self.host_number.get() != 'Enter Host Number' and self.port_number.get() != 'Enter Port Number':
                    if type(self.get_host()) is str:
                        self.host['state'] = 'disabled'
                      
                    if type(self.get_port()) is int:
                        self.port['state'] = 'disabled'
                    
               
                    self.results.set('Enter Username')
                    
                    self.nameInput['state'] = 'normal'
                  
                else:
                    self.results.set('Invalid host and port entry.\nTry Again.')
            except TypeError:
              
                self.results.set('Invalid host and port entry.\nTry Again.')
            except Exception:
         
                self.results.set('Socket Connection Failed')
     
    def results_display(self) -> None:
        self.results.set('Please Enter: \nHost\nPort')
        self.display = tkinter.Label(self.master, textvariable=self.results, height = 10, width = 10)
        self.display.grid(column = 1, row = 3, sticky = 'we')

    def play_again_button(self) -> None:
        self.play_again = tkinter.Button(self.master, text = 'Play Again', width = 10, command=self.sendYes)
        self.play_again['state'] = 'disabled'
        self.play_again.grid(column = 1, row = 3, sticky = 'sw')

    def sendYes(self) -> None:
        self.client_socket.send(b'Play Again')

        #resets to base state
        self.results.set('Enter Move')
        self.my_board.resetGameBoard()
        self.disabled_buttons.clear()
        for moves in range(len(self.my_board.get_board())):
            self.Buttons[moves].configure(text = self.my_board.get_board()[moves])
            self.Buttons[moves]['state'] = 'normal'
        self.quit['state'] = 'disabled'
        self.play_again['state'] = 'disabled'
        self.set_last_turn(self.player1.get())
        self.current_turn.set(self.player1.get())
     
        self.master.update()

    def quit_button(self) -> None:
        self.quit = tkinter.Button(self.master, text = 'Quit', width = 10, command=self.sendNo)
        self.quit['state'] = 'disabled'
        self.quit.grid(column = 1, row = 3, sticky = 'se')

#fix so it uses displaystats()
    def sendNo(self) -> None:
        self.client_socket.send(b'Fun Times')
        self.quit['state'] = 'disabled'
        self.play_again['state'] = 'disabled'
        self.results.set(f'Game has ended{self.my_board.printStats()}')
        self.client_socket.close()

    def run_game(self) -> None:
        self.master.mainloop()

#socket part

    def host_Entry(self) -> None:
        self.host_number.set('')
        self.host = tkinter.Entry(self.master, textvariable = self.host_number, width = 7)
        self.host.grid(row=3, column=0, sticky = 'swe')
        self.host.insert(0, 'Enter Host Address')

    def port_Entry(self) -> None:
        self.port_number.set('')
        self.port = tkinter.Entry(self.master, textvariable=self.port_number, width = 7)
        self.port.grid(row=4, column=0, sticky = 'nwe')
        self.port.insert(0, 'Enter Port Number')

    def get_port(self) -> int:
        return int(self.port_number.get())

    def get_host(self) -> None:
        return self.host_number.get()

    def build_client(self, host: str, port: int) -> None:
        Player1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        HostAddress = host
        HostPort = port
        Player1Socket.connect((HostAddress,HostPort))

        return Player1Socket

    # for player 2 
    def build_server(self, serverAddress: str, port: int) -> None:
        
      
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((serverAddress,port))
        serverSocket.listen()
        self.results.set('Waiting for Connection')
        self.master.update()
        clientSocket,clientAddress = serverSocket.accept()
        
        return (clientSocket, serverSocket)

    def exchange_usernames(self, socket: socket.socket) -> str:
        if self.username.get() == self.player1.get():
           
            socket.send(bytes(self.username.get(), 'utf-8'))
            self.master.update()
            player2_username = socket.recv(1024).decode('ascii')

            self.connect.set(f'{player2_username} is connected')
            self.results.set('Enter Move')
            self.master.update()
            return player2_username

        if self.username.get() == self.player2.get():
            self.master.update()
            player1_username = socket.recv(1024).decode('ascii')

            self.connect.set(f'{player1_username} is connected')
            self.master.update()
            socket.send(bytes(self.username.get(), 'utf-8'))
         
            return player1_username


