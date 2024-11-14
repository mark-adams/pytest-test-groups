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
    
    # Randomize the test order, split into 10 groups, and run the second group
    py.test --test-group-count 10 --test-group=2 --test-group-random-seed=12345


Why would I use this?
------------------------------------------------------------------

Sometimes you may have some long running test jobs that take a
while to complete. This can be a major headache when trying to
run tests quickly. pytest-test-groups allows you to easily say
"split my tests into groups of 10 tests and run the second group".
This is primarily useful in the context of CI builds.
