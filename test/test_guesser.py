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
