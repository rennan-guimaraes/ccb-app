from setuptools import setup, find_packages

setup(
    name="gestao_vista",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas==2.1.4",
        "matplotlib==3.8.2",
        "numpy==1.26.3",
        "openpyxl==3.1.2",
        "xlrd==2.0.1",
        "et-xmlfile==1.1.0",
        "odfpy==1.4.1",
        "defusedxml==0.7.1",
        "python-dateutil==2.8.2",
        "pytz==2024.1",
        "six==1.16.0",
        "tkmacosx==1.0.5",
    ],
    python_requires=">=3.6",
)
