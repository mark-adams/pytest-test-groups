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
