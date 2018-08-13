from setuptools import setup, find_packages
import tileIndexPythonGenerator
setup(
    name='tileIndexPythonGenerator',
    version='0.1.0.1',
    description='Python module to generate a TileIndex',
    url='https://github.com/Gabriel-Desharnais/TileIndexPythonGenerator',
    author='Gabriel Desharnais',
    author_email='gabriel.desharnais@hotmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Atmospheric Science',

        'License :: OSI Approved :: MIT License',

		'Natural Language :: English',
		'Natural Language :: French',

        'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
        ],
    keywords='mapserver mapfile tileindex',
    packages=find_packages(),

    install_requires=[],
	long_description=open('README.md').read(),


    )
