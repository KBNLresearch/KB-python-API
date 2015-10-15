from setuptools import setup

setup(
    author="WillemJan Faber",
    author_email=["WillemJan.faber@kb.nl", "lab@kb.nl"],
    name='kb',
    url="https://github.com/KBNLresearch/KB-python-API",
    description='Access to National Library of the Netherlands datasets',
    version='0.1.6',
    packages=['kb.nl.api', 'kb.nl.helpers', 'kb', 'kb.nl', 'kb.nl.collections'],
    license='GNU General Public License',
    install_requires=['lxml>=2.3', 'requests'],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Natural Language :: Dutch',
                 'Topic :: Sociology :: History']
)
