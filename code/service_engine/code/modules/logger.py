import logging
from sys import stdout
from os import environ


if environ.get('LOG_LEVEL') == 'DEBUG':
  logging.basicConfig(stream=stdout, level=logging.DEBUG)
else:
  logging.basicConfig(stream=stdout, level=logging.INFO)