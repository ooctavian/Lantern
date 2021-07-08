from setuptools import setup

setup(
    name='lantern',
    version='0.1',
    packages=['lantern'],
    description='Sets desktop wallpaper depending on the League of Legends champion/skin selected',
    install_requires=[
        'requests',
        'lcu-driver'
    ],
    entry_points={
        'console_scripts': ['lantern=lantern.main:main']
    }
)
