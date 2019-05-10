"""Module for running all test
"""
import unittest
from track_record.tests import db_tests  # , stat_tests


def run_all():
    """Runs all tests"""
    # db_tests.create_test_database()
    runner = unittest.TextTestRunner()
    # result = unittest.TestResult()
    all_tests = unittest.TestSuite()
    all_tests.addTest(db_tests.db_tool_suite())
    runner.run(all_tests)
    # runner.run(all_tests)
    # db_tests.test_database_fill()
    # stat_tests.test_predefined_queries()

    # db_tests.delete_test_database()


if __name__ == "__main__":
    # unittest.main()
    run_all()
