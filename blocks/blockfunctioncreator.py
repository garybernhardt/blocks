from textwrap import dedent


class BlockFunctionCreator:
    def __init__(self, source):
        self.anonymous_function_name = 'block_function'

    def translate(self):
        return dedent("""
                      describe(block_function)
                      def block_function():
                      return 5
                      """)

