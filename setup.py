from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in socket_manager/__init__.py
from frappe_push_notification import __version__ as version

setup(
    name="frappe_push_notification",
    version=version,
    description="Expo Push Notification Integration for Frappe",
    author="Janak Vaghela",
    author_email="janak@pseudocode.co",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)