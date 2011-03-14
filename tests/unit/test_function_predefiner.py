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

    def it_doesnt_translate_function_definitions_around_blocks(self):
        assert_translated(
            """
            def before(something):
                pass
            block_taker(%(function_name)s)
            def %(function_name)s():
                pass
            def after(something):
                pass
            """ % dict(function_name=BLOCK_FUNCTION_NAME),
            """
            def before(something):
                pass
            def %(function_name)s():
                pass
            block_taker(%(function_name)s)
            def after(something):
                pass
            """ % dict(function_name=BLOCK_FUNCTION_NAME))

    def it_translates_nested_blocks(self):
        assert_translated(
            """
            block_taker(%(function_name)s_1)
            def %(function_name)s_1():
                block_taker(%(function_name)s_2)
                def %(function_name)s_2():
                    pass
            """ % dict(function_name=BLOCK_FUNCTION_NAME),
            """
            def %(function_name)s_1():
                def %(function_name)s_2():
                    pass
                block_taker(%(function_name)s_2)
            block_taker(%(function_name)s_1)
            """ % dict(function_name=BLOCK_FUNCTION_NAME))

    def it_translates_consecutive_blocks(self):
        assert_translated(
            """
            block_taker(%(function_name)s_1)
            def %(function_name)s_1():
                pass
            block_taker(%(function_name)s_2)
            def %(function_name)s_2():
                pass
            """ % dict(function_name=BLOCK_FUNCTION_NAME),
            """
            def %(function_name)s_1():
                pass
            block_taker(%(function_name)s_1)
            def %(function_name)s_2():
                pass
            block_taker(%(function_name)s_2)
            """ % dict(function_name=BLOCK_FUNCTION_NAME))

    # def it_translates_blocks_that_arent_the_first_arg(self):


def assert_translated(original, expected):
    parsed_original = parse(dedent(original))
    parsed_expected = parse(dedent(expected))
    predefiner = FunctionPredefiner(parsed_original)
    transformed = predefiner.transform()
    try:
        expect(dump(transformed)) == dump(parsed_expected)
    except:
        print
        print 'expected:'
        print '-%s-' % dump(parsed_expected, annotate_fields=False)
        print
        print 'actual:'
        print '-%s-' % dump(transformed, annotate_fields=False)
        print
        raise

