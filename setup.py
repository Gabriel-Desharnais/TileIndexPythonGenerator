from setuptools import setup, find_packages
import tileIndexPythonGenerator
setup(
    name='tileIndexPythonGenerator',
    version='0.0.0.7',
    description='Python module to generate a TileIndex',
    url='https://github.com/Gabriel-Desharnais/TileIndexPythonGenerator',
    author='Gabriel Desharnais',
    author_email='gabriel.desharnais@hotmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Atmospheric Science',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
        ],
    keywords='mapserver mapfile tileindex',
    packages=find_packages(),

    install_requires=[],


    )
