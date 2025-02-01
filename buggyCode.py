# import statements
from random import shuffle


# TODO: Write the functions as described in the instructions

def get_user_input(question):
    """
    Takes in a string as its argument, to be used as the question that the game wants the user to be asked.
    Remove leading and trailing whitespaces.
    If the length of the user input after removing leading and trailing whitespaces is 0, reprompt the question.
    If the input is a number, cast and return an integer type.
    If the input is a power card, return the power card as an uppercase string.
    If the input is any other string, return the string as a lowercase string.
    Returns: A post-processed user input
    """

    # take the question paramter to get user input
    user_input = input(question)

    # remove leading and trailing whitespaces
    stripped_user_input = user_input.strip()

    # if the length of the stripped_user_input is 0, reprompt the question
    while len(stripped_user_input) == 0:
        user_input = input(question)
        stripped_user_input = user_input.strip()

    # if the input is a number, cast and return an integer type.
    if stripped_user_input.isnumeric():
        return int(stripped_user_input)

    # if the input is a power card, return the power card as an uppercase string.
    if stripped_user_input.upper() in ("SOH", "DOT", "DMT"):
        stripped_user_input = stripped_user_input.upper()

    # If the input is any other string, return the string as a lowercase string.
    else:
        stripped_user_input = stripped_user_input.lower()

    return stripped_user_input


def setup_water_cards():
    """
    Create a shuffled list of water cards with given values and quantities.
    for value and quantity of cards, we use following convention:
        1. Water cards with value 1, there are 30 cards
        2. Water cards with value 5, there are 15 cards
        3. Water cards with value 10, there are 8 cards
    Returns: A list of random integer as water cards.
    """

    # create a list of water cards that contains 30 cards with value 1
    value_one_lst = [1] * 30

    # create a list of water cards that contains 15 cards with value 5
    value_five_lst = [5] * 15

    # create a list of water cards that contains 8 cards with value 10
    value_eight_lst = [10] * 8

    # create a list that combine all three values of water cards
    sum_water_card = value_one_lst + value_five_lst + value_eight_lst

    # use the shuffle function to generate the random integer list
    shuffle(sum_water_card)

    return sum_water_card


def setup_power_cards():
    """
    Create a shuffled list of power cards with the given values and quantities.
      1. There are 10 cards of "SOH".
      2. There are 2 cards of "DOT".
      3. There are 3 cards of "DMT".
    Returns: A list of random integer as power cards.
    """

    # create a list of power cards that contains 10 cards of "SOH"
    soh_lst = ["SOH"] * 10

    # create a list of power cards that contains 2 cards of "DOT"
    dot_lst = ["DOT"] * 2

    # create a list of power cards that contains 3 cards of "DMT"
    dmt_lst = ["DMT"] * 3

    # create a list that combines all power cards
    sum_power_card = soh_lst + dot_lst + dmt_lst

    # use the shuffle function to generate a random power card list
    shuffle(sum_power_card)

    return sum_power_card


def setup_cards():
    """
    Create both water card and power card lists using setup_water_cards and setup_power_cards functions.
    Returns: A 2-tupe with water cards pile and the power cards pile
    """

    # create a water card list
    water_cards = setup_water_cards()

    # create a power card list
    power_cards = setup_power_cards()

    return (water_cards, power_cards)


def get_card_from_pile(pile, index):
    """
    Removes the entry at the specified index of the given pile (water or power) and modifies the pile by reference.
    Returns: A card at the specified index.
    """
    card_picked = pile[index]

    pile.pop(index)

    return card_picked


def arrange_cards(cards_list):
    """
    Arrange the players cards such that:
      1. The first three indices are water cards, sorted in ascending order.
      2. The last two indices are power cards, sorted in alphabetical order.
    No Return
    """
    water_cards_list = []
    power_cards_list = []

    for card in cards_list:
        if isinstance(card, int):
            water_cards_list.append(card)
        else:
            power_cards_list.append(card)

    # Sort the first 3 indices (water cards) in ascending order
    water_cards_list.sort()

    # Sort the last 2 elements (power cards) in ascending order
    power_cards_list.sort()

    cards_list[:] = water_cards_list + power_cards_list


