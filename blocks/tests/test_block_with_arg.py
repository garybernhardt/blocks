#coding: blocks

def block_taker_with_arg(x, block):
    return x + block()
# Test block with indentation inside
x = block_taker_with_arg(1) do:
    return 2
assert x == 3

print 'OK!'

