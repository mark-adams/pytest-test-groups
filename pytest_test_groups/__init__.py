# -*- coding: utf-8 -*-

# Import python libs
import math
from random import Random

# Import 3rd-party libs
from _pytest.config import create_terminal_writer


def get_group_size(total_items, total_groups):
    """Return the group size."""
    return int(math.ceil(float(total_items) / total_groups))


def get_group(items, group_size, group_id):
    """Get the items from the passed in group based on group size."""
    start = group_size * (group_id - 1)
    end = start + group_size

    if start >= len(items) or start < 0:
        raise ValueError("Invalid test-group argument")

    return items[start:end]


def pytest_addoption(parser):
    group = parser.getgroup('split your tests into evenly sized groups and run them')
    group.addoption('--test-group-count', dest='test-group-count', type=int,
                    help='The number of groups to split the tests into')
    group.addoption('--test-group', dest='test-group', type=int,
                    help='The group of tests that should be executed')
    group.addoption('--test-group-random-seed', dest='random-seed', type=int,
                    help='Integer to seed pseudo-random test ordering')


def pytest_collection_modifyitems(session, config, items):
    group_count = config.getoption('test-group-count')
    group_id = config.getoption('test-group')
    seed = config.getoption('random-seed', False)

    if not group_count or not group_id:
        return

    if seed:
        seeded = Random(seed)
        seeded.shuffle(items)

    total_items = len(items)

    group_size = get_group_size(total_items, group_count)
    tests_in_group = get_group(items, group_size, group_id)
    items[:] = tests_in_group

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