def deal_cards(water_cards_pile, power_cards_pile):
    """
    Deals cards to player 1 and player 2. Each player would get 3 water cards and 2 power cards.
    Then, call the arrange_cards function to arrange the cards.
    When dealing, alternately take off a card from the first entry in the pile.
    Returns: A 2-tuple containing the cards of player 1 and player 2
    """
    player_1_cards = []
    player_2_cards = []

    # deal three water cards to the two players
    for card in range(3):
        player_1_cards.append(water_cards_pile.pop(0))
        player_2_cards.append(water_cards_pile.pop(0))

    # deal two power cards to the two players
    for card in range(2):
        player_1_cards.append(power_cards_pile.pop(0))
        player_2_cards.append(power_cards_pile.pop(0))

    # arrange the cards for each player
    arrange_cards(player_1_cards)
    arrange_cards(player_2_cards)

    return (player_1_cards, player_2_cards)


def apply_overflow(tank_level):
    """
    Calculate the overflow when the water level of a player exceeds the maximum fill value of the tank.
    The amount of water that remains in the tank is determined by a formula: remaining water = maximum fill value - overflow
    Returns: the tank level
    """

    max_tank_capacity = 80

    if tank_level > max_tank_capacity:
        overflow = tank_level - max_tank_capacity
        tank_level = max_tank_capacity - overflow

    return tank_level


def use_card(player_tank, card_to_use, player_cards, opponent_tank):
    """
    Get that card from the player, and update the tank level based on the card that was used.
    Remove the card once card_to_use is used. Apply overflow if necessary.
    Returns: A 2-tuple containing the player_tank and the opponent_tank
    """

    # update the player tank based the card that was used
    if isinstance(card_to_use, int):
        player_tank += card_to_use
    elif card_to_use == "SOH":
        player_tank += int(opponent_tank / 2)
        opponent_tank -= int(opponent_tank / 2)
    elif card_to_use == "DOT":
        opponent_tank = 0
    elif card_to_use == "DMT":
        player_tank = player_tank * 2

    # remove the card after use it
    player_cards.remove(card_to_use)

    # apply overflow if needed
    player_tank = apply_overflow(player_tank)

    return (player_tank, opponent_tank)


def discard_card(card_to_discard, player_cards, water_cards_pile, power_cards_pile):
    """
    Discard the given card from the player and return it to the bottom of the appropriate pile.
    Water cards should go in the water card pile and power cards should go in the power card pile.
    Remove the card once card_to_discard is used.
    No Return
    """
    if isinstance(card_to_discard, int):
        water_cards_pile.append(card_to_discard)

    elif isinstance(card_to_discard, str):
        power_cards_pile.append(card_to_discard)

    if card_to_discard in player_cards:
        player_cards.remove(card_to_discard)


def filled_tank(tank):
    """
    Determine if the tank level is between the maximum and minimum fill values (inclusive).
    Returns: A boolean indicates whether the tank is filled
    """
    # define the maximum and minimum fill values (inclusive)
    max_fill_value = 80
    min_fill_value = 75

    # if the tank is filled, return True, otherwise, return False
    if min_fill_value <= tank <= max_fill_value:
        return True
    else:
        return False


def check_pile(pile, pile_type):
    """
    Checks if the given pile is empty. If so, call the pile setup function to replenish the pile.
    Use pile_type to determine which type of pile needs to replenish.
    No Return
    """
    if len(pile) == 0:
        if pile_type == "water":
            pile[:] = setup_water_cards()
        else:
            pile[:] = setup_power_cards()


def human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, opponent_tank):
    """
    """
    print(human_tank)
    print(opponent_tank)
    print(human_cards)

    human_choice = ""

    while human_choice != "u" and human_choice != "d":
        human_choice = get_user_input("Do you want to use or discard the card? ")

    pick_card = ""

    while pick_card not in human_cards:
        pick_card = get_user_input("Which card do you want to play? ")

    print(pick_card)

    if human_choice == "u":
        human_tank, opponent_tank = use_card(human_tank, pick_card, human_cards, opponent_tank)
        if filled_tank(human_tank):
            human_tank = apply_overflow(human_tank)

    elif human_choice == "d":
        discard_card(pick_card, human_cards, water_cards_pile, power_cards_pile)

    if isinstance(pick_card, int):
        new_card = get_card_from_pile(water_cards_pile, 0)
        human_cards.append(new_card)
    else:
        new_card = get_card_from_pile(power_cards_pile, 0)
        human_cards.append(new_card)

    arrange_cards(human_cards)

    print(human_tank)
    print(opponent_tank)
    print(human_cards)

    return (human_tank, opponent_tank)


