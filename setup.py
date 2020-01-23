from distutils.core import setup, Extension

rsamodule = Extension('rsa',
                    sources = ['rsamodule.cpp', 'rsa.cpp'],
                    libraries = ['gmp', 'gmpxx']
                    )

setup (name = 'RSA Module',
       version = '1.0',
       description = 'RSA Encryption for our ISN project.',
       ext_modules = [rsamodule])
