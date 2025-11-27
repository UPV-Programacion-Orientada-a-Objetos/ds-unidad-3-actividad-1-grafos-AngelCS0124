from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import sys

class BuildExt(build_ext):
    def build_extensions(self):
        compiler_type = self.compiler.compiler_type
        for ext in self.extensions:
            if compiler_type == 'msvc':
                ext.extra_compile_args = ['/std:c++14']
            else:
                ext.extra_compile_args = ['-std=c++14']
        build_ext.build_extensions(self)

extensions = [
    Extension(
        "neuronet",
        sources=["cython/neuronet.pyx", "src/GrafoDisperso.cpp"],
        include_dirs=["src"],
        language="c++",
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    cmdclass={'build_ext': BuildExt},
)
