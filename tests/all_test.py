""" Our tests are defined in here """
from mockle.mockle import donotrun


def test_donotrun():
    donotrun(str, [1])
