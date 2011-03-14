from textwrap import dedent
import random
from tokenize import generate_tokens, NAME, OP, STRING, NL, INDENT, DEDENT
from StringIO import StringIO
import tokenize


class BlockFunctionCreator:
    def __init__(self, source):
        self.source = source
        self.function_name = '__block_function'

    def translate(self):
        tokens = generate_tokens(StringIO(self.source).readline)

        result = []

        for tokenum, value, _, _, _ in tokens:
            if tokenum == NAME and value == 'do':
                BlockTranslator(tokens, result, self.function_name).translate()
            else:
                result.append([tokenum, value])

        return tokenize.untokenize(result)


class BlockTranslator:
    def __init__(self, token_generator, result, function_name):
        self.token_generator = token_generator
        self.result = result
        self.function_name = function_name

    def anonymous_function_name(self):
        random_string = ''.join(random.choice('0123456789')
                                for _ in range(32))
        return '_anon_func_%s' % random_string

    def translate(self):
        # Consume the colon after the "do"
        self.token_generator.next()

        # Add the new anonymous function as an argument to the call
        self.add_anonymous_function_as_argument()

        # Add the function definition
        self.add_anonymous_function()

    def add_anonymous_function(self):
        self.result.append([NAME, 'def'])
        self.result.append([NAME, self.function_name])
        self.result.append([OP, '('])
        self.result.append([OP, ')'])
        self.result.append([OP, ':'])
        self.result.append([NL, '\n'])

    def add_anonymous_function_as_argument(self):
        closing_function_call_paren = self.result.pop()
        last_token_in_arg_list = self.result[-1]
        call_has_other_args = last_token_in_arg_list != [OP, '(']
        if call_has_other_args:
            self.result.append([OP, ','])
        self.result.append([NAME, self.function_name])
        self.result.append(closing_function_call_paren)
        self.result.append([NL, '\n'])

