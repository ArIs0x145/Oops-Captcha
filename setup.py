from setuptools import setup, find_packages

setup(
    name="oops-captcha",
    version="0.1.0",
    description="一個靈活且可擴展的Python驗證碼(CAPTCHA)生成庫",
    author="ArIs0x145",
    url="https://github.com/ArIs0x145/Oops-Captcha",
    packages=find_packages(),
    install_requires=[
        "captcha",
        "pillow",
        "numpy",
        "pyyaml",
    ],
    entry_points={
        'console_scripts': [
            'oops-captcha=oopscaptcha.cli:main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 