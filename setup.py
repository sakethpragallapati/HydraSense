from setuptools import find_packages, setup
from typing import List


def get_requirements(requirements_path: str) -> List[str]:
    requirements = []
    with open(requirements_path, "r") as file_obj:
        for line in file_obj:
            req = line.strip()
            if req and not req.startswith("-e"):
                requirements.append(req)
    return requirements


setup(
    name="Hydration-Prediction",
    version="0.1",
    author="Pragallapati Saketh",
    author_email="pragallapati.saketh@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)