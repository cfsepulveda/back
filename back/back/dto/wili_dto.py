class WilyDto(object):
  def __init__(self, path, file_name, code_line, cyclomatic_complexity, unique_operands, maintainability_index):
    self.path = path
    self.file_name = file_name
    self.code_line = code_line
    self.cyclomatic_complexity = cyclomatic_complexity
    self.unique_operands = unique_operands
    self.maintainability_index = maintainability_index

    class Meta:
        file_name = 'file_name'
        code_line = 'code_line'
