import numpy as np
import torch
import combine

from flask import Flask, request, render_template

global agent1
global player_turn
global AI_turn
global gameBoard
global AI

state = torch.load('models/modelX',map_location=torch.device('cpu'))
netX = combine.ttt_netX()
netX.load_state_dict(state)

agent1 = combine.agent(netX)

AI = 'AI: X'
AI_turn = -1
player_turn = 1
app = Flask(__name__)
gameBoard = combine.ttt()

@app.route("/")
def hello():
    global player_turn
    global AI_turn
    global gameBoard
    global AI
    global agent1
    game = gameBoard.getBoard()
    win = ""
    if AI_turn == gameBoard.turn:
        agent1.set_player(AI_turn)
        move,_ = agent1.make_move(gameBoard)
        gameBoard.play(move[0],move[1])
        game = gameBoard.getBoard()
    return render_template("index.html",game=game,win=win,AI=AI)

@app.route("/", methods = ['POST'])
def submit():
    global player_turn
    global AI_turn
    global gameBoard
    global AI
    global agent1
    game = gameBoard.getBoard()
    win = ""
    if request.method == 'POST':
        if player_turn == gameBoard.turn:
            if '00' in request.form:
                gameBoard.play(0,0)
                game = gameBoard.getBoard()
            elif '01' in request.form:
                gameBoard.play(0,1)
                game = gameBoard.getBoard()
            elif '02' in request.form:
                gameBoard.play(0,2)
                game = gameBoard.getBoard()
            elif '10' in request.form:
                gameBoard.play(1,0)
                game = gameBoard.getBoard()
            elif '11' in request.form:
                gameBoard.play(1,1)
                game = gameBoard.getBoard()
            elif '12' in request.form:
                gameBoard.play(1,2)
                game = gameBoard.getBoard()
            elif '20' in request.form:
                gameBoard.play(2,0)
                game = gameBoard.getBoard()
            elif '21' in request.form:
                gameBoard.play(2,1)
                game = gameBoard.getBoard()
            elif '22' in request.form:
                gameBoard.play(2,2)
                game = gameBoard.getBoard()
        if AI_turn == gameBoard.turn and gameBoard.win == None:
            agent1.set_player(AI_turn)
            move,_ = agent1.make_move(gameBoard)
            gameBoard.play(move[0],move[1])
            game = gameBoard.getBoard()

        if 'reset' in request.form:
            gameBoard.reset()
            game = gameBoard.getBoard()
            if AI_turn == gameBoard.turn:
                agent1.set_player(AI_turn)
                move,_ = agent1.make_move(gameBoard)
                gameBoard.play(move[0],move[1])
                game = gameBoard.getBoard()
        if 'AI' in request.form:
            gameBoard.reset()
            game = gameBoard.getBoard()
            AI_turn = AI_turn*-1
            player_turn = player_turn*-1
            if (AI_turn == -1):
                AI = 'AI: X'
            else:
                AI = 'AI: O'
            if AI_turn == gameBoard.turn:
                agent1.set_player(AI_turn)
                move,_ = agent1.make_move(gameBoard)
                gameBoard.play(move[0],move[1])
                game = gameBoard.getBoard()
        if gameBoard.win == -1:
            win = "X wins"
        if gameBoard.win == 1:
            win = "0 wins"
        if gameBoard.win == 0:
            win = "Draw"
        return render_template("index.html",game=game,win=win,AI=AI)
if __name__ == "__main__":
    app.run(debug=True)

