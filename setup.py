# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@author: metalcorebear
"""

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="stonk",
    version="0.0.1",
    author="metalcorebear",
    author_email="mark.mbailey@gmail.com",
    description="A set of tools to pull and analyze stock data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metalcorebear/stonks",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'numpy', 'pandas'],
    py_modules=["stock_functions", "stonk"],
    package_data={},
    classifiers=[
        "Topic :: Scientific/Engineering :: Mathematics", 
        "Topic :: Office/Business :: Financial :: Investment", 
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)