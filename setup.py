from setuptools import setup, find_packages

setup(
    name='SpotifyAnalysis',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    # py_modules=['spot'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        spot=spot:cli
    ''',
    )