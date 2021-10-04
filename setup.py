import setuptools

__version__ = "1.0.0"

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
    url="https://github.com/yezz123/fastapi-class",
    packages=setuptools.find_packages(
        exclude=["tests", "tests.*", "*.tests", "*.tests.*"],
    ),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["fastapi==0.68.1", "pydantic==1.8.2"],
)
