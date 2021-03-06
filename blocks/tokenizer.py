import traceback
import random
import sys
from tokenize import generate_tokens, NAME, OP, STRING, NL, INDENT, DEDENT
from encodings import utf_8
import codecs
import cStringIO
import encodings
import tokenize


def translate(token_generator):
    result     = []

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
        """
        Read tokens until we're at the indentation level higher that we started
        at, which means we've exited the block definition
        """
        indentation_level = 0
        seen_indent = False

        while True:
            tokenum, value, _, _, _ = self.token_generator.next()
            self.result.append([tokenum, value])

            if tokenum == INDENT:
                indentation_level += 1
                seen_indent = True
            elif tokenum == DEDENT:
                indentation_level -= 1

            if seen_indent and indentation_level == 0:
                break

    def pop_partial_function_call(self):
        removed_nodes = []
        while True:
            token = self.result.pop()
            if token in ([NL, '\n'], [DEDENT, '']):
                # Don't remove the newline or dedent
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
        try:
            tokens = generate_tokens(self.stream.readline)
            data = tokenize.untokenize(translate(tokens))
        except Exception, e:
            traceback.print_exc()
            raise
        self.stream = cStringIO.StringIO(data)


def search_function(s):
    if s!='blocks': return None
    utf8=encodings.search_function('utf8')
    return codecs.CodecInfo(
        name='blocks',
        encode = utf8.encode,
        decode = utf8.decode,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=utf8.incrementaldecoder,
        streamreader=StreamReader,
        streamwriter=utf8.streamwriter)


codecs.register(search_function)

