import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-simplechoice',
    version='0.1.0',

    author='Axel Juraske',
    author_email='axel.juraske@short-report.de',
    url='https://github.com/axju/django-simplechoice',
    description='A simple Django app to build a multiple choice game.',
    long_description=README,

    license='MIT License',
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'django',
        'django-nested-inline',
    ],

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
