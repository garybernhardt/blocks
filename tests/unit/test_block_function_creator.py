from expecter import expect
from textwrap import dedent
from blocks.blockfunctioncreator import BlockFunctionCreator


class describe_block_function_creator:
    def it_translates_blocks_to_functions(self):
        assert_translated(
            dedent("""
                   describe() do:
                       return 5
                   """),
            dedent("""
                   describe (%(function_name)s )
                   def %(function_name)s ():

                       return 5 
                   """))

    def it_generates_unique_function_names(self):
        creator1 = BlockFunctionCreator('')
        creator2 = BlockFunctionCreator('')
        expect(creator1.function_name) != creator2.function_name

    def it_passes_block_function_arguments(self):
        assert_translated(
            dedent("""
                   describe(4) do:
                       return 5
                   """),
            dedent("""
                   describe (4 ,%(function_name)s )
                   def %(function_name)s ():

                       return 5 
                   """))

    # def it_translates_nested_blocks
    # def it_translates_with_code_before_and_after_block_calls
    # def it_translates_blocks_with_arguments


def assert_translated(original, expected):
    creator = BlockFunctionCreator(original)
    translated = creator.translate()
    function_name = creator.function_name
    expect(translated) == expected % dict(function_name = function_name)

