import pytest
from src.widget import mask_account_card, get_date

@pytest.mark.parametrize("n, expected_result", [('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
                                                ('Счет 64686473678894779589', 'Счет **9589'),
                                                ('MasterCard 7158300734726758', 'MasterCard 7158 30** **** 6758'),
                                                ('Счет 35383033474447895560', 'Счет **5560')])
def test_mask_account_card(n, expected_result):
    assert mask_account_card(n) == expected_result

assert mask_account_card('Maestro 1596837868705199') == 'Maestro 1596 83** **** 5199'
assert mask_account_card('Счет 64686473678894779589') == 'Счет **9589'

with pytest.raises(ValueError):
    assert mask_account_card('Maestro 64686473678894779589')
    assert mask_account_card('321')

assert get_date('2025-12-17T04:08:25.671407') == '17.12.2025'
assert get_date('2025.12.17') == '17.12.2025'
assert get_date('2025 12 17') == '17.12.2025'
assert get_date('') == 0