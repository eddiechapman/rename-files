from setuptools import setup

setup(
    name="rename-files",
    version="0.1.0",
    py_modules=["rename"],
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "inspect = rename:inspect",
            "rename = rename:rename"
        ],
    },
)
