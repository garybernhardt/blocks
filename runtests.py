#!/usr/bin/env python

import sys

import nose


if __name__ == '__main__':
    nose_args = sys.argv + [r'-m',
                            r'((?:^|[b_.-])(:?test|describe|it))',
                            r'--with-doctest',
                            r'--doctest-extension=']
    nose.run(argv=nose_args)

