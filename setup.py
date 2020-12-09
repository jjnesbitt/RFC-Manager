from setuptools import setup

setup(
    # Basic info
    name="rfc-manager",
    version="0.0.1",
    author="Jacob Nesbitt",
    author_email="jjnesbitt2@gmail.com",
    url="https://github.com/AlmightyYakob/RFC-Manager",
    description="Manage RFCs.",
    packages=["rfc_manager"],
    install_requires=["click==7.1.2", "pathlib==1.0.1", "gitpython==3.1.11"],
    entry_points={"console_scripts": ["rfc = rfc_manager.main:main"]},
)
