pytest_plugins = ['pytester']


def test_group_runs_appropriate_tests(testdir):
    testdir.makepyfile("""
        def test_x(): pass
        def test_y(): pass
        def test_z(): pass
    """)

    result = testdir.runpytest_subprocess('--test-group-count', '2', '--test-group', '1')
    result.assert_outcomes(passed=2)
    result.stdout.fnmatch_lines([
        'Running test group #1 (2 tests)'
    ])

    result = testdir.runpytest_subprocess('--test-group-count', '2', '--test-group', '2')
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines([
        'Running test group #2 (1 tests)'
    ])


def test_group_runs_all_test(testdir):
    """Given a large set of tests executed with a random seed, assert that all
    tests are executed exactly once.
    """
    testdir.makepyfile("""
        def test_b(): pass
        def test_c(): pass
        def test_d(): pass
        def test_e(): pass
        def test_f(): pass
        def test_g(): pass
        def test_h(): pass
        def test_i(): pass
        def test_j(): pass
        def test_k(): pass
        def test_l(): pass
        def test_m(): pass
        def test_n(): pass
        def test_o(): pass
        def test_p(): pass
        def test_q(): pass
        def test_r(): pass
        def test_s(): pass
        def test_t(): pass
        def test_u(): pass
        def test_v(): pass
        def test_w(): pass
        def test_x(): pass
        def test_y(): pass
        def test_z(): pass
    """)

    result = testdir.inline_run('--test-group-count', '2',
                                '--test-group', '1',
                                '--test-group-random-seed', '5')
    group_1 = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']
    result.assertoutcome(passed=13)

    result = testdir.inline_run('--test-group-count', '2',
                                '--test-group', '2',
                                '--test-group-random-seed', '5')
    group_2 = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']
    result.assertoutcome(passed=12)

    result = testdir.inline_run('--test-group-count', '1',
                                '--test-group', '1',
                                '--test-group-random-seed', '5')
    all_tests = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']

    assert set(group_1 + group_2) == set(all_tests)

def test_group_by_files(testdir):
    testdir.makepyfile(test_file_1="""
        def test_a(): pass
        def test_b(): pass
        def test_c(): pass
    """,
                       test_file_2="""
        def test_d(): pass
        def test_e(): pass
     """)

    result = testdir.inline_run('--test-group-count', '2',
                                '--test-group', '1',
                                '--test-group-by', 'filename')
    group_1 = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']
    result.assertoutcome(passed=3)

    assert set(group_1) == {'test_a', 'test_b', 'test_c'}

    result = testdir.inline_run('--test-group-count', '2',
                                '--test-group', '2',
                                '--test-group-by', 'filename')
    group_2 = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']
    result.assertoutcome(passed=2)
    assert set(group_2) == {'test_d', 'test_e'}


def test_group_by_files__more_groups_than_files(testdir):
    testdir.makepyfile(test_file_1="""
        def test_a(): pass
        def test_b(): pass
    """,
                       test_file_2="""
        def test_c(): pass
        def test_d(): pass
        def test_e(): pass
     """)

    result = testdir.inline_run(
        '--test-group-count', '3',
        '--test-group', '1',
        '--test-group-by', 'filename',
    )
    group_1 = set(x.item.name for x in result.calls if x._name == 'pytest_runtest_call')
    result.assertoutcome(passed=3)

    assert group_1 == {'test_c', 'test_d', 'test_e'}

    result = testdir.inline_run(
        '--test-group-count', '3',
        '--test-group', '2',
        '--test-group-by', 'filename',
    )

    group_2 = set(x.item.name for x in result.calls if x._name == 'pytest_runtest_call')
    result.assertoutcome(passed=2)

    assert group_2 == {'test_a', 'test_b'}

    result = testdir.inline_run(
        '--test-group-count', '3',
        '--test-group', '3',
        '--test-group-by', 'filename',
    )

    group_3 = set(x.item.name for x in result.calls if x._name == 'pytest_runtest_call')
    result.assertoutcome(passed=0)

    assert group_3 == set()


def test_group_by_files__more_files_than_groups(testdir):
    testdir.makepyfile(test_file_1="""
        def test_a(): pass
        def test_b(): pass
    """,
                       test_file_2="""
        def test_c(): pass
        def test_d(): pass
        def test_e(): pass
     """)

    result = testdir.inline_run(
        '--test-group-count', '1',
        '--test-group', '1',
        '--test-group-by', 'filename',
    )
    result.assertoutcome(passed=5)

def test_group_runs_after_std_item_collection(testdir):
    """If @pytest.hookimpl(hookwrapper=True) is not used, the plugin will split the item
    list of items before other filtering (like -k) has been applied. This could potentially
    result in non-evenly sized groups or even empty groups.

    This test splits the two tests into two groups but excludes the first test with -k.
    Before adding pytest.hookimpl, this test failed because test_x was in group 2 instead of group 1.
    """
    testdir.makepyfile("""
        def test_x(): pass
        def test_y(): pass
    """)

    result = testdir.runpytest_subprocess('-k', 'test_y', '--test-group-count', '2', '--test-group', '1')
    result.assert_outcomes(passed=1)

    result = testdir.runpytest_subprocess('-k', 'test_y', '--test-group-count', '2', '--test-group', '2')
    assert 'Invalid test-group argument' in result.stderr.str()

def test_random_group_runs_in_original_order(testdir):
    """When running tests with a random seed, check test order is unchanged"""
    testdir.makepyfile("""
        def test_i(): pass
        def test_h(): pass
        def test_g(): pass
        def test_f(): pass
        def test_e(): pass
        def test_d(): pass
        def test_c(): pass
        def test_b(): pass
    """)

    result = testdir.inline_run('--test-group-count', '2',
                                '--test-group', '1',
                                '--test-group-random-seed', '5')
    group_1 = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']
    assert group_1 == sorted(group_1, reverse=True)