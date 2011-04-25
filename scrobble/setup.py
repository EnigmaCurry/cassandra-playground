import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pyramid',
    'pyramid_beaker',
    'SQLAlchemy',
    'transaction',
    'repoze.tm2>=1.0b1', # default_commit_veto
    'zope.sqlalchemy',
    'WebError',
    'pycassa',
    'thrift',
    'py-bcrypt',
    'babel'
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='scrobble',
      version='0.0',
      description='scrobble',
      long_description="A demo Last.fm clone written for Cassandra",
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='scrobble',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = scrobble:main
      """,
      paster_plugins=['pyramid'],
      )

