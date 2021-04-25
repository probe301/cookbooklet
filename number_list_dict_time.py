
"""--------------
处理列表和可迭代对象
--------------"""


def dedupe(items, key=None):
  '''去除重复，可以保留原list的顺序'''
  seen = set()
  for item in items:
    val = item if key is None else key(item)
    if val not in seen:
      yield item
      seen.add(val)



def rotate(array, n):
  '''list 滑动元素的顺序，n可以是负数'''
  n = n % len(array)
  if n == 0:
    return array
  return array[n:] + array[:n]



def flatten(sequence, to_expand=lambda x: isinstance(x, (list, tuple))):
  '''展平嵌套的list'''
  iterators = [iter(sequence)]
  while iterators:
    # 循环当前的最深嵌套（最后）的迭代器
    for item in iterators[-1]:
      # print(item)
      if to_expand(item):
        # 找到了子序列，循环子序列的迭代器
        iterators.append(iter(item))
        break
      else:
        yield item
    else:
      # 最深嵌套的迭代器耗尽，回过头来循环它的父迭代器
      iterators.pop()



def lrange(n, m=None, step=1):
  '''range转list'''
  if m is not None:
    return list(range(n, m, step))
  else:
    return list(range(0, n, step))


def enumer(iterable, first=None, skip=0):
  ''' 迭代开头的 n 个元素, 顺便 yield 元素的索引
      enumfirst('abcdefg')            => 0a 1b 2c 3d 4e 5f 6g
      enumfirst('abcdefg', first=4)   => 0a 1b 2c 3d
      enumfirst('abcdefg', skip=2)    => 2c 3d 4e 5f 6g
      enumfirst('abcdefg', first=3, skip=2) => 2c 3d 4e
  '''
  for i, item in enumerate(iterable):
    if skip != 0 and i < skip:
      continue
    if first is not None and i >= first+skip:
      break
    else:
      yield i, item



def transpose(data):
  '''矩阵转置'''
  return map(list, zip(*data))



def windows(iterable, length=2, overlap=0, yield_tail=True):
  '''按照固定窗口大小切片list, 可以重叠
  滑动array窗口,
  每次提供length数目的元素,如果有overlap则重复之前的元素
  yield_tail: 最后不足 length 的那部分元素是否也要 yield'''
  import itertools
  if length <= overlap:
    raise AttributeError(
        'overlap {} cannot larger than length {}'.format(overlap, length))
  it = iter(iterable)
  results = list(itertools.islice(it, length))
  while len(results) == length:
    yield results
    results = results[length-overlap:]
    results.extend(itertools.islice(it, length-overlap))
  if results and yield_tail:
    yield results



def ensure_plural(obj):
  ''' 把 str, num 等变成 list, 用于参数需要接受 iterable 的情形'''
  if isinstance(obj, (tuple, list)):
    return obj
  elif isinstance(obj, (int, float, str)):
    return [obj]
  else:
    raise ValueError('cannot plural {}'.format(obj))



def top(iterable, n=1, smallest=False, key=None):
  ''' 返回列表中最大或最小的n个元素, 适合于n比较小的情况
  如果只需要最大或最小的一个元素, 应该用 max(), min()
  如果需要非常多的元素, 应该 sorted(iterable)[:n] '''
  import heapq
  if smallest:
    return heapq.nsmallest(n, iterable, key=key)
  else:
    return heapq.nlargest(n, iterable, key=key)
  # portfolio = [
  #     {'name': 'IBM', 'shares': 100, 'price': 91.1},
  #     {'name': 'AAPL', 'shares': 50, 'price': 543.22},
  #     {'name': 'FB', 'shares': 200, 'price': 21.09},
  #     {'name': 'HPQ', 'shares': 35, 'price': 31.75},
  #     {'name': 'YHOO', 'shares': 45, 'price': 16.35},
  #     {'name': 'ACME', 'shares': 75, 'price': 115.65}
  # ]
  # cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
  # expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])



from copy import deepcopy
def dict_merge(a, b=None):
  a = deepcopy(a)
  if b is None:
    b = {}
  a.update(b)
  return a



def is_array(obj):
  '''
  print(is_array([12, 4]))  # => True
  print(is_array([]))       # => True
  print(is_array((24, )))   # => True

  print(is_array(1.1))      # => False
  print(is_array(None))     # => False
  print(is_array('qwihr'))  # => False
  '''
  if isinstance(obj, str):
    return False
  return isinstance(obj, (list, set, tuple))



def joiner(iterable, sep='\n', indent=0, precision=None):
  ''' 以指定的间隔字符拼合列表
      提供 precision 则按照该精度格式化浮点数
  '''
  def format_element(x):
    x = str(x)
    if precision and x.replace('.', '', 1).isdigit():
      return ('{:.'+str(precision)+'f}').format(float(x))
    else:
      return x
  return sep.join(' ' * indent + format_element(elem) for elem in iterable)













