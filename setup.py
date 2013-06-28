from setuptools import setup

setup(
    name='scraping_intro',
    version='0.0.1',
    packages=['scraping_intro'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'beautifulsoup4',
        'mechanize',
        'requests'
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)
