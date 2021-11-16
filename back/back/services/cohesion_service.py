import os
import json
from pathlib import Path
from back.serializer.cohesion_serializer import print_module_structure
from cohesion.module import Module
from back.dto.cohesion_dto import CohesionDto

def generate_report_cohesion(files: str, url:str):
    jsonResponse = []
    sizePaths = len(getPaths(url))
    acumulate = 0
    for path in getPaths(url):
        if not url:
            url = 'code_to_analyze/'
        file = str(path).split(url)
        file_name = file[len(file) - 1]
        acumulate = acumulate+1
        try:
            file_modules = {
                    filename: Module.from_file(path)
                for filename in files
            }

            for filename, file_module in file_modules.items():
                arraycoh = CohesionDto
                arraycoh = print_module_structure(file_name, file_module.structure, True)
                if "Error" not in arraycoh.__getattribute__("file_name"):
                    jsonResponse.append(arraycoh)

                    break
                else:
                    arraycoh = CohesionDto(file_name+"- Sin análisis: Error en estructura del archivo", None, 0)
                    jsonResponse.append(arraycoh)
                    break
        except Exception as inst:
            arraycoh = CohesionDto(file_name + "- Sin análisis: Error en estructura del archivo", None, 0)
            jsonResponse.append(arraycoh)
            if sizePaths == acumulate:
                 return jsonResponse
    return jsonResponse

def getPaths(url:str):
    paths = []
    absolute_path: str = str(Path().cwd().parent)+"/code_to_analyze/"
    if not url:
        url = ''
    for root, dirs, files in os.walk(absolute_path+url):
        for file in files:
            if file.endswith(".py"):
                paths.append(os.path.join(root, file))
    return paths