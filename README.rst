.. image:: https://img.shields.io/pypi/v/pytest-test-groups.svg
    :target: https://pypi.org/project/pytest-test-groups/

.. image:: https://img.shields.io/pypi/pyversions/pytest-test-groups.svg
    :target: https://pypi.org/project/pytest-test-groups/

.. image:: https://github.com/mark-adams/pytest-test-groups/actions/workflows/python-tests.yml/badge.svg
    :target: https://github.com/mark-adams/pytest-test-groups/actions?query=workflow%3Apython-tests
    
Welcome to pytest-test-groups!
==============================

pytest-test-groups allows you to split your test runs into groups of a specific
size to make it easier to split up your test runs.


Usage
---------------------

::

    # Install pytest-test-groups
    pip install pytest-test-groups

    # Split the tests into 10 groups and run the second group
    py.test --test-group-count 10 --test-group=2
    
    # Assign tests pseudo-randomly into 10 groups, and run the second group
    py.test --test-group-count 10 --test-group=2 --test-group-random-seed=12345

    # Split the tests by files instead of items into 3 groups and run the second group.
    # The groups might not be in the same size as each group contains full test files
    py.test --test-group-count 10 --test-group=2 --test-group-by filename


Why would I use this?
------------------------------------------------------------------

Sometimes you may have some long running test jobs that take a
while to complete. This can be a major headache when trying to
run tests quickly. pytest-test-groups allows you to easily say
"split my tests into groups of 10 tests and run the second group".
This is primarily useful in the context of CI builds.


Command-line Arguments
----------------------

.. option:: --test-group-count <N>

   Total number of groups to split the tests into. There must be at least this many tests.

.. option:: --test-group <I>

   The ``[1, N]`` test group to run, where ``N`` is the ``--test-group-count`` argument.
   Use ``0`` to run all tests.

.. option:: --test-group-random-seed <SEED>

   If provided, assigns tests to groups pseudo-randomly using the given seed.
   The default is a consisten order based on test node id hash.

.. option:: --test-group-by <method>

   Method for assigning tests to groups. Valid options are:

   - ``item`` (default): Split by individual test items (default behavior).
   - ``filename``: Split by test files, all tests from a single file remain in the same group.
