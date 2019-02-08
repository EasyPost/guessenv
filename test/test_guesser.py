from guessenv import guesser


def test_basic():
    e = guesser.EnvVisitor()
    e.parse_and_visit('''
    import os
    from os import environ

    os.environ["one"]
    os.environ.get("two")
    os.environ.get("three", default="bar")
    os.getenv("four")
    os.getenv("five", "bar")
    environ['six']
    environ['sev' 'en']

    not_environment = {}
    not_environment.get('nope')
    not_environment['nope']
    '''.replace('    ', ''))
    assert e.optional_environment_variables == set(['two', 'three', 'four', 'five'])
    assert e.required_environment_variables == set(['one', 'six', 'seven'])


def test_environ_method_call():
    e = guesser.EnvVisitor()
    e.parse_and_visit('''
    import os

    KEY = os.environ['foo'].strip()
    '''.replace('    ', ''))
    assert e.optional_environment_variables == set()
    assert e.required_environment_variables == set(['foo'])


def test_nested():
    e = guesser.EnvVisitor()
    e.parse_and_visit('''
    import os

    FOO = os.environ[os.environ['foo']]
    BAR = os.getenv(os.getenv('bar'))
    '''.replace('    ', ''))
    assert e.optional_environment_variables == set(['bar'])
    assert e.required_environment_variables == set(['foo'])
