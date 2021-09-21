import click
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wily.__main__ import cli, report;
from wily.config import load as load_config


@api_view(['GET'])
def hello_world(request):

    #cli()
    report('cfsm')

    fruits = ["apple", "banana", "cherry"]
    for x in fruits:
        print(x)
    for x in fruits:
        print(x)
    return Response({"message": "Hello, Apple!"})

