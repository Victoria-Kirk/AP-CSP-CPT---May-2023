### Citations ###
# 1.cmu_graphics module
# Original Source: CMU CS Academy
# URL to Original: https://academy.cs.cmu.edu/desktop
# First Use: Line 13



### Code Starts Here ###

# Citation 1
# import the cmu_graphics module
import cmu_graphics
from cmu_graphics import *

# import the random library 
import random 

# import the math library to do fancy calculations!
import math



# store necesary game data as custom app properties
    # counter for how many cards have been opened 
cmu_graphics.app.moveCount=0
    # list of open cards
cmu_graphics.app.pickedCards=[]
    # list of open cardIds 
cmu_graphics.app.pickedCardIDs=[]
    # step counter to track timing between the opening and flipping of cards
cmu_graphics.app.stepCounter=0
    # optional barrier to add borders to the game
cmu_graphics.app.wall=10
    # optional spacing between cards
cmu_graphics.app.percentCushion=0.05
    # tracking when cards need to be hidden
cmu_graphics.app.hidePair=False
    # track the number of matches that have been made
cmu_graphics.app.matchCounter=0
    # store the current game deck
cmu_graphics.app.deck=[]
    # be able to access restart button from the onMousePress function to click it
cmu_graphics.app.restartButton=Group(
    Rect(125,250,150,100,fill=rgb(32, 178, 170)),
    Label("RESTART", 200, 300, fill = rgb(255,255,255),bold=True,size=25)
)
    # group to contain the end screen
cmu_graphics.app.endScreen=Group(
    Rect(0,0,400,400,fill=rgb(0, 0, 0)),
    Label("You Did It!", 200, 150, fill = rgb(200,200,200),size=50,bold=True),
    cmu_graphics.app.restartButton
)
    # be able to access start button from the onMousePress function to click it
cmu_graphics.app.startButton=Group(
    Rect(125,250,150,100,fill=rgb(65, 105, 225)),
    Label("START", 200, 300, fill = rgb(255,255,255),bold=True,size=25)
)
    # group to contain the start screen
cmu_graphics.app.startScreen=Group(
    Rect(0,0,400,400,fill=rgb(0, 0, 0)),
    Label("Charmed", 200, 75, fill = rgb(255,255,255),size=80,bold=True,font = 'sacramento'),
    Label("A Card-Matching Game", 200, 150, fill = rgb(200,200,200),size=30),
    cmu_graphics.app.startButton
)



# function to create a list of symbol types
def makeSymbolTypeList(numberOfPairs):
    # initialize a list to contain the symbol types
    symbolTypeList=[]

    # list to contain the colors
    colors=[rgb(255, 0, 0),rgb(255, 215, 0),rgb(0, 255, 0),rgb(0, 0, 255),rgb(148, 0, 211)]

    # list to contain the shapes
    shapes=["Circle", "NormalStar", "Rectangle", "Tringle", "HorizontalLine", "RoundedStar", "VerticalLine", "Oval", "Diamond"]

    # number of symbol types needed
    numberNeeded=numberOfPairs
    
    # assemble symbol types list
    for number in range(numberNeeded):        
        unique=False

        # check that the newly selected symbol will be unique
        while not (unique):
            color=random.choice(colors)
            shape=random.choice(shapes)
            isMatching=False

            if (len(symbolTypeList)>0):
                for symbolType in symbolTypeList:
                    if ((symbolType[0] == color) and (symbolType[1] == shape)):
                        isMatching=True
        
                if not (isMatching):
                    unique=True
            else:
                unique=True

        newSymbolType=[color,shape]
        symbolTypeList.append(newSymbolType)
        
    return symbolTypeList


