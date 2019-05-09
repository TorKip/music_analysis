"""Module for running all test
"""
from track_record.tests import db_tests, stat_tests


def run_all():
    """Runs all tests"""
    # db_tests.create_test_database()

    # db_tests.test_database_fill()
    # stat_tests.test_predefined_queries()

    # db_tests.delete_test_database()


if __name__ == "__main__":
    run_all()
