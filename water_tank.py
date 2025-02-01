import random


power_cards = ("SOH", "DOT", "DMT")
water_cards = (1, 5, 10)

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
    return cards

#return tuple of 2 list with full size water and card pile,(int[53], str[15])
def setup_cards():
    return (setup_water_cards(), setup_power_cards())

# pop out element from list (pile:any[]) at index of (index: int)
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


def deal_cards(water_cards_pile, power_cards_pile):
    pass

def apply_overflow(tank_level):
    pass

def use_card(player_tank, card_to_use, player_cards, opponent_tank):
    pass

def discard_card(card_to_discard, player_cards, water_cards_pile, power_cards_pile):
    pass

def filled_tank(tank):
    pass

def check_pile(pile, pile_type):
    pass

def human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, opponent_tank):
    pass

def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank):
    pass

def main():
    pass

if __name__ == '__main__':
    main()