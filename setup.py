"""
Setup script for Face Recognition Camera System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="face-recognition-camera-system",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A real-time face recognition system with ID assignment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/face-recognition-camera-system",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "face-recognition>=1.3.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "dlib>=19.24.0",
    ],
    entry_points={
        "console_scripts": [
            "face-recognition=main:main",
            "register-face=register_face:main",
        ],
    },
)
