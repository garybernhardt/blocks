#coding: blocks

def block_taker(block):
    return block()
# Test simplest block
x = block_taker() do:
    return 5
assert x == 5

print 'OK!'

