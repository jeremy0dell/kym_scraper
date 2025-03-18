from setuptools import setup, find_packages

setup(
    name="kym_scraper",
    version="0.1.0",
    description="Know Your Meme scraper for AI agents",
    author="Jeremy Odell",
    author_email="example@example.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "typing>=3.7.4.3",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
) 