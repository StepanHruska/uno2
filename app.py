from flask import Flask, render_template, request
from uno2 import buildDeck, shuffleDeck, drawCards, canPlay, showHand

app = Flask(__name__)

# Initialize game variables
unoDeck = shuffleDeck(buildDeck())
players = []
discards = []
colours = ["Red", "Green", "Blue", "Yellow"]
numPlayers = 2
playerTurn = 0
playDirection = 1
playing = True

# Route for the main game page
@app.route('/')
def index():
    global players, discards, unoDeck, playerTurn, playing
    if not players:
        # Initialize players and deal cards
        players = [drawCards(7) for _ in range(numPlayers)]
        discards.append(unoDeck.pop(0))
    return render_template('index.html', players=players, discards=discards, playerTurn=playerTurn)

# Route to handle player actions
@app.route('/play', methods=['POST'])
def play():
    global players, discards, playerTurn, playing
    card_index = int(request.form['card_index'])
    if canPlay(discards[-1].split()[0], discards[-1].split()[-1], [players[playerTurn][card_index]]):
        discards.append(players[playerTurn].pop(card_index))
        if len(players[playerTurn]) == 0:
            playing = False
            return f"Player {playerTurn + 1} wins!"
    return "Card played!"

if __name__ == '__main__':
    app.run(debug=True)