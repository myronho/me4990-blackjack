# Program by Myron Ho
# ME 4990
# Final Project
# Black Jack

# Card Image Source: http://acbl.mybigcommerce.com/52-playing-cards/

import pygame
from enum import Enum, IntEnum
import random



## CUSTOM FUNCTIONS

# Create Card Object
class Card():
    def __init__(self,V,N,S,P):
        self.value = V      # Card Value
        self.name = N       # Card Name
        self.suit = S       # Card Suit
        self.image = P      # Card Picture


# Create deck of card objects
def initializeDeck():
    # Initialize Empty Deck
    deck = []
    i = 0
    for j in range(len(CARD_VALUES)):
        for k in CARD_SUITS:
            # Create card object and append to deck
            deck.append(Card(CARD_VALUES[j], CARD_NAMES[j], k, card_img[i]))
            i += 1

    return deck


# Find card index of a 1D card storage array/list
def card_index(V,S):
    if S == 'S':
        T = 1
    elif S == 'C':
        T = 2
    elif S == 'D':
        T = 3
    elif S == 'H':
        T = 4
    else:
        print("Error with T in card_index()")

    return (V-1)*4 + (T-1)


# Display cards to screen / GUI
def display_card():

    # Display every card in player's hand    
    if (len( player_hand) != 0):
        for i in range(len( player_hand)):
            win.blit( player_hand[i].image, (card_x_pos[i],card_y_pos[i]))

    if(reveal or spectate):
        # Display every card in AI's hand face up       
        if (len( AI_hand) != 0):
            for i in range(len( AI_hand)):
                win.blit( AI_hand[i].image, (AI_card_x_pos[i],AI_card_y_pos[i]))
    else:
        # Displayu every card in AI's hand face down
        if (len( hidden_hand) != 0):
            for i in range(len( hidden_hand)):
                win.blit( hidden_hand[i].image, (hidden_card_x_pos[i],hidden_card_y_pos[i]))

    pygame.display.update() 


# Randomly select a card from the deck
def get_random_card():
    global full_deck
    r = random.randint(0,len(full_deck)-1)
    # print(len(full_deck), end=' ')
    # print(r)

    # Remove and return a card from the deck
    return full_deck.pop(r)


# Assign card from deck into player's hand
def player_draw_cards():
    global card_x_pos
    global card_y_pos

    # Add card into player's hand
    player_hand.append(get_random_card())

    # Add new card's position
    if (len(card_x_pos) == 0):
        card_x_pos.append(DEFAULT_X)
    else:
        card_x_pos.append(card_x_pos[-1] + DEFAULT_OFFSET)

    card_y_pos.append(DEFAULT_Y)


# Assign card from deck into AI's hand
def AI_draw_card():
    global AI_card_x_pos
    global AI_card_y_pos
    global hidden_card_x_pos
    global hidden_card_y_pos

    # If AI's card value is under 18, draw card.
    if get_card_value(AI_hand) < 18:
        AI_hand.append(get_random_card())
        hidden_hand.append(bg_card)

        # Add card to default position if AI's hand is empty
        if (len(AI_card_x_pos) == 0):
            AI_card_x_pos.append(DEFAULT_X)
            hidden_card_x_pos.append(DEFAULT_X)
        else:
            # Add card next to previous card
            AI_card_x_pos.append(AI_card_x_pos[-1] + DEFAULT_OFFSET)
            hidden_card_x_pos.append(hidden_card_x_pos[-1] + DEFAULT_OFFSET)

        # All cards have the same y-value
        AI_card_y_pos.append(AI_DEFAULT_Y)
        hidden_card_y_pos.append(AI_DEFAULT_Y)

        # Did AI draw a card?
        return True
    else:
        return False


# Obtain current score of player / AI hand      
def get_card_value(hand):
    # If hand is empty, return zero
    if len(hand) == 0:
        return 0
    else:
        # Initialize variables
        Aces = []
        sum = 0

        # Go through entire hand
        for i in hand:
            # How many aces exist in the hand?
            if i.name == 1:
                Aces.append(i)

            # Sum of card values
            sum += i.value
        
        # Reduce value of aces to prevent bust
        if sum > 21 and (len(Aces) != 0):
            sum -= 10
        return sum


