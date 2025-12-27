




.from setuptools import setup, find_packages

setup(
    name="medical-ai-book-backend",
    version="1.0.0",
    description="Backend API for AI in Medical Laboratory Diagnostics book",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "sqlalchemy==2.0.23",
        "asyncpg==0.29.0",
        "pydantic==2.5.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
        "qdrant-client==1.7.0",
        "openai==1.3.5",
        "python-dotenv==1.0.0",
        "better-exceptions==0.3.4",
        "pytest==7.4.3",
        "httpx==0.25.2",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ]
    },
    python_requires=">=3.8",
)