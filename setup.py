from setuptools import setup, find_packages

setup(
    name='exmo',
    version='0.1.9',
    author='ChatGPT and Denis Ustinov',
    author_email='revers-06-checkup@icloud.com',
    description='A Python package for working with Exmo API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DenisUstinov/exmo',
    license='MIT',
    packages=find_packages(),
    install_requires=['websockets', 'backoff'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)

