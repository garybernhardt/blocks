from expecter import expect
from textwrap import dedent
from blocks.blockfunctioncreator import BlockFunctionCreator


class describe_block_function_creator:
    def it_translates_blocks_to_functions(self):
        source = dedent("""
                        describe() do:
                            return 5
                        """)
        creator = BlockFunctionCreator(source)
        translated = creator.translate()
        function_name = creator.anonymous_function_name
        expected = dedent("""
                          describe(%s)
                          def %s():
                          return 5
                          """ %
                          (function_name, function_name))
        expect(translated) == expected

