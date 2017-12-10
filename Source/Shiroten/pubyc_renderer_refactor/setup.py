

# Aufruf: python3 setup.py build_ext --inplace
# Windows: zusaetzliche Option --compiler=mingw32
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy


ext_modules=[ Extension("calculation_function", ["calculation_function.pyx"],
        extra_compile_args=['-O3'], libraries=['m']),
             Extension("simulation_engine", ["simulation_engine.pyx"],
        extra_compile_args=['-O3', '-fopenmp'], libraries=['m'],
        #extra_compile_args=['-O3'], libraries=['m'],
        extra_link_args=['-fopenmp'],
)

        
        #Maybe needed
        #extra_compile_args=['-O3'], libraries=['m'],
        #include_dirs=[numpy.get_include()]),
]
             
setup( name = 'cython demo',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
     include_dirs=[numpy.get_include()])
