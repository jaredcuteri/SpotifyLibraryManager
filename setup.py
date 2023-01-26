from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='spotify-ext',
    version='0.1.0',
    author='Jared Cuteri',
    author_email='jaredcuteri@gmail.com',
    packages=find_packages('spotify_ext', exclude=['test']),
    scripts=[''],
    url='http://pypi.python.org/pypi/spotipy_ext/',
    license='LICENSE.txt',
    description='Extension of Spotipy allowing endless calls',
    long_description=open('README.md').read(),
    install_requires=requirements,
)
