import json
from pathlib import Path

from back.services.wily_service import generate_report
from back.serializer.wily_serializer import WilySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wily.helper.custom_enums import ReportFormat


@api_view(['GET'])
def hello_world(request):
    return Response(WilySerializer(generate_report(), many=True).data)