def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank):
    """
    """

    print(computer_tank)
    print(opponent_tank)
    print(computer_cards)

    for card in computer_cards:
        if isinstance(card, int):
            new_computer_tank = computer_tank + card
            if new_computer_tank > 80:
                new_computer_tank = apply_overflow(new_computer_tank)
            if filled_tank(new_computer_tank):
                computer_tank, opponent_tank = use_card(computer_tank, card, computer_cards, opponent_tank)

    for card in computer_cards:
        if card == "SOH":
            # SOH card halves the opponent's tank and adds to the computer's tank.
            half_opponent_tank = int(opponent_tank / 2)
            new_computer_tank = computer_tank + half_opponent_tank

            # Check if the computer's tank exceeds 80 and handle overflow
            if new_computer_tank > 80:
                new_computer_tank = apply_overflow(new_computer_tank)

            # Update the computer's tank with the new value
            if filled_tank(new_computer_tank):  # Ensure the tank is valid
                computer_tank, opponent_tank = use_card(computer_tank, card, computer_cards, opponent_tank)

        elif card == "DOT" and opponent_tank > 50:
            computer_tank, opponent_tank = use_card(computer_tank, card, computer_cards, opponent_tank)

        elif card == "DMT":
            double_computer_tank = computer_tank * 2
            if double_computer_tank > 80:
                double_computer_tank = apply_overflow(double_computer_tank)
            if filled_tank(double_computer_tank):
                computer_tank, opponent_tank = use_card(computer_tank, card, computer_cards, opponent_tank)

    # Solution 2

    # pick_card = None
    # for card in computer_cards:
    #   if isinstance(card, int):
    #     new_computer_tank = computer_tank + card
    #     if new_computer_tank > 80:
    #       new_computer_tank = apply_overflow(new_computer_tank)
    #     if filled_tank(new_computer_tank):
    #       computer_tank, opponent_tank = use_card(computer_tank, card, computer_cards, opponent_tank)
    #       pick_card = card
    #       break
    #     else:
    #       discard_card(card, computer_cards, water_cards_pile, power_cards_pile)

    #   elif isinstance(card, str):
    #     if card == "SOH":
    #       # SOH card halves the opponent's tank and adds to the computer's tank.
    #       half_opponent_tank = int(opponent_tank / 2)
    #       new_computer_tank = computer_tank + half_opponent_tank

    #       # Check if the computer's tank exceeds 80 and handle overflow
    #       if new_computer_tank > 80:
    #         new_computer_tank = apply_overflow(new_computer_tank)

    #       # Update the computer's tank with the new value
    #       if filled_tank(new_computer_tank):  # Ensure the tank is valid
    #         computer_tank, opponent_tank = use_card(computer_tank, card, computer_cards, opponent_tank)
    #         pick_card = card
    #         break
    #       else:
    #         discard_card(card, computer_cards, water_cards_pile, power_cards_pile)
    #     elif card == "DOT":
    #       if opponent_tank >= 65 or 38 <= opponent_tank <= 42:
    #         computer_tank, opponent_tank = use_card(computer_tank, card, computer_cards, opponent_tank)
    #         pick_card = card
    #       else:
    #         discard_card(card, computer_cards, water_cards_pile, power_cards_pile)
    #     elif card == "DMT":
    #       double_computer_tank = computer_tank * 2
    #       if double_computer_tank > 80:
    #         double_computer_tank = apply_overflow(double_computer_tank)
    #         if filled_tank(double_computer_tank):
    #           computer_tank, opponent_tank = use_card(computer_tank, card, computer_cards, opponent_tank)
    #           pick_card = card
    #           break
    #       else:
    #         discard_card(card, computer_cards, water_cards_pile, power_cards_pile)

    # if isinstance(pick_card, int):
    #   new_card = get_card_from_pile(water_cards_pile, 0)
    #   computer_cards.append(new_card)
    # else:
    #   new_card = get_card_from_pile(power_cards_pile, 0)
    #   computer_cards.append(new_card)

    arrange_cards(computer_cards)

    print(computer_tank)
    print(opponent_tank)
    print(computer_cards)

    return (computer_tank, opponent_tank)


def main():
    # TODO: Write your code as described in the instructions
    pass


if __name__ == '__main__':
    main()
