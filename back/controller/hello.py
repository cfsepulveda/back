from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello_world(request):
    fruits = ["apple", "banana", "cherry"]
    for x in fruits:
        print(x)
    return Response({"message": "Hello, Apple!"})