"""--------------
数值操作
--------------"""
import random
def rand(start, end=None):
  if isinstance(start, int):
    if end:
      return random.randint(start, end-1)
    else:
      return random.randint(0, start-1)
  elif isinstance(start, float):
    if end:
      return random.uniform(start, float(end))
    else:
      return random.uniform(0.0, start)



def random_split(seq, p=0.1):
  '''按照概率 p 随机拆分集合'''
  train = []
  test = []
  roll = random.random
  for row in seq:
    if roll() < p:
      test.append(row)
    else:
      train.append(row)
  return train, test



def statistic(seq, reverse=False, precision=None):
  ''' 统计 list 中的数据
      a = [1,1,1,1,2,2]
      b = a*100 + list(range(1,100))
      c = list('aaaaaaasghkghewxckbv')
      print(statistic(a))
      print(statistic(b))
      print(statistic(c)) '''
  from collections import Counter
  array = list(seq)
  if precision:
    array = [round(e, precision) for e in array]
  counter = Counter(array)
  length = len(array)
  s = 'statistic ({} items):\n'.format(length)
  s += ''.join('  <{}>: {} ({:.1%})\n'.format(k, v, v/length) for k, v in sorted(list(counter.items()), reverse=reverse))
  if all(isinstance(n, (int, float)) for n in array):
    s += '  sum:{:.4f}  ave:{:.4f}  min:{}  max:{}'.format(sum(array), sum(array)/length, min(array), max(array))
  return s







"""--------------
time datetime 处理日期
--------------"""
import time
def random_sleep(min, max=None):
  '''休眠指定的时间,或范围内的随机值'''
  if max is None:
    return time.sleep(float(min))
  else:
    t = random.uniform(float(min), float(max))
    return time.sleep(t)

import datetime
def get_datetime():
  datetime.datetime.now()              # datetime(2019, 8, 29, 19, 12, 27, 384604)
  datetime.datetime.now().timestamp()  # 1567077158.420575
  return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # '2019-08-29 19:11:28'

def to_timestamp(i):
  return datetime.datetime.fromtimestamp(i / 1000 / 1000).strftime("%Y-%m-%d %H:%M:%S.%f")[11:]
# to_timestamp(1567077158420575)  -> '19:12:38.420575'





def arrow_usage():
  import arrow
  t = arrow.utcnow()             # <Arrow [2017-02-01T08:30:37.627622+00:00]>
  arrow.now()                    # <Arrow [2017-02-01T16:32:02.857411+08:00]>
  t = arrow.utcnow()
  t.timestamp                    # 1485937837
  t = arrow.now()
  t.format()                     # '2017-02-01 17:00:42+08:00'
  t.format("YYYY-MM-DD HH:mm")   # '2017-02-01 17:00'

  arrow.get("2017-01-20 11:30", "YYYY-MM-DD HH:mm")
  # <Arrow[2017-01-20T11:30:00+00:00] >
  arrow.get("1485937858.659424")
  # <Arrow[2017-02-01T08:30:58.659424+00:00] >
  arrow.get(1485937858.659424)
  # <Arrow[2017-02-01T08:30:58.659424+00:00] >

  t = arrow.now()               # <Arrow[2017-02-01T17:19:19.933507+08:00] >
  t.shift(days=-1)    # 前一天   # <Arrow[2017-01-31T17:19:19.933507+08:00] >
  t.shift(weeks=-1)   # 前一周   # <Arrow[2017-01-25T17:19:19.933507+08:00] >
  t.shift(months=-2)  # 前两月   # <Arrow[2016-12-01T17:19:19.933507+08:00] >
  t.shift(years=1)    # 明年     # <Arrow[2018-02-01T17:19:19.933507+08:00] >





"""--------------
使用 arrow 处理日期
--------------"""

import arrow
def time_from_stamp(s):
  return arrow.get(s) # s in (float, str)
def time_from_str(s, zone='+08:00'):
  return arrow.get(s+zone, "YYYY-MM-DD HH:mm:ssZZ")
def time_now():
  return arrow.now()
def time_now_stamp():
  return arrow.now().timestamp
def time_now_str():
  return arrow.now().format("YYYY-MM-DD HH:mm:ss")
def time_to_stamp(t):
  return t.timestamp
def time_to_str(t):
  return t.format("YYYY-MM-DD HH:mm:ss")
def time_to_humanize(t):
  return t.humanize()
  # return arrow.get(d.strftime('%Y-%m-%d %H:%M:%S') + zone).humanize()

