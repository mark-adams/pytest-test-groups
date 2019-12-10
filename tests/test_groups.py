from itertools import chain

import pytest

from pytest_test_groups import get_group


def test_group_is_the_proper_size():
    items = [str(i) for i in range(32)]
    group = get_group(items, 8, 1)

    assert len(group) == 4


def test_all_groups_together_form_original_set_of_tests():
    group_count = 8
    for item_size in range(group_count, 32):
        items = [str(i) for i in range(item_size)]
        groups = [get_group(items, group_count, i) for i in range(1, group_count + 1)]
        combined = set(chain.from_iterable(groups))
        assert combined == set(items)


def test_group_that_is_too_high_raises_value_error():
    items = [str(i) for i in range(32)]

    with pytest.raises(ValueError):
        # When group_count=4, group_id=5 is out of bounds
        get_group(items, 4, 5)


def test_group_that_is_too_low_raises_value_error():
    items = [str(i) for i in range(32)]

    with pytest.raises(ValueError):
        # When group_count=4, group_id=0 is out of bounds
        get_group(items, 4, 0)
