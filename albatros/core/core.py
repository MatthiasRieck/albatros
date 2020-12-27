class AlbatrosError(Exception):
    """General exception used in albatros python"""


def assert_that(condition, exception):
    """
    assert_that(condition, exception)

    In case `condition` is not met the `exception` is raised.

    Parameters
    ----------
    condition : Scalar, boolean expression that will be checked
    exception : Exception to be thrown in case the condition is not met
    """

    if not condition:
        raise exception


class ConsistencyCheckable:
    """Class that implements a check_consistency method"""

    def check_consistency(self):
        """Implementations of these method shall raise Exceptions/Errors"""
        raise NotImplementedError
