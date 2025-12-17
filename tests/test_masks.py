import pytest
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number():
    assert get_mask_card_number('1234567891012134') == '1234 56** **** 2134'
    assert get_mask_card_number('1234 5678 9101 2134') == '1234 56** **** 2134'
    with pytest.raises(ValueError):
        assert get_mask_card_number('')
        assert get_mask_card_number('321')


def test_get_mask_account():
    assert get_mask_account('12345678910121348908') == '**8908'
    assert get_mask_account('1234 5678 9101 2134 8908') == '**8908'
    with pytest.raises(ValueError):
        assert get_mask_account('')
        assert get_mask_account('321')
