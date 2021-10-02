import tkinter as tk
from checkers_logic import *


class CheckersUI(tk.Frame):
    STICKY = tk.N + tk.S + tk.E + tk.W

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.game_startup_dialog()

    def game_startup_dialog(self):
        self.start = tk.Frame(self)
        self.start.grid(row=0)
        self.p1Name = tk.StringVar()
        self.p2Name = tk.StringVar()

        tk.Label(self.start, text="Player 1 Name").grid(
            row=0, column=0)
        tk.Entry(self.start, textvariable=self.p1Name).grid(
            row=0, column=1)

        tk.Label(self.start, text="Player 2 Name").grid(
            row=1, column=0)
        tk.Entry(self.start, textvariable=self.p2Name).grid(
            row=1, column=1)

        self.okButton = tk.Button(self, text="Ok", command=self.begin_game)
        self.okButton.grid(row=3, column=0)

    def draw(self):
        self.boardCanvas.destroy()
        self.boardCanvas = tk.Canvas(self.game, width=560, height=560)
        self.boardCanvas.grid(row=2, column=0, columnspan=2)
        self.boardCanvas.create_image((280, 280), image=self.backgroundPhoto)

        for i in range(8):
            for j in range(8):
                if self.positions[i][j] != None:
                    self.boardCanvas.create_image((35 + 70 * i, 35 + 70 * j),
                                                  image=self.checkersPieceDict[self.positions[i][j]])

        self.boardCanvas.bind("<Button-1>", self.click_board)

    def begin_game_helper(self):
        self.okButton.grid_forget()
        self.start.grid_forget()

        self.game = tk.Frame(self)
        self.game.grid(row=0)

        self.backgroundPhoto = tk.PhotoImage(file="assets/board.png")
        self.checkersPieceDict = dict()
        photo = tk.PhotoImage(file="assets/wс.png")
        self.checkersPieceDict[Piece(0)] = photo
        photo = tk.PhotoImage(file="assets/bс.png")
        self.checkersPieceDict[Piece(1)] = photo

        photo = tk.PhotoImage(file="assets/wсk.png")
        self.checkersPieceDict[Piece(0, True)] = photo

        photo = tk.PhotoImage(file="assets/bсk.png")
        self.checkersPieceDict[Piece(1, True)] = photo

        self.boardCanvas = tk.Canvas(self.game, width=560, height=560)
        self.boardCanvas.grid(row=2, column=0, columnspan=2)
        self.boardCanvas.create_image((280, 280), image=self.backgroundPhoto)
        self.boardCanvas.bind("<Button-1>", self.click_board)

        self.statusLabel = tk.Label(self.game, text="")
        self.statusLabel.grid(row=3, column=0, columnspan=2)

        tk.Button(self.game, text="Resign", command=self.resign_game).grid(
            row=4, column=0)

        self.offerDrawButton = tk.Button(
            self.game, text="Offer Draw", command=self.offer_draw)
        self.offerDrawButton.grid(row=4, column=1)

        self.acceptDrawButton = tk.Button(
            self.game, text="Accept Draw", command=self.accept_draw)

        self.selected = False
        self.drawOffered = False

    def begin_game(self):

        self.begin_game_helper()

        self.positions = initial_board()
        self.draw()

        if (self.p1Name.get() == ""):
            self.player1Name = "Player 1"
        else:
            self.player1Name = self.p1Name.get()

        if (self.p2Name.get() == ""):
            self.player2Name = "Player 2"
        else:
            self.player2Name = self.p2Name.get()

        self.playerTurnLabel = tk.Label(self.game, text="* " + self.player1Name)
        self.playerTurnLabel.grid(row=0, column=0)
        self.playerTurnLabel2 = tk.Label(self.game, text=self.player2Name)
        self.playerTurnLabel2.grid(row=0, column=1)

        self.turn = 0

    def click_board(self, event):

        if no_move_detection(self.positions, self.turn):
            self.statusLabel["text"] = "No possible moves, you have lost"
            self.resign_game()

        else:
            jmpDetectLst = jump_detection(self.positions, self.turn)

            if self.selected == False:
                ptx, pty = pixel_to_int(event.x, event.y)

                if (self.positions[ptx][pty] == None):
                    self.statusLabel["text"] = "No piece selected"

                else:
                    if (self.positions[ptx][pty].color != self.turn):
                        self.statusLabel["text"] = "Wrong color selected"

                    else:
                        s = set(jmpDetectLst)
                        if len(jmpDetectLst) != 0 and ((ptx, pty) not in s):
                            self.statusLabel["text"] = "Incorrect selection. You have to jump"
                        else:
                            self.selected = True
                            self.selectedPt = (ptx, pty)
                            self.statusLabel["text"] = str(self.selectedPt) + " selected"

            else:
                ptx, pty = pixel_to_int(event.x, event.y)
                self.move(ptx, pty)

    def set_player1(self):
        self.playerTurnLabel["text"] = "* " + self.player1Name
        self.playerTurnLabel2["text"] = self.player2Name
        self.selected = False
        self.statusLabel["text"] = ""
        self.turn = 0

        if (self.drawOffered):
            self.offerDrawButton.grid_forget()
            self.acceptDrawButton.grid(row=4, column=1)
            self.drawOffered = False
        else:
            self.acceptDrawButton.grid_forget()
            self.offerDrawButton.grid(row=4, column=1)
            self.offerDrawButton["state"] = tk.NORMAL

    def set_player2(self):
        self.playerTurnLabel["text"] = self.player1Name
        self.playerTurnLabel2["text"] = "* " + self.player2Name
        self.selected = False
        self.statusLabel["text"] = ""
        self.turn = 1

        if (self.drawOffered):
            self.offerDrawButton.grid_forget()
            self.acceptDrawButton.grid(row=4, column=1)
            self.drawOffered = False
        else:
            self.acceptDrawButton.grid_forget()
            self.offerDrawButton.grid(row=4, column=1)
            self.offerDrawButton["state"] = tk.NORMAL

    def move(self, x2, y2):
        ptx, pty = self.selectedPt
        jmplst = jump_positions(self.positions[ptx][pty], ptx, pty, self.positions)
        mvlst = move_positions(self.positions[ptx][pty], ptx, pty, self.positions)

        if len(jmplst) != 0:
            s = set(jmplst)
            if ((x2, y2) not in s):
                self.statusLabel["text"] = str(self.selectedPt) + " selected, you have to take the jump"
                return
            else:
                delX = int((x2 + ptx) / 2.0)
                delY = int((y2 + pty) / 2.0)
                self.positions[delX][delY] = None
                self.positions[x2][y2] = self.positions[ptx][pty]
                self.positions[ptx][pty] = None
                self.selected = True
                self.selectedPt = (x2, y2)

                convert_to_king(self.positions)
                self.draw()

                jmplst2 = jump_positions(self.positions[x2][y2], x2, y2, self.positions)

                if len(jmplst2) != 0:
                    self.statusLabel["text"] = str(self.selectedPt) + " selected, you must jump again"
                    return

                else:
                    if no_opponent_piece_detection(self.positions, self.turn):
                        self.win_game()

                    else:
                        if self.turn == 0:
                            self.set_player2()
                        else:
                            self.set_player1()
        else:
            s = set(mvlst)
            if (x2, y2) not in s:
                self.statusLabel["text"] = "Invalid move. Select a piece and try again"
                self.selected = False
                return
            else:
                self.positions[x2][y2] = self.positions[ptx][pty]
                self.positions[ptx][pty] = None

                convert_to_king(self.positions)
                self.draw()

                if self.turn == 0:
                    self.set_player2()
                else:
                    self.set_player1()

    def end_game(self):
        self.game.destroy()

        self.endFrame = tk.Frame(self)
        self.endFrame.grid(row=0)
        self.endGameResult = tk.Label(self.endFrame, text="")
        self.endGameResult.grid(row=0)
        tk.Button(self.endFrame, text="New Game", command=self.end_game_new).grid(row=1)
        tk.Button(self.endFrame, text="Exit", command=self.quit).grid(row=2)

    def end_game_new(self):
        self.endFrame.destroy()
        self.okButton.destroy()
        self.start.destroy()

        self.game_startup_dialog()

    def resign_game(self):
        self.end_game()

        if self.turn == 0:
            winner = self.player2Name
            loser = self.player1Name

        else:
            winner = self.player1Name
            loser = self.player2Name

        self.endGameResult["text"] = winner + " won this game. " + loser + " lost."

    def win_game(self):
        self.end_game()

        if self.turn == 0:
            winner = self.player1Name
            loser = self.player2Name

        else:
            winner = self.player2Name
            loser = self.player1Name

        self.endGameResult["text"] = winner + " won this game. " + loser + " lost."

    def accept_draw(self):
        self.end_game()
        self.endGameResult["text"] = "This game was a draw"

    def offer_draw(self):
        self.drawOffered = True
        self.offerDrawButton["state"] = tk.DISABLED


def pixel_to_int(x, y):
    retx = 0
    retx_tot = 70

    rety = 0
    rety_tot = 70

    while (x > retx_tot and retx < 7):
        retx = retx + 1
        retx_tot = retx_tot + 70

    while (y > rety_tot and rety < 7):
        rety = rety + 1
        rety_tot = rety_tot + 70

    return (retx, rety)


def tkinter_main():
    root = tk.Tk()
    app = CheckersUI(master=root)
    app.mainloop()


tkinter_main()
