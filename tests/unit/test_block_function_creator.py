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
                          describe (%s )
                          def %s ():

                              return 5 
                          """ %
                          (function_name, function_name))
        expect(translated) == expected

    def it_generates_unique_function_names(self):
        creator1 = BlockFunctionCreator('')
        creator2 = BlockFunctionCreator('')
        expect(creator1.function_name) != creator2.function_name

    def it_passes_block_function_arguments(self):
        source = dedent("""
                        describe(4) do:
                            return 5
                        """)
        creator = BlockFunctionCreator(source)
        translated = creator.translate()
        function_name = creator.function_name
        expected = dedent("""
                          describe (4 ,%s )
                          def %s ():

                              return 5 
                          """ %
                          (function_name, function_name))
        expect(translated) == expected

    # def it_translates_nested_blocks
    # def it_translates_with_code_before_and_after_block_calls
    # def it_translates_blocks_with_arguments

