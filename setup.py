from setuptools import setup

setup(
    # Application name:
    name="Ctrl-Email",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Quentin Guilloteau",
    author_email="Quentin.Guilloteau@grenoble-inp.org",

    # Packages
    packages=["app"],

    # Include additional files into the package
    # include_package_data=True,
    entry_points={
        'console_scripts': ['ctrl_email=app.ctrl_email:main'],
    },

    # Details
    url="https://github.com/GuilloteauQ/Ctrl-Email",

    #
    # license="LICENSE.txt",
    description="PID controlled application checking your email inboxes",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "google_api_python_client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "notify2",
    ]
)
