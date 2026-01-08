from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = "-e."
def get_requirements(requirements_path : str) -> List[str]:

    requirements = []
    with open(requirements_path,"r") as file_obj:
        requirements = file_obj.readlines()
        requirements = [requirement.replace("\n","") for requirement in requirements]

        if(HYPEN_E_DOT in requirements):
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name = "Hydration Prediction",
    version = "0.1",
    author="Pragallapati Saketh",
    author_email="pragallapati.saketh@gmail.com",
    packages= find_packages(),
    install_requirements = get_requirements("requirements.txt")
)