from setuptools import setup

setup(
    name='Sweeper',
    version='0.1.0',
    py_modules=['settings'],
    install_requires=[
        'click'
        'python-decouple',
        'termcolor',
        'web3',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'sweep = run:sweep',
        ],
    },
)