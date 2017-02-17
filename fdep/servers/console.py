# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
from inspect import signature

from fdep.servers import RPCServer


class ConsoleServer(RPCServer):
    """Implement a simple console try out interface."""

    def register_functions(self, func_pairs):
        self.funcs = dict(func_pairs)

    def serve_forever(self, **kwargs):
        if not kwargs.get('func'):
            print(
                'Missing --func. Available functions: {}'.format(
                    ', '.join(self.funcs.keys())
                ),
                file=sys.stderr
            )
            return

        func_name = kwargs['func']
        func = self.funcs[func_name]
        params = list(signature(func).parameters)

        args = []
        for param in params:
            if kwargs.get(param):
                arg = kwargs[param]
            else:
                sys.stderr.write("{}: ".format(param))
                sys.stderr.flush()
                arg = sys.stdin.readline().strip()
            args.append(arg)
        print(self.funcs[func_name](*args))
