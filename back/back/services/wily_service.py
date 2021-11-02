import os
from pathlib import Path

import click
from back.dto.wili_dto import WilyDto
from wily.cache import get_default_metrics
from wily.commands.report import report
from wily.commands.build import build as build_wily
from wily.cache import clean
from wily.lang import _



from wily.archivers import resolve_archiver
from wily.operators import resolve_operators

from wily.config import WilyConfig
from wily.config import load as load_config
from wily.config import DEFAULT_ARCHIVER
from wily.config import DEFAULT_OPERATORS
from wily.helper.custom_enums import ReportFormat

def generate_report():
    json = []
    absolute_path: str = str(Path().cwd().parent) + "\\code_to_analyze"
    build(setWilyConfig(absolute_path))


    for path in getPaths():
        config: WilyConfig = setWilyConfig(path)
        file = str(path).split('\\')
        file_name = file[len(file)-1]
        json.append(call_report(config, file_name))
    return json


def setWilyConfig(path: str):
    config: WilyConfig = load_config()
    config.path = str(Path(path))
    config.operators = DEFAULT_OPERATORS
    config.archiver = DEFAULT_ARCHIVER
    return config


def call_report(config, file_name: str):
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
    return buildWilyDto(data, file_name)


def buildWilyDto(data, file_name):
    for element in data:
        wilyDto = WilyDto(
            file_name, element[4], element[5], element[6], element[7])
    return wilyDto


def getPaths():
    paths = []
    absolute_path: str = str(Path().cwd().parent)+"\\code_to_analyze"
    for root, dirs, files in os.walk(absolute_path):
        for file in files:
            if file.endswith(".py"):
                paths.append(os.path.join(root, file))
    return paths

def build(config, operators):
    clean(config)

    try:
        build_wily(
            config=config,
            archiver=resolve_archiver("git"),
            operators=resolve_operators(operators),
        )
    except NameError:
        print("ocurrio un error")
        print(NameError)
        print("ocurrio un error")
