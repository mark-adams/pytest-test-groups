import random
from itertools import chain
from uuid import uuid4

import pytest

from pytest_test_groups import get_group_default, get_group_by_filename


def unique(prefix):
    return prefix + uuid4().hex[:6]


class MockItem:
    class MockModule:
        def __init__(self, name):
            self.__file__ = name

    def __init__(self, module):
        self.module = self.MockModule(module)
        self.test_name = unique('test_')


def test_group_is_the_proper_size():
    items = [str(i) for i in range(32)]
    group = get_group_default(items, 8, 1)

    assert len(group) == 4


def test_all_groups_together_form_original_set_of_tests():
    group_count = 8
    for item_size in range(group_count, 32):
        items = [str(i) for i in range(item_size)]
        groups = [get_group_default(items, group_count, i) for i in range(1, group_count + 1)]
        combined = set(chain.from_iterable(groups))
        assert combined == set(items)


def test_group_that_is_too_high_raises_error():
    items = [str(i) for i in range(32)]

    with pytest.raises(pytest.UsageError, match='Invalid test-group argument'):
        # When group_count=4, group_id=5 is out of bounds
        get_group_default(items, 4, 5)


def test_group_that_is_too_low_raises_error():
    items = [str(i) for i in range(32)]

    with pytest.raises(pytest.UsageError, match='Invalid test-group argument'):
        # When group_count=4, group_id=0 is out of bounds
        get_group_default(items, 4, 0)


def test_file_group_is_the_proper_size():
    items = [MockItem(i) for i in range(32)]
    group = get_group_by_filename(items, 8, 1)

    assert len(group) == 4


def test_all_file_groups_together_form_original_set_of_tests():
    group_count = 8
    for item_size in range(group_count, 32):
        items = [MockItem(i) for i in range(item_size)]
        groups = [get_group_by_filename(items, group_count, i) for i in range(1, group_count + 1)]
        combined = set(chain.from_iterable(groups))
        assert combined == set(items)


def test_file_group_that_is_too_high_raises_error():
    items = [MockItem(i) for i in range(32)]

    with pytest.raises(pytest.UsageError, match='Invalid test-group argument'):
        # When group_count=4, group_id=5 is out of bounds
        get_group_by_filename(items, 4, 5)


def test_file_group_that_is_too_low_raises_error():
    items = [MockItem(i) for i in range(32)]

    with pytest.raises(pytest.UsageError, match='Invalid test-group argument'):
        # When group_count=4, group_id=0 is out of bounds
        get_group_by_filename(items, 4, 0)


def test_file_group_groups_by_modules():
    module1 = unique('module1')
    module2 = unique('module2')
    items = [MockItem(module1), MockItem(module2), MockItem(module2), MockItem(module1)]

    group = get_group_by_filename(items, 2, 1)

    assert len(group) == 2
    assert len({item.module.__file__ for item in group}) == 1


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

    group1 = get_group_by_filename(items, 3, 1)
    assert len(group1) == 100
    assert {item.test_name for item in group1} == _get_modules_items({module1}, items)

    group2 = get_group_by_filename(items, 3, 2)
    assert len(group2) == 60
    assert {item.test_name for item in group2} == _get_modules_items({module3}, items)

    group3 = get_group_by_filename(items, 3, 3)
    assert len(group3) == 47
    assert {item.test_name for item in group3} == _get_modules_items({module2, module4}, items)


def _get_modules_items(module_names, items):
    return {item.test_name for item in items if item.module.__file__ in module_names}
