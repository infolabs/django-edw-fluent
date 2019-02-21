from setuptools import setup, find_packages

setup(
    name='django-edw-fluent',
    version=__import__('edw_fluent').__version__,
    description='Package for connect Django EDW and Django Fluent Pages.',
    author='Infolabs LLC',
    author_email='team@infolabs.ru',
    url='https://github.com/infolabs/django-edw-fluent',
    packages=find_packages(),
    zip_safe=False,
    package_data={
        'edw_fluent': [
            'locale/*/LC_MESSAGES/*',
            'static/edw_fluent/*',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
