import pytest

from pytest_test_groups import get_group, get_group_size


def test_group_size_computed_correctly_for_even_group():
    expected = 8
    actual = get_group_size(32, 4)  # 32 total tests; 4 groups

    assert expected == actual


def test_group_size_computed_correctly_for_odd_group():
    expected = 8
    actual = get_group_size(31, 4)  # 31 total tests; 4 groups

    assert expected == actual


def test_group_is_the_proper_size():
    items = [str(i) for i in range(32)]
    group = get_group(items, 8, 1)

    assert len(group) == 8


def test_all_groups_together_form_original_set_of_tests():
    items = [str(i) for i in range(32)]

    groups = [get_group(items, 8, i) for i in range(1, 5)]

    combined = []
    for group in groups:
        combined.extend(group)

    assert combined == items


def test_group_that_is_too_high_raises_value_error():
    items = [str(i) for i in range(32)]

    with pytest.raises(ValueError):
        get_group(items, 8, 5)


def test_group_that_is_too_low_raises_value_error():
    items = [str(i) for i in range(32)]

    with pytest.raises(ValueError):
        get_group(items, 8, 0)
