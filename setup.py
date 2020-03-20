from setuptools import setup, find_packages

setup(
    name='Corona Virus Bot',
    version='0.1',
    description='Discord bot for reporting corona virus statistics',
    author='John Lancaster',
    author_email='lancaster.js@gmail.com',
    install_requires=[
        'requests',
        'pandas',
        'pyyaml',
        'discord.py'
    ],
    packages=find_packages()
)