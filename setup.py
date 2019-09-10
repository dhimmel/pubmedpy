import itertools
import pathlib
import re

import setuptools

directory = pathlib.Path(__file__).parent.resolve()

# version
init_path = directory.joinpath('pubmedpy', '__init__.py')
text = init_path.read_text(encoding='utf-8-sig')
pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]", re.MULTILINE)
version = pattern.search(text).group(1)

# long_description
readme_path = directory.joinpath('readme.md')
long_description = readme_path.read_text(encoding='utf-8-sig')

# dependencies including extra depedencies with an "all" option
install_requires = [
    'requests',
    'lxml',
    'tqdm',
    'pandas',
]
extras_require = {
    'dev': [
        'pytest',
        'flake8',
    ],
}
extras_require['all'] = list(dict.fromkeys(itertools.chain.from_iterable(extras_require.values())))

setuptools.setup(
    # Package details
    name='pubmedpy',
    version=version,
    url='https://github.com/dhimmel/pubmedpy',
    project_urls={
        'Source': 'https://github.com/dhimmel/pubmedpy',
        'Tracker': 'https://github.com/dhimmel/pubmedpy/issues',
    },
    description='Utilities for interacting with NCBI EUtilities relating to PubMed',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license='BlueOak-1.0.0',

    # Author details
    author='Daniel Himmelstein',
    author_email='daniel.himmelstein@gmail.com',

    # Package topics
    keywords='pubmed eutilities bibliometrics',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=setuptools.find_packages(),

    # Specify python version
    python_requires='>=3.6',

    # Run-time dependencies
    install_requires=install_requires,

    # Additional groups of dependencies
    extras_require=extras_require,
)
