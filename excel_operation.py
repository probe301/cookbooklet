
import sys
import os
import win32com.client

xlapp = win32com.client.Dispatch("KET.Application")   # WPS Office
xlapp = win32com.client.Dispatch("Excel.Application") # Office Excel
xlapp.Visible = True
doc_path = 'C:/Work/demo.xlsx'
doc = xlapp.Workbooks.Open(doc_path)
doc.ActiveSheet  # 当前激活页
# 访问 sheet
doc.WorkSheets.Item(1).Name, doc.WorkSheets.Item(2).Name
sheet = doc.WorkSheets.Item("IO")

cells = list(sheet.UsedRange.Cells)
len(cells)

cells = sheet2.Range('E6:H7')
for cell in cells:
  print(repr(cell.Value))

# 遍历选择区
for cell in app.Selection:
  iter cell

"""找到cell上方的带有数据的cell
"""
def find_first_header_cell(cell):
  while True:
      if cell.Value:
        return cell
      else:
        cell = sheet.Cells(cell.Row-1, cell.Column)

"""在指定cell附近, 以row=+1, col=-1的相对定位, 导航到偏移值所指的另一个cell
"""
def cell_neighbor(cell, row=0, col=0):
  return sheet.Cells(cell.Row+row, cell.Column+col)

# for cell in app.Selection:
#   t1 = find_first_header_cell(sheet.Cells(cell.Row, cell.Column-4)).Value.split()[0]
#   t2 = find_first_header_cell(sheet.Cells(cell.Row, cell.Column-3)).Value.split()[0]
#   t3 = sheet.Cells(cell.Row, cell.Column-2).Value.split()[0]
#   t4 = sheet.Cells(cell.Row, cell.Column-1).Value.split()[1]

def cell_replace(cell, new_value, preview=True):
  """ 替换cell内容, 事先可以预览, 然后才真的替换
  """
  if preview:
    print(show_diff(cell.Value, new_value))
    # print(cell.Value)
    # print(new_value)
  else:
    cell.Value = new_value

# def cell_set_color(cell, level):
#   # WPS 19浅黄, 20浅蓝 40浅棕黄 36高亮度黄
#   cell.Interior.ColorIndex = 19
#   cell.Interior.ColorIndex = 20
#   cell.Interior.ColorIndex = 21
#   # cell.Interior.Color 可以拿到 float 型的 truecolor, 而 ColorIndex 只是索引, 会失真

def cell_set_color(cell, color):
  ''' cell.Interior.Color 可以拿到 float 型的 truecolor, 而 ColorIndex 只是索引, 会失真
      WPS的cell背景色, 可以自己涂色后, 打印这些单元格得出
        for cell in app.Selection:
          print(f"'{cell.Value}': {cell.Interior.Color}") '''
  data = {
      '浅浅红': 14083324.0, '浅浅黄': 13431551.0, '浅浅蓝': 15917529.0, '浅浅绿': 14348258.0, '浅浅灰': 15592941.0, '浅浅青': 16247773.0, '浅浅灰蓝': 14998742.0,
      '浅红': 11389944.0, '浅黄': 10086143.0, '浅蓝': 15189684.0, '浅绿': 11854022.0, '浅灰': 14408667.0, '浅青': 15652797.0, '浅灰蓝': 13285804.0,
      '红': 8696052.0, '黄': 6740479.0, '蓝': 14395790.0, '绿': 9359529.0, '灰': 13224393.0, '青': 15123099.0, '灰蓝': 11573124.0,
  }
  if color in data:
    cell.Interior.Color = data[color]
  else:
    raise ValueError(f'Invalid color {color}')


"""读取 selection, 取得每一行 row index, 取 Ai~Xi 的值
拿到这些 cell value 转成二维的表
selection 可以是 app.Selection, 或者 app.Range('N18:N740')
"""
def select_cell_values(selection):
  if 'y' != input(f'you select range {selection.Address}'):
    raise ValueError
  p = parse.parse('${col1}${row1:d}:${col2}${row2:d}', selection.Address)
  if p:
    row1 = p['row1']
    row2 = p['row2']
  else:
    p = parse.parse('${col1}${row1:d}', selection.Address)
    row1 = row2 = p['row1']
  print(f'got lines {row1} ~ {row2}')
  ret = []
  for index in range(row1, row2+1):
    line = sheet.Range(f'A{index}:X{index}').Value[0]
    ret.append(line)
  return ret



"""将Excel元组的每一行, 转为Record
"""
class Record():
  TITLES = 'columnname1 columnname2 columnname3 columnname4'.split(' ')

  @classmethod
  def from_line(cls, line):
    return cls(line)

  @classmethod
  def auto_create(cls, line):
    # 派发创建具体的实例, 因为 Record 可能被继承
    if cond:
      return Inherited1Record(line)
    elif cond2:
      return Inherited2Record(line)
    else:
      raise ValueError(f'factory cannot create Record from {line}')

  def __init__(self, line):
    self.record = line
    if len(TITLES) != len(line):
      raise ValueError(f'cannot match record col size {line} R{len(line)} vs T{len(TITLES)}')
    for t, v in zip(TITLES, line):
      setattr(self, t, v)

    self.filename_desc = '<desc>'
    self.tmpl_folder = r'...'

    # 后处理, 可以在子类重写
    self.init_post_process()

  def brief_value(self, v):
    if isinstance(v, str):
      return v.replace("\n", ' ')[:30]
    elif v is None:
      return 'none'
    else:
      return v

  def __str__(self):
    return '; '.join(f'{t}={self.brief_value(v)}' for t, v in zip(TITLES, self.record))




import re
import difflib
class cell_replacer():
  '''
  预览和调整替换cell的文字内容
  '''
  def __init__(self, pat, repl, preview=False):
    self.pat = pat
    self.repl = repl
    self.preview = preview
  def __ror__(self, cell):
    if cell and cell.Value:
      new_value = re.sub(self.pat, self.repl, cell.Value)
      if self.preview:
          diff = difflib.ndiff(cell.Value, new_value)
          print('\n'.join(line for line in diff if not line.startswith(' ')))
      else:
        cell.Value = new_value
    else:
      raise ValueError(f'Invalid cell {cell}')
  def __str__(self):
    return f'<cell_replacer object> pat={self.pat} repl={self.repl}'


删除整行
cell.EntireRow.Delete()