def assertThat(actual):
    if isinstance(actual, basestring):
        return StringAssert(actual)
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


class ListAssert(AbstractAssert):

    def hasSize(self, expected):
        assert len(self.actual) == expected, str(self.actual) + " has size [" + str(len(self.actual)) + "], but expected size [" + str(expected) + "]"
        return self
