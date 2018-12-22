from distutils.core import setup

setup(
    name='bee_pi',
    version='0.1dev',
    author='Peter White',
    author_email='pwhite@delpwhite.org',
    maintainer='Peter White',
    maintainer_email='pwhite@delpwhite.org',
    packages=['bee_pi'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    description='Bee Pi - Data capture for Raspberry PI.',
    install_requires=[
        "netifaces >= 0.10.6",
        "requests >= 2.18.4",
        "urllib3 >= 1.22",
    ],
)
