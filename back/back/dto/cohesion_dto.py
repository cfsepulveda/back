import json
from json import JSONEncoder
class Variables(object):
  def __init__(self, name, status):
    self.name = name,
    self.status = status

class FunctionsDto(object):
  def __init__(self, name,number, percentageval, variable= [] ):
    self.name = name
    self.number = number
    self.percentageval = percentageval
    self.variable = variable


class ClassDto(object):
  def __init__(self, name, functions: [FunctionsDto]):
    self.name = name
    self.functions = functions

class CohesionDto(object):
  def __init__(self, file_name, classtype: [ClassDto], total):
    self.file_name = file_name
    self.classtype = classtype
    self.total = total

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)

class CohesionResponse(object):
  def __init__(self,cohedto: CohesionDto):
    self.cohedto = cohedto








