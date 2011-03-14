from expecter import expect
from textwrap import dedent
from blocks.blockfunctioncreator import BlockFunctionCreator


class describe_block_function_creator:
    def it_translates_blocks_to_functions(self):
        assert_translated(
            """
            describe() do:
                return 5
            """,
            """
            describe (%(function_name)s )
            def %(function_name)s ():

                return 5 
            """)

    def it_passes_block_function_arguments(self):
        assert_translated(
            """
            describe(4) do:
                return 5
            """,
            """
            describe (4 ,%(function_name)s )
            def %(function_name)s ():

                return 5 
            """)

    def it_translates_with_code_before_and_after_block_calls(self):
        assert_translated(
            """
            x = 1
            describe(4) do:
                return 5
            y = 6
            """,
            """
            x =1 
            describe (4 ,%(function_name)s )
            def %(function_name)s ():

                return 5 
            y =6 
            """)

    def it_translates_nested_blocks(self):
        assert_translated(
            """
            describe('something') do:
                it('does something') do:
                    expect(1) == 2
            """,
            """
            describe ('something',%(function_name)s )
            def %(function_name)s ():

                it ('does something',%(function_name)s )
                def %(function_name)s ():

                    expect (1 )==2 
            """)

    # def it_translates_blocks_with_arguments


def assert_translated(original, expected):
    original, expected = dedent(original), dedent(expected)
    creator = BlockFunctionCreator(original)
    translated = creator.translate()
    function_name = creator.function_name
    expected = expected % dict(function_name = function_name)
    try:
        expect(translated) == expected
    # XXX: Expecter should do this for us
    except AssertionError:
        print 'Failed assertion:\n-%s-\n-%s-' % (
            translated.replace(' ', '_'),
            expected.replace(' ', '_'))
        raise

