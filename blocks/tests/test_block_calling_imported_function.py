#coding: blocks
from blocktaker import block_taker


x = block_taker() do:
    return 5
assert x == 5

print 'OK!'

