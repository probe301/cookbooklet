
# part 1
import os
import sys
import re
import random
from pprint import pprint
from time import sleep
import math
from itertools import groupby
from collections import OrderedDict as odict
from collections import defaultdict
from collections import namedtuple
from collections import Counter
import yaml
import json


# part 2
import traceback
import io
from datetime import datetime
import platform
import fnmatch
import inspect
from itertools import compress
from itertools import cycle
from collections import deque
import functools


from pathlib import Path




def partial_sample():
  import functools
  write = functools.partial(print, file=out)







def dict_merge_sample():
  LISTER_DEFAULT_OPTION = {'1': 100, '2': 200}
  lister_option = {'3': 300, '2': 900}
  # lister_option 必须是 string 类型的 key
  lister_default_option = dict(LISTER_DEFAULT_OPTION, **lister_option)
  print(lister_default_option)

# 或者
def dict_merge_sample2():
  from copy import deepcopy
  def dict_merge(a, b=None):
    a = deepcopy(a)
    if b is None:
      b = {}
    a.update(b)
    return a





def namedtuple_sample():
  from collections import namedtuple
  Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
  sub = Subscriber('jonesy@example.com', '2012-10-19')
  # >>> Subscriber(addr='jonesy@example.com', joined='2012-10-19')
  sub.addr
  # >>> 'jonesy@example.com'
  sub.joined
  # >>> '2012-10-19'







def enum_sample():
  from enum import Enum
  TaskType = Enum('TaskType', ('FetchPage', 'FindIndex'))
  print(TaskType.FetchPage, TaskType.FetchPage.name)
  # >>> (<TaskType.FetchPage: 1>, 'FetchPage')
  for t in TaskType:
    print(repr(t), repr(t.name))
  # >>> <TaskType.FetchPage: 1> 'FetchPage'
  # >>> <TaskType.FindIndex: 2> 'FindIndex'



def platform_sample():
  import platform
  if(platform.system() == "Windows"):
    print ("Call Windows tasks")
  elif(platform.system() == "Linux"):
    print ("Call Linux tasks")
  else:
    print ("Other System tasks")


def ordered_default_dict_sample():
  from collections import OrderedDict
  result = OrderedDict()
  for key, val in custom_generater():
      result.setdefault(key, []).append(val)




"""
simple class defination
"""
class Page:
  def __init__(self):
    pass
  def __str__(self):
    return '<Page #{}>'.format(id(self))
  def __to_id(self):
    return '<Page #{}>'.format(id(self))
  @classmethod
  def create(cls, params):
    return cls(params)
  @property
  def is_valid(self):
    return True
# =========================================================
# =================== end of class Page ===================
# =========================================================








"""
standard lib api
"""
def random_usage():
  import random
  random.random()
  # 生成一个随机浮点数：range[0.0,1.0)
  random.uniform(a, b)
  # 生成一个指定范围内的随机浮点数，a,b为上下限，只要a!=b,就会生成介于两者之间的一个浮点数，若a=b，则生成的浮点数就是a
  random.randint(a, b)
  # 生成一个指定范围内的整数，a为下限，b为上限，生成的随机整数a<=n<=b;若a=b，则n=a；若a>b，报错
  random.randrange(start, stop, step)  # ([start], stop [,step])
  # 从指定范围内，按指定基数递增的集合中获取一个随机数，基数缺省值为1
  random.randrange(10, 100)
  # 输出为10到100间的任意数
  random.randrange(10, 100, 4)
  # 输出为10到100内以4递增的序列[10,14,18,22...]
  random.choice(range(10, 100, 4))
  # 输出在结果上与上一条等效
  random.choice(sequence)
  # 从序列中获取一个随机元素，参数sequence表示一个有序类型，泛指list，tuple，字符串等
  random.shuffle(x, random)  # (x[,random])
  # 将一个列表中的元素打乱
  random.sample(sequence, k)
  # 随机取k个元素作为片段返回，不会修改原有序列







