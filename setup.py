from setuptools import setup

setup(
    author="WillemJan Faber",
    author_email=["WillemJan.faber@kb.nl", "lab@kb.nl"],
    name='kb',
    url="http://www.kb.nl/lab/",
    version='0.1dev',
    packages=['kb.nl.api', 'kb.nl.helpers'],
    license='GNU General Public License',
    install_requires=['lxml>=2.3', 'requests>=2.4'],
    long_description=open('README.rst').read(),
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Programming Language :: Python :: 2.7'
                 'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Natural Language :: Dutch',
                 'Topic :: Sociology :: History']
)
