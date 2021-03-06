from setuptools import setup

setup(
    name='misnamer',
    author='ygreenc',
    author_email='',
    version='1.0.0',
    url='https://github.com/ygreenc/misnamer',
    packages=['misnamer'],
    description='Rename movie file',
    license='MIT',
    install_requires=[
        'requests==2.9.1',
        'click==6.2'
    ],
    tests_require=['pytest==2.8.5'],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'misnamer = misnamer.main:main'
        ]
    }
)
