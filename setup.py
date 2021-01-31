"""
Turbo-Flask
-----------

Use Hotwire Turbo in your Flask application.
"""
from setuptools import setup


setup(
    name='Turbo-Flask',
    version='0.0.1',
    url='http://github.com/miguelgrinberg/turbo-flask/',
    license='MIT',
    author='Miguel Grinberg',
    author_email='miguel.grinberg@gmail.com',
    description='Use Hotwire Turbo in your Flask application',
    long_description=__doc__,
    packages=['turbo_flask'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
