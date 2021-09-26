from rest_framework import serializers


class WilySerializer(serializers.Serializer):
    file_name=serializers.CharField(max_length=400)
    code_line=serializers.CharField(max_length=400)
    cyclomatic_complexity=serializers.CharField(max_length=400)
    unique_operands=serializers.CharField(max_length=400)
    maintainability_index=serializers.CharField(max_length=400)
