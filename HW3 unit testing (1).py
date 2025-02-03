import inspect
import unittest
from random import randint, choice
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch
from timeout_decorator import timeout

import water_tank


class Test(unittest.TestCase):
    ###############################################
    ### Test Cases for checking argument names  ###
    ###############################################

    def test_signature_for_computer_play(self):
        sig = inspect.signature(water_tank.computer_play)
        names = list(sig.parameters.keys())
        self.assertEqual(['computer_tank',
                          'computer_cards',
                          'water_cards_pile',
                          'power_cards_pile',
                          'opponent_tank'],
                         names,
                         "The argument names and order in the computer_play function should appear like this "
                         "so our tests work:\ncomputer_tank computer_cards water_cards_pile power_cards_pile opponent_tank")
        self.assertEqual(5, len(names), "The computer_play function should have exactly 5 arguments")

    def test_signature_for_human_play(self):
        sig = inspect.signature(water_tank.human_play)
        names = list(sig.parameters.keys())
        self.assertEqual(['human_tank',
                          'human_cards',
                          'water_cards_pile',
                          'power_cards_pile',
                          'opponent_tank'],
                         names,
                         "The argument names and order in the human_play function should appear like this so our tests work:\n"
                         "human_tank human_cards water_cards_pile power_cards_pile opponent_tank")
        self.assertEqual(5, len(names), "The human_play function should have exactly 5 arguments")

    def test_signature_for_use_card(self):
        sig = inspect.signature(water_tank.use_card)
        names = list(sig.parameters.keys())
        self.assertEqual(['player_tank', 'card_to_use', 'player_cards', 'opponent_tank'], names,
                         "The use_card function should have exactly 4 arguments")
        self.assertEqual(4, len(names), "The use_card function should have exactly 4 arguments")

    def test_signature_for_check_pile(self):
        sig = inspect.signature(water_tank.check_pile)
        names = list(sig.parameters.keys())
        self.assertEqual(['pile', 'pile_type'], names,
                         "The check_pile function should have exactly 2 arguments")
        self.assertEqual(2, len(names), "The check_pile function should have exactly 2 arguments")

    def test_signature_for_get_card_from_pile(self):
        sig = inspect.signature(water_tank.get_card_from_pile)
        names = list(sig.parameters.keys())
        self.assertEqual(['pile', 'index'], names,
                         "The get_card_from_pile function should have exactly 2 arguments")
        self.assertEqual(2, len(names), "The get_card_from_pile function should have exactly 2 arguments")

    def test_signature_for_deal_cards(self):
        sig = inspect.signature(water_tank.get_card_from_pile)
        names = list(sig.parameters.keys())
        self.assertEqual(['pile', 'index'], names,
                         "The deal_cards function should have exactly 2 arguments")
        self.assertEqual(2, len(names), "The deal_cards function should have exactly 2 arguments")

    def test_signature_for_discard_card(self):
        sig = inspect.signature(water_tank.get_card_from_pile)
        names = list(sig.parameters.keys())
        self.assertEqual(['pile', 'index'], names,
                         "The discard_card function should have exactly 2 arguments")
        self.assertEqual(2, len(names), "The discard_card function should have exactly 2 arguments")

    def test_signature_for_single_argument_functions(self):
        functions = ['arrange_cards', 'filled_tank', 'apply_overflow', 'get_user_input']
        valid = True
        for function_name in functions:
            function = getattr(water_tank, function_name)
            sig = inspect.signature(function)
            names = list(sig.parameters.keys())
            if len(names) != 1:
                valid = False
                break
        self.assertEqual(True, valid, "There should only be one argument for the following functions:\n"
                                      "    -- arrange_cards\n"
                                      "    -- filled_tank\n"
                                      "    -- apply_overflow\n"
                                      "    -- get_user_input")

    def test_signature_for_zero_argument_functions(self):
        functions = ['setup_water_cards', 'setup_power_cards', 'setup_cards']
        valid = True
        for function_name in functions:
            function = getattr(water_tank, function_name)
            sig = inspect.signature(function)
            names = list(sig.parameters.keys())
            if len(names) != 0:
                valid = False
                break
        self.assertEqual(True, valid, "There should not be any arguments for the following functions:\n"
                                      "    -- setup_water_cards\n"
                                      "    -- setup_power_cards\n"
                                      "    -- setup_cards")

    ######################################
    ###Test Cases for get_user_input###
    ######################################
    @patch('water_tank.input', side_effect=['SOH', 'DOT', 'DOT', 'DMT', 'SOH'])
    @timeout(3, exception_message="Check the get_user_input function for infinite loops")
    def test_get_user_input_with_with_several_correct_entries(self, one):
        return_values = []
        for i in range(5):
            value = water_tank.get_user_input("question")
            return_values.append(value)
        # decided not to test water value inputs here, just in case they decide to convert to int within this function
        self.assertEqual(['SOH', 'DOT', 'DOT', 'DMT', 'SOH'], return_values,
                         "The get_user_input function doesn't capture valid input properly.")

    @patch('water_tank.input', side_effect=['', '', '', 'SOH'])
    @timeout(3, exception_message="Check the get_user_input function for infinite loops")
    def test_get_string_input_with_several_enters_first(self, one):
        with patch('sys.stdout'):
            return_value = water_tank.get_user_input("question")
        self.assertEqual('SOH', return_value,
                         "The get_user_input function should re-prompt and accept new input when given an invalid response")

    @patch('water_tank.input', side_effect=['soh', 'dot', 'dmt'])
    @timeout(3, exception_message="Check the get_user_input function for infinite loops")
    def test_get_user_input_power_card_lowercase(self, one):
        return_values = []
        for entry in range(3):
            value = water_tank.get_user_input("question")
            return_values.append(value)
        self.assertEqual(['SOH', 'DOT', 'DMT'], return_values,
                         "The get_user_input function doesn't capture lowercase power card entries.")

    @patch('water_tank.input', side_effect=['1', '5', '10'])
    @timeout(3, exception_message="Check the get_user_input function for infinite loops")
    def test_get_user_input_water_card(self, one):
        return_values = []
        for entry in range(3):
            value = water_tank.get_user_input("question")
            return_values.append(value)
        self.assertEqual([1, 5, 10], return_values,
                         "The get_user_input function doesn't capture water card entries.")

    @patch('water_tank.input', side_effect=['  u  ', ' U', ' d  ', ' D'])
    @timeout(3, exception_message="Check the get_user_input function for infinite loops")
    def test_get_user_input_string_input(self, one):
        return_values = []
        for entry in range(4):
            value = water_tank.get_user_input("question")
            return_values.append(value)
        self.assertEqual(['u', 'u', 'd', 'd'], return_values,
                         "The get_user_input function doesn't strip leading and trailing whitespaces and/or convert "
                         "non-power card strings to lowercase.")

    ######################################
    ###Test Cases for setup_water_cards###
    ######################################

    @timeout(3, exception_message="Check the setup_water_cards function for infinite loops")
    def test_setup_water_cards_length_of_array(self):
        """
        Test the number of water cards is 53 (30 + 15 + 8)
        """
        self.assertEqual(53, len(water_tank.setup_water_cards()), "There should be 53 total cards")

    @timeout(3, exception_message="Check the setup_water_cards function for infinite loops")
    def test_setup_water_cards_successful_shuffle(self):
        """
        Test that water cards get shuffled by checking if the first 8 items are all the same
        """
        water_shuffle = water_tank.setup_water_cards()
        unshuffled = []
        unshuffled.append([1 for i in range(30)] + [5 for i in range(15)] + [10 for i in range(8)])
        unshuffled.append([1 for i in range(30)] + [10 for i in range(8)] + [5 for i in range(15)])
        unshuffled.append([5 for i in range(15)] + [10 for i in range(8)] + [1 for i in range(30)])
        unshuffled.append([5 for i in range(15)] + [1 for i in range(30)] + [10 for i in range(8)])
        unshuffled.append([10 for i in range(8)] + [1 for i in range(30)] + [5 for i in range(15)])
        unshuffled.append([10 for i in range(8)] + [5 for i in range(15)] + [1 for i in range(30)])

        self.assertNotIn(water_shuffle, unshuffled, "The water cards do not appear to have shuffled")

    @timeout(3, exception_message="Check the setup_water_cards function for infinite loops")
    def test_setup_water_cards_card_count(self):
        """
        Counts each card type
        """
        water_cards = water_tank.setup_water_cards()
        self.assertEqual(30, water_cards.count(1),
                         "There should be 30 x water cards with value 1 after setting up the cards")
        self.assertEqual(15, water_cards.count(5),
                         "There should be 15 x water cards with value 5 after setting up the cards")
        self.assertEqual(8, water_cards.count(10),
                         "There should be 8 x water cards with value 10 after setting up the cards")

    ############################################
    ###   Test Cases for setup_power_cards   ###
    ############################################

    @timeout(3, exception_message="Check the setup_power_cards function for infinite loops")
    def test_setup_power_cards_length_of_array(self):
        self.assertEqual(15, len(water_tank.setup_power_cards()),
                         "There should be 15 power cards total after setting up the cards")

    @timeout(3, exception_message="Check the setup_power_cards function for infinite loops")
    def test_setup_power_cards_successful_shuffle(self):
        """
        Test that power cards get shuffled by checking if the first items are all the same
        """
        power_shuffle = water_tank.setup_power_cards()
        unshuffled = []
        unshuffled.append(["SOH" for i in range(10)] + ["DOT" for i in range(2)] + ["DMT" for i in range(3)])
        unshuffled.append(["SOH" for i in range(10)] + ["DMT" for i in range(3)] + ["DOT" for i in range(2)])
        unshuffled.append(["DMT" for i in range(3)] + ["DOT" for i in range(2)] + ["SOH" for i in range(10)])
        unshuffled.append(["DMT" for i in range(3)] + ["SOH" for i in range(10)] + ["DOT" for i in range(2)])
        unshuffled.append(["DOT" for i in range(2)] + ["DMT" for i in range(3)] + ["SOH" for i in range(10)])
        unshuffled.append(["DOT" for i in range(2)] + ["SOH" for i in range(10)] + ["DMT" for i in range(3)])

        self.assertNotIn(power_shuffle, unshuffled, "It doesn't look like the power cards shuffled")

    @timeout(3, exception_message="Check the setup_power_cards function for infinite loops")
    def test_setup_power_cards_card_count(self):

        power_shuffle = water_tank.setup_power_cards()
        self.assertEqual(10, power_shuffle.count("SOH"), "There should be 10 SOH cards after shuffling")
        self.assertEqual(2, power_shuffle.count("DOT"), "There should be 2 DOT cards after shuffling")
        self.assertEqual(3, power_shuffle.count("DMT"), "There should be 3 DMT cards after shuffling")

    #############################################
    ###   Test Cases for setup_cards          ###
    #############################################
    @timeout(3, exception_message="Check the setup_cards function for infinite loops")
    def test_setup_cards(self):
        water_cards_pile, power_cards_pile = water_tank.setup_cards()
        self.assertIsInstance(water_cards_pile[0], int, "Water cards pile should be a list of integers")
        self.assertIsInstance(power_cards_pile[0], str, "Power cards pile should be a list of strings")

    #############################################
    ###   Test Cases for get_card_from_pile   ###
    #############################################

    @timeout(3, exception_message="Check the get_card_from_pile function for infinite loops")
    def test_get_card_from_pile(self):
        """
        Make sure the return values match and the selected cards pop off
        """
        mock_pile = [1, 5, 5, 10, 1, 1, 1, 5]
        self.assertEqual(1, water_tank.get_card_from_pile(mock_pile, 0),
                         "Check the return value for the get_card_from_pile function")
        self.assertEqual(5, mock_pile[0], "Check if the selected value is popped from the list")
        self.assertEqual(10, water_tank.get_card_from_pile(mock_pile, 2),
                         "Check the return value for the get_card_from_pile function")
        self.assertEqual(0, mock_pile.count(10), "Check if the selected value is popped from the list")
        self.assertEqual(3, mock_pile.count(5), "Check if popping from the list manipulates more than one list item")
        self.assertEqual(3, mock_pile.count(1), "Check if popping from the list manipulates more than one list item")
        self.assertEqual(6, len(mock_pile),
                         "The number of items in the list is not as expected after several operations")

    #####################################
    ###   Test Cases for deal_cards   ###
    #####################################

    @timeout(3, exception_message="Check the deal_cards function for infinite loops")
    def test_deal_cards_5_cards_each_deck(self):
        mock_power_cards = ['SOH', 'SOH', 'DOT', 'DMT', 'DOT', 'SOH', 'SOH', 'DMT',
                            'SOH', 'SOH', 'SOH', 'SOH', 'DMT', 'SOH', 'SOH']
        mock_water_cards = [5, 1, 1, 1, 1, 5, 1, 10, 1, 10, 5, 1, 1, 5, 1, 1, 5, 10, 1, 1, 5, 10, 5, 1, 1, 1, 10, 1, 5,
                            1, 5, 1, 5, 1, 5, 1, 5, 1, 10, 1, 1, 10, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 10]
        # count to make sure there are 5 cards in each deck
        player_1_cards, player_2_cards = water_tank.deal_cards(mock_water_cards, mock_power_cards)
        self.assertEqual(5, len(player_1_cards),
                         "After dealing cards, Player 1 does not have 5 cards")
        self.assertEqual(5, len(player_2_cards),
                         "After dealing cards, Player 2 does not have 5 cards")
        water_1 = player_1_cards[:3]
        power_1 = player_1_cards[3:]
        water_2 = player_2_cards[:3]
        power_2 = player_2_cards[3:]
        self.assertListEqual(sorted(water_1), water_1, "Player 1 cards were not arranged.")
        self.assertListEqual(sorted(water_2), water_2, "Player 2 cards were not arranged.")
        self.assertListEqual(sorted(power_1), power_1, "Player 1 cards were not arranged.")
        self.assertListEqual(sorted(power_2), power_2, "Player 2 cards were not arranged.")

    @timeout(3, exception_message="Check the deal_cards function for infinite loops")
    def test_deal_cards_2_str_3_int_ea_deck(self):
        # reset card piles
        mock_power_cards = ['SOH', 'SOH', 'DOT', 'DMT', 'DOT', 'SOH', 'SOH', 'DMT',
                            'SOH', 'SOH', 'SOH', 'SOH', 'DMT', 'SOH', 'SOH']
        mock_water_cards = [5, 1, 1, 1, 1, 5, 1, 10, 1, 10, 5, 1, 1, 5, 1, 1, 5, 10, 1, 1, 5, 10, 5, 1, 1, 1, 10, 1, 5,
                            1, 5, 1, 5, 1, 5, 1, 5, 1, 10, 1, 1, 10, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 10]
        # three ints and two str in each deck

        player_1_cards, player_2_cards = water_tank.deal_cards(mock_water_cards, mock_power_cards)
        self.assertEqual(3,
                         sum(isinstance(x, int) for x in player_1_cards),
                         "After dealing cards, Player 1 does not have 3 water cards")
        self.assertEqual(2,
                         sum(isinstance(x, str) for x in player_1_cards),
                         "After dealing cards, Player 1 does not have 2 power cards")
        self.assertEqual(3,
                         sum(isinstance(x, int) for x in player_2_cards),
                         "After dealing cards, Player 2 does not have 3 water cards")
        self.assertEqual(2,
                         sum(isinstance(x, str) for x in player_2_cards),
                         "After dealing cards, Player 2 does not have 2 power cards")

        self.assertTrue(len(mock_power_cards) == 11, "Cards were not taken off from power cards pile.")
        self.assertTrue(len(mock_water_cards) == 47, "Cards were not taken off from water cards pile.")

        self.assertListEqual([1, 1, 5, 'DOT', 'SOH'], player_1_cards, "Doesn't deal cards alternately to each player.")
        self.assertListEqual([1, 1, 5, 'DMT', 'SOH'], player_2_cards, "Doesn't deal cards alternately to each player.")

        self.assertListEqual(['DOT', 'SOH', 'SOH', 'DMT', 'SOH', 'SOH', 'SOH', 'SOH', 'DMT', 'SOH', 'SOH'],
                             mock_power_cards, "Doesn't deal cards alternately to each player.")
        self.assertListEqual(
            [1, 10, 1, 10, 5, 1, 1, 5, 1, 1, 5, 10, 1, 1, 5, 10, 5, 1, 1, 1, 10, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 10, 1,
             1, 10, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 10], mock_water_cards,
            "Doesn't deal cards alternately to each player.")

    #########################################
    ###   Test Cases for apply_overflow   ###
    #########################################

    @timeout(3, exception_message="Check the apply_overflow function for infinite loops")
    def test_apply_overflow(self):
        random_tank_level = randint(81, 99)
        overflow = random_tank_level - 80
        expected_tank_level = 80 - overflow
        error_message = "If the tank value is {}, the remaining water should be {} after applying overflow rules.".format(
            random_tank_level, expected_tank_level)
        self.assertEqual(expected_tank_level, water_tank.apply_overflow(random_tank_level), error_message)

        random_tank_level = randint(81, 99)
        overflow = random_tank_level - 80
        expected_tank_level = 80 - overflow
        error_message = "If the tank value is {}, the remaining water should be {} after applying overflow rules.".format(
            random_tank_level, expected_tank_level)
        self.assertEqual(expected_tank_level, water_tank.apply_overflow(random_tank_level), error_message)

    ########################################
    ###   Test Cases for test_use_card   ###
    ########################################
    @timeout(3, exception_message="Check the use_card function for infinite loops")
    def test_use_water_card(self):
        with redirect_stdout(StringIO()) as f:
            # player_tank, card_used, player_cards, opponent_tank
            player_cards = [1, 5, 10, "DOT", "DMT"]
            player_tank, opponent_tank = water_tank.use_card(25, 1, player_cards, 25)
            self.assertEqual(26, player_tank,
                             "Using a water card does not update the tank level correctly.")
            self.assertEqual(25, opponent_tank,
                             "Using a water card does not update the opponent tank level correctly.")
            self.assertTrue(len(player_cards) == 4, "Card should be removed from player's hand when it is used.")

    @timeout(3, exception_message="Check the use_card function for infinite loops")
    def test_use_soh_card(self):
        with redirect_stdout(StringIO()) as f:
            # player_tank, card_used, player_cards, opponent_tank
            player_cards = [1, 5, 10, "DOT", "SOH"]
            player_tank, opponent_tank = water_tank.use_card(25, "SOH", player_cards, 25)
            self.assertEqual(37, player_tank,
                             "Using SOH does not update the tank level correctly.")
            self.assertEqual(13, opponent_tank,
                             "Using SOH does not update the tank level correctly.")
            self.assertTrue(len(player_cards) == 4, "Card should be removed from player's hand when it is used.")

            # Even Steal
            player_cards = [1, 5, 10, "DOT", "SOH"]
            player_tank, opponent_tank = water_tank.use_card(25, "SOH", player_cards, 26)
            self.assertEqual(38, player_tank,
                             "Using SOH does not update the tank level correctly.")
            self.assertEqual(13, opponent_tank,
                             "Using SOH does not update the tank level correctly.")
            self.assertTrue(len(player_cards) == 4, "Card should be removed from player's hand when it is used.")

    @timeout(3, exception_message="Check the use_card function for infinite loops")
    def test_use_dmt_card(self):
        with redirect_stdout(StringIO()) as f:
            # player_tank, card_used, player_cards, opponent_tank
            player_cards = [1, 5, 10, "DOT", "DMT"]
            player_tank, opponent_tank = water_tank.use_card(25, "DMT", player_cards, 25)
            self.assertEqual(50, player_tank,
                             "Using DMT does not update the tank level correctly.")
            self.assertEqual(25, opponent_tank,
                             "Using DMT does not update the tank level correctly.")
            self.assertTrue(len(player_cards) == 4, "Card should be removed from player's hand when it is used.")

    @timeout(3, exception_message="Check the use_card function for infinite loops")
    def test_use_dot_card(self):
        with redirect_stdout(StringIO()) as f:
            # player_tank, card_used, player_cards, opponent_tank
            player_cards = [1, 5, 10, "DOT", "DMT"]
            player_tank, opponent_tank = water_tank.use_card(25, "DOT", player_cards, 25)
            self.assertEqual(25, player_tank,
                             "Using DOT does not update the tank level correctly.")
            self.assertEqual(0, opponent_tank,
                             "Using DOT does not update the tank level correctly.")
            self.assertTrue(len(player_cards) == 4, "Card should be removed from player's hand when it is used.")

    #######################################
    ###   Test Cases for discard_card   ###
    #######################################
    @timeout(3, exception_message="Check the discard_card function for infinite loops")
    def test_discard_card_water(self):
        with redirect_stdout(StringIO()) as f:
            # player_tank, card_used, player_cards, opponent_tank
            water_cards_pile = [1, 5, 10, 5, 10, 1]
            power_cards_pile = ['SOH', 'DMT', 'DMT', 'DOT']
            player_cards = [1, 5, 10, 'SOH', 'DMT']
            water_tank.discard_card(1, player_cards, water_cards_pile, power_cards_pile)
            self.assertListEqual([1, 5, 10, 5, 10, 1, 1], water_cards_pile,
                                 "Using the discard card does not function correctly.")
            self.assertListEqual([5, 10, 'SOH', 'DMT'], player_cards,
                                 "Using the discard card does not function correctly.")

    @timeout(3, exception_message="Check the discard_card function for infinite loops")
    def test_discard_card_power(self):
        with redirect_stdout(StringIO()) as f:
            # player_tank, card_used, player_cards, opponent_tank
            water_cards_pile = [1, 5, 10, 5, 10, 1]
            power_cards_pile = ['SOH', 'DMT', 'DMT', 'DOT']
            player_cards = [1, 5, 10, 'SOH', 'DMT']
            water_tank.discard_card('DMT', player_cards, water_cards_pile, power_cards_pile)
            self.assertListEqual(['SOH', 'DMT', 'DMT', 'DOT', 'DMT'], power_cards_pile,
                                 "Using the discard card does not function correctly.")
            self.assertListEqual([1, 5, 10, 'SOH'], player_cards, "Using the discard card does not function correctly.")

    #######################################
    ###   Test Cases for filled_tank    ###
    #######################################

    @timeout(3, exception_message="Check the filled_tank function for infinite loops")
    def test_filled_tank(self):
        self.assertTrue(water_tank.filled_tank(80), "A tank filled to 80 is full")
        self.assertTrue(water_tank.filled_tank(75), "A tank filled to 75 is full")
        self.assertFalse(water_tank.filled_tank(74), "A tank filled to 74 is underfull")
        self.assertFalse(water_tank.filled_tank(81), "A tank filled to 81 is overfull")
        self.assertFalse(water_tank.filled_tank(-1), "A tank filled to -1 should not return as full")

    #########################################
    ###   Test Cases for arrange_cards    ###
    #########################################

    @timeout(3, exception_message="Check the arrange_cards function for infinite loops")
    def test_arrange_cards(self):
        mock_deck = ["SOH", 1, "DMT", 10, 1]
        water_tank.arrange_cards(mock_deck)

        self.assertIsInstance(mock_deck[0], int,
                              "The card at index 0 (first item) should be an water card which has a type of integer")
        self.assertIsInstance(mock_deck[1], int,
                              "The card at index 1 (second item) should be an water card which has a type of integer")
        self.assertIsInstance(mock_deck[2], int,
                              "The card at index 2 (third item) should be an water card which has a type of integer")
        self.assertIsInstance(mock_deck[3], str,
                              "The card at index 3 (fourth item) should be a power card which has a type of string")
        self.assertIsInstance(mock_deck[4], str,
                              "The card at index 4 (fifth item) should be a power card which has a type of string")
        self.assertTrue(mock_deck[0] == 1, "Check the water cards sorting")
        self.assertTrue(mock_deck[1] == 1, "Check the water cards sorting")
        self.assertTrue(mock_deck[2] == 10, "Check the water cards sorting")
        self.assertTrue(mock_deck[3] == "DMT", "Check the power cards sorting")
        self.assertTrue(mock_deck[4] == "SOH", "Check the power cards sorting")

    #####################################
    ###   Test Cases for check_pile   ###
    #####################################

    @timeout(3, exception_message="Check the check_piles function for infinite loops")
    def test_check_water_pile_with_card(self):
        # the way the sample code is written we have to get them to at least call
        # the pile "water" or something else, keep in mind for instructions
        """
        Checks that the check pile function adds a whole new deck when presented an empty
        list, and doesn't when the list still has at least one element
        """
        pile = [1]
        water_tank.check_pile(pile, "water")
        self.assertEqual(1, len(pile), "The water pile should not change while there is still a card left")

    @timeout(3, exception_message="Check the check_piles function for infinite loops")
    def test_check_power_pile_with_card(self):
        pile = ["SOH"]
        water_tank.check_pile(pile, "power")
        self.assertEqual(1, len(pile), "The power pile should not change while there is still a card left")

    @timeout(3, exception_message="Check the check_piles function for infinite loops")
    def test_check_empty_water_pile(self):
        pile = []
        water_tank.check_pile(pile, "water")
        self.assertEqual(53, len(pile),
                         "When the water pile is empty, check_piles should start a new 53 water card deck. "
                         "Check if you are modifying the pile by reference.")

    @timeout(3, exception_message="Check the check_piles function for infinite loops")
    def test_check_empty_power_pile(self):
        pile = []
        water_tank.check_pile(pile, "power")
        self.assertEqual(15, len(pile),
                         "When the power pile is empty, check_piles should start a new 25 power card deck. "
                         "Check if you are modifying the pile by reference.")

    ###################################
    ###  Test Cases for human_play  ###
    ###################################

    @timeout(3, exception_message="Check human_play for infinite loops")
    @patch('water_tank.input', side_effect=['u', '1'])
    def test_human_play_displays_human_water_level(self, one):
        with patch('sys.stdout', new=StringIO()) as output:
            random_tank = randint(0, 50)
            water_tank.human_play(human_tank=random_tank, human_cards=[1, 1, 1, 'SOH', 'SOH'], water_cards_pile=[5], power_cards_pile=[],
                                  opponent_tank=0)
        printed_output = output.getvalue()
        self.assertIn(str(random_tank), printed_output,
                      "The output to the screen should include the value of the human player's tank.")

    @timeout(3, exception_message="Check the human_play function for infinite loops")
    @patch('water_tank.input', side_effect=['u', '1'])
    def test_human_play_displays_opponent_water_level(self, one):
        with patch('sys.stdout', new=StringIO()) as output:
            random_tank = randint(0, 50)
            water_tank.human_play(human_tank=66, human_cards=[1, 1, 1, 'SOH', 'SOH'], water_cards_pile=[5], power_cards_pile=[],
                                  opponent_tank=random_tank)
        printed_output = output.getvalue()
        self.assertIn(str(random_tank), printed_output,
                      "The output to the screen should include the value of the opponent's tank.")

    @timeout(3, exception_message="Check the human_play function for infinite loops")
    @patch('water_tank.input', side_effect=['u', '1'])
    def test_human_play_displays_current_cards(self, one):
        with patch('sys.stdout', new=StringIO()) as output:
            random_cards = []
            random_cards.append(1)
            random_cards.append(choice([1, 5, 10]))
            random_cards.append(choice([1, 5, 10]))
            random_cards.sort()
            random_cards.append(choice(["DMT", "DOT"]))
            random_cards.append("SOH")
            water_tank.human_play(human_tank=66, human_cards=random_cards, water_cards_pile=[5],
                                  power_cards_pile=['SOH'], opponent_tank=0)
        printed_output = output.getvalue()
        self.assertIn(str(random_cards), printed_output,
                      "The output to the screen should include the human's current cards.")

    @timeout(3, exception_message="Check the human_play function for infinite loops")
    @patch('water_tank.input', side_effect=['u', '1'])
    def test_human_play_uses_water_card(self, one):
        with patch('sys.stdout', new=StringIO()) as output:
            random_tank = randint(0, 50)
            water_pile = [5]
            water_tank.human_play(human_tank=random_tank, human_cards=[1, 5, 10, 'SOH', 'DMT'],
                                  water_cards_pile=water_pile,
                                  power_cards_pile=['SOH'], opponent_tank=0)
        printed_output = output.getvalue()
        new_tank_level = random_tank + 1
        self.assertIn(str(new_tank_level), printed_output,
                      "The output to the screen should include the human's new tank level.")
        self.assertIn(str([5, 5, 10, 'DMT', 'SOH']), printed_output,
                      "The output to the screen should include the human's new hand after using a card and drawing a "
                      "replacement card.")
        self.assertTrue(len(water_pile) == 0, "After using a water card, draw a new card from the water pile.")

    @timeout(3, exception_message="Check the human_play function for infinite loops")
    @patch('water_tank.input', side_effect=['u', 'DMT', 'u', 'DMT'])
    def test_human_play_uses_power_card(self, one):
        with patch('sys.stdout', new=StringIO()) as output:
            random_tank = randint(0, 37)  # Test a non winning value for DMT
            power_pile = ['DOT']
            water_tank.human_play(human_tank=random_tank, human_cards=[1, 5, 10, 'SOH', 'DMT'], water_cards_pile=[5],
                                  power_cards_pile=power_pile, opponent_tank=0)
        printed_output = output.getvalue()
        new_tank_level = 2 * random_tank
        self.assertIn(str(new_tank_level), printed_output,
                      "The output to the screen should include the human's new tank level.")
        self.assertIn(str([1, 5, 10, 'DOT', 'SOH']), printed_output,
                      "The output to the screen should include the human's new hand after using a card and drawing a "
                      "replacement card.")
        self.assertTrue(len(power_pile) == 0, "After using a power card, draw a new card from the power pile.")

        with patch('sys.stdout', new=StringIO()) as output:
            random_tank_2 = randint(42, 74)  # Test an overflow value for DMT
            overflow = (random_tank_2 * 2) - 80
            new_tank_level = 80 - overflow
            power_pile = ['DOT']
            water_tank.human_play(human_tank=random_tank_2, human_cards=[1, 5, 10, 'SOH', 'DMT'], water_cards_pile=[5],
                                  power_cards_pile=power_pile, opponent_tank=0)
        printed_output = output.getvalue()

        self.assertIn(str(new_tank_level), printed_output,
                      "Overflow was not applied correctly to the human's new tank level.")

    ########################################
    ###   Test Cases for computer_play   ###
    ########################################

    @timeout(3, exception_message="Check computer_play for infinite loops")
    def test_computer_play_chooses_soh(self):
        with redirect_stdout(StringIO()) as f:
            computer_deck = [1, 1, 1, 'SOH', 'SOH']
            power_pile = ['SOH']
            computer_tank, human_tank = water_tank.computer_play(39, computer_deck, [1], power_pile, 73)
            self.assertEqual(75, computer_tank, "Check how the computer play handles SOH")
            self.assertEqual(37, human_tank, "Check how the computer play handles SOH")

    @timeout(3, exception_message="Check computer_play for infinite loops")
    def test_computer_play_chooses_dmt(self):
        with redirect_stdout(StringIO()) as f:
            computer_deck = [1, 1, 1, 'DMT', 'DMT']
            power_pile = ['DMT', 'DMT']
            computer_tank, human_tank = water_tank.computer_play(38, computer_deck, [1], power_pile, 73)
            self.assertEqual(76, computer_tank, "Check how the computer play handles DMT")
            self.assertEqual(73, human_tank, "Check how the computer play handles DMT")

            # Test for overflow
            random_tank = choice([43, 44])  # Test an overflow value for DMT
            overflow = (random_tank * 2) - 80
            new_tank_level = 80 - overflow
            computer_tank, human_tank = water_tank.computer_play(random_tank, computer_deck, [1], power_pile, 73)
            self.assertEqual(new_tank_level, computer_tank, "Check how the computer play handles overflow.")

    @timeout(3, exception_message="Check computer_play for infinite loops")
    def test_computer_play_chooses_dot(self):
        with redirect_stdout(StringIO()) as f:
            computer_deck = [1, 1, 1, 'DOT', 'DOT']
            power_pile = ['DOT']
            computer_tank, human_tank = water_tank.computer_play(1, computer_deck, [1], power_pile, 74)
            self.assertEqual(1, computer_tank, "Check how the computer play handles DOT")
            self.assertEqual(0, human_tank, "Check how the computer play handles DOT")

    @timeout(3, exception_message="Check computer_play for infinite loops")
    def test_computer_play_chooses_water_card(self):
        with redirect_stdout(StringIO()) as f:
            computer_deck = [10, 10, 10, 'SOH', 'SOH']
            water_pile = [10, 10]
            computer_tank, human_tank = water_tank.computer_play(65, computer_deck, water_pile, ['SOH'], 0)
            self.assertEqual(75, computer_tank, "Check how the computer play handles a water card")
            self.assertEqual(0, human_tank, "Check how the computer play handles a water card")

            # Test for overflow
            random_tank = randint(71, 74)  # Test an overflow for add-in 10
            overflow = (random_tank + 10) - 80
            new_tank_level = 80 - overflow
            computer_tank, human_tank = water_tank.computer_play(random_tank, computer_deck, [1], ['SOH'], 0)
            self.assertEqual(new_tank_level, computer_tank, "Check how the computer play handles a water card overflow")
            self.assertEqual(0, human_tank, "Check how the computer play handles a water card overflow")

    #########################################
    ###   Test Cases for computer LOGIC   ###
    #########################################
    @timeout(3, exception_message="Check computer_play for infinite loops")
    def test_computer_play_chooses_winning_power_card(self):
        with redirect_stdout(StringIO()) as f:
            computer_deck = [1, 1, 1, 'DMT', 'DOT']
            water_cards_pile = [10, 10]
            power_cards_pile = ['DOT', 'DOT']
            self.assertEqual(78, water_tank.computer_play(39, computer_deck, water_cards_pile, power_cards_pile, 74)[0],
                             "The computer_play logic should choose to win when presented with a clear winning power card")

    @timeout(3, exception_message="Check computer_play for infinite loops")
    def test_computer_play_chooses_winning_water_card(self):
        with redirect_stdout(StringIO()) as f:
            computer_deck = [1, 1, 10, 'DMT', 'DOT']
            water_cards_pile = [10, 10]
            power_cards_pile = ['DOT', 'DOT']
            self.assertEqual(75, water_tank.computer_play(65, computer_deck, water_cards_pile, power_cards_pile, 20)[0],
                             "The computer_play logic should choose to win when presented with a clear winning water card")

    @timeout(3, exception_message="Check computer_play for infinite loops")
    def test_computer_play_selects_a_card_that_is_in_computer_deck(self):
        with redirect_stdout(StringIO()) as f:
            computer_deck = [1, 1, 1, 'SOH', 'SOH']
            self.assertEqual(74,
                             water_tank.computer_play(computer_tank=73, computer_cards=computer_deck,
                                                      water_cards_pile=[1],
                                                      power_cards_pile=['DMT'], opponent_tank=0)[0],
                             "Computer did not select the most logical card")
            self.assertEqual(0,
                             water_tank.computer_play(computer_tank=2, computer_cards=computer_deck,
                                                      water_cards_pile=[10],
                                                      power_cards_pile=['DMT'], opponent_tank=0)[1],
                             "Computer did not select the most logical card")
            self.assertEqual([1, 1, 10, 'SOH', 'SOH'], computer_deck,
                             "Computer's deck is not as expected after operation")

    #####################################
    ###   Test Cases for game_round   ###
    #####################################
    @timeout(3, exception_message="Check computer_play for infinite loops")
    def test_game_round(self):
        with redirect_stdout(StringIO()) as f:
            # All code lines generating console output within this context manager
            # will have those outputs suppressed.
            rounds = 5
            for i in range(rounds):
                water_cards_pile, power_cards_pile = water_tank.setup_cards()
                player_1_cards, player_2_cards = water_tank.deal_cards(water_cards_pile, power_cards_pile)
                player_1_tank = 0
                player_2_tank = 0
                while True:
                    # For Player 1
                    copy_opponent_cards = player_2_cards.copy()
                    player_1_tank, player_2_tank = water_tank.computer_play(player_1_tank, player_1_cards,
                                                                            water_cards_pile,
                                                                            power_cards_pile,
                                                                            player_2_tank)

                    if water_tank.filled_tank(player_1_tank):
                        break
                    self.assertListEqual(copy_opponent_cards, player_2_cards, "Human player's hand should not change "
                                                                              "when the computer makes a move")
                    self.assertTrue(len(player_1_cards) == 5, "Computer Player should have 5 cards in its hand.")

                    water_tank.check_pile(water_cards_pile, "water")
                    water_tank.check_pile(power_cards_pile, "power")

                    # For Player 2
                    copy_opponent_cards = player_1_cards.copy()
                    player_2_tank, player_1_tank = water_tank.computer_play(player_2_tank, player_2_cards,
                                                                            water_cards_pile,
                                                                            power_cards_pile,
                                                                            player_1_tank)

                    if water_tank.filled_tank(player_2_tank):
                        break
                    self.assertListEqual(copy_opponent_cards, player_1_cards, "Human player's hand should not change "
                                                                              "when the computer makes a move")
                    self.assertTrue(len(player_2_cards) == 5, "Computer Player should have 5 cards in its hand.")

                    water_tank.check_pile(water_cards_pile, "water")
                    water_tank.check_pile(power_cards_pile, "power")

        self.assertTrue(True, "Check computer_play for infinite loops")


if __name__ == '__main__':
    unittest.main()
