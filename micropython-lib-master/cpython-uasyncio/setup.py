import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup
sys.path.append("..")
import sdist_upip

setup(name='micropython-cpython-uasyncio',
      version='0.2.1',
      description='MicroPython module uasyncio ported to CPython',
      long_description='This is MicroPython compatibility module, allowing applications using\nMicroPython-specific features to run on CPython.\n',
      url='https://github.com/micropython/micropython-lib',
      author='micropython-lib Developers',
      author_email='micro-python@googlegroups.com',
      maintainer='micropython-lib Developers',
      maintainer_email='micro-python@googlegroups.com',
      license='Python',
      cmdclass={'sdist': sdist_upip.sdist},
      py_modules=['uasyncio'])
