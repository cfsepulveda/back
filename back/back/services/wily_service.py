from pathlib import Path

from back.dto.wili_dto import WilyDto
from wily.cache import get_default_metrics
from wily.commands.report import report
from wily.config import WilyConfig
from wily.config import load as load_config
from wily.helper.custom_enums import ReportFormat


def generate_report():
    config: WilyConfig = setWilyConfig()
    return call_report(config)


def setWilyConfig():
    config: WilyConfig = load_config()
    path_string = str(Path.cwd())
    config.path = path_string + '\\back\\controller'
    return config


def call_report(config):
    new_output = Path().cwd()
    data = report(
        config=config,
        path='hello.py',
        metrics=get_default_metrics(config),
        n=1,
        output=new_output,
        include_message=True,
        format=ReportFormat.CONSOLE,
        console_format=None,
    )
    return buildJson(data)


def buildJson(data):
    json = []
    for element in data:
        json.append(
            WilyDto('hello.py', element[4], element[5], element[6], element[7]))
    return json