def regexp_usage():
  import re
  pattern = re.compile(r'hello')
  match = pattern.match('hello world!')
  if match:
    print(match.group())
  re.compile(strPattern, flag)
  # flag: 匹配模式，取值可以使用按位或运算符'|'表示同时生效，比如re.I | re.M
  # re.compile('pattern', re.I | re.M) 与 re.compile('(?im)pattern')是等价的
  # re.I(re.IGNORECASE): 忽略大小写（括号内是完整写法，下同）
  # M(MULTILINE): 多行模式，改变'^'和'$'的行为（参见上图）
  # S(DOTALL): 点任意匹配模式，改变'.'的行为
  # L(LOCALE): 使预定字符类 \w \W \b \B \s \S 取决于当前区域设定
  # U(UNICODE): 使预定字符类 \w \W \b \B \s \S \d \D 取决于unicode定义的字符属性
  # X(VERBOSE): 详细模式。这个模式可以是多行，忽略空白字符，并可以加入注释。
  m = re.match(r'hello', 'hello world!')
  print(m.group())



  # Match对象

  # 匹配的结果，包含了很多关于此次匹配的信息，
  # 属性：
  # string: 匹配时使用的文本。
  # re: 匹配时使用的Pattern对象。
  # pos: 文本中正则表达式开始搜索的索引。值与Pattern.match()和Pattern.search()方法的同名参数相同。
  # endpos: 文本中正则表达式结束搜索的索引。值与Pattern.match()和Pattern.search()方法的同名参数相同。
  # lastindex: 最后一个被捕获的分组在文本中的索引。如果没有被捕获的分组，将为None。
  # lastgroup: 最后一个被捕获的分组的别名。如果这个分组没有别名或者没有被捕获的分组，将为None。
  # 方法：
  # group([group1, …]):
  # 获得一个或多个分组截获的字符串；指定多个参数时将以元组形式返回。
  # group1可以使用编号也可以使用别名；编号表整个匹配的子串；
  # 不填写参数时，返回group(0)；
  # 截获字符串的组返回None；
  # 截获了多次的组返回最后一次截获的子串。
  # groups([default]):
  # 以元组形式返回全部分组截获的字符串。相当于调用group(1,2,…last)。
  # ult表示没有截获字符串的组以这个值替代，默认为None。
  # groupdict([default]):
  # 返回以有别名的组的别名为键、以该组截获的子串为值的字典，
  # 没有别名的组不包含在内。default含义同上。
  # start([group]):
  # 返回指定的组截获的子串在string中的起始索引（子串第一个字符的索引）。group默认值为0。
  # end([group]):
  # 返回指定的组截获的子串在string中的结束索引（子串最后一个字符的索引+1）。group默认值为0。
  # span([group]):
  # 返回(start(group), end(group))。
  # expand(template):
  # 将匹配到的分组代入template中然后返回。
  # template中可以使用\id或\g<id>、\g<name>引用分组，
  # 但不能使用编号0。
  # \id与\g<id>是等价的；但\10将被认为是第10个分组，
  # 如果你想表达\1之后是字符'0'，只能使用\g<1>0。

  # 引用分组编号匹配：
  # >>> pat=re.compile(r'(?P<K>a)\w(c)(?P=K)\2')  #\2引用分组2的值，就是c
  # >>> pat.findall('Aabcadef')                   #匹配不到，因为完整'a\wcac',模式的第5位是c
  # []
  # >>> pat.findall('Aabcacdef')                  #匹配到，模式的第5位和组2一样,值是c
  # [('a', 'c')]
  # >>> pat.search('Aabcacdef').groups()
  # ('a', 'c')
  # >>> pat.search('Aabcacdef').group()
  # 'abcac'
  # >>> pat.search('Aabcacdef').group(1)
  # 'a'
  # >>> pat.search('Aabcacdef').group(2)
  # 'c'

  # (?P=name)：引用别名为的分组匹配到的串
  # >>> pat=re.compile(r'(?P<K>a)\w(c)(?P=K)')    #(?P=K)引用分组1的值，就是a
  # >>> pat.search('abcdef').group()              #匹配不到，因为完整'a\wca',模式的第4位是a
  # AttributeError: 'NoneType' object has no attribute 'group'
  # >>> pat.search('abcadef').group()             #匹配到，模式的第4位和组1一样,值是c
  # 'abca'
  # >>> pat.search('abcadef').groups()
  # ('a', 'c')
  # >>> pat.search('abcadef').group(1)
  # 'a'
  # >>> pat.search('abcadef').group(2)
  # 'c


  text = '''提取<span color='red'>自定义的</span>颜色 可能出现在缩进块里, 可能有<font style='background:#def; font-size:1.5rem; color: #edb;'>不同的颜色定义</font>型式 '''
  pat2 = r'(<(span|font)[^>]+?color ?= ?([\'\"]?).+?\3[^>]+?>.+?</ ?\2>)'
  # findall 一般把整个表达式括起来, 所以里面的分组注意从 \2 开始
  result = re.findall(pat2, text)
  print(result)

  m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
  print("m.string:", m.string)            # m.string: hello world!
  print("m.re:", m.re)                    # m.re: <_sre.SRE_Pattern object at 0x016E1A38>
  print("m.pos:", m.pos)                  # m.pos: 0
  print("m.endpos:", m.endpos)            # m.endpos: 12
  print("m.lastindex:", m.lastindex)      # m.lastindex: 3
  print("m.lastgroup:", m.lastgroup)      # m.lastgroup: sign
  print("m.group(1,2):", m.group(1, 2))   # m.group(1,2): ('hello', 'world')
  print("m.groups():", m.groups())        # m.groups(): ('hello', 'world', '!')
  print("m.groupdict():", m.groupdict())  # m.groupdict(): {'sign': '!'}
  print("m.start(2):", m.start(2))        # m.start(2): 6
  print("m.end(2):", m.end(2))            # m.end(2): 11
  print("m.span(2):", m.span(2))          # m.span(2): (6, 11)
  print(r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3')) # m.expand(r'\2 \1\3'): world hello!


  # Pattern对象
  # 是一个编译好的正则表达式，通过Pattern提供的一系列方法可以对文本进行匹配查找。
  # Pattern不能直接实例化，必须使用re.compile()进行构造。
  # pattern: 编译时用的表达式字符串。
  # flags: 编译时用的匹配模式。数字形式。
  # groups: 表达式中分组的数量。
  # groupindex: 以表达式中有别名的组的别名为键、以该组对应的编号为值的字典，没有别名的组不包含在内。

  p = re.compile(r'(\w+) (\w+)(?P<sign>.*)', re.DOTALL)
  print("p.pattern:", p.pattern)       # p.pattern: (\w+) (\w+)(?P<sign>.*)
  print("p.flags:", p.flags)           # p.flags: 48
  print("p.groups:", p.groups)         # p.groups: 3
  print("p.groupindex:", p.groupindex) # p.groupindex: {'sign': 3}


  # match(string[, pos[, endpos]]) | re.match(pattern, string[, flags]):
  # 将从string的pos下标处起尝试匹配pattern；
  # 如果pattern结束时仍可匹配，则返回一个Match对象；
  # 如果匹配过程中pattern无法匹配，或者匹配未结束就已到达endpos，则返回None。

  # 注意：这个方法并不是完全匹配。当pattern结束时若string还有剩余字符，仍然视为成功。
  # 想要完全匹配，可以在表达式末尾加上边界匹配符'$'。

  # search(string[, pos[, endpos]]) | re.search(pattern, string[, flags]):
  # 用于查找字符串中可以匹配成功的子串。
  # 从string的pos下标处起尝试匹配pattern，
  # 如果pattern结束时仍可匹配，则返回一个Match对象；
  # 若无法匹配，则将pos加1后重新尝试匹配；
  # 直到pos=endpos时仍无法匹配则返回None。
  # pos和endpos的默认值分别为0和len(string))；
  # re.search()无法指定这两个参数，参数flags用于编译pattern时指定匹配模式。
  pattern = re.compile(r'world')
  # 这个例子中使用match()无法成功匹配
  match = pattern.search('hello world!')
  if match:
    print(match.group())



  # split(string[, maxsplit]) | re.split(pattern, string[, maxsplit]):
  # 按照能够匹配的子串将string分割后返回列表。
  # maxsplit用于指定最大分割次数，不指定将全部分割。
  p = re.compile(r'\d+')
  print(p.split('one1two2three3four4')) # ['one', 'two', 'three', 'four', '']

  # findall(string[, pos[, endpos]]) | re.findall(pattern, string[, flags]):
  # 搜索string，以列表形式返回全部能匹配的子串。
  p = re.compile(r'\d+')
  print(p.findall('one1two2three3four4')) # ['1', '2', '3', '4']

  # finditer(string[, pos[, endpos]]) | re.finditer(pattern, string[, flags]):
  # 搜索string，返回一个顺序访问每一个匹配结果（Match对象）的迭代器。
  p = re.compile(r'\d+')
  for m in p.finditer('one1two2three3four4'):
    print(m.group()) # 1 2 3 4


  # sub(repl, string[, count]) | re.sub(pattern, repl, string[, count]):
  # 使用repl替换string中每一个匹配的子串后返回替换后的字符串。
  # 当repl是字符串时，可以使用\id或\g<id>、\g<name>引用分组，但不能使用编号0。
  # 当repl是方法时，这个方法应当只接受一个参数（Match对象），
  # 并返回一个字符串用于替换（返回的字符串中不能再引用分组）。
  # count用于指定最多替换次数，不指定时全部替换。
  p = re.compile(r'(\w+) (\w+)')
  s = 'i say, hello world!'
  print(p.sub(r'\2 \1', s)) # say i, world hello!
  def func(m):
    return m.group(1).title() + ' ' + m.group(2).title()
  print(p.sub(func, s)) # I Say, Hello World!

  # subn(repl, string[, count]) | re.sub(pattern, repl, string[, count]):
  # 返回 (sub(repl, string[, count]), 替换次数)。
  p = re.compile(r'(\w+) (\w+)')
  s = 'i say, hello world!'
  print(p.subn(r'\2 \1', s)) # ('say i, world hello!', 2)
  def func(m):
    return m.group(1).title() + ' ' + m.group(2).title()
  print(p.subn(func, s)) # ('I Say, Hello World!', 2)






def path_usage():

  import pathlib
  p = pathlib.Path('.')  
  [x for x in p.iterdir() if x.is_dir()]     # 列出所有子目录
  # [WindowsPath('.git'), WindowsPath('.idea'), WindowsPath('.vscode'), ...]
  list(p.glob('**/*.py'))   # 列出指定类型的文件
  # [PosixPath('pathlib.py'), PosixPath('setup.py'), PosixPath('test_pathlib.py')]

  p = pathlib.Path(r'F:\cookies\python')  
  q = p / 'learnPython'  # 使用 / 拼接路径
  print(q)
  # F: \cookies\python\learnPython  

  q.exists()  # 查询属性
  # True
  q.is_dir()
  # True
  q.stat().st_size
  # 956

  q = q / "hello_world.py"  # 打开文件
  with q.open() as f:
    print(f.readline())

  p = PurePath('/etc')
  str(p)    # '/etc'
  bytes(p)  # b'/etc'
  p = PureWindowsPath('c:/Program Files')
  str(p)    # 'c:\\Program Files'


  PureWindowsPath('c:/Program Files/').drive    # 'c:'
  PurePosixPath('/etc').root                    # '/'
  p = PureWindowsPath('c:/foo/bar/setup.py')
  p.parents[0]                                  # PureWindowsPath('c:/foo/bar')
  p.parents[1]                                  # PureWindowsPath('c:/foo')
  p.parents[2]                                  # PureWindowsPath('c:/')

  PureWindowsPath('//some/share/setup.py').name # 'setup.py'
  PureWindowsPath('//some/share').name          # ''
  PurePosixPath('my/library/setup.py').suffix   # '.py'
  PurePosixPath('my/library.tar.gz').suffix     # '.gz'
  PurePosixPath('my/library').suffix            # ''
  PurePosixPath('my/library.tar.gar').suffixes  # ['.tar', '.gar']
  PurePosixPath('my/library.tar.gz').suffixes   # ['.tar', '.gz']
  PurePosixPath('my/library').suffixes          # []
  PurePosixPath('my/library.tar.gz').stem       # 'library.tar'
  PurePosixPath('my/library.tar').stem          # 'library'
  PurePosixPath('my/library').stem              # 'library'


  p = PureWindowsPath('c:\\windows')
  p.as_posix()                               # 'c:/windows'
  p = PurePosixPath('/etc/passwd')
  p.as_uri()                                 # 'file:///etc/passwd'
  p = PureWindowsPath('c:/Windows')
  p.as_uri()                                 # 'file:///c:/Windows'
  PurePath('a/b.py').match('*.py')           # True
  PurePath('/a/b/c.py').match('a/*.py')      # False
  p = PurePosixPath('/etc/passwd')
  p.relative_to('/')        # PurePosixPath('etc/passwd')
  p.relative_to('/etc')     # PurePosixPath('passwd')
  p.relative_to('/usr')     # ValueError: '/etc/passwd' does not start with '/usr'

  p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
  p.with_name('setup.py')  # PureWindowsPath('c:/Downloads/setup.py')
  p = PureWindowsPath('c:/')
  p.with_name('setup.py')  # ValueError: PureWindowsPath('c:/') has an empty name




  import os # os.path 模块中的路径名访问函数
  # 分隔
  os.path.basename()   # 去掉目录路径, 返回文件名
  os.path.dirname()    # 去掉文件名, 返回目录路径
  os.path.join()       # 将分离的各部分组合成一个路径名
  os.path.split()      # 返回 (dirname(), basename()) 元组
  os.path.splitdrive() # 返回 (drivename, pathname) 元组
  os.path.splitext()   # 返回 (filename, extension) 元组

  # 信息
  os.path.getatime()   # 返回最近访问时间
  os.path.getctime()   # 返回文件创建时间
  os.path.getmtime()   # 返回最近文件修改时间
  os.path.getsize()    # 返回文件大小(以字节为单位)

  # 查询
  os.path.exists()     # 指定路径(文件或目录)是否存在
  os.path.isabs()      # 指定路径是否为绝对路径
  os.path.isdir()      # 指定路径是否存在且为一个目录
  os.path.isfile()     # 指定路径是否存在且为一个文件
  os.path.islink()     # 指定路径是否存在且为一个符号链接
  os.path.ismount()    # 指定路径是否存在且为一个挂载点
  os.path.samefile()   # 两个路径名是否指向同个文件

  os.path.abspath(name)   # 获得绝对路径
  os.path.normpath(path)  # 规范path字符串形式

  # 分离文件名：
  os.path.split(r"c:\python\hello.py")        # ("c:\\python", "hello.py")
  # 分离扩展名：
  os.path.splitext(r"c:\python\hello.py")     # ("c:\\python\\hello", ".py")
  # 获取路径名：
  os.path.dirname(r"c:\python\hello.py")      # "c:\\python"
  # 获取文件名：
  os.path.basename(r"r:\python\hello.py")     # "hello.py"
  # 判断文件是否存在：
  os.path.exists(r"c:\python\hello.py")       # True
  # 判断是否是绝对路径：
  os.path.isabs(r".\python")                  # False
  # 判断是否是目录：
  os.path.isdir(r"c:\python")                 # True
  # 判断是否是文件：
  os.path.isfile(r"c:\python\hello.py")       # True
  # 判断是否是链接文件：
  os.path.islink(r"c:\python\hello.py")       # False
  # 获取文件大小：
  os.path.getsize(filename)
  # 搜索目录下的所有文件：
  os.path.walk()


  # os 模块属性
  os.linesep   # 用于在文件中分隔行的字符串
  os.sep       # 用来分隔文件路径名的字符串
  os.pathsep   # 用于分隔文件路径的字符串
  os.curdir    # 当前工作目录的字符串名称
  os.pardir    # 当前工作目录的父目录字符串名称

  os.rename(old, new)             # 重命名
  os.remove(file)                 # 删除
  os.listdir(path)                # 列出目录下的文件
  os.getcwd()                     # 获取当前工作目录
  os.chdir(newdir)                # 改变工作目录
  os.makedirs(r"c:\python\test")  # 创建多级目录
  os.mkdir("test")                # 创建单个目录
  os.removedirs(r"c:\python")     # 删除多个目录
  # 删除所给路径最后一个目录下所有空目录
  os.rmdir("test")         # 删除单个目录
  os.stat(file)            # 获取文件属性
  os.chmod(file)           # 修改文件权限与时间戳
  os.system("dir")         # 执行操作系统命令
  os.exec(), os.execvp()   # 启动新进程
  osspawnv()               # 在后台执行程序
  os.exit(), os._exit()    # 终止当前进程



  import shutil  # shutil模块对文件的操作
  shutil.copy(oldfile, newfile)            # 复制单个文件
  shutil.copytree(r".\setup", r".\backup") # 复制整个目录树
  shutil.rmtree(r".\backup")               # 删除整个目录树
  tempfile.mktemp()                        # --> filename  创建一个唯一的临时文件：
  tempfile.TemporaryFile()                 # 打开临时文件









def time_usage():

  # 最常用的 time.time() 返回的是一个浮点数，单位为秒。
  # 但 strftime 处理的类型是 time.struct_time，
  # 实际上是一个 tuple。
  # strptime 和 localtime 都会返回这个类型。

  import time
  t = time.time()       # 1202872416.4920001
  type(t)               # <type 'float'>
  t = time.localtime()  # (2008, 2, 13, 10, 56, 44, 2, 44, 0)
  type(t)               # <type 'time.struct_time'>
  time.strftime('%Y-%m-%d', t)             # '2008-02-13'
  time.strptime('2008-02-14', '%Y-%m-%d')  # (2008, 2, 14, 0, 0, 0, 3, 45, -1)


  import datetime
  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # '2019-08-29 18:47:27'






def string_usage():

  ''' bytes to text
  '''
  b = b'123'
  bytes.decode(b, encoding='utf-8')


  ''' string letters
  '''
  import string
  print(string.ascii_letters)
  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  print(string.ascii_lowercase)
  # 'abcdefghijklmnopqrstuvwxyz'
  print(string.ascii_uppercase)
  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  print(string.digits)
  # '0123456789'
  print(string.hexdigits)
  # '0123456789abcdefABCDEF'
  print(string.octdigits)
  # '01234567'
  print(string.punctuation)
  # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
  print(string.printable)
  # '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
  print(string.whitespace)
  # '\t\n\x0b\x0c\r


  ''' str methods
  '''
  "hello".capitalize()
  # 'Hello'
  "hello world".capitalize()
  # 'Hello world'
  'ww'.ljust(20)
  # 'ww                  '
  'ww'.rjust(20)
  # '                  ww'
  'ww'.center(20)
  # '         ww         '


  ''' str format
  '''

  'Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
  # 'Coordinates: 37.24N, -115.81W'
  coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
  'Coordinates: {latitude}, {longitude}'.format(**coord)
  # 'Coordinates: 37.24N, -115.81W'

  coord = (3, 5)
  'X: {0[0]};  Y: {0[1]}'.format(coord)
  # 'X: 3;  Y: 5'

  "repr() shows quotes: {!r}; str() doesn't: {!s}".format('test1', 'test2')
  # "repr() shows quotes: 'test1'; str() doesn't: test2"

  '{:<30}'.format('left aligned')
  # 'left aligned                  '
  '{:>30}'.format('right aligned')
  # '                 right aligned'
  '{:^30}'.format('centered')
  # '           centered           '
  '{:*^30}'.format('centered')  # use '*' as a fill char
  # '***********centered***********'

  '{:+f}; {:+f}'.format(3.14, -3.14)   # show it always
  # '+3.140000; -3.140000'
  '{: f}; {: f}'.format(3.14, -3.14)   # show a space for positive numbers
  # ' 3.140000; -3.140000'
  '{:-f}; {:-f}'.format(3.14, -3.14)   # show only the minus -- same as '{:f}; {:f}'
  # '3.140000; -3.140000'
  '{:05d}; {:05d}'.format(123, 123456) # Display number with leading zeros
  # '00123; 123456'

  # format also supports binary numbers
  "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}".format(42)
  # 'int: 42;  hex: 2a;  oct: 52;  bin: 101010'
  # with 0x, 0o, or 0b as prefix:
  "int: {0:d};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}".format(42)
  # 'int: 42;  hex: 0x2a;  oct: 0o52;  bin: 0b101010'

  '{:,}'.format(1234567890)
  # '1,234,567,890'

  points = 19.5
  total = 22
  'Correct answers: {:.2%}.'.format(points/total)
  # 'Correct answers: 88.64%'

  import datetime
  d = datetime.datetime(2010, 7, 4, 12, 15, 58)
  '{:%Y-%m-%d %H:%M:%S}'.format(d)
  # '2010-07-04 12:15:58'

  octets = [192, 168, 0, 1]
  octets_str = '{:02X}{:02X}{:02X}{:02X}'.format(*octets) # 'C0A80001'
  int(octets_str, 16)                                     # 3232235521

  width = 5
  for num in range(5, 12):
    for base in 'dXob':
      print('{0:{width}{base}}'.format(num, base=base, width=width), end=' ')
    print()
  #     5     5     5   101
  #     6     6     6   110
  #     7     7     7   111
  #     8     8    10  1000
  #     9     9    11  1001
  #    10     A    12  1010
  #    11     B    13  1011





def sys_and_platform_usage():
  import sys
  import platform
  sys.argv                            # 从程序外部向程序传递参数
  # sys.exit([arg])                   # 退出，arg=0为正常退出
  sys.getdefaultencoding()            # 'utf-8' 获取系统当前编码
  sys.setdefaultencoding()            # 设置系统默认编码，执行reload(sys), setdefaultencoding('utf8')，将系统默认编码设置为utf8
  sys.getfilesystemencoding()         # 获取文件系统使用编码方式，Windows下返回 'mbcs'，mac下返回'utf-8'. 
  sys.path                            # 获取指定模块搜索路径的字符串集合
  sys.platform                        # 'win32' 获取当前系统平台
  sys.stdin, sys.stdout, sys.stderr   # 与标准I/O流对应的流对象

  platform.system()    # 获取操作系统类型，'Windows' 'Linux'
  platform.platform()  # 获取操作系统，'Windows-10-10.0.18362-SP0' 'Darwin-9.8.0-i386-32bit'
  platform.version()   # 获取系统版本信息 '10.0.18362'
  platform.mac_ver() 
  platform.win32_ver() # ('10', '10.0.18362', 'SP0', 'Multiprocessor Free')



  