from setuptools import setup, find_packages

setup(
    name="problem_solver",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gradio",
        "openai",
        "python-dotenv",
        "Pillow",
    ],
)