from distutils.core import setup

setup(
    name='bee_pi',
    version='0.2dev',
    author='Peter White',
    author_email='pwhite@delpwhite.org',
    maintainer='Peter White',
    maintainer_email='pwhite@delpwhite.org',
    packages=['bee_pi'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    description='Bee Pi - Data capture for Raspberry PI.',
    url='http://github.com:BeeRaspberry/bee_pi',
    install_requires=[
        "netifaces >= 0.10.7",
        "requests >= 2.21.0",
        "urllib3 >= 1.24.1",
    ],
)
