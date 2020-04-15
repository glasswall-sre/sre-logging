import logging

import pytest

import srelogging


def test_configure_logging_file(mock_filesystem):
    with open("logging.yaml", 'w') as logging_config_file:
        logging_config_file.write("""version: 1
formatters:
  default:
    class: srelogging.UTCFormatter
    format: "%(asctime)s.%(msecs)03dZ [%(levelname)s] <%(module)s.py:%(lineno)d> %(message)s"
    datefmt: "%Y-%m-%d %H:%M:%S"
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: default
    stream: ext://sys.stdout
root:
  level: WARNING
  handlers: [console]

""")
    srelogging.configure_logging("logging.yaml")
    assert logging.root.handlers[
        0].formatter._fmt == "%(asctime)s.%(msecs)03dZ [%(levelname)s] <%(module)s.py:%(lineno)d> %(message)s"


def test_configure_logging_file_error(capsys):
    srelogging.configure_logging("notexist.yaml")
    captured = capsys.readouterr()
    assert "error loading logging config: [Errno 2] No such file or directory: 'notexist.yaml' - using default instead" in captured.out
