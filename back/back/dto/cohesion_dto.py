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






