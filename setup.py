from setuptools import setup, find_packages

setup(
    name='rl_framework',
    version='0.1',
    url='https://github.com/malex1106/rl_framework',
    author='Alexander Fichtinger',
    description='Framework for Reinforcement Learning',
    packages=find_packages(),
    install_requires=[
        'numpy >= 1.19.2',
        'tqdm >= 4.52.0',
        'matplotlib >= 3.3.0',
        'dill >= 0.3.3',
        'scipy >= 1.5.3'
    ],
)
