# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from enum import Enum
from random import Random

import pytest

# Import 3rd-party libs
from _pytest.config import create_terminal_writer

class StrEnum(str, Enum):
    """Custom StrEnum for Python < 3.11 compatibility."""
    def __str__(self):
        return self.value
    
class GroupBy(StrEnum):
    DEFAULT = ""
    FILENAME = "filename"

def get_group_default(items, group_count, group_id):
    """Get the items from the passed in group based on group count."""
    start = _get_start(group_id, group_count)
    return items[start:len(items):group_count]

def get_group_by_filename(items, group_count, group_id):
    """Get the items from the passed in group, split by files, based on group count."""
    start = _get_start(group_id, group_count)
    modules_to_items = defaultdict(list)

    for item in items:
        modules_to_items[item.module.__file__].append(item)

    sorted_modules_items = sorted(
        modules_to_items.items(),
        key=lambda mod_items: len(mod_items[1]),
        reverse=True
    )

    group_to_items = OrderedDict((i, []) for i in range(group_count))
    for module, items in sorted_modules_items:
        # add largest module to minimal group, based on greedy algorithm from:
        # https://www.ijcai.org/Proceedings/09/Papers/096.pdf
        minimal_group = min(group_to_items.values(), key=lambda items: len(items))
        minimal_group.extend(items)

    return group_to_items[start]

def _get_start(group_id, group_count):
    if not (1 <= group_id <= group_count):
        raise pytest.UsageError('Invalid test-group argument')
    return group_id - 1

groupByHandlers = {
    GroupBy.DEFAULT: get_group_default,
    GroupBy.FILENAME: get_group_by_filename
}

def pytest_addoption(parser):
    group = parser.getgroup('split your tests into groups and run them')
    group.addoption('--test-group-count', dest='test-group-count', type=int,
                    help='The number of groups to split the tests into')
    group.addoption('--test-group', dest='test-group', type=int,
                    help='The group of tests that should be executed')
    group.addoption('--test-group-by', dest='test-group-by', type=GroupBy, default=GroupBy.DEFAULT)
    group.addoption('--test-group-random-seed', dest='random-seed', type=int,
                    help='Integer to seed pseudo-random test selection')


def _sort_in_original_order(items, orig_items):
    original_order = {item: index for index, item in enumerate(orig_items)}
    items.sort(key=original_order.__getitem__)
    return items

@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(session, config, items):
    yield
    group_count = config.getoption('test-group-count')
    group_id = config.getoption('test-group')
    group_by = config.getoption("test-group-by")
    seed = config.getoption('random-seed', False)

    if not group_count or not group_id:
        return
    
    original_items = items[:]

    if seed is not False:
        seeded = Random(seed)
        seeded.shuffle(items)

    group_by = groupByHandlers[group_by]
    items[:] = group_by(items, group_count, group_id)

    if len(items) == 0:
        raise pytest.UsageError('Invalid test-group argument')

    if seed is not False:
        items = _sort_in_original_order(items, original_items)

    terminal_reporter = config.pluginmanager.get_plugin('terminalreporter')
    terminal_writer = create_terminal_writer(config)
    message = terminal_writer.markup(
        'Running test group #{0} ({1} tests)\n'.format(
            group_id,
            len(items)
        ),
        yellow=True
    )
    terminal_reporter.write(message)
