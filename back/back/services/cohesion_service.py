import os
from pathlib import Path
from back.serializer.cohesion_serializer import print_module_structure
from cohesion.module import Module
from back.dto.cohesion_dto import CohesionDto

def generate_report_cohesion(files: str, url:str):
    json = []
    path2 = ""
    for path in getPaths(url):


        if files in path:
            path2 = path
    try:
        file_modules = {
                filename: Module.from_file(path2)
            for filename in files
        }

        for filename, file_module in file_modules.items():
            json.append(print_module_structure(files, file_module.structure, True))
            return json
    except Exception as inst:
        json = [CohesionDto(inst, None, None)]
        return json

def getPaths(url:str):
    paths = []
    absolute_path: str = str(Path().cwd().parent)+"/code_to_analyze/"
    print(absolute_path)
    for root, dirs, files in os.walk(absolute_path+url):
        for file in files:
            if file.endswith(".py"):
                paths.append(os.path.join(root, file))
    return paths