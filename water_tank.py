import random

power_cards = ("SOH", "DOT", "DMT")
water_cards = (1, 5, 10)
all_cards = (1,5,10,"SOH", "DMT", "DOT")
used_power_cards=[]
game_instruction="*****Welcome to Water tank game*****\nYou can choose a card to use or discard each turn.\nEverytime you lose a card will get a new card in the same type\nThere are two kind of card in the game\n\t1.Water card:\n\t\tto add water in your tank.\n\t2.Power card:\n\t\t(1) SOH: steal half of your opponent's current water and add in to your tank.\n\t\t(2) DOT: Drain your opponent's tank completely.\n\t\t(3) DMT: Double your current water\nYour goal is to fill your tank to 75-80(inclusuve)\nHowever, if your tank is overflowed(more than 80), the overflowed water will be wasted and there is a punishment\n\tyour water will be max-tank capacity - overflow amount(wink wink~)\nfor example:\n\tIf your water is 85, overflowed 5 water will be wasted and your wwater will be max capacity(80)-overflow(5) witch ended with 75 (still winning lololol)\n"


# prompt question, get valid non-empty userinput 
# return either a interger if input a num, or stripped lowercase str/uppercase power card str
def get_user_input(question):
    user_input=""
    while not user_input:
        user_input = input(f'{question}\n').strip()
    def is_number(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    if is_number(user_input): return int(float(user_input))
    
    if user_input.upper() in power_cards:
        return user_input.upper()
    else:
        return user_input.lower()

# return a 53 randomized ***interger*** list with 30 1s, 15 5s, 10 8s
def setup_water_cards():
    cards = [1]*30 + [5]*15 + [10]*8
    random.shuffle(cards)
    return cards

# return 15 ramdomized str list of power card, 10SOH, 2 DOT, 3DMT
def setup_power_cards():
    cards = [power_cards[0]]*10 + [power_cards[1]]*2 + [power_cards[2]]*3
    random.shuffle(cards)
    used_power_cards[:] = []
    return cards

#return tuple of 2 list with full size water and card pile,(int[53], str[15])
def setup_cards():
    return (setup_water_cards(), setup_power_cards())

# pop out element from list (pile:any[]) at index of (index: int) return popped out card
def get_card_from_pile(pile, index):
    card = pile.pop(index)
    return card
    
# modify the input list to the sorted order of [sortedInt, sortedString]
def arrange_cards(cards_list):
    water_cards = [card for card in cards_list if isinstance(card, int)]
    power_cards = [card for card in cards_list if isinstance(card, str)]
    water_cards.sort()
    power_cards.sort()
    cards_list[:] = water_cards + power_cards

# pass in two list and pop 6 in first and 4 in second list into each player, return tuple of two list with 5 card
def deal_cards(water_cards_pile, power_cards_pile):
    if len(water_cards_pile) < 6 or len(power_cards_pile) < 4: 
        print("not enough card")
        return
    Player_hand =[]
    computer_hand =[]
    for _ in range(3):
        Player_hand.append(water_cards_pile.pop(0))
        computer_hand.append(water_cards_pile.pop(0))
    
    for _ in range(2):
        Player_hand.append(power_cards_pile.pop(0))
        computer_hand.append(power_cards_pile.pop(0))

    arrange_cards(Player_hand)
    arrange_cards(computer_hand)

    return (Player_hand, computer_hand)
    
# apply over flow base on input int, return a new int
#tanklevel=apply_overflow(tank_level)
def apply_overflow(tank_level):
    return 80 - (tank_level - 80) if tank_level > 80 else tank_level
    
# use a card and adjust both tank, return tuple of new tank, NEED UNPACK AND ASSIGNIT TO TANK VALUE
# (player_tank, opponent_tank) = use_card(...)
def use_card(player_tank, card_to_use, player_cards, opponent_tank):
    if card_to_use not in player_cards:
        print("use_card(): you don't have that card!!!")
        return (player_tank, opponent_tank )

    match card_to_use:
        case 1 | 5 | 10:
            player_tank += card_to_use
        case "SOH":
            player_tank += opponent_tank//2
            opponent_tank //= 2
        case "DOT":
            opponent_tank = 0
        case "DMT":
            player_tank *= 2
        case _:
            print("invalid card")
            return (player_tank, opponent_tank)
    player_cards.remove(card_to_use) # <-if editor dont recognize remove(), define a array type on param if your school won't complain
    if isinstance(card_to_use, str):
        used_power_cards.append(card_to_use)
    player_tank = apply_overflow(player_tank)

    return (player_tank, opponent_tank)

# discard a target card and add it to the end or origninal pile return void
def discard_card(card_to_discard, player_cards, water_cards_pile, power_cards_pile):
    if card_to_discard not in player_cards or card_to_discard not in all_cards:
        print("discard_card get a valid card to discard")
        return
    water_cards_pile.append(card_to_discard) if card_to_discard in water_cards else power_cards_pile.append(card_to_discard)
    player_cards.remove(card_to_discard)

# did not check apply_overflow here, only true if tank is 75-80 (80-85 should be filled according to the overflow rule)
def filled_tank(tank):
    if not isinstance(tank, int):
        print("filled_tank get a invalid input")
    return 75 <= tank <= 80

# refil type of pile only if it is completly empty
def check_pile(pile, pile_type):
    if not len(pile):
        match pile_type:
            case "water":
                pile[:] = setup_water_cards()
            case "power":
                pile[:] = setup_power_cards()

# return tuple of both hands, NEED UNPACK ASSIGN TO NEW VALUE
#(tankA, tankB) = huam_play(...)
def human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, opponent_tank):
    print(f"Your water level: \n{human_tank}\ncomputer's water level: \n{opponent_tank}")
    print(f"Here is your hand: \n{human_cards}")
    input("It's your turn: \npress Enter to continue")


    player_action = ""
    while player_action != 'u' and player_action != 'd':
        player_action = get_user_input("would you like to use or discard a card?\nEnter 'u' to use a card \nEndter 'd' to discard a card")
    
    is_using = True if player_action == 'u' else False

    card_in_action = ''
    while card_in_action not in human_cards:
        print(f"Here is your hand: \n{human_cards}")
        card_in_action = get_user_input(f"Witch card would you like to {"use" if is_using else "discard"}")
    pile_type = water_cards_pile if card_in_action in water_cards else power_cards_pile

    if is_using:
        (human_tank, opponent_tank) = use_card(human_tank, card_in_action, human_cards, opponent_tank)
    else:
        discard_card(card_in_action, human_cards, water_cards_pile, power_cards_pile)
    print(f"you {"used" if is_using else "dicarded"} {card_in_action}")
    human_cards.append(get_card_from_pile(pile_type, 0))
    arrange_cards(human_cards)

    return (human_tank, opponent_tank)

