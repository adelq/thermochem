from setuptools import setup, find_packages
import thermochem

setup(
    name="thermochem",
    version=thermochem.__version__,
    description="Python utilities for thermodynamics and thermochemistry",
    long_description=open("README.rst").read(),
    author="Adel Qalieh",
    author_email="adelq@med.umich.edu",
    url="https://github.com/adelq/thermochem",
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['scipy>=0.6.0', 'numpy>=1.2.1', 'pandas>=0.17.0'],
    zip_safe=False,
    keywords='thermo chemistry physics',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics'
    ],
)
