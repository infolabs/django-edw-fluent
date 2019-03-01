#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install as st_install


class install(st_install):
    def _post_install(self, lib_dir):
        packages = ('edw', 'email_auth', 'social_extra')
        backend_dir = os.path.join(lib_dir, 'backend')
        if os.path.exists(backend_dir):
            for package in packages:
                src_dir = os.path.join(backend_dir, package)
                dst_dir = os.path.join(lib_dir, package)
                if os.path.exists(dst_dir):
                    shutil.rmtree(dst_dir)
                shutil.copytree(src_dir, dst_dir, symlinks=True)
            if os.path.exists(backend_dir):
                shutil.rmtree(backend_dir)

    def run(self):
        st_install.run(self)
        self.execute(self._post_install, (self.install_lib,),
                     msg="Running post install task")


setup(
    name='django-edw-fluent',
    version='1.0.1',
    description='Package for connect Django EDW and Django Fluent Pages.',
    author='Infolabs LLC',
    author_email='team@infolabs.ru',
    url='https://github.com/infolabs/django-edw-fluent',
    packages=find_packages(),
    zip_safe=False,
    cmdclass={'install': install},
    package_data={
        'edw_fluent': [
            'locale/*/LC_MESSAGES/*',
            'static/*',
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
    ],
    install_requires = [
        "Django==1.9.13",
        "django-edw",
        "django-page-builder",
        "django-fluent-pages==1.1.1",
        "django-fluent-contents==1.2"
    ],
)
