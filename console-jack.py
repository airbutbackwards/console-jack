import random
import os #solely for clearing terminal

playing = True

# to change for more fun
startingMoney = 15

money = startingMoney

# i get how atrocious these dictionaries are but its very simple to work with, if tedious, so idc ♥

cards = {
    "1" : 0,
    "A" : 4,
    "2" : 4,
    "3" : 4,
    "4" : 4,
    "5" : 4,
    "6" : 4,
    "7" : 4,
    "8" : 4,
    "9" : 4,
    "10" : 4,    
    "J" : 4,    
    "Q" : 4,    
    "K" : 4
}

values = {
    "1" : 1,
    "A" : 11,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "10" : 10,
    "J" : 10,
    "Q" : 10,
    "K" : 10
}

playerHand = {
    "1" : 0,
    "A" : 0,
    "2" : 0,
    "3" : 0,
    "4" : 0,
    "5" : 0,
    "6" : 0,
    "7" : 0,
    "8" : 0,
    "9" : 0,
    "10" : 0,
    "J" : 0,
    "Q" : 0,
    "K" : 0,
}
dealerHand = {
    "1" : 0,
    "A" : 0,
    "2" : 0,
    "3" : 0,
    "4" : 0,
    "5" : 0,
    "6" : 0,
    "7" : 0,
    "8" : 0,
    "9" : 0,
    "10" : 0,
    "J" : 0,
    "Q" : 0,
    "K" : 0,
}

# resets all dicts and whatnot 
def initialize():
    for card,count in playerHand.items():
        playerHand[card] = 0
    for card,count in dealerHand.items():
        dealerHand[card] = 0
    for card,count in cards.items():
        cards[card] = 4
    cards["1"] = 0

def clearConsole(): #for clearing
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# picks a random card for the picker
def pickCard(picker):
    available = [item for item, count in cards.items() if count >= 1]
    chosen = random.choice(available)
    cards[chosen] -= 1
    if picker == 'player':
        playerHand[chosen] += 1
    if picker == 'dealer':
        dealerHand[chosen] += 1

# calculates hand
def calculateHand(target):
    global totalPlayer
    global totalDealer
    if target == 'player':
        totalPlayer= 0
        for card, count in playerHand.items():   
            if count == 0:
                continue
            totalPlayer += values[card] * count
    if target == 'dealer':
        totalDealer= 0
        for card, count in dealerHand.items():   
            if count == 0:
                continue
            totalDealer += values[card] * count

def showHand(hand):
    cardlist = [f"{count} {card}" for card, count in hand.items() if count > 0]
    print("You have: " + ", ".join(cardlist))


clearConsole()
print("Welcome to Blackjack!")



while playing == True:
    initialize()

    print("Your money:", money)
    bet = int(input("What is your bet? : "))
    # to prevent betting more than you have
    while bet > money:
        bet = int(input("You can't bet more than your money! Try again: "))

    money -= bet

    # yea i get that the dealer is supposed to pick up two but one of them is hidden. 
    # only mild RNG differences here that are probably overshadowed by not weighting different # of cards differently lol
    pickCard('dealer')
    calculateHand('dealer')

    pickCard('player')
    pickCard('player')
    calculateHand('player')

    Hit=True
    while Hit==True:
        clearConsole()
        print("The dealer's card totals ",totalDealer)
        showHand(playerHand)
        print("Your cards total to ",totalPlayer,".")
        playerBust = False
        if totalPlayer <= 21:
            qHit = input("Would you like to hit (Y/N): ")
            if qHit == "Y":
                pickCard('player')
                calculateHand('player')
            elif qHit == "N":
                Hit = False
            else:
                print("Not a fitting response. Try again!")
        else:
            # ace logic. turns an A (worth 11) to a 1 (worth 1) (ik that it should be just one card but really this makes it even easier for the PLAYER to read (as well as being easier to code))
            if playerHand["A"] > 0:
                playerHand["A"] -= 1
                playerHand["1"] += 1
                calculateHand('player')
            else:
                Hit = False
                print("You busted!")
                playerBust = True
                totalPlayer = 0
        
    clearConsole()

    #  calculate winner

    #get dealers final cards

    if playerBust:
        print("You busted!")
    else:
        print("Your cards total to ",totalPlayer,".")
    pickCard('dealer')
    calculateHand('dealer')
    print("The dealer has", totalDealer, ".")
    while totalDealer < 17:
        print("The dealer's hand is worth", totalDealer, ". He pulls again.")
        pickCard('dealer')
        calculateHand('dealer')
        
    #win calc
    if totalDealer > 21:
        print('Dealer busted with', totalDealer, "!")
        totalDealer = 0


    if totalPlayer > totalDealer:
        print("You win!")
        print("You have won ", (bet*2), " money.")
        money += (bet*2)
    if totalPlayer == totalDealer:
        print("You have tied.")
        print("You got your money back.")
        money += bet
    if totalPlayer < totalDealer:
        print("You have lost!")

    if money > 0:
        playQuestion = input("Would you like to play again? (Y/N): ")
        if playQuestion == 'Y':
            pass
        if playQuestion == 'N':
            playing = False
            clearConsole()
    else:
        print("You have no more money. Get outta here!")
        playing = False
