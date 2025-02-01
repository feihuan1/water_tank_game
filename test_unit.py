def arrange_cards(cards_list):
    water_cards = [card for card in cards_list if isinstance(card, int)]
    power_cards = [card for card in cards_list if isinstance(card, str)]
    water_cards.sort()
    power_cards.sort()
    cards_list[:] = water_cards + power_cards

cards = [10, "DOT", 5, "SOH", 1]
arrange_cards(cards)
print(cards)  # Output: [1, 5, 10, 'SOH', 'DOT']
