import os

from pathlib import Path

from back.dto.wili_dto import WilyDto
from wily.cache import get_default_metrics
from wily.commands.report import report
from wily.cache import clean


from wily.config import WilyConfig
from wily.config import load as load_config
from wily.helper.custom_enums import ReportFormat

def generate_report(url:str, file:str):
    data = getSubfoldersAndFiles(url,file)
    json = []
    for index, path in enumerate(data):
        config: WilyConfig = None
        config = setWilyConfig(path[0])
        build(config)
        json.append(call_report(config, path[1], config.path))
    return json



def getSubfoldersAndFiles(url:str, file:str):
    paths = []
    absolute_path:str
    if url:
        absolute_path = str(Path().cwd().parent)+"/code_to_analyze/" + url
    else:
        absolute_path: str = str(Path().cwd().parent)+"/code_to_analyze"
    if file:
        paths.append([absolute_path, file])
        return paths
    else:
        for root, dirs, files in os.walk(absolute_path):
            for file in files:
                if file.endswith(".py"):
                    paths.append([root, file])
        return paths

def setWilyConfig(path: str):
    config: WilyConfig = load_config()
    config.path = path
    return config

def call_report(config:WilyConfig, file_name: str, path: str):
    print(config)
    print(file_name)
    new_output = Path().cwd()
    data = report(
        config=config,
        path=file_name,
        metrics=get_default_metrics(config),
        n=100,
        output=new_output,
        include_message=True,
        format=ReportFormat.CONSOLE,
        console_format=None,
    )
    return buildWilyDto(data, file_name, path)


def buildWilyDto(data, file_name, path: str):
    for element in data:
        wilyDto = WilyDto(
            path,file_name, element[4], element[5], element[6], element[7])
    return wilyDto

def build(config):
    os.system("cd " + config.path+" && wily clean -y && wily build")
