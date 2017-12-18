from setuptools import setup, find_packages
import thermochem

setup(
    name="thermochem",
    version=thermochem.__version__,
    description="Python utilities for thermodynamics and thermochemistry",
    author="Adel Qalieh",
    author_email="adelq@sas.upenn.edu",
    url="https://github.com/adelq/thermochem",
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['scipy>=0.6.0', 'numpy>=1.2.1', 'pandas>=0.17.0'],
    zip_safe=False,
    keywords='thermo chemistry physics',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
