from setuptools import setup, find_packages
import sandp

setup(
    name = "sandp",
    version = sandp.__version__,
    description = "processor for SanDix detector",
    author = "YWei, Qiang",
    author_email = "ywei@physics.ucsd.edu, yejingqiang1992@gmail.com",
    url = "https://wiki.nigroup.ucsd.edu/doku.php?id=sandix",
    packages = ['sandp','sandp.config', 'sandp.data'],
    package_dir={'sandp': 'sandp'},
    package_data={'sandp': ['config/*.ini']},
    scripts=['bin/sandper']
)
