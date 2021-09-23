import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supply-chain-file-watcher",
    version="0.0.12",
    author="Daniel Balagula",
    author_email="d0b06gj@walmart.com",
    description="File watcher utility for supply chain data generated on Jetson devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dev.azure.com/jet-tfs/Kepler/_git/supply-chain-file-watcher",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)
