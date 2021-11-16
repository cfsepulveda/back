from rest_framework import serializers
from back.dto.cohesion_dto import CohesionDto
from back.dto.cohesion_dto import CohesionResponse
from back.dto.cohesion_dto import FunctionsDto
from back.dto.cohesion_dto import Variables
from back.dto.cohesion_dto import ClassDto

def print_module_structure(filename, module_structure, verbose=False):

    filename = format(filename)
    classList = []

    try:
        for class_name, class_structure in module_structure.items():

            class_output_string = "Class: {} ({}:{})".format(
                class_name,
                class_structure["lineno"],
                class_structure["col_offset"]
            )


            functionsList = []
            for function_name, function_structure in class_structure["functions"].items():
                function_variable_percentage = percentage(
                    len(function_structure["variables"]),
                    len(class_structure["variables"])
                )
                function_output_string = "Function: {}".format(function_name)
                if function_structure["staticmethod"]:
                    function_output_string = "{} staticmethod".format(function_output_string)
                elif function_structure["classmethod"]:
                    function_output_string = "{} classmethod".format(function_output_string)
                elif not function_structure["bounded"]:
                    function_variable_percentage = 0.0
                    function_output_string = "{0} {1}/{2} 0.0%".format(
                        function_output_string,
                        len(function_structure["variables"]),
                        len(class_structure["variables"])
                    )

                else:
                    function_output_string = "{0} {1}/{2} {3:.2f}%".format(
                        function_output_string,
                        len(function_structure["variables"]),
                        len(class_structure["variables"]),
                        function_variable_percentage
                    )

                if verbose:
                    variablesList = []
                    for class_variable_name in sorted(class_structure["variables"]):
                        if class_variable_name in function_structure["variables"]:
                            variablesList.append(Variables(class_variable_name, True))


                        else:
                            variablesList.append(Variables(class_variable_name, False))

                number = function_output_string.split(' ')[2]
                sizepercent = len(function_output_string.split(' '))
                if(sizepercent>=4):
                    percentageval = function_output_string.split(' ')[3]
                else:
                    percentageval = ""
                functionsDto = FunctionsDto(format(function_name), number, percentageval,variablesList )
                functionsList.append(functionsDto)


            classList.append(ClassDto(class_output_string,functionsList))
        cohesionDto = CohesionDto(filename,classList,format(class_structure["cohesion"]))

        return cohesionDto
    except Exception as inst:
        cohesionDto = CohesionDto("Error formato clase", None, None)
        return cohesionDto


def percentage(part, whole):
        if not whole:
            return 0.0

        return 100.0 * float(part) / float(whole)


class VariableSerializer(serializers.Serializer):
    name = serializers.StringRelatedField(read_only=True)
    status = serializers.BooleanField(read_only=True)

class FunctinosSerializer(serializers.Serializer):
    name = serializers.StringRelatedField(read_only=True)
    number = serializers.StringRelatedField(read_only=True)
    percentageval = serializers.StringRelatedField(read_only=True)
    variable = VariableSerializer(many=True)

class ClassSerializer(serializers.Serializer):
    name = serializers.StringRelatedField(read_only=True)
    functions = FunctinosSerializer(many=True)

class CohesionSerializer(serializers.Serializer):

    file_name=serializers.CharField(max_length=400)
    total =serializers.CharField(max_length=400)
    classtype=ClassSerializer(many=True)

class CohesionResponseSerializer(serializers.Serializer):
    cohedto = CohesionSerializer(many=True)


