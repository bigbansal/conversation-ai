from setuptools import setup, find_packages

setup(
    name="conversation-ai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "requests",
        "pytest",
        "google-api-python-client",
        "oauth2client",
        "pytz"
    ],
    entry_points={
        'console_scripts': [
            'conversation-ai=src.main:main',
        ],
    },
)