# function to create a symbol list
def makeSymbolList(numberOfPairs):
    # list to contain card symbol types (call "makeSymbolTypeList" function)
    symbolTypeList=makeSymbolTypeList(numberOfPairs)
    
    # initialize a list to contain the symbols
    symbolList=[]
    
    # number of symbol types needed
    numberNeeded=numberOfPairs
    
    # create symbols and add an identification
    for number in range(numberNeeded): 

        # make two identical symbols in order to make a matching pair of cards
        for count in range(2): 

            # check what shape the symbol will be and make an instance of that shape object (using a cmu_graphics class)      
            match symbolTypeList[number][1]:
                case "Circle":
                    symbol = Circle(200,200,100,visible=False)
                case "NormalStar":
                    symbol = Star(200,200,100,5,roundness=40,visible=False)
                case "Rectangle":
                    symbol = Rect(100,100,200,200,visible=False)
                case "Tringle":
                    symbol = Polygon(100,300,200,100,300,300,visible=False)
                case "HorizontalLine":
                    symbol = Line(100,200,300,200,lineWidth=20,visible=False)
                case "RoundedStar":
                    symbol = Star(200,200,100,7,roundness=70,visible=False)
                case "VerticalLine":
                    symbol = Line(200,100,200,300,lineWidth=20,visible=False)
                case "Oval":
                    symbol = Oval(200,200,150,200,visible=False)
                case "Diamond":
                    symbol = Rect(100,100,200,200,rotateAngle=45,visible=False)

            # color the symbol with the appropriate color
            color = symbolTypeList[number][0]
            symbol.fill = color

            # append the symbol to the list
            symbolList.append(symbol)

    return symbolList


# function that gets the user input for the numeber of pairs in the deck of cards
def getCardPairCount():
    pairs=cmu_graphics.app.getTextInput("How many pairs of cards would you like? Please enter a number between 1 and 46.")
    pairsAreValid=False

    # perform an integer check to make sure the input is usable
    while ((pairsAreValid==False)or((int(pairs)<1)or(int(pairs)>46))):
        try:
            pairs=int(pairs)
            if (int(pairs)>1)and(int(pairs)<46):
                pairsAreValid=True
            else:
                pairs=cmu_graphics.app.getTextInput("I'm sorry, the input you submitted is not within the range. Please enter a number between 1 and 46.")
        except:
            pairs=cmu_graphics.app.getTextInput("I'm sorry, the input you submitted is not a number. Please enter a number between 1 and 46.")

    # convert the input for the number of pairs to an integer and return from the function
    return int(pairs)

    
# function to determine the number of rows and columns
def calcRowAndCol(numberOfPairs):
    cards=numberOfPairs*2
    if (cards==4):
        rows=2
    else:
        rows=1
    columns=int(math.sqrt(cards))
    while (rows*columns!=cards):
        columns+=1
        rows=int(cards/columns)
    return rows, columns


# function to assemble the deck of cards
def assembleCards(numberOfPairs):
    numberOfRows, numberOfColumns = calcRowAndCol(numberOfPairs)
    symbolList=makeSymbolList(numberOfPairs)
    
    # make the array for cards
    cards=[]

    # initialize a varible to track a new identification number to every other card
    cardIdValue=1

    # make individual cards
    for row in range(numberOfRows):
        for col in range(numberOfColumns):
            symbol=symbolList.pop(0)

            # draw front (symbol) side of card
            cardFront=Group(
                        Rect(0,0,400,400,fill="black",border="gray"), 
                        symbol)
            
            # draw back side of card
            cardBack=Group(
                        Rect(0,0,400,400,fill="white",border="gray"),
                        Rect(100,100,200,200,fill="gray",rotateAngle=45),
                        )
            
            # give card an identification number
            cardId=int(cardIdValue)

            # put card elements together
            card=[
                cardId,
                cardBack,
                cardFront
            ]
            cards.append(card)
            
            # increase the card identification value tracker
            cardIdValue += 0.5

    return cards

    
# function to display the deck
def displayDeck(numberOfPairs):
    # determine card spacing
    numberOfRows, numberOfColumns = calcRowAndCol(numberOfPairs)
    deckSpace=400-(2*cmu_graphics.app.wall)
    horizontalSpace=deckSpace/numberOfRows
    verticalSpace=deckSpace/numberOfColumns
    percentCushion=cmu_graphics.app.percentCushion
    horizontalCushion=horizontalSpace*percentCushion/2
    verticalCushion=verticalSpace*percentCushion/2
    cardWidth=((deckSpace-(horizontalCushion*numberOfColumns+horizontalCushion))/numberOfColumns)
    cardHeight=((deckSpace-(verticalCushion*numberOfRows+verticalCushion))/numberOfRows)

    # calling a function to make the card list
    cards=assembleCards(numberOfPairs)
    
    # shuffle cards before displaying ("placing") 
    random.shuffle(cards)

    # make the array for cards
    deck=makeList(numberOfRows,numberOfColumns)
    
    # add the shuffled cards to the deck
    for row in range(numberOfRows):
        for col in range(numberOfColumns):
            deck[row][col]=cards.pop(0)
 
    # draw cards
    for row in range(numberOfRows):
        for col in range(numberOfColumns):
            positioningRectangle=Rect(cmu_graphics.app.wall+horizontalCushion+col*cardWidth+horizontalCushion*col,
                    cmu_graphics.app.wall+verticalCushion+row*cardHeight+verticalCushion*row,
                    cardWidth,
                    cardHeight,
                    fill=None,
                    )
            
            # possition card (both sides)
            index=1           
            while index < 3:
                side = deck[row][col][index]
                side.width=positioningRectangle.width
                side.height=positioningRectangle.height
                side.centerX=positioningRectangle.centerX
                side.centerY=positioningRectangle.centerY
                index += 1
    
    return deck
 
 
