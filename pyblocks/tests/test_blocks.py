#coding: pyblocks

def function_taking_block(block):
    return block()


x = function_taking_block() do:
    return 5


assert x == 5

