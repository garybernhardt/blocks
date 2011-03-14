from copy import deepcopy
from ast import parse, dump
from textwrap import dedent

from expecter import expect

from blocks.functionpredefiner import FunctionPredefiner
from blocks.blockfunctioncreator import BLOCK_FUNCTION_NAME


class describe_function_predefiner:
    def it_moves_function_before_use(self):
        assert_translated(
            """
            block_taker(%(function_name)s)
            def %(function_name)s():
                pass
            """ % dict(function_name=BLOCK_FUNCTION_NAME),
            """
            def %(function_name)s():
                pass
            block_taker(%(function_name)s)
            """ % dict(function_name=BLOCK_FUNCTION_NAME))

    def it_ignores_functions_that_arent_blocks(self):
        original = (
            """
            block_taker(some_function)
            def some_function():
                pass
            """)
        assert_translated(original, original)

    # def it_doesnt_translate_function_definitions_around_blocks


def assert_translated(original, expected):
    parsed_original = parse(dedent(original))
    parsed_expected = parse(dedent(expected))
    predefiner = FunctionPredefiner(parsed_original)
    transformed = predefiner.transform()
    expect(dump(transformed)) == dump(parsed_expected)

