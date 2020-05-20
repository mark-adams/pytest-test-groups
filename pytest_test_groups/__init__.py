# -*- coding: utf-8 -*-

# Import python libs
from math import ceil
from random import Random
from collections import defaultdict

# Import 3rd-party libs
from _pytest.config import create_terminal_writer


def get_group(items, group_count, group_id):
    """Get the items from the passed in group based on group count."""
    start = _get_start(group_id, group_count)
    return items[start:len(items):group_count]


def get_file_group(items, group_count, group_id):
    """Get the items from the passed in group, split by files, based on group count."""
    start = _get_start(group_id, group_count)
    items_in_module = defaultdict(int)

    for item in items:
        items_in_module[item.module] += 1

    max_items_per_group = ceil(len(items) / float(group_count))

    modules = sorted(
        items_in_module.keys(),
        key=lambda group: items_in_module[group],
        reverse=True
    )

    group_to_modules = defaultdict(list)
    for i in range(group_count):
        try:
            module = modules.pop(0)  # start with max
            group_to_modules[i].append(module)
            items_in_group = items_in_module[module]
            while items_in_group < max_items_per_group:
                module = modules.pop(-1)  # add min
                group_to_modules[i].append(module)
                items_in_group += items_in_module[module]
        except IndexError:
            break

    return [item for item in items if item.module in group_to_modules[start]]


def _get_start(group_id, group_count):
    if not (1 <= group_id <= group_count):
        raise ValueError("Invalid test-group argument")
    return group_id - 1


def pytest_addoption(parser):
    group = parser.getgroup('split your tests into evenly sized groups and run them')
    group.addoption('--test-group-count', dest='test-group-count', type=int,
                    help='The number of groups to split the tests into')
    group.addoption('--test-group', dest='test-group', type=int,
                    help='The group of tests that should be executed')
    group.addoption('--test-group-by-files', dest='group-by-files', action='store_true',
                    help='Group by files instead of collected items')
    group.addoption('--test-group-random-seed', dest='random-seed', type=int,
                    help='Integer to seed pseudo-random test ordering')


def pytest_collection_modifyitems(session, config, items):
    group_count = config.getoption('test-group-count')
    group_id = config.getoption('test-group')
    group_by_files = config.getoption("group-by-files", False)
    seed = config.getoption('random-seed', False)

    if not group_count or not group_id:
        return

    if seed:
        seeded = Random(seed)
        seeded.shuffle(items)

    if group_by_files:
        items[:] = get_file_group(items, group_count, group_id)
    else:
        items[:] = get_group(items, group_count, group_id)

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
