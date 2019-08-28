


def generate_ascii_title(text):
  from pyfiglet import Figlet
  f = Figlet()
  # ogre.flf, 6x10.flf, space_op.flf, o8.flf
  fonts = ['ogre', '6x10', 'space_op']
  for font in fonts:
    f.setFont(font=font)
    print(f.renderText(text=text.strip()))

# generate_ascii_title('ascii title')

# >>>     #####   ######  ###### ###### ######  
# >>>    ##   ## ##      ###       ##     ##    
# >>>    #######  #####  ##        ##     ##    
# >>>    ##   ##      ## ###       ##     ##    
# >>>    ##   ## ######   ###### ###### ######  
# >>>                                
# >>>    ####### ###### ####### ##      #######  
# >>>       ##     ##      ##   ##      ##       
# >>>       ##     ##      ##   ##      ######   
# >>>       ##     ##      ##   ##      ##       
# >>>       ##   ######    ##   ####### #######  










# def yaml_ordered_load(stream, Loader=None, object_pairs_hook=None):
#   '''按照有序字典载入yaml'''
#   import yaml
#   from collections import OrderedDict
#   if Loader is None:
#     Loader = yaml.Loader
#   if object_pairs_hook is None:
#     object_pairs_hook = OrderedDict

#   class OrderedLoader(Loader):
#     pass

#   def construct_mapping(loader, node):
#     loader.flatten_mapping(node)
#     return object_pairs_hook(loader.construct_pairs(node))
#   OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
#   return yaml.load(stream, OrderedLoader)

