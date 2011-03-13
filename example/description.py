# coding: pyblocks
# No nested blocks yet. :(


def describe(description, block):
    print description
    block()

describe('something') do:
    assert 1 == 1

describe('something else') do:
    assert 2 == 2

