from setuptools import setup, find_packages

setup(
    name="credit-risk-model",
    version="0.1.0",
    description="Credit Risk Model Predict",
    python_requires=">=3.11",
    packages=find_packages(where=".", include=["src*", "app*", "models*"]),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0,<2.0.0",
        "scikit-learn>=1.3.0",
        "xgboost>=1.7.0",
        "lightgbm>=4.0.0",
        "prophet>=1.1.0",
        "skrub>=0.3.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "duckdb>=1.0.0",
        "pyarrow>=14.0.0",
        "requests>=2.31.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
    ],
    include_package_data=True,
    package_data={
        "": ["data/*", "data/raw/*", "data/processed/*"],
    },
)
