from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Python SDK for the QvaPay API'
LONG_DESCRIPTION = open('README.md').read()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name='qvapay',
    version=VERSION,
    author='Carlos Lugones',
    author_email='contact@lugodev.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    license='MIT',
    install_requires=['requests'],
    keywords=['QvaPay', 'api', 'payments'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    project_urls={
        'Documentation': 'https://qvapay.com/docs',
        'Source': 'https://github.com/lugodev/qvapay-python',
        'Tracker': 'https://github.com/lugodev/qvapay-python/issues'
    }
)
