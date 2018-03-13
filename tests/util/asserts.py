import collections

from tests.util.joiner import join


def assert_that(actual):
    if isinstance(actual, basestring):
        return StringAssert(actual)
    elif isinstance(actual, bool):
        return BooleanAssert(actual)
    elif isinstance(actual, int):
        return NumberAssert(actual)
    elif isinstance(actual, collections.Iterable):
        return IterableAssert(actual)
    else:
        return AbstractAssert(actual)


class AbstractAssert():

    def __init__(self, actual):
        self.actual = actual

    def is_instance(self, cls):
        assert isinstance(self.actual, cls), "expected actual to be of type " + str(cls) + ", but was " + str(
            type(self.actual))
        return self

    def is_none(self):
        assert self.actual is None, "expected actual to be None, but it was not: " + str(self.actual)

    def is_not_none(self):
        assert self.actual is not None, "expected actual to not be None, but it was None"
        return self

    def is_equal_to(self, expected):
        assert self.actual == expected, "expected " + str(self.actual) + " to be equal to " + str(expected)
        return self

    def is_not_equal_to(self, expected):
        assert self.actual != expected, "expected " + str(self.actual) + " to be not equal to " + str(expected)
        return self


class StringAssert(AbstractAssert):

    def contains(self, expected):
        assert expected in self.actual, "[" + str(self.actual) + "] does not contain [" + str(expected) + "]"
        return self

    def is_blank(self):
        assert self.__is_blank(), "Expected " + str(self.actual) + " to be blank."
        return self

    def is_not_blank(self):
        assert not self.__is_blank(), "Expected " + str(self.actual) + " to not be blank."
        return self

    def __is_blank(self):
        return self.actual is not None and len(self.actual.strip()) == 0


class BooleanAssert(AbstractAssert):

    def is_false(self):
        assert not self.actual, "Expected " + str(self.actual) + " to be False, but it was True"

    def is_true(self):
        assert self.actual, "Expected " + str(self.actual) + " to be True, but it was False"


class NumberAssert(AbstractAssert):

    def is_not_zero(self):
        assert_that(self.actual == 0).is_false()

    def is_zero(self):
        assert_that(self.actual == 0).is_true()


class IterableAssert(AbstractAssert):

    def has_size(self, expected):
        assert len(self.actual) == expected, str(self.actual) + " has size [" + str(
            len(self.actual)) + "], but expected size [" + str(expected) + "]"
        return self

    def is_empty(self):
        return self.has_size(0)

    def contains_exactly_in_any_order(self, *args):
        self.has_size(len(args))
        for arg in args:
            assert arg in self.actual, "expected " + str(self.actual) + " to contain " + str(args)
        return self

    def contains_exactly(self, *args):
        lst = list(args)
        for index, expectedvalue in enumerate(lst):
            assert expectedvalue == self.actual[index], \
                "on index " + str(index) + ", expected " + str(expectedvalue) + " but was " + str(self.actual[index])
        assert lst == self.actual, "expected [" + join(lst) + "], but was [" + join(self.actual) + "]"
        return self

    def extracting(self, field_name):
        values = []
        for item in self.actual:
            values.append(getattr(item, field_name))
        return assert_that(values)
