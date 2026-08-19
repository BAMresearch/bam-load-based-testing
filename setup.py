# -*- coding: utf-8 -*-
"""
Created on 20.09.2023

@author: Stephan Göbel (RWTH Aachen University)

Setup-Function for bamLoadBasedTesting package

"""
# ======================================================================================================================
#                                                    Imports
# ======================================================================================================================
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = ["numpy == 2.4.4",
                    "matplotlib == 3.10.8",
                    "pandas == 3.0.3",
                    "keyboard == 0.13.5",
                    "openpyxl== 3.1.5",
                    ]

SETUP_REQUIRES = INSTALL_REQUIRES.copy()

setuptools.setup(name="bamLoadBasedTesting",
                 version="1.0.0",
                 description="Package for load-based-testing with one-mass-model.",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/BAMresearch/bam-load-based-testing",
                 author="Stephan Göbel",
                 classifiers=["Programming Language :: Python :: 3.11",
                              "Programming Language :: Python :: 3.12",
                              "License :: OSI Approved :: MIT License"
                              ],
                 python_requires=">=3.11",
                 packages=setuptools.find_packages(exclude=[""]),
                 setup_requires=SETUP_REQUIRES,
                 install_requires=INSTALL_REQUIRES,
                 include_package_data=True
                 )
