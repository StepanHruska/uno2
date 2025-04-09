import random

#vygeneruje balicek(list) 180 karet
def buildDeck():
    deck = []
    colours = ["Red", "Green", "Blue", "Yellow"]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Draw two", "Skip", "Reverse"]
    wilds = ["Wild", "Draw four"]
    for colour in colours:
        for value in values:
            cardValue = "{} {}".format(colour,value)
            deck.append(cardValue)  
            if value != 0:
                deck.append(cardValue)
    for i in range (4):
        deck.append(wilds[0])
        deck.append(wilds[1])
    return deck

#zamicha balicek
def shuffleDeck(deck):
    for cardPos in range(len(deck)):
        randPos = random.randint(0, 107)
        deck[cardPos], deck[randPos] = deck[randPos], deck[cardPos]
    return deck

#funkce pro lizani karet
def drawCards(numCards):
    cardsDrawn = []
    for x in range(numCards):
        cardsDrawn.append(unoDeck.pop(0))
    return cardsDrawn

def showHand(player, playerHand):
    print("Player {}s Turn".format(player+1))
    print("Your hand")
    print("------------")
    y = 1
    for card in playerHand:
        print("{} {}".format(y,card))
        y += 1
    print("")

#overi jestli hrac muze hrat, nebo ne
def canPlay(colour, value, playerHand):
    for card in playerHand:
        if "Wild" in card:
            return True
        elif colour in card or value in card:
            return True
    return False

#herni promenne

discards = []
players = []
colours = ["Red", "Green", "Blue", "Yellow"]
numPlayers = int(input("How many players?"))
playerTurn = 0
playDirection = 1
playing = True

#zacatek hry - vygenerovani zamichaneho balicku
unoDeck = buildDeck()
unoDeck = shuffleDeck(unoDeck)

#overi pocet hracu a kezdemu rozda 7 karet
while numPlayers<2 or numPlayers>4:
    numPlayers = int(input("please enter a number between 2 - 4. How many players?"))
for player in range(numPlayers):
    players.append(drawCards(7))
print(players)

#balicek pouzitych karet
discards.append(unoDeck.pop(0))
splitCard = discards[0].split(" ",1)

#overeni Wild karty
currentColour = splitCard[0]
if currentColour != "Wild":
    cardValue = splitCard[1]
else:
    cardValue = "Any"

#prubeh hry
while playing:
    showHand(playerTurn, players[playerTurn])
    print("Card on top of the discard pile: {}".format(discards [-1]))
    if canPlay(currentColour, cardValue, players[playerTurn]):
        cardChosen = int(input("Which card do you want to play?"))
        while not canPlay(currentColour, cardValue,[players[playerTurn][cardChosen-1]]):
            cardChosen = int(input("Not a valid card. Which card do you want to play?"))
        print("You played {}".format(players[playerTurn][cardChosen-1]))
        discards.append(players[playerTurn].pop(cardChosen-1))
        #check if player won
        if len(players[playerTurn]) == 0:
            playing = False
            winner = "Player {}".format(playerTurn+1)
        else:
            #check for special cards
            splitCard = discards[-1].split(" ",1)
            currentColour = splitCard[0]
            if len(splitCard) == 1:
                cardValue = "Any"
            else:
                cardValue = splitCard[1]
            if currentColour == "Wild":
                for x in range(len(colours)):
                    print("{} {}".format(x+1, colours[x]))
                newColour = int(input("What colour would you like to choose?"))
                while newColour < 1 or newColour > 4:
                    newColour = int(input("Invalid option. What colour would you like to choose?")) 
                currentColour = colours[newColour-1]
            if cardValue == "Reverse":
                playDirection = playDirection * -1
            elif cardValue == "Skip":
                playerTurn += playDirection
                if playerTurn >= numPlayers:
                    playerTurn = 0
                elif playerTurn < 0:
                    playerTurn = numPlayers-1
            elif cardValue == "Draw two":
                playerDraw = playerTurn + playDirection
                if playerDraw == numPlayers:
                    playerDraw = 0
                elif playerDraw < 0:
                    playerDraw = numPlayers-1
                players[playerTurn].extend(drawCards(2))
            elif cardValue == "Draw four":
                playerDraw = playerTurn + playDirection
                if playerDraw == numPlayers:
                    playerDraw = 0
                elif playerDraw < 0:
                    playerDraw = numPlayers-1
                players[playerTurn].extend(drawCards(4))
            print("")
    else:
        print("You cant play, you have to draw a card")
        players[playerTurn].extend(drawCards(1))

    
    playerTurn += playDirection
    if playerTurn >= numPlayers:
        playerTurn = 0
    elif playerTurn < 0:
        playerTurn = numPlayers-1

print("Game over")
print("{} is the winner".format(winner))