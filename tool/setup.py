from setuptools import setup

setup(
    # Basic info
    name="multinet-rfc",
    version="0.0.1",
    author="Jacob Nesbitt",
    author_email="jjnesbitt2@gmail.com",
    url="https://github.com/multinet-app/multinet-rfcs",
    description="Manage Multinet RFCs.",
    packages=["multinet_rfc"],
    install_requires=["click==7.1.2", "pathlib==1.0.1", "gitpython==3.1.11"],
    entry_points={"console_scripts": ["multinet-rfc = multinet_rfc.main:main"]},
)
