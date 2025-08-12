#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
音声文字起こしアプリケーション セットアップスクリプト
"""

from setuptools import setup, find_packages
import os

# README.mdを読み込み
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# requirements.txtを読み込み
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name="speech-recognition-app",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="音声をリアルタイムでテキストに変換するデスクトップアプリケーション",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/speech-recognition-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "speech-recognition-app=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.cfg"],
    },
    zip_safe=False,
)