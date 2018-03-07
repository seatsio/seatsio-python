def assertThat(actual):
    if isinstance(actual, basestring):
        return StringAssert(actual)
    elif isinstance(actual, bool):
        return BooleanAssert(actual)
    elif isinstance(actual, int):
        return NumberAssert(actual)
    elif isinstance(actual, list):
        return ListAssert(actual)
    else:
        return AbstractAssert(actual)

class AbstractAssert():

    def __init__(self, actual):
        self.actual = actual

    def isNone(self):
        assert self.actual is None, "expected actual to be None, but it was not: " + str(self.actual)

    def isNotNone(self):
        assert self.actual is not None, "expected actual to not be None, but it was None"
        return self

    def isEqualTo(self, expected):
        assert self.actual == expected, "expected " + str(self.actual) + " to be equal (==) to " + str(expected)
        return self


class StringAssert(AbstractAssert):

    def contains(self, expected):
        assert expected in self.actual, "[" + self.actual + "] does not contain [" + expected + "]"
        return self

    def isBlank(self):
        assert self.__isBlank() == True, "Expected " + str(self.actual) + " to be blank."

    def isNotBlank(self):
        assert self.__isBlank() == False, "Expected " + str(self.actual) + " to not be blank."

    def __isBlank(self):
        return self.actual is not None and len(self.actual.strip()) == 0

class BooleanAssert(AbstractAssert):

    def isFalse(self):
        assert self.actual == False, "Expected " + str(self.actual) + " to be False, but it was True"

    def isTrue(self):
        assert self.actual == True, "Expected " + str(self.actual) + " to be True, but it was False"

class NumberAssert(AbstractAssert):

    def isNotZero(self):
        assertThat(self.actual == 0).isFalse()

    def isZero(self):
        assertThat(self.actual == 0).isTrue()

class ListAssert(AbstractAssert):

    def hasSize(self, expected):
        assert len(self.actual) == expected, str(self.actual) + " has size [" + str(len(self.actual)) + "], but expected size [" + str(expected) + "]"
        return self

    def isEmpty(self):
        return self.hasSize(0)

    def containsExactlyInAnyOrder(self, *args):
        self.hasSize(len(args))
        for arg in args:
            assert arg in self.actual, "expected " + str(self.actual) + " to contain " + str(args)
        return self
