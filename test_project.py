import project as p
import card
import player
import deck
import pytest

# suit doesn't matter so they are all spades
card_1 = card.Card(0, 2)
card_2 = card.Card(0, 10)
card_3 = card.Card(0, 11)
card_4 = card.Card(0, 12)
card_5 = card.Card(0, 13)
card_6 = card.Card(0, 1)
card_7 = card.Card(0, 8)


def test_evaluate_hand():
    assert p.evaluate_hand([card_1, card_2]) == 12
    assert p.evaluate_hand([card_1, card_2], True) == 10
    assert p.evaluate_hand([card_1, card_3]) == 12
    assert p.evaluate_hand([card_1, card_4]) == 12
    assert p.evaluate_hand([card_1, card_5]) == 12
    assert p.evaluate_hand([card_1, card_6]) == 13
    assert p.evaluate_hand([card_3, card_2]) == 20
    assert p.evaluate_hand([card_6, card_2]) == 21
    assert p.evaluate_hand([card_7, card_6]) == 19
    assert p.evaluate_hand([card_7, card_6, card_7]) == 17


def test_compare_hands():
    assert p.compare_hands([card_7, card_6, card_7], [card_7, card_6, card_7]) == False
    assert p.compare_hands([card_7, card_6], [card_7, card_6, card_7]) == True
    assert p.compare_hands([card_2, card_3], [card_4, card_6]) == False
    assert p.compare_hands([card_3, card_6], [card_1, card_6]) == True
    assert p.compare_hands([card_7, card_7, card_7, card_7], [card_7, card_6, card_7]) == False
    assert p.compare_hands([card_7, card_6, card_7], [card_7, card_7, card_7, card_7]) == True


def test_get_load_data():
    #this is also testing save_game
    assert p.get_load_data("tuesday.wednesday") == {}
    test_player = player.Player("test", 1000)
    p.save_game(test_player)
    assert test_player.name in p.get_load_data().keys()
    test_player = player.Player("test again", 1)
    p.save_game(test_player)
    assert test_player.name in p.get_load_data().keys()
