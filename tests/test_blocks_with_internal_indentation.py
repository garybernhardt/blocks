#coding: blocks

def block_taker(block):
    return block()
# Test block with indentation inside
x = block_taker() do:
    if True:
        return 4
assert x == 4

print 'OK!'

