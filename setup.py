import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='django-o2o_tagging',
    version=__import__('o2o_tagging').__version__,
    author='Alejandro Varas',
    author_email='alej0varas@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/alej0varas/django-o2o_tagging',
    license='GNU General Public License',
    description=u' '.join(__import__('o2o_tagging').__doc__.splitlines()).strip(),
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.rst'),
    test_suite="runtests.runtests",
    zip_safe=False,
    install_requires=[
        'django-model-utils',
    ],
    tests_require=[
        'mock-django',
    ]
)
