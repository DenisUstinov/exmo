# setup.py
import setuptools

setuptools.setup(
    name='exmo',
    version='0.1',
    author='Denis Ustinov',
    packages=setuptools.find_packages(),
    install_requires=['websockets'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
