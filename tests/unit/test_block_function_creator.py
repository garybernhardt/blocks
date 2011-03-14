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
        function_name = creator.function_name
        expected = dedent("""
                          describe(%s)
                          def %s():
                          return 5
                          """ %
                          (function_name, function_name))
        expect(translated) == expected

    def it_generates_unique_function_names(self):
        creator1 = BlockFunctionCreator('')
        creator2 = BlockFunctionCreator('')
        expect(creator1.function_name) != creator2.function_name