def time_shift():
  t = arrow.now()
  # t.shift(days=-1)
  # t.shift(weeks=-1)
  # t.shift(months=-2)
  # t.shift(years=1)

import re
def time_shift_from_humanize(t, shift_expr):
  ''' 返回 t 变动了 shift_expr 后的时刻
      shift_expr 只接受 秒 分 时 和 天
      like: 3days, -3day, 20min, +20mins, 1seconds'''
  pat = r'^(\+?\-?\d+) ?(second|seconds|minute|minutes|hour|hours|day|days)$'
  m = re.match(pat , shift_expr)
  if not m:
    raise ValueError('time_shift cannot parse shift_expr: {shift_expr}'.format(**locals()))
  kargs = dict()
  unit = m.group(2) if m.group(2)[-1] == 's' else m.group(2)+'s' # 必须是 days=1, 不是 day=1
  kargs[unit] = int(m.group(1))
  return t.shift(**kargs)
  # t.shift(weeks=-1)
  # t.shift(months=-2)
  # t.shift(years=1)

def duration_from_humanize(expr):
  ''' 返回 expr 语义中的 diff 秒数
      expr 只接受 秒 分 时 和 天'''
  pat = r'^(\+?\-?\d+) ?(second|seconds|minute|minutes|hour|hours|day|days)$'
  m = re.match(pat, expr)
  if not m:
    raise ValueError(
        'duration_from_humanize cannot parse duration expr: {expr}'.format(**locals()))
  kargs = dict()
  unit = m.group(2) if m.group(2)[-1] == 's' else m.group(2)+'s'
  kargs[unit] = int(m.group(1))
  diff = arrow.now().shift(**kargs) - arrow.now()
  return diff.days * 24 * 3600 + diff.seconds



# Random Rollor
import random
class Roller():

  def __init__(self, seed=None):
    if seed is None:
      seed = random.randint(1, 999)
    self.init_seed = seed
    self.fields = {}
    self.seeds = {}

  def _choice(self, field, seed):
    random.seed(seed)
    if isinstance(field, set) or isinstance(field, list):
      return random.choice(field)
    elif isinstance(field, range):
      return random.randrange(field.start, field.stop, field.step)
    else:
      raise NotImplmentedError

  def add(self, **kvargs):
    for key, value in kvargs.items():
      self.fields[key] = value

  def __getattr__(self, name):
    if name in self.fields:
      seed = self.seeds.get(name, self.init_seed) + 1
      self.seeds[name] = seed
      return self._choice(self.fields[name], seed)
    else:
      raise NameError(f'Key={name} not found')

# roller = Roller(24)
# roller.add(paramA=range(10, 40, 3), paramB=[0,3,4,5])
# roller.paramA, roller.paramB
# # 对于同样的 Roller(24), 调用多次 .paramA, 一定会生成决定的值




def systematic_sample(data, n):
  # 系统抽样 systematic sampling
  # 又称机械抽样、等距抽样，
  # 先将总体的观察单位按某一顺序号分成n个部分，
  # 依次用相等间距，从每一部分个抽取一个观察单位组成样本。
  len_data = len(data)
  sample = []
  for i in range(n):
    sample.append(data[int((len_data-1) * i / (n-1))])
  return sample



'''groupby demo
将文本中带有内容的行设为一组, 将空行丢弃
'''
from itertools import groupby

data = '''

SD size (or range) must be large enough

    11:54:52.168                                                                                                        *
    11:54:52.677 SD size for cache misses not large enough.
    11:54:52.677
    java.lang.RuntimeException: SD size for cache misses not large enough.
        at Vdb.common.failure(common.java:350)

jro run, without journal path

    12:03:07.724 input argument scanned: '-fspec'
    12:03:07.725 input argument scanned: '-jro'
    java.lang.RuntimeException: Slave localhost-0 prematurely terminated.
        at Vdb.common.failure(common.java:350)
        at Vdb.SlaveStarter.startSlave(SlaveStarter.java:188)
        at Vdb.SlaveStarter.run(SlaveStarter.java:47)

jn run Not a directory

    12:04:21.768 localhost-0 : 	at Vdb.DV_map.allocateSDMaps(DV_map.java:861)
    12:04:23.107 Look at file localhost-0.stdout.html for more information.
    java.lang.RuntimeException: Slave localhost-0 prematurely terminated.
        at Vdb.common.failure(common.java:350)
        at Vdb.SlaveStarter.startSlave(SlaveStarter.java:188)
        at Vdb.SlaveStarter.run(SlaveStarter.java:47)

'''
datalines = []
for key, group in groupby(data.splitlines(), key=lambda l: l.startswith('    ') or not(l.strip())):
    datalines.append('\n'.join(group))