import yaml
from collections import OrderedDict
class IncludeOrderedLoader(yaml.Loader):
  ''' yaml loader
      以有序 dict 替代默认 dict
      值为 !include 开头时, 嵌套另一个 yaml

        -- main.yaml
        key_normal: [foo, bar]
        key_included: !include 'another.yaml'

        -- another.yaml
        foo: bar
        bar: baz

        -- nested result
        key_normal: [foo, bar]
        key_included:
          foo: bar
          bar: baz

      !include 可以是绝对路径或相对路径
      如果嵌套太深, 可能遇到相对路径错乱的问题
  '''
  def __init__(self, stream):
    super(IncludeOrderedLoader, self).__init__(stream)
    self.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                         self._construct_mapping)
    self.add_constructor('!include', self._include)
    self._root = os.path.split(stream.name)[0]

  def _include(self, loader, node):
    filename = os.path.join(self._root, self.construct_scalar(node))
    return yaml.load(encode_open(filename), IncludeOrderedLoader)

  def _construct_mapping(self, loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


def yaml_load(path, loader=IncludeOrderedLoader):
  ''' 按照有序字典载入yaml 支持 !include
  '''
  return yaml.load(open(path, encoding='utf-8'), loader)


def yaml_save(data, path):
  '''支持中文, 可以识别 OrderedDict'''
  class OrderedDumper(yaml.SafeDumper):
    pass
  def _dict_representer(dumper, data):
    return dumper.represent_mapping(
              yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
              data.items()
            )
  with open(path, 'w', encoding='utf-8') as file:
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    yaml.dump(data, file, OrderedDumper, allow_unicode=True)
  return True


def yaml_loads(text, loader=IncludeOrderedLoader):
  try:
    from StringIO import StringIO
  except ImportError:
    from io import StringIO
  fd = StringIO(text)
  fd.name = 'tempyamltext'
  return yaml.load(fd, loader)

# def yaml_saves(data):
#   return yaml.safe_dump(data, allow_unicode=True)

# def test_yaml_load():
#   path = 'E:/GitHub/Documasonry/test/nested.inf'
#   a = yaml_load(encode_open(path))
#   puts(a)

# test_yaml_load()


"""--------------
文件, 文件夹, 文本
--------------"""


def all_files(root, patterns='*', single_level=False, yield_folders=False):
  ''' 取得文件夹下所有文件
  single_level 仅处理 root 中的文件(文件夹) 不处理下层文件夹
  yield_folders 也遍历文件夹'''

  import fnmatch
  patterns = patterns.split(';')
  for path, subdirs, files in os.walk(root):
    if yield_folders:
      files.extend(subdirs)
    files.sort()
    for name in files:
      for pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
          yield os.path.join(path, name)
          break
    if single_level:
      break


def sample_convert_str_bytes():
  # 字节和字符串转换
  b = b"example"
  s = "example"
  # str to bytes
  str.encode(s)
  # bytes to str
  bytes.decode(b)


def datalines(text, limit=None, comment='#'):
  '''返回一段文字中有效的行(非空行, 且不以注释符号开头)'''
  lines = [line.strip() for line in text.splitlines()]
  lines = [line for line in lines if line and not line.startswith(comment)]
  if limit:
    return lines[:limit]
  else:
    return lines


def trim_leading_spaces(text):
  ''' 移除文本行首的空白字符

  首先去掉位于文本中完全为空的行
  然后查看每行的开始空格数, 记录开始空格的最小值
  对每一行都去掉该最小值的空格数

  如 (以_表示空格, 以^表示开头)
  ^__
  ^____headerline
  ^________contentline1
  ^________contentline2
  ^__
  ^________contentline3
  ^____footerline

  将返回

  ^headerline
  ^____contentline1
  ^____contentline2
  ^____contentline3
  ^footerline

  '''
  pat = re.compile(r'^( *).+$')
  array = [line for line in text.splitlines() if line.strip()]
  min_leading_space_count = min(len(pat.match(line).group(1)) for line in array)
  # print(min_leading_space_count)
  return joiner(line[min_leading_space_count:] for line in array)






def sections(iterable, is_title=lambda line: line.startswith('#')):
  ''' 通过小节的标题和之后文字生成 {标题: 内容} 的 order dict
  '''
  result = odict()
  title_index = 0
  title = (title_index, 'DEFAULT HEADER')
  result.setdefault(title, [])
  for line in iterable:
    if is_title(line):
      title_index += 1
      title = (title_index, line)
      result.setdefault(title, [])
    else:
      result[title].append(line)
  return result


def datalines_from_file(path):
  '''返回文本文件中有效的行'''
  if not os.path.exists(path):
    raise Exception("not os.path.exists({})".format(path))
  try:
    with open(path, 'r', encoding='utf-8') as f:
      lines = f.read()
  except UnicodeDecodeError:
    with open(path, 'r', encoding='gbk') as f:
      lines = f.read()
  return datalines(lines)


def encode_open(filename):
  '''读取文本, 依次尝试不同的解码'''
  try:
    open(filename, 'r', encoding='utf-8').read()
    encoding = 'utf-8'
  except UnicodeDecodeError:
    encoding = 'gbk'
  return open(filename, 'r', encoding=encoding)


def paragraphs(lines, is_separator=str.isspace, joiner=''.join):
  '''返回文本中的段落'''
  import itertools
  for sep_group, lineiter in itertools.groupby(lines, key=is_separator):
    # print(sep_group, list(lineiter))
    if not sep_group:
      yield joiner(lineiter)


def datamatrix(text, title=True, sep=','):
  ''' 多行文本转换为二维数据, 自动识别数字
  # d = "
  # Col1,Col2,Col3,中文列
  # 1,2,1,female
  # 2,3,1,male
  # 3,2,6.03,male
  # "
  # mat, title = datamatrix(d, title=True)
  # mat   | should.eq([[1,2,1,'female'],[2,3,1,'male'],[3,2,6.03,'male'],])
  # title | should.eq(['Col1','Col2','Col3','中文列'])
  '''
  def convert(text):
    if text.isdigit():
      return int(text)
    try:
      return float(text)
    except ValueError:
      return text

  data = iter(datalines(text))

  regexp = r'\s*{}\s*'.format(sep)
  if title:
    title = re.split(regexp, next(data))
  else:
    title = []

  array = []
  for line in data:
    line = [convert(e) for e in re.split(regexp, line)]
    array.append(line)
  return array, title


def file_timer(path=None, prefix='', suffix='', ext=None):
  '''在文件名中加入时间戳，使其命名唯一'''
  # t = time.strftime('%Y%m%d_%H%M%S')
  t = time.strftime('%m%d_%H%M%S')
  if path is None:
    return prefix+t+suffix
  else:
    path, file = os.path.split(path)
    name, old_ext = os.path.splitext(file)
    if ext:
      old_ext = '.'+ext
    return os.path.join(path, prefix+name+t+suffix+old_ext)


def to_timestamp(i):
  return datetime.fromtimestamp(i / 1000 / 1000).strftime("%Y-%m-%d %H:%M:%S.%f")[11:]


def random_sleep(*arg):
  '''休眠指定的时间,或范围内的随机值'''
  if len(arg) == 1:
    return time.sleep(arg[0])
  else:
    t = random.uniform(float(arg[0]), float(arg[1]))
    return time.sleep(t)

	


def relative_path(path):
  path = os.path.join(os.getcwd(), path)
  return path


def format_filename(s):
  """ 转换为有效的文件名
  Note: this method may produce invalid filenames such as ``, `.` or `..`
  """
  import string
  valid_chars = "-_[].,() %s%s" % (string.ascii_letters, string.digits)
  filename = ''.join(c if c in valid_chars else '_' for c in s)
  filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
  return filename





def show_diff(old_code, new_code):
  from difflib import ndiff
  diff = ndiff(old_code.splitlines(1), new_code.splitlines(1))
  print(''.join(line for line in diff if not line.startswith(' ')))






def load_txt(pat, encoding='utf-8'):
  with open(path, 'r', encoding=encoding) as f:
    ret = f.read()
  return ret


def save_txt(path, data, encoding='utf-8'):
  with open(path, 'w', encoding=encoding) as f:
    ret = f.write(data)


DEFAULT_INVALID_CHARS = {':', '*', '?', '"', '<', '>', '|', '\r', '\n'}
EXTRA_CHAR_FOR_FILENAME = {'/', '\\'}
def remove_invalid_char(dirty, invalid_chars=None, for_path=False):
  if invalid_chars is None:
    invalid_chars = set(DEFAULT_INVALID_CHARS)
  else:
    invalid_chars = set(invalid_chars)
    invalid_chars.update(DEFAULT_INVALID_CHARS)
  if not for_path:
    invalid_chars.update(EXTRA_CHAR_FOR_FILENAME)
  return ''.join([c for c in dirty if c not in invalid_chars]).strip()








def load_csv(path, sample=10, only_title=False, include=(), exclude=()):

  def _load_csv_value_convert(text):
    '''载入csv时处理每个字段的值, 转换整数等'''
    if text == 'nan':
      return float('nan')
    if text.isdigit():
      return int(text)
    try:
      return float(text)
    except ValueError:
      return text


  def _start_or_end_with(text, pattern):
    pattern = tuple(pattern)
    return text.startswith(pattern) or text.endswith(pattern)

  from itertools import compress
  import csv

  with open(path) as f:
    titles = f.readline().strip().split(',')

  if include:
    column_compress = [_start_or_end_with(title, include) for title in titles]
  else:
    column_compress = [True] * len(titles)
  if exclude:
    column_compress = [not _start_or_end_with(title, exclude) and tb for title, tb in zip(titles, column_compress)]

  if only_title:
    return list(compress(titles, column_compress))

  with open(path) as f:
    lines = csv.reader(f)
    next(lines)
    result = []
    for i, line in enumerate(lines, 1):
      if sample and i > sample:
        break
      # result.append([_load_csv_value_convert(x) for x in compress(line, column_compress)])
      result.append([x for x in compress(line, column_compress)])

  return result


def save_csv(headers, data, filename):
  # 将 obj 存储到 csv
  # headers = ['Symbol','Price','Date','Time','Change','Volume']
  # rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
  #          ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
  #          ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
  #        ]

  with open(filename, 'w') as f:
      f_csv = csv.writer(f)
      f_csv.writerow(headers)
      f_csv.writerows(data)