# i need help un-mess this function lollololol-> return (HUMAN_TANK, COMPUTER_TANK)-> not the reverse
def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank):
    print(f"Your water level: \n{opponent_tank}\n computer's water level: \n{computer_tank}")
    input("It's computer's turn: \npress Enter to continue")

    existing_SOH_in_pile, existing_DOT_in_pile, existing_DMT_in_pile = 10, 2, 3
    for pc in used_power_cards:
        if pc == "SOH":
            existing_SOH_in_pile -= 1
        elif pc == "DOT":
            existing_DOT_in_pile -= 1
        elif pc == "DMT":
            existing_DMT_in_pile -= 1
    for pc in computer_cards:
        if pc == "SOH":
            existing_SOH_in_pile -= 1
        elif pc == "DOT":
            existing_DOT_in_pile -= 1
        elif pc == "DMT":
            existing_DMT_in_pile -= 1
    # ------------immediate winning case-----------------
    if 38 <= computer_tank <= 42 and "DMT" in computer_cards:
        print(f"computer is using: DMT")
        (computer_tank, opponent_tank) = use_card(computer_tank, "DMT", computer_cards, opponent_tank)
        computer_cards.append(get_card_from_pile(power_cards_pile, 0))
        arrange_cards(computer_cards)
        return (opponent_tank, computer_tank)
    elif 75 <= computer_tank + (opponent_tank//2) <= 85 and "SOH" in computer_cards:
        print(f"computer is using: SOH")
        (computer_tank, opponent_tank) = use_card(computer_tank, "SOH", computer_cards, opponent_tank)
        computer_cards.append(get_card_from_pile(power_cards_pile, 0))
        arrange_cards(computer_cards)
        return (opponent_tank, computer_tank)
    elif computer_tank >= 74:
        print(f"computer is using: {computer_cards[0]}")
        (computer_tank, opponent_tank) = use_card(computer_tank, computer_cards[0], computer_cards, opponent_tank)
        computer_cards.append(get_card_from_pile(water_cards_pile, 0))
        arrange_cards(computer_cards)
        return (opponent_tank, computer_tank)
    elif computer_tank >= 70 and 5 in computer_cards:
        print(f"computer is using: 5")
        (computer_tank, opponent_tank) = use_card(computer_tank, 5, computer_cards, opponent_tank)
        computer_cards.append(get_card_from_pile(water_cards_pile, 0))
        arrange_cards(computer_cards)
        return (opponent_tank, computer_tank)
    elif computer_tank >= 65 and 10 in computer_cards:
        print(f"computer is using: 10")
        (computer_tank, opponent_tank) = use_card(computer_tank, 10, computer_cards, opponent_tank)
        computer_cards.append(get_card_from_pile(water_cards_pile, 0))
        arrange_cards(computer_cards)
        return (opponent_tank, computer_tank)
    else:
        #-------------prevent player immediate win------------
        if 38 <= computer_tank <= 42 and existing_DMT_in_pile:
            if "SOH" in computer_cards:
                print(f"computer is using: SOH")
                (computer_tank, opponent_tank) = use_card(computer_tank, "SOH", computer_cards, opponent_tank)
            elif "DOT" in computer_cards:
                print(f"computer is using: DOT")
                (computer_tank, opponent_tank) = use_card(computer_tank, "DOT", computer_cards, opponent_tank)
            computer_cards.append(get_card_from_pile(power_cards_pile, 0))
            arrange_cards(computer_cards)
            return (opponent_tank, computer_tank)
        elif 75 <= computer_tank + (opponent_tank//2) <= 85 and existing_SOH_in_pile:
            if "SOH" in computer_cards:
                print(f"computer is using: SOH")
                (computer_tank, opponent_tank) = use_card(computer_tank, "SOH", computer_cards, opponent_tank)
            elif "DOT" in computer_cards:
                print(f"computer is using: DOT")
                (computer_tank, opponent_tank) = use_card(computer_tank, "DOT", computer_cards, opponent_tank)
            computer_cards.append(get_card_from_pile(power_cards_pile, 0))
            arrange_cards(computer_cards)
            return (opponent_tank, computer_tank)
        elif opponent_tank >= 65:
            if "SOH" in computer_cards:
                print(f"computer is using: SOH")
                (computer_tank, opponent_tank) = use_card(computer_tank, "SOH", computer_cards, opponent_tank)
            elif "DOT" in computer_cards:
                print(f"computer is using: DOT")
                (computer_tank, opponent_tank) = use_card(computer_tank, "DOT", computer_cards, opponent_tank)
            computer_cards.append(get_card_from_pile(power_cards_pile, 0))
            arrange_cards(computer_cards)
            return (opponent_tank, computer_tank)
        else:
            #------increase tank with water card (could implement logic try to get immediate winning condition next turn)---
            print(f"computer is using: {computer_cards[2]}")
            (computer_tank, opponent_tank) = use_card(computer_tank, computer_cards[2], computer_cards, opponent_tank)
            computer_cards.append(get_card_from_pile(water_cards_pile, 0))
            arrange_cards(computer_cards)
            return (opponent_tank, computer_tank)



def main():
    # print(game_instruction)
    # input("Press Enter to start the game")
    player_tank, computer_tank = 0, 0
    (water_pile, power_pile) = setup_cards()
    (player_hand, computer_hand) = deal_cards(water_pile, power_pile)
    roll = input("lets decide who play first by enter your favorate quote:")
    dice = random.randint(0, 1)
    is_player_first = len(roll) % 2 == dice

    winner = ''

    while(not winner):
        if(not len(water_pile)):
            water_pile[:] = setup_water_cards()
        if(not len(power_pile)):
            power_pile[:] = setup_power_cards()

        (player_tank, computer_tank) = human_play(player_tank,player_hand,water_pile,power_pile,computer_tank) if is_player_first else computer_play(computer_tank,computer_hand,water_pile, power_pile,player_tank)

        (player_tank, computer_tank) = computer_play(computer_tank,computer_hand,water_pile, power_pile,player_tank) if is_player_first else human_play(player_tank,player_hand,water_pile,power_pile,computer_tank)

        if 75 <= player_tank <= 85: 
            winner = "Player"
        elif 75 <= computer_tank <= 85: 
            winner = "Computer"
    
    print(f"Player: {player_tank} vs. Computer: {computer_tank}")
    print(f"\n****Winner is: {winner}!!!****\n\n")
    restart = input("Would you like to start over?\nEnter 'Y' to start over\nEnter anything else to quit game.")

    if restart.lower() == 'y':
        main()
    else:
        print("\n\n**********Thank you for playing my game :)***************")




if __name__ == '__main__':
    main()