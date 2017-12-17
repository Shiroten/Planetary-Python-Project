# Aufruf: python3 setup.py build_ext --inplace
# Windows: zusaetzliche Option --compiler=mingw32
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

ext_modules=[ Extension("PubycWorker", ["PubycWorker.py"],
        extra_compile_args=['-O3'], libraries=['m']),
             Extension("PubycWorkerEngine", ["PubycWorkerEngine.pyx"],
        extra_compile_args=['-O3', '-fopenmp'], libraries=['m'],
        extra_link_args=['-fopenmp'],
)       
        #Maybe needed
        #extra_compile_args=['-O3'], libraries=['m'],
        #include_dirs=[numpy.get_include()]),
]
             
setup( name = 'Pubyc',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
     include_dirs=[numpy.get_include()])