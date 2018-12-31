import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ksscrape",
    version="0.0.1",
    author="Mike Hall",
    author_email="mikehall.dev@gmail.com",
    description="Scrape Kickstarter Discovery using Python with Selenium.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/televisedprogram/ksscrape.git",
    packages=setuptools.find_packages(),
    install_requires=['selenium']
)