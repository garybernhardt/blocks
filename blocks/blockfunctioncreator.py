from textwrap import dedent
import random


class BlockFunctionCreator:
    def __init__(self, source):
        self.function_name = ''.join(random.choice('0123456789')
                                     for _ in range(16))

    def translate(self):
        return dedent("""
                      describe(%s)
                      def %s():
                      return 5
                      """ % (self.function_name, self.function_name))

