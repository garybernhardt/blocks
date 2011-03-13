import random
import sys
from tokenize import generate_tokens, NAME, OP, STRING, NL, DEDENT
from encodings import utf_8
import codecs
import cStringIO
import encodings
import tokenize


def translate(readline):
    result     = []

    token_generator = generate_tokens(readline)

    for tokenum, value, _, _, _ in token_generator:
        if tokenum == NAME and value == 'do':
            BlockTranslator(token_generator, result).translate()
        else:
            result.append([tokenum, value])

    return result


class BlockTranslator:
    def __init__(self, token_generator, result):
        self.token_generator = token_generator
        self.result = result
        self.function_name = self.anonymous_function_name()

    def anonymous_function_name(self):
        random_string = ''.join(random.choice('0123456789')
                                for _ in range(32))
        return '_anon_func_%s' % random_string

    def translate(self):
        # Consume the colon after the "do"
        self.token_generator.next()

        # Remove the call so we can add the def before it
        popped_function_call = self.pop_partial_function_call()

        # Add the function definition
        self.add_anonymous_function()

        # Fast forward past the body of the function
        self.fast_forward_to_end_of_block_definition()

        # Restore to the point where we started before we rolled back to add
        # the def
        self.restore_popped_partial_function_call(popped_function_call)

        # Add the new anonymous function as an argument to the call
        self.add_anonymous_function_as_argument()

    def add_anonymous_function(self):
        self.result.append([NAME, 'def'])
        self.result.append([NAME, self.function_name])
        self.result.append([OP, '('])
        self.result.append([OP, ')'])
        self.result.append([OP, ':'])
        self.result.append([NL, '\n'])

    def fast_forward_to_end_of_block_definition(self):
        while True:
            tokenum, value, _, _, _ = self.token_generator.next()
            self.result.append([tokenum, value])

            if tokenum == DEDENT:
                break

    def pop_partial_function_call(self):
        removed_nodes = []
        while True:
            token = self.result.pop()
            if token == [DEDENT, '']:
                self.result.append(token)
                break
            else:
                removed_nodes.append(token)

        removed_nodes = list(reversed(removed_nodes))
        return removed_nodes

    def add_anonymous_function_as_argument(self):
        closing_function_call_paren = self.result.pop()
        last_token_in_arg_list = self.result[-1]
        call_has_other_args = last_token_in_arg_list != [OP, '(']
        if call_has_other_args:
            self.result.append([OP, ','])
        self.result.append([NAME, self.function_name])
        self.result.append(closing_function_call_paren)
        self.result.append([NL, '\n'])

    def restore_popped_partial_function_call(self, popped_function_call):
        self.result.extend(popped_function_call)


class StreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        data = tokenize.untokenize(translate(self.stream.readline))
        self.stream = cStringIO.StringIO(data)


def search_function(s):
    if s!='pyblocks': return None
    utf8=encodings.search_function('utf8')
    return codecs.CodecInfo(
        name='pyblocks',
        encode = utf8.encode,
        decode = utf8.decode,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=utf8.incrementaldecoder,
        streamreader=StreamReader,
        streamwriter=utf8.streamwriter)


codecs.register(search_function)

