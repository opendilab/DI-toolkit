import os.path

_TESTFILE_DIR = os.path.normpath(os.path.join(__file__, '..', '..', 'testfile'))


def get_testfile(path, *paths):
    return os.path.join(_TESTFILE_DIR, path, *paths)
