import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='bootlets',
    version='0.0.1',
    description="Build HTML in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NixonInnes/bootlets",
    author="NixonInnes",
    author_email="nixoninnes@echonet.io",
    packages=setuptools.find_packages(),
    license="MIT",
    classifier=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Text Processing :: Markup :: HTML",
        "License :: OSI Approved :: MIT License"
    ]
)