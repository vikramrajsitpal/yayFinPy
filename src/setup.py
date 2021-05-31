from setuptools import setup

setup(
   name='yayFinPy',
   version='1.0',
   description='An upgraded API for yahoo finance based on yfinance',
   license="Apache",
   long_description="17-780 Course Project. Read README.md for more.",
   author='Chirag Sachdeva, Shubham Gupta, Tianyang Zhan, Vasudev Luthra, Vikramraj Sitpal',
   author_email='csachdev@andrew.cmu.edu, shubhamg@andrew.cmu.edu, tzhan@andrew.cmu.edu, vasudevl@andrew.cmu.edu, vsitpal@andrew.cmu.edu',
   url="",
   packages=['yayFinPy'],  #same as name
   install_requires=['pandas', 'numpy', 'yfinance', 'ta-lib','tweepy','sentifish','google','beautifulsoup4'], #external packages as dependencies
   entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    }
)