# reset game varibles
def resetGameVaribles():
    cmu_graphics.app.stepCounter=0
    cmu_graphics.app.hidePair=False
    cmu_graphics.app.pickedCards.clear()
    cmu_graphics.app.moveCount=0
    cmu_graphics.app.pickedCardIDs.clear()


def checkMatch():
    if (cmu_graphics.app.pickedCardIDs[0]!=cmu_graphics.app.pickedCardIDs[1]):
        cmu_graphics.app.hidePair=True

    # if the cards did match, then reset the game variables
    else:
        resetGameVaribles()
        cmu_graphics.app.matchCounter+=1

#  hide unmatching cards
def hideCards():
    cardOne=cmu_graphics.app.pickedCards[0]
    cardTwo=cmu_graphics.app.pickedCards[1]
    cardOne[1].visible=True
    cardTwo[1].visible=True
    resetGameVaribles()


# check if the player clicks on an available card and check for a match
def checkClick(x,y,deck,numberOfPairs):
    numberOfRows, numberOfColumns = calcRowAndCol(numberOfPairs)
        
    # check each card in the deck for a click
    for row in range(numberOfRows):
        for column in range(numberOfColumns):

           # check that less than two cards have been revealed
            if (cmu_graphics.app.moveCount<2):

                # check that the coordinates of the click landed on the card and that the selected card has not been revealed 
                if((deck[row][column][1].hits(x,y))and(deck[row][column][1].visible==True)): 
                    
                    # reveal the front side of the card 
                    deck[row][column][1].visible=False

                    # record the card and its identification number in order to check for a match
                    cmu_graphics.app.pickedCardIDs.append(deck[row][column][0])
                    cmu_graphics.app.pickedCards.append(deck[row][column])
            
                    # increase the move count
                    cmu_graphics.app.moveCount+=1

            # check for a match if two cards have been revealed
            if (cmu_graphics.app.moveCount==2):
                checkMatch()


# make a function to check if the game is over
def checkGameEnd():
    # clear old game
    cmu_graphics.app.matchCounter=0
    cmu_graphics.app.group.clear()

    # display end screen
    cmu_graphics.app.endScreen.visible=True
    cmu_graphics.app.endScreen.toFront()


# make a function that will generate a new game
def newGame():
    # hide start screen
    cmu_graphics.app.startScreen.visible=False

    # hide end screen
    cmu_graphics.app.endScreen.visible=False  

    # call function to obtain number of pairs for game
    cmu_graphics.app.numberOfPairs=getCardPairCount()

    # call function to display (and return) the card deck
    cmu_graphics.app.deck=displayDeck(cmu_graphics.app.numberOfPairs)



# enable a player to click on cards in order to flip them
def onMousePress(x,y):
    # if the player clicks on the start button, the start screen dissapears and the game begins
    if ((cmu_graphics.app.startScreen.visible) and (cmu_graphics.app.startButton.hits(x,y))):
        newGame()

    # if the player clicks on the restart button, a new game is generated
    elif ((cmu_graphics.app.endScreen.visible) and (cmu_graphics.app.restartButton.hits(x,y))):
        newGame()

    # if the player clicks somewhere within the game, it will look for a match
    elif ((len(cmu_graphics.app.deck)!=0) and ((not(cmu_graphics.app.endScreen.visible)) and (not(cmu_graphics.app.startScreen.visible)))):
        checkClick(x,y,cmu_graphics.app.deck,cmu_graphics.app.numberOfPairs)

                        
# track the amount of time passing after a second card is clicked in order to flip the cards over at the right time 
def onStep():
    if ((len(cmu_graphics.app.deck)!=0) and (cmu_graphics.app.matchCounter==cmu_graphics.app.numberOfPairs)):
        checkGameEnd()

    if cmu_graphics.app.hidePair:
        cmu_graphics.app.stepCounter+=1

        if (cmu_graphics.app.stepCounter>=15):
            hideCards()



cmu_graphics.run()

