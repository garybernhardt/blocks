from ast import parse, dump
from textwrap import dedent

from expecter import expect

from blocks.functionpredefiner import FunctionPredefiner
from blocks.blockfunctioncreator import BLOCK_FUNCTION_NAME


class describe_function_predefiner:
    def it_moves_function_before_use(self):
        original = dedent(
            """
            block_taker(%(function_name)s)
            def %(function_name)s():
                pass
            """ % dict(function_name=BLOCK_FUNCTION_NAME))
        expected = dedent(
            """
            def %(function_name)s():
                pass
            block_taker(%(function_name)s)
            """ % dict(function_name=BLOCK_FUNCTION_NAME))
        parsed_original = parse(original)
        parsed_expected = parse(expected)
        predefiner = FunctionPredefiner(parsed_original)
        transformed = predefiner.transform()
        expect(dump(transformed)) == dump(parsed_expected)
