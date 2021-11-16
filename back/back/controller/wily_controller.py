import json
from pathlib import Path

from back.services.wily_service import generate_report
from back.serializer.wily_serializer import WilySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wily.helper.custom_enums import ReportFormat
from back.services.cohesion_service import generate_report_cohesion
from back.serializer.cohesion_serializer import CohesionSerializer

@api_view(['POST'])
def complexity(request):
    return Response(WilySerializer(generate_report(), many=True).data)

@api_view(['POST'])
def cohesion_analisys(request):
    body = json.loads(request.body.decode("utf-8"))
    url = body.get("route")
    file = body.get("file")
    if not file:
        file = ""
    cohesionList = generate_report_cohesion(file+".py",url)
    return Response(CohesionSerializer(cohesionList,    many=True).data)