# Display texts on screen / GUI
def draw_texts():
    # Display GUI texts
    ai_hand_text = GUI_font.render("AI HAND:",True,white)
    player_hand_text = GUI_font.render("PLAYER HAND:",True,white)
    hand_value_text = GUI_font.render('HAND VALUE: '+ str(get_card_value(player_hand)),True,white)
    winner_text = WIN_font.render(win_str[win_int],True,white)

    win.blit(winner_text, (WIN_WIDTH//2-win_x[win_int], WIN_HEIGHT//2-win_y[win_int]))
    win.blit(hand_value_text, (15,WIN_HEIGHT-CARD_HEIGHT-85))
    win.blit(ai_hand_text, (15,15))
    win.blit(player_hand_text, (15,WIN_HEIGHT-CARD_HEIGHT-60))

    # Display Instructions
    esc_text = INST_font.render('Press [ESC] to restart', True, white)
    space_text = INST_font.render('Press [SPACE] to hit', True, white)
    enter_text = INST_font.render('Press [ENTER] to pass', True, white)
    spec_text = INST_font.render('Press [TAB] to enable spectator mode', True, white)

    win.blit(esc_text, (WIN_WIDTH//2+30,WIN_HEIGHT//2+15))
    win.blit(space_text, (WIN_WIDTH//2+30,WIN_HEIGHT//2+30))
    win.blit(enter_text, (WIN_WIDTH//2+30,WIN_HEIGHT//2+45))
    win.blit(spec_text, (WIN_WIDTH//2+30,WIN_HEIGHT//2+60))

    # Display Credit
    name_text = INST_font.render('Programmed by Myron Ho', True, white)
    class_text = INST_font.render('ME 4990', True, white)

    win.blit(name_text, (355,7))
    win.blit(class_text, (450,7+15))

    # Display AI score if spectator mode is toggled
    if spectate:
        AI_value_text = GUI_font.render('AI VALUE: '+ str(get_card_value(AI_hand)),True,white)
        win.blit(AI_value_text, (175,15))



## INITIALIZE VARIABLES

# Create GUI
pygame.init()

# Initialize GUI window
WIN_WIDTH = 500
WIN_HEIGHT = 500
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("BlackJack (Final Project by Myron Ho)")


# Initialize Card Data
CARD_VALUES = [11,2,3,4,5,6,7,8,9,10,10,10,10]
CARD_NAMES = list(range(1,14))
CARD_SUITS = list(range(1,5))

# Define Pixel Size of Card
CARD_WIDTH = 100
CARD_HEIGHT = 150

card_img_dir = []
card_img = []

# Define colors in RGB values
black = (0,0,0)
white = (255,255,255)


# Obtain directory and objects for card images
for i in CARD_NAMES:
    for j in CARD_SUITS:
        card_img_dir.append("images/" + str(i) + "-" + str(j) + ".png")

for i in card_img_dir:
    card_img.append(pygame.transform.scale(pygame.image.load(i), (CARD_WIDTH, CARD_HEIGHT)))

bg_card = Card(0,0,0,pygame.transform.scale(pygame.image.load("images/blue_back.png"), (CARD_WIDTH, CARD_HEIGHT)))


# Initialize Player and AI deck
player_hand = []
card_x_pos = []
card_y_pos = []

AI_hand = []
AI_card_x_pos = []
AI_card_y_pos = []

hidden_hand = []
hidden_card_x_pos = []
hidden_card_y_pos = []

DEFAULT_X = 30
DEFAULT_Y = WIN_HEIGHT-CARD_HEIGHT-30
AI_DEFAULT_Y = 45
DEFAULT_OFFSET = 30


# Initialize Font and Score Texts
GUI_font = pygame.font.SysFont(None, 32)
WIN_font = pygame.font.SysFont(None, 42)
INST_font = pygame.font.SysFont(None, 16)
TITLE_font = pygame.font.SysFont(None, 24)

win_int = 0
win_str = ['', 'PLAYER WINS', 'AI WINS', 'PLAYER BUST — AI WINS', 'PLAYER WINS — AI BUST', 'TIED', 'NO WINNERS']
win_x = [0, 100, 65, 180, 180, 40, 100]
win_y = [0, 30, 30, 30, 30, 30, 30]


# Initialize booleans for GUI mantainence
main_loop = 0
run_game = True
reveal = False
session = True
spectate = False


# Create deck and a copy of the deck to maintain original copy
original_deck = initializeDeck()
full_deck = list(original_deck)


# Main Game Loop
while run_game:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # GUI window will remain open until [X] button is clicked or GUI is closed.
            run_game = False

    # Create background
    win.fill(black)
    draw_texts()

    # Used to prevent button spam
    if main_loop > 0:
        main_loop += 1
    if main_loop > 5:
        main_loop = 0


    # Obtain all keys pressed
    keys = pygame.key.get_pressed()

    # Restart Game
    if keys[pygame.K_ESCAPE]:
        # Reinitialize everything
        full_deck = list(original_deck)
        run_game = True
        session = True
        main_loop = 0
        win_int = 0
        reveal = False
        session = True
        player_hand = []
        card_x_pos = []
        card_y_pos = []
        AI_hand = []
        AI_card_x_pos = []
        AI_card_y_pos = []
        hidden_hand = []
        hidden_card_x_pos = []
        hidden_card_y_pos = []

    # Player hit / obtain another card
    if keys[pygame.K_SPACE] and main_loop == 0 and session:
        player_draw_cards()
        main_loop = 1
        
        AI_hit = AI_draw_card()

        print("AI: ", end='')
        print(get_card_value(AI_hand))

        # Test all possible outcomes
        if get_card_value(AI_hand) > 21 and get_card_value(player_hand) > 21:
            session = False
            print("NO WINNERS")
            win_int = 6
            reveal = True
        elif get_card_value(AI_hand) > 21:
            session = False
            print("AI BUST, PLAYER WINS")
            win_int = 4
            reveal = True
        elif get_card_value(player_hand) > 21:
            # PLAYER BUST
            # AI WINS     
            print('PLAYER BUST, AI WINS')
            win_int = 3
            session = False
            reveal = True
        elif get_card_value(AI_hand) == 21 and get_card_value(player_hand) == 21:
            # TIED
            print('TIED')
            win_int = 5
            session = False
            reveal = True
        elif get_card_value(AI_hand) == 21 and get_card_value(player_hand) != 21:
            # AI WINS
            print('AI WINS')
            win_int = 2
            session = False
            reveal = True
        elif get_card_value(AI_hand) != 21 and get_card_value(player_hand) == 21:
            # PLAYER WINS
            print('PLAYER WINS')
            win_int = 1
            session = False
            reveal = True
    
    # Player passes
    if (keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]) and main_loop == 0 and session:
        main_loop = 1

        AI_hit = AI_draw_card()

        print("AI: ", end='')
        print(get_card_value(AI_hand))

        # Test all possible outcomes
        if (AI_hit == False):
            if get_card_value(AI_hand) > get_card_value(player_hand):
                session = False
                print("AI WINS")
                win_int = 2
                reveal = True
            elif get_card_value(AI_hand) < get_card_value(player_hand):
                session = False
                print("PLAYER WINS")
                win_int = 1
                reveal = True
            else:
                session = False
                print("TIED")
                win_int = 5
                reveal = True
        else:
            if get_card_value(AI_hand) > 21 and get_card_value(player_hand) > 21:
                session = False
                print("NO WINNERS")
                win_int = 6
                reveal = True
            elif get_card_value(AI_hand) > 21:
                session = False
                print("AI BUST, PLAYER WINS")
                win_int = 4
                reveal = True
            elif get_card_value(AI_hand) == 21 and get_card_value(player_hand) == 21:
                # TIED
                print('TIED')
                win_int = 5
                session = False
                reveal = True
            elif get_card_value(AI_hand) == 21 and get_card_value(player_hand) != 21:
                # AI WINS
                print('AI WINS')
                win_int = 2
                session = False
                reveal = True
            elif get_card_value(AI_hand) != 21 and get_card_value(player_hand) == 21:
                # PLAYER WINS
                print('PLAYER WINS')
                win_int = 1
                session = False
                reveal = True

    # Toggle Spectator Mode
    if keys[pygame.K_TAB] and main_loop == 0:
        if spectate == False:
            spectate = True
        else:
            spectate = False

        main_loop = 1

    display_card()

pygame.quit()
