from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='spotipy-ext',
    version='0.1.0',
    author='Jared Cuteri',
    author_email='jaredcuteri@gmail.com',
    packages=find_packages(include=['spotipy_ext'], exclude=['test']),
    url='http://pypi.python.org/pypi/spotipy_ext/',
    license='LICENSE.txt',
    description='Extension of Spotipy allowing endless calls',
    long_description=open('README.md').read(),
    install_requires=requirements,
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'download_from_spotify=spotipy_ext.export_spotify:main',
        ]
    }
)
