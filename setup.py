# -*- coding: utf-8 -*-

import os

if os.name == 'posix':
    from setuptools import setup
    
    APP = ['main.py']
    DATA_FILES = []
    OPTIONS = {
        'iconfile':'chinchilla.icns',
        'plist': {'CFBundleShortVersionString':'0.1.0',}
    }
    
    setup(
        app=APP,
        name=u'枫丹龙猫',
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
else:
    from distutils.core import setup
    import py2exe
     
    setup(
        windows=[
            {
                "script": 'main.py',
                "icon_resources": [(1, "chinchilla.ico")]
            }
        ],
        data_files=["chinchilla.ico"]
    )