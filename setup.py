from setuptools import find_packages, setup 
from typing import List

def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the packages required for the project
    '''
    with open(file_path) as lib_name:
        requirements = lib_name.readlines()
        requirements=[req.replace('\n','') for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
        
        return requirements

HYPEN_E_DOT = '-e .'
setup(
name='machine-learning-pro',
version='0.0.1',
author='pum-pum-pum-pum',
author_email='pvnkmrwrlrd@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)


        
        
    
    