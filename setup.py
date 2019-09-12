from distutils.core import setup, Extension

rsamodule = Extension('rsa',
                    sources = ['rsamodule.c'],
                    libraries = ['gmp', 'sodium']
                    )

setup (name = 'RSA Module',
       version = '1.0',
       description = 'RSA Encryption for our ISN project.',
       ext_modules = [rsamodule])
