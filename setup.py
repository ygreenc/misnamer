from setuptools import setup

setup(
    name='misnamer',
    author='ygreenc',
    author_email='',
    version='0.1',
    url='',
    packages=['misnamer'],
    description='Rename movie file',
    entry_points={
        'console_scripts': [
            'misnamer = misnamer.main:main'
        ]
    }
)
