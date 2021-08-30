import io
import os
import re

from setuptools import setup, find_packages


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())

setup(
    name='qvapay',
    version='0.0.3',
    url="https://qvapay.com/docs",
    license='MIT',

    author='Carlos Lugones',
    author_email='contact@lugodev.com',
    
    description='Python SDK for the QvaPay API',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    
    packages=find_packages(),

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
