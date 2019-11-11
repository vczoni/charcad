from setuptools import setup

with open('charcad.version.py') as f:
    exec(f.read())

VERSION = __version__

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='charcad',
    packages=['charcad'],
    version=VERSION,
    license='MIT',
    description='Character-based drawing tool',
    author='Victor Zoni',
    author_email='vczoni@gmail.com',
    url='https://github.com/vczoni/charcad',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['CHARACTER', 'DRAWING', 'BASIC'],
    install_requires=requirements,
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
