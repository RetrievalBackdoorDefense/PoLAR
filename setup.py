from setuptools import setup, find_packages

packages = find_packages()
print(f"packages = {packages}")
setup(
    name="PositiveFeedback",
    version="0.1.0",
    packages=packages,
    python_requires=">=3.9",
    # install_requires=["timeout_decorator", "libcst", "json_repair"],
)

# python setup.py bdist_wheel
