from collections.abc import Iterable
from datetime import datetime, timedelta

from past.builtins import basestring

from tests.util.joiner import join


def assert_that(actual):
    if isinstance(actual, basestring):
        return StringAssert(actual)
    elif isinstance(actual, bool):
        return BooleanAssert(actual)
    elif isinstance(actual, int):
        return NumberAssert(actual)
    elif isinstance(actual, Iterable):
        return IterableAssert(actual)
    elif isinstance(actual, datetime):
        return DatetimeAssert(actual)
    else:
        return AbstractAssert(actual)


class AbstractAssert():

    def __init__(self, actual):
        self.actual = actual

    def is_instance(self, cls):
        assert isinstance(self.actual, cls), "expected actual to be of type " + str(cls) + ", but was " + str(
            type(self.actual))
        return self

    def is_not_instance(self, cls):
        assert not isinstance(self.actual, cls), "expected actual to not be of type " + str(cls) + ", but was " + str(
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
        assert expected in str(self.actual), "[" + str(self.actual) + "] does not contain [" + str(expected) + "]"
        return self

    def is_blank(self):
        assert self.__is_blank(), "Expected " + str(self.actual) + " to be blank."
        return self

    def is_not_blank(self):
        assert not self.__is_blank(), "Expected " + str(self.actual) + " to not be blank."
        return self

    def __is_blank(self):
        return self.actual is not None and len(self.actual.strip()) == 0


class DatetimeAssert(AbstractAssert):

    def is_between(self, after, before):
        assert after <= self.actual <= before, "Expected actual (" + str(
            self.actual) + ") to be in the range [" + str(
            after) + ", " + str(before) + "]"
        return self

    def is_between_now_minus_and_plus_minutes(self, now, minutes):
        after = now - timedelta(minutes=minutes)
        before = now + timedelta(minutes=minutes)
        return self.is_between(after, before)


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

    def is_between(self, min, max):
        assert min <= self.actual <= max, "Expected actual (" + str(
            self.actual) + ") to be in the range [" + str(
            min) + ", " + str(max) + "]"
        return self


class IterableAssert(AbstractAssert):

    def has_size(self, expected):
        assert len(self.actual) == expected, str(self.actual) + " has size [" + str(
            len(self.actual)) + "], but expected size [" + str(expected) + "]"
        return self

    def is_empty(self):
        return self.has_size(0)

    def is_not_empty(self):
        assert len(self.actual) > 0, "expected " + str(self.actual) + " to be empty."
        return self

    def contains(self, *args):
        for arg in args:
            assert arg in self.actual, "expected " + str(self.actual) + " to contain " + str(args)

    def does_not_contain(self, *args):
        for arg in args:
            assert arg not in self.actual, "expected " + str(self.actual) + " not to contain " + str(args)

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

    def contains_no_nones(self):
        for item in self.actual:
            assert_that(item).is_not_none()

    def extracting(self, field_name):
        values = []
        for item in self.actual:
            if (isinstance(item, dict)):
                values.append(item.get(field_name))
            else:
                values.append(getattr(item, field_name, None))
        return assert_that(values)

    def mapping(self, fn):
        values = []
        for item in self.actual:
            values.append(fn(item))
        return assert_that(values)
