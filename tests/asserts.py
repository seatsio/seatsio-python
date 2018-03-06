def assertThat(actual):
    if isinstance(actual, basestring):
        return StringAssert(actual)


class StringAssert:

    pass
