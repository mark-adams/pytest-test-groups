import random
from itertools import chain
from uuid import uuid4

import pytest

from pytest_test_groups import get_group, get_file_group


def unique(suffix):
    return uuid4().hex[:6] + suffix


class MockItem:
    def __init__(self, module):
        self.module = str(module)
        self.filename = unique('.py')


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


def test_file_group_is_the_proper_size():
    items = [MockItem(i) for i in range(32)]
    group = get_file_group(items, 8, 1)

    assert len(group) == 4


def test_all_file_groups_together_form_original_set_of_tests():
    group_count = 8
    for item_size in range(group_count, 32):
        items = [MockItem(i) for i in range(item_size)]
        groups = [get_file_group(items, group_count, i) for i in range(1, group_count + 1)]
        combined = set(chain.from_iterable(groups))
        assert combined == set(items)


def test_file_group_that_is_too_high_raises_value_error():
    items = [MockItem(i) for i in range(32)]

    with pytest.raises(ValueError):
        # When group_count=4, group_id=5 is out of bounds
        get_file_group(items, 4, 5)


def test_file_group_that_is_too_low_raises_value_error():
    items = [MockItem(i) for i in range(32)]

    with pytest.raises(ValueError):
        # When group_count=4, group_id=0 is out of bounds
        get_file_group(items, 4, 0)


def test_file_group_groups_by_modules():
    module1 = unique('module1')
    module2 = unique('module2')
    items = [MockItem(module1), MockItem(module2), MockItem(module2), MockItem(module1)]

    group = get_file_group(items, 2, 1)

    assert len(group) == 2
    assert len({item.module for item in group}) == 1


def test_file_group__group_evenly():
    module1 = unique('module1')
    module2 = unique('module2')
    module3 = unique('module3')
    module4 = unique('module4')

    items = [MockItem(module1) for _ in range(100)]
    items += [MockItem(module2) for _ in range(22)]
    items += [MockItem(module3) for _ in range(60)]
    items += [MockItem(module4) for _ in range(25)]

    random.shuffle(items)

    # total of 245 tests between 3 groups. Desired: 81.66 tests in each group.
    # Using greedy algorithm, this means:
    # group1: module1
    # group2: module3
    # group3: module2 + module4

    group1 = get_file_group(items, 3, 1)
    assert len(group1) == 100
    assert {item.filename for item in group1} == {item.filename for item in items if item.module == module1}

    group2 = get_file_group(items, 3, 2)
    assert len(group2) == 60
    assert {item.filename for item in group2} == {item.filename for item in items if item.module == module3}

    group3 = get_file_group(items, 3, 3)
    assert len(group3) == 47
    assert {item.filename for item in group3} == {item.filename for item in items if item.module in (module4, module2)}
