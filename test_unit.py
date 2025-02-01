import water_tank


def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank):
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
        (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, "DMT", computer_cards, opponent_tank)
        computer_cards.append(water_tank.get_card_from_pile(power_cards_pile, 0))
        water_tank.arrange_cards(computer_cards)
        return (computer_tank, opponent_tank)
    elif 75 <= computer_tank + (opponent_tank//2) <= 85 and "SOH" in computer_cards:
        print(f"computer is using: SOH")
        (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, "SOH", computer_cards, opponent_tank)
        computer_cards.append(water_tank.get_card_from_pile(power_cards_pile, 0))
        water_tank.arrange_cards(computer_cards)
        return (computer_tank, opponent_tank)
    elif computer_tank >= 74:
        print(f"computer is using: {computer_cards[0]}")
        (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, computer_cards[0], computer_cards, opponent_tank)
        computer_cards.append(water_tank.get_card_from_pile(water_cards_pile, 0))
        water_tank.arrange_cards(computer_cards)
        return (computer_tank, opponent_tank)
    elif computer_tank >= 70 and 5 in computer_cards:
        print(f"computer is using: 5")
        (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, 5, computer_cards, opponent_tank)
        computer_cards.append(water_tank.get_card_from_pile(water_cards_pile, 0))
        water_tank.arrange_cards(computer_cards)
        return (computer_tank, opponent_tank)
    elif computer_tank >= 65 and 10 in computer_cards:
        print(f"computer is using: 10")
        (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, 10, computer_cards, opponent_tank)
        computer_cards.append(water_tank.get_card_from_pile(water_cards_pile, 0))
        water_tank.arrange_cards(computer_cards)
        return (computer_tank, opponent_tank)
    else:
        #-------------prevent player immediate win------------
        if 38 <= opponent_tank <= 42 and existing_DMT_in_pile:
            if "SOH" in computer_cards:
                print(f"computer is using: SOH")
                (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, "SOH", computer_cards, opponent_tank)
            elif "DOT" in computer_cards:
                print(f"computer is using: DOT")
                (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, "DOT", computer_cards, opponent_tank)
            computer_cards.append(water_tank.get_card_from_pile(power_cards_pile, 0))
            water_tank.arrange_cards(computer_cards)
            return (computer_tank, opponent_tank)
        elif 75 <= opponent_tank + (computer_tank//2) <= 85 and existing_SOH_in_pile:
            if "SOH" in computer_cards:
                print(f"computer is using: SOH")
                (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, "SOH", computer_cards, opponent_tank)
            elif "DOT" in computer_cards:
                print(f"computer is using: DOT")
                (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, "DOT", computer_cards, opponent_tank)
            computer_cards.append(water_tank.get_card_from_pile(power_cards_pile, 0))
            water_tank.arrange_cards(computer_cards)
            return (computer_tank, opponent_tank)
        elif opponent_tank >= 65:
            if "SOH" in computer_cards:
                print(f"computer is using: SOH")
                (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, "SOH", computer_cards, opponent_tank)
            elif "DOT" in computer_cards:
                print(f"computer is using: DOT")
                (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, "DOT", computer_cards, opponent_tank)
            computer_cards.append(water_tank.get_card_from_pile(power_cards_pile, 0))
            water_tank.arrange_cards(computer_cards)
            return (computer_tank, opponent_tank)
        else:
            #------increase tank with water card (could implement logic try to get immediate winning condition next turn)---
            print(f"computer is using: {computer_cards[2]}")
            (computer_tank, opponent_tank) = water_tank.use_card(computer_tank, computer_cards[2], computer_cards, opponent_tank)
            computer_cards.append(water_tank.get_card_from_pile(water_cards_pile, 0))
            water_tank.arrange_cards(computer_cards)
            return (computer_tank, opponent_tank)


used_power_cards = []
computer_tank=22
opponent_tank=64
computer_cards=[1,5,10, "DMT", "DOT"]
water_cards_pile=[5, 1, 1, 1, 1, 5, 1, 10, 1, 10, 5, 1, 1, 5, 1]
power_cards_pile=['SOH', 'SOH', 'DOT', 'DMT', 'DOT', 'SOH', 'SOH']

(computer_tank, opponent_tank) = computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank)
print("computer_tank: ",computer_tank)
print("opponent_tank: ", opponent_tank)
print("computer_cards: ",computer_cards)
print("water_cards_pile: ",water_cards_pile)
print("power_cards_pile: ",power_cards_pile)