


def generate_ascii_title(text):
  from pyfiglet import Figlet
  f = Figlet()
  # ogre.flf, 6x10.flf, space_op.flf, o8.flf
  fonts = ['ogre', '6x10', 'space_op']
  for font in fonts:
    f.setFont(font=font)
    print(f.renderText(text=text.strip()))

# generate_ascii_title('ascii title')





####### ####### ##   ## #######
   ##   ##       ## ##     ##
   ##   ######    ###      ##
   ##   ##       ## ##     ##
   ##   ####### ##   ##    ##

"""--------------
文本和字符处理
--------------"""

def encode_len(t, encode=None):
  ''' encode='gbk' 计算长度时, 中文字符视为长度2, 这样统计字数方便对齐
      encode='utf-8' 计算长度时, 中文字符视为长度3
      encode=None 使用普通的 len(text) 计算长度'''
  return len(t.encode(encode) if encode else t)



def match_previous(lines, pattern, history=5):
  ''' 返回匹配的行以及之前的n行
      usage
      # with open(r'../../cookbook/somefile.txt') as f:
      #   for line, prevlines in search(f, 'Python', 5):
      #     for pline in prevlines:
      #       print(pline, end='')
      #     print(line, end='')
      #     print('-' * 20)
  '''
  from collections import deque
  previous_lines = deque(maxlen=history)
  for li in lines:
    if pattern in li:
      yield li, previous_lines
    previous_lines.append(li)




def convert_str_bytes_usage():
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


import re
def trim_leading_spaces(text):
  ''' 移除文本行首的空白字符
      首先去掉位于文本中完全为空的行
      然后查看每行的开始空格数, 记录开始空格的最小值
      对每一行都去掉该最小值的空格数
  如: (下面以 `_` 表示空格, `^` 表示行首)
          ^__
          ^____headerline
          ^________contentline1
          ^________contentline2
          ^__
          ^________contentline3
          ^____footerline

  将返回:
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
  return '\n'.join(line[min_leading_space_count:] for line in array)



def truncate(text, limit=20, with_end=False, ellipsis='... ', encode=None):
  ''' 截断字符串尾部, 保留指定长度
      encode='gbk' 计算长度时, 中文字符视为长度2, 这样方便对齐
      encode='utf8' 计算长度时, 中文字符视为长度3
      encode=None 使用普通的 len(text) 计算长度
      TODO with_end=True 保留开头和结束, 省略中间的字符
  '''
  encode_len = lambda t: len(t.encode(encode) if encode else t)
  limit = max(limit, encode_len(ellipsis))
  len_text = encode_len(text)
  if len_text <= limit:
    return text
  else:
    dest_length =  limit - encode_len(ellipsis)
    current_index = len(text)
    while encode_len(text[:current_index]) > dest_length:
      current_index -= 1
    return text[:current_index] + ellipsis




from collections import OrderedDict as odict
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




def clean_xml(text):
  ''' 清理用于 xml 的有效字符
      曾遇到标题里有字符 backspace \x08, 在 CentOS 中无法生成 xml feed
      用于文本内容,
      一般不用于路径或 yaml csv 中 '''
  def valid_xml_char_ordinal(c):
    # conditions ordered by presumed frequency
    codepoint = ord(c)
    return (0x20 <= codepoint <= 0xD7FF or
            codepoint in (0x9, 0xA, 0xD) or
            0xE000 <= codepoint <= 0xFFFD or
            0x10000 <= codepoint <= 0x10FFFF)
  return ''.join(c for c in text if valid_xml_char_ordinal(c))


DEFAULT_INVALID_CHARS = {':', '*', '?', '"', "'", '<', '>', '|', '\r', '\n', '\t'}
EXTRA_CHAR_FOR_FILENAME = {'/', '\\'}

def remove_invalid_char(dirty, invalid_chars=None, for_path=False, combine_whitespaces=True):
  ''' 清理无效字符, 用于文件路径, 配置字段, 或 yaml csv 等
      for_path = True   允许出现 `/` 和 `\\`
      for_path = False  只保留纯文件名, 不能出现 `/` 和 `\\`'''
  text = clean_xml(dirty)
  if invalid_chars is None:
    invalid_chars = set(DEFAULT_INVALID_CHARS)
  else:
    invalid_chars = set(invalid_chars)
    invalid_chars.update(DEFAULT_INVALID_CHARS)
  if not for_path:
    invalid_chars.update(EXTRA_CHAR_FOR_FILENAME)
  text = ''.join([c for c in text if c not in invalid_chars]).strip()
  if combine_whitespaces:
    text = re.sub(r'\s+', ' ', text).strip()
  return text










##   ##  #####  ##   ## ##
##   ## ##   ## ### ### ##
 #####  ####### ## # ## ##
  ##   ##   ## ##   ## ##
  ##   ##   ## ##   ## #######

"""--------------
yaml json csv 载入和存储
--------------"""


import os
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
    return yaml.load(open(filename, encoding='utf-8'), IncludeOrderedLoader)

  def _construct_mapping(self, loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


def yaml_load(path, loader=IncludeOrderedLoader):
  ''' 按照有序字典载入yaml 支持 !include'''
  with open(path, encoding='utf-8') as f:
    result = yaml.load(f, loader)
  return result

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

def yaml_saves(data):
  return yaml.safe_dump(data, allow_unicode=True)



import json
def json_load(path):
  with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
  return data
def json_save(data, path):
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f)
def json_loads(s):
  return json.loads(s)
def json_saves(data):
  return json.dumps(data)



import os
def text_load(path, encoding=None):
  ''' 读取文本, 尝试不同的解码 '''
  if not os.path.exists(path):
    raise ValueError("path `{}` not exist".format(path))
  if encoding is None:  # 猜测 encoding
    try:
      open(path, 'r', encoding='utf-8').read()
      encoding = 'utf-8'
    except UnicodeDecodeError:
      encoding = 'gbk'
  with open(path, 'r', encoding=encoding) as f:
    ret = f.read()
  return ret
def text_save(path, data, encoding='utf-8'):
  with open(path, 'w', encoding=encoding) as f:
    f.write(data)
  return True



def csv_load(path, sample=10, only_title=False, include=(), exclude=()):
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

import csv
def csv_save(headers, data, filename):
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



class TranslationDict:
  '''
  在两组字符串之间相互转换
  usage:
    transdict = TranslationDict()
    'IDE' | transdict                                                # 正向转换
    >>> 'Integrated Development Environment：集成开发环境'
    'Java Database Connectivity：Java 数据库连接' ^ transdict         # 反向转换
    >>> 'JDBC'
    'IDE' ^ transdict                                                # 失败的转换
    >>> ValueError: cannot reversed translate user specified `IDE`
  '''

  data = '''
    IDE          Integrated Development Environment：集成开发环境
    JDBC         Java Database Connectivity：Java 数据库连接
    JDK          Java SE Development Kit：Java 标准版开发工具包
  '''
  def __ror__(self, key):
    if key in self.transdict:
      return self.transdict[key]
    else:
      raise ValueError(f'cannot translate user specified `{key}`')

  def __rxor__(self, key):
    if key in self.reversed_transdict:
      return self.reversed_transdict[key]
    else:
      raise ValueError(f'cannot reversed translate user specified `{key}`')

  def __init__(self):
    transdict = {}
    for line in self.data.splitlines():
      if line.strip():
        key, *_, value = re.split(r'  +', line.strip())
        transdict[key] = value
    self.transdict = transdict
    self.reversed_transdict = {v: k for k, v in transdict.items()}




'''
整形转换十六进制格式化
'''
def to_hex(i):
  return f'{hex(i)[2:]:>02}'.upper()












####### ###### ##      #######
##        ##   ##      ##
######    ##   ##      ######
##        ##   ##      ##
##      ###### ####### #######

"""--------------
文件夹, 文件处理
--------------"""

import fnmatch
def all_files(root, patterns='*',
              blacklist=('.git', '__pycache__', '.ipynb_checkpoints'),
              single_level=False, yield_folders=False):
  ''' 取得文件夹下所有文件
  single_level 仅处理 root 中的文件(文件夹) 不处理下层文件夹
  yield_folders 也遍历文件夹'''

  patterns = patterns.split(';')
  for path, subdirs, files in os.walk(root, topdown=True):
    subdirs[:] = [d for d in subdirs if d not in blacklist]
    subdirs.sort()
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

import fnmatch
def all_subdirs(root, patterns='*',
                blacklist=('.git', '__pycache__', '.ipynb_checkpoints'),
                single_level=False):
  ''' 取得文件夹下所有文件夹 '''

  patterns = patterns.split(';')
  for path, subdirs, __ in os.walk(root, topdown=True):
    subdirs[:] = [d for d in subdirs if d not in blacklist]
    subdirs.sort()
    for name in subdirs:
      for pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
          yield os.path.join(path, name)
          break
    if single_level:
      break

# When `topdown` is true, the caller can modify the dirnames
# list in-place and walk will only recurse into the subdirectories
# whose names remain in dirnames; can be used to prune the search...
# `dirs[:] = value` modifies dirs in-place. It changes the contents
# of the list dirs without changing the container.




def from_relative_path(path):
  ''' 相对于当前执行环境的路径 '''
  path = os.path.join(os.getcwd(), path)
  return path




import difflib
def sep_split(text, sep=r"([.。!！?？\n+])"):
  '''分割字符串, 保留分隔符'''
  result = re.split(sep, text)
  values = result[::2]
  delimiters = result[1::2] + ['']
  return [v+d for v, d in zip(values, delimiters)]

def show_diff(old_code, new_code):
  diff = difflib.ndiff(sep_split(old_code), sep_split(new_code))
  # diff = difflib.ndiff(old_code.splitlines(1), new_code.splitlines(1)) # splitlines(1) 保留行尾的换行
  print('\n'.join(line for line in diff if not line.startswith(' ')))

def compare_text(t1, t2, prefix=''):
  changes = [l for l in difflib.unified_diff(t1.split('\n'), t2.split('\n'))]
  for change in changes:
    print(prefix + change)
  return changes


# AES 加密解密

# 样例:
# 首先约定 key utf8 字符串
# 以该指定 key 加密 (在 python 中)
# 以该指定 key 解密 (在 javascript 中)

# 均使用 AES MODE_OFB, 该模式加密时不要求定长序列, 但是 python API 仍然需要 pad?
# AES key 应为定长向量, 以 md5 将字符串 key 转为向量
# 密钥key长度须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度. AES-128足够用
# 参数还有个 iv, 以 key 代替, 需检查缺陷

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import hashlib

class CryptorAES():
  BS = 16
  mode = AES.MODE_OFB
  def __init__(self, password):
    self.key = self.make_key(password)
    # hash.hexdigest() 返回摘要，作为十六进制数据字符串值
    # 取前16位 print(ord(c), end=',') for c in self.key
  def encrypt(self, text):
    ''' 加密函数，如果text不是16的倍数就补足为16的倍数 '''
    # iv = Random.new().read(AES.block_size) # AES.block_size==16
    cryptor = AES.new(self.key, self.mode, self.key)

    data = str.encode(text)
    if(len(data) % self.BS != 0): add = self.BS - (len(data) % self.BS)
    else: add = 0
    data = data + (b'\0' * add)
    self.ciphertext = cryptor.encrypt(data)
    # 加密得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以转为16进制字符串
    return bytes.hex(self.ciphertext)

  def make_key(self, password):
    ''' 字符串 key 转为定长向量 '''
    return hashlib.md5(str.encode(password.strip())).hexdigest()[:self.BS]

  def decrypt(self, text, password=None):
    ''' 解密后，去掉补足的空格 
    如果提供key, 以该指定密码解密, 用于测试错误密码的情况'''
    if password: key = self.make_key(password)
    else: key = self.key
    cryptor = AES.new(key, self.mode, key)
    plain = cryptor.decrypt(a2b_hex(text))
    return bytes.decode(plain.strip(b'\0'), errors="ignore")
  
