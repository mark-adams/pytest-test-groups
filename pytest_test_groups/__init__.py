from random import Random
import math


def get_group_size(total_items, total_groups):
    return int(math.ceil(float(total_items) / total_groups))


def get_group(items, group_size, group_id):
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
                    help='Integer to seed psuedo-random test ordering')


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
    del items[:]
    items.extend(tests_in_group)

    print('Running test group #{0} ({1} tests)'.format(group_id, len(items)))
