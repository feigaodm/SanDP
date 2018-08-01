from setuptools import setup, find_packages
import sandp

setup(
    name = "sandp",
    version = sandp.__version__,
    description = "processor for SanDix detector",
    author = "Yuehuan Wei",
    author_email = "ywei@physics.ucsd.edu",
    url = "https://wiki.nigroup.ucsd.edu/doku.php?id=sandix",
    packages = ['sandp'],
    scripts=['bin/sandper']
)
