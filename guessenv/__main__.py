import argparse
import sys
import io
import os
import os.path
import re
from itertools import repeat

from . import guesser


if sys.version_info < (3, 0):
    open_function = io.open
else:
    open_function = open


class _Exclude(object):
    def __init__(self, regex):
        self.raw = regex
        self.path = re.compile(regex)

    def match(self, path):
        path = path.lstrip('./')
        return self.path.search(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-O', '--with-optional', action='store_true', help='Include optional environment variables')
    parser.add_argument('-A', '--assert-present', action='store_true',
                        help='Exit non-zero if any required environment variables are missing')
    parser.add_argument('-x', '--exclude', action='append', default=[], type=_Exclude,
                        help='Exclude files matching the given regex. May be repeated')
    parser.add_argument('-X', '--standard-exclude', action='store_true', help='Add a standard set of excludes')
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    if args.verbose and args.quiet:
        parser.error('cannot pass both --verbose and --quiet')

    if args.standard_exclude:
        args.exclude.append(_Exclude('^venv/.*'))
        args.exclude.append(_Exclude('^.tox/.*'))
        args.exclude.append(_Exclude('^test/.*'))
        args.exclude.append(_Exclude('^tests/.*'))

    filenames = []
    envvars = []

    # Handle argv.
    for file_or_dir_name in args.files:
        if os.path.isdir(file_or_dir_name):
            for root, _, files in os.walk(file_or_dir_name):
                for f in files:
                    if f.endswith('.py'):
                        full_path = os.path.join(root, f)
                        if any(exclude.match(full_path) for exclude in args.exclude):
                            continue
                        filenames.append(os.path.join(root, f))
        elif os.path.exists(file_or_dir_name):
            if not any(exclude.match(file_or_dir_name) for exclude in args.exclude):
                filenames.append(file_or_dir_name)
        else:
            pass

    status = 0
    for filename in filenames:
        v = guesser.EnvVisitor()
        with open_function(filename, 'r', encoding='utf-8') as f:
            try:
                v.parse_and_visit(f.read(), filename)
                if args.with_optional:
                    envvars.extend(list(zip(
                        repeat(filename),
                        repeat('optional'),
                        sorted(v.optional_environment_variables)
                    )))
                envvars.extend(list(zip(
                    repeat(filename),
                    repeat('required'),
                    sorted(v.required_environment_variables)
                )))
            except SyntaxError as e:
                print('{filename}:{lineno} - syntax error!'.format(
                    filename=filename,
                    lineno=e.lineno
                ))
                status = 1

    if args.assert_present:
        required_envvars = set(v for _, k, v in envvars if k == 'required')
        for envvar in required_envvars:
            if envvar not in os.environ:
                print('MISSING: {0}'.format(envvar))
                status = 1

    if args.verbose:
        for filename, kind, variable_name in envvars:
            print('{filename} {kind} {variable_name}'.format(filename=filename, kind=kind, variable_name=variable_name))
    elif not args.quiet:
        envvars = set(v for _, _, v in envvars)
        print('\n'.join(sorted(str(v) for v in envvars)))

    return status


if __name__ == '__main__':
    sys.exit(main())
