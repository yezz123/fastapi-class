import setuptools

__version__ = "1.1.2"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi_class",
    version=__version__,
    author="Yasser Tahiri",
    author_email="yasserth19@gmail.com",
    description="Generate Class & Decorators for your FastAPI project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source Code": "https://github.com/yezz123/fastapi-class",
        "Bug Tracker": "https://github.com/yezz123/fastapi-class/issues",
        "Documentation": "https://yezz123.github.io/fastapi-class/",
    },
    packages=setuptools.find_packages(
        exclude=["tests", "tests.*", "*.tests", "*.tests.*"],
    ),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Framework :: FastAPI",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=["fastapi==0.70.0", "pydantic==1.8.2"],
)
