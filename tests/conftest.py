import builtins
import contextlib
from io import StringIO
import os
from os import path

import pytest


class BytesIOWrapper:
    """Used in mock_filesystem as it deals with underlying string types.
    We need it to also support bytes, so this is used as a shim to
    convert to/from bytes."""
    def __init__(self, string_buffer, encoding='utf-8'):
        self.string_buffer = string_buffer
        self.encoding = encoding

    def __getattr__(self, attr):
        return getattr(self.string_buffer, attr)

    def read(self, size=-1):
        content = self.string_buffer.read(size)
        return content.encode(self.encoding)

    def write(self, b):
        content = b.decode(self.encoding)
        return self.string_buffer.write(content)


@pytest.fixture
def mock_filesystem(monkeypatch):
    """Fixture used to mock open() and walk() to make sure tests don't write 
    to the host filesystem."""
    files = {}

    @contextlib.contextmanager
    def mocked_open(filename, encoding, *args, **kwargs):
        filename = path.normpath(filename)
        if "b" in encoding:
            # use BytesIOWrapper as a shim to transparently handle underlying
            # string datatype
            file = BytesIOWrapper(StringIO(files.get(filename, "")))
        else:
            file = StringIO(files.get(filename, ""))
        try:
            yield file
        finally:
            files[filename] = file.getvalue()
            file.close()

    def mocked_walk(*args, **kwargs):
        yield "", [], files.keys()

    def mocked_exists(filepath):
        return filepath in files

    monkeypatch.setattr(builtins, "open", mocked_open)
    monkeypatch.setattr(os, "walk", mocked_walk)
    monkeypatch.setattr(path, "exists", mocked_exists)