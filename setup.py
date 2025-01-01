from setuptools import setup, find_packages

setup(
    name='Historic_Crypto',
    version='0.1.7',
    description='An open source Python library for scraping Historical Cryptocurrency data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='David Woroniuk',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

