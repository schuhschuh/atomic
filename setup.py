# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103

import io

from distutils.command.build_ext import build_ext
from setuptools.dist import Distribution
from setuptools import setup, find_packages, Extension

class BinaryDistribution(Distribution):

    def is_pure(self):
        # pylint: disable=R0201
        return False

class GetPybindInclude(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

class BuildExtension(build_ext):

    def build_extensions(self):
        if self.compiler.compiler_type == 'unix':
            for ext in self.extensions:
                ext.extra_compile_args += ['-std=c++11']
        build_ext.build_extensions(self)

with io.open('README.rst', encoding='utf-8') as f:
    README = f.read()

with io.open('requirements.txt', encoding='utf-8') as f:
    REQUIREMENTS = f.read()

setup(
    name='atomic',
    version='0.8.0',
    description='An atomic class that guarantees atomic updates to its contained value.',
    long_description=README,
    author='Timothée Peignier',
    author_email='timothee.peignier@tryphon.org',
    url='https://github.com/cyberdelia/atomic',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    setup_requires=REQUIREMENTS,
    install_requires=REQUIREMENTS,
    test_suite="tests",
    ext_modules=[
        Extension(
            'atomic.detail',
            sources=['atomic/detail.cpp'],
            include_dirs=[
                GetPybindInclude(user=False),
                GetPybindInclude(user=True)
            ],
            language='c++'
        )
    ],
    cmdclass={'build_ext': BuildExtension},
    distclass=BinaryDistribution,
)
