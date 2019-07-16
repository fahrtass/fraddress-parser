try:
    from setuptools import setup, find_packages
    with open("README.md", "r") as readme_file:
        readme = readme_file.read()
    requirements = ['python-crfsuite>=0.7','lxml']
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")

setup(
    version='0.0.1',
    author='Mathieu FRANCK',
    url='',
    description='A parser to help with recognizing and normalizing unstructured FR addresses',
    long_description=readme,
    name="fraddress-parser",
    url='https://github.com/fahrtass/fraddress-parser',
    packages=find_packages(),
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis']
)
