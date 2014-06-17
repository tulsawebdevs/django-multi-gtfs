#!/usr/bin/env python
'''Generate tox.ini'''

from __future__ import print_function

# Python versions (major, minor)
pythons = [(2, 7), (3, 4)]
# Python package versions (major, minor)
djangos = [(1, 5), (1, 6)]
souths = [(0, 8), (None, None)]
# Backend databases (names)
dbs = ['spatiallite', 'postgis']


# Base environments are used to build up the specific environments
base_environs = {
    'postgis': '''\
deps=
    psycopg2
'''}

# Populate base environments for package versions
for major, minor in djangos:
    name = "django{}{}".format(major, minor)
    base_environs[name] = '''\
deps=
    Django>={major}.{minor},<{major}.{next_minor}
'''.format(major=major, minor=minor, next_minor=minor+1)

for major, minor in souths:
    if major is not None:
        name = "south{}{}".format(major, minor)
        base_environs[name] = '''\
deps=
    South>={major}.{minor},<{major}.{next_minor}
'''.format(major=major, minor=minor, next_minor=minor+1)

# Environs are test environments
environs = dict()

for py_major, py_minor in pythons:
    py_name = 'py{}{}'.format(py_major, py_minor)
    basepython = 'python{}.{}'.format(py_major, py_minor)
    for dj_major, dj_minor in djangos:
        dj_name = 'django{}{}'.format(dj_major, dj_minor)
        for s_major, s_minor in souths:
            if s_major is None:
                s_name = 'southNo'
            else:
                s_name = 'south{}{}'.format(s_major, s_minor)
            for db in dbs:
                environ = (
                    '{py_name}-{dj_name}-{s_name}-{db_name}'.format(
                        py_name=py_name, dj_name=dj_name, s_name=s_name,
                        db_name=db))
                env = "basepython = {}\n".format(basepython)
                deps = []
                deps.append('{[' + dj_name + ']deps}')
                if s_major is not None:
                    deps.append('{[' + s_name + ']deps}')
                if db == 'postgis':
                    env += "setenv =\n    MULTIGTFS_TEST_POSTGIS = 1\n"
                    deps.append('{[postgis]deps}')
                deps.append('{[testenv]deps}')
                env += "deps =\n    " + "\n    ".join(deps)
                environs[environ] = env

# print out the tox.ini
env_names = sorted(environs.keys())
env_names_out = ",\n    ".join(env_names)
print("""\
[tox]
envlist =
    {}

[flake8]
exclude = .tox/*

[testenv]
deps=
    nose
    django-nose
    jsonfield
commands=./run_tests.py
""".format(env_names_out))

for name in sorted(base_environs.keys()):
    print("""\
[{}]
{}""".format(name, base_environs[name]))

for name in sorted(environs.keys()):
    print("""\
[testenv:{}]
{}
""".format(name, environs[name]))
