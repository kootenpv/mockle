""" You can kind of see this as the scope of `mockle` when you 'import mockle'
The following functions become available:
mockle.__project__
mockle.__version__
mockle.run
mockle.print_version
"""
import sys

__project__ = "mockle"
__version__ = "0.0.2"


def print_version():
    """ Convenient function for printing the version of the package """
    sv = sys.version_info
    py_version = "{}.{}.{}".format(sv.major, sv.minor, sv.micro)
    version_parts = __version__.split(".")
    s = "{} version: [{}], Python {}".format(__project__, __version__, py_version)
    s += "\nMajor version: {}  (breaking changes)".format(version_parts[0])
    s += "\nMinor version: {}  (extra feature)".format(version_parts[1])
    s += "\nMicro version: {} (commit count)".format(version_parts[2])
    return s
