"""
Setup script for Claude Code Context Plugin
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-code-context-plugin",
    version="1.0.0",
    author="Claude Context Management Team",
    author_email="support@claude-context-plugin.com",
    description="A practical plugin for Claude Code that provides intelligent context management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claude-code-context-plugin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "asyncio",
        "pathlib",
        "dataclasses",
        "typing-extensions",
        "argparse",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
        "enhanced": [
            "psutil",
            "aiofiles",
            "aiohttp",
            "rich",
            "click",
        ],
    },
    entry_points={
        "console_scripts": [
            "claude-code-plugin=claude_code_plugin.cli.commands:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)