from distutils.core import setup

setup(
    name='awesome_print',
    version='0.1.4',
    author='Kyle Moore',
    author_email='mynameskyle@gmail.com',
    packages=['awesome_print', 'awesome_print.test'],
    license='LICENSE',
    description='Awesome print.',
    long_description=open('README.md').read(),
    url='https://github.com/kmmoore/awesome_print',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
        ]
)
