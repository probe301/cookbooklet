

import pprint
pp = pprint.PrettyPrinter(width=160, compact=True).pprint
# pp(complex_object)


import reprlib
'''演示 repr 的用法'''
reprlib.repr(None)

'''演示递归 repr 的用法'''
class MyList(list):
  @reprlib.recursive_repr()
  def __repr__(self):
    return '<' + '|'.join(map(repr, self)) + '>'

# m = MyList('abc')
# m.append(m)
# m.append('x')
# print(m)

'''演示typing Union用法'''
from typing import Union
def (a: Union[str, int]):
  if isinstancec(a, str):
    print(a*2)
  elif isinstancec(a, int):
    print(a+1)

def post_xml(data: Union[str, ET.Element]):
  pass


"""--------------
调试和测试
--------------"""

class TestException(Exception):
  pass

def microtest(modulename, verbose=None, log=sys.stdout):
  '''自动测试
  运行模块中所有以 _test_ 开头的没有参数的函数
  modulename = 要测试的模块名称
  verbose    = 打印更多的内容
  成功后返回 None, 失败时报异常'''
  module = __import__(modulename)
  total_tested = 0
  total_failed = 0
  total_pending = 0
  # print(111, file=sys.stdout)
  for name in dir(module):
    # print(name)
    if name.startswith('_test_'):
      obj = getattr(module, name)
      if (isinstance(obj, types.FunctionType) and not obj.__code__.co_argcount):
        if verbose:
          print('        MicroTest: = <%s> on test' % name, file=log)
        try:
          total_tested += 1
          obj()
          print('        MicroTest: . <%s> tested' % name, file=log)
        except Exception:
          total_failed += 1
          print('')
          print('---- ↓ MicroTest: %s.%s() FAILED ↓ ----' % (modulename, name), file=sys.stderr)
          traceback.print_exc()
          print('---- ↑ MicroTest: %s.%s() FAILED ↑ ----' % (modulename, name), file=sys.stderr)
          print('')
    elif 'test' in name:
      total_pending += 1
      if verbose:
        print('        MicroTest: ? <%s> detect pending test' % name, file=log)

  message = '\n\n        MicroTest: module "%s" failed (%s/%s) unittests. (pending %s unittests)\n\n' % (modulename, total_failed, total_tested, total_pending)
  if total_failed > 0:
    raise TestException(message)
  if verbose:
    print(message, file=log)





"""--------------
同时 log 到 stdout 和 file.log
--------------"""
from pprint import pprint
from datetime import datetime
class create_logger:
  def __init__(self, file_path):
    self.filepath = file_path + '.log'
  def custom_print(self, data, prefix='', filepath=None, pretty=False):
    out = open(filepath, 'a', encoding='utf-8') if filepath else sys.stdout
    if filepath:  # 在输出到文件时增加记录时间戳, 输出到 stdout 不记录时间戳
      prefix = '[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + ']' + prefix

    if prefix:
      print(prefix, file=out, end=' ')
    if pretty:
      pprint(data, stream=out, width=80, compact=True, depth=2)
    else:
      print(data, file=out)
    # if filepath:
    #   out.close()
  def output(self, values, pretty=False):
    if len(values) == 1:
      s = values[0]
    else:
      s = ', '.join(str(v) for v in values)
    try:
      self.custom_print(s, filepath=None, pretty=pretty)
    except UnicodeEncodeError as e:
      self.custom_print(str(e), prefix='logger output error: ')
    try:
      self.custom_print(s, filepath=self.filepath, pretty=pretty)
    except UnicodeEncodeError as e:
      self.custom_print(str(e), filepath=self.filepath, prefix='logger output error: ')
  def __ror__(self, *other):
    self.output(other, pretty=True)
    return other
  def __call__(self, *other, pretty=False):
    self.output(other, pretty=pretty)

# usage
# from tools import create_logger
# log = create_logger(__file__)
# log_error = create_logger(__file__ + '.error')








def watch(variableName, watchOutput=sys.stdout):
  '''调用 watch(secretOfUniverse) 打印出如下的信息：
     # => File "trace.py", line 57, in __testTrace
     # =>   secretOfUniverse <int> = 42'''
  watch_format = ('File "%(fileName)s", line %(lineNumber)d, in'
                  ' %(methodName)s\n  %(varName)s <%(varType)s>'
                  ' = %(value)s\n\n')
  if __debug__:
    stack = traceback.extract_stack()[-2:][0]
    actualCall = stack[3]
    if actualCall is None:
      actualCall = "watch([unknown])"
    left = actualCall.find('(')
    right = actualCall.rfind(')')
    paramDict = dict(varName=actualCall[left+1:right].strip(),
                     varType=str(type(variableName))[8:-2],
                     value=repr(variableName),
                     methodName=stack[2],
                     lineNumber=stack[1],
                     fileName=stack[0])
    watchOutput.write(watch_format % paramDict)







import cProfile
import pstats
from io import StringIO
def profiler(func):
  def wrapper(*args, **kwargs):
    datafn = func.__name__ + ".profile"  # Name the data file
    prof = cProfile.Profile()
    retval = prof.runcall(func, *args, **kwargs)
    prof.dump_stats(datafn)
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(prof, stream=s).sort_stats(sortby)  # 拦截report stream
                                                          # 否则会跟其它的print混在一起
    ps.print_stats()
    print(s.getvalue())
    return retval
  return wrapper

'''
profiler 样例
def center(p1, p2, p3):
  # 已知三点求圆心
  a1, b1 = p1
  a2, b2 = p2
  a3, b3 = p3
  u = (a1**2 - a2**2 + b1**2 - b2**2) / (2*a1 - 2*a2)
  v = (a1**2 - a3**2 + b1**2 - b3**2) / (2*a1 - 2*a3)
  k1 = (b1-b2) / (a1-a2)
  k2 = (b1-b3) / (a1-a3)
  centerx = v - (u-v)*k2 / (k1-k2)
  centery = (u-v) / (k1-k2)
  return (centerx, centery)

@profiler
def test_center():
  for i in range(1000000):
    try:
      center([1+i*.0001, 2], [1.1, 5+i*.0001], [4, 6+i*.0001])
    except ZeroDivisionError:
      print('000')
      continue
test_center()

# >>> 000
# >>> 000
# >>>          1000004 function calls in 7.982 seconds
# >>>
# >>>    Ordered by: cumulative time
# >>>
# >>>    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# >>>         1    2.160    2.160    7.982    7.982 E:\GitHub\kaggle\play.py:49(test_center)
# >>>   1000000    5.821    0.000    5.821    0.000 E:\GitHub\kaggle\play.py:36(center)
# >>>         2    0.000    0.000    0.000    0.000 {built-in method print}
# >>>         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

'''







from functools import wraps

def func_logger(fn):
  '''打印函数的实参, 返回结果, 执行时间'''
  @wraps(fn)
  def wrapper(*args, **kwargs):
    ts = time.time()
    result = fn(*args, **kwargs)
    te = time.time()
    print("function    = {0}".format(fn.__name__))
    print("  arguments = {0} {1}".format(args, kwargs))
    print("  return    = {0}".format(result))
    print("  time      = %.6f sec" % (te - ts))
    return result
  return wrapper

'''
@func_logger
def multipy(x, y, d='default', *args, **kw):
  return x * y

@func_logger
def sum_num(n):
  s = 0
  for i in range(n + 1):
    s += i
  return s

multipy(2, 10)
multipy(2, 30, 'bar', 'foo', d2='new1')
sum_num(100)
sum_num(10000000)

# >>> function    = multipy
# >>>   arguments = (2, 10) {}
# >>>   return    = 20
# >>>   time      = 0.000000 sec
# >>>
# >>> function    = multipy
# >>>   arguments = (2, 30, 'bar', 'foo') {'d2': 'new1'}
# >>>   return    = 60
# >>>   time      = 0.000000 sec
# >>>
# >>> function    = sum_num
# >>>   arguments = (100,) {}
# >>>   return    = 5050
# >>>   time      = 0.000000 sec
# >>>
# >>> function    = sum_num
# >>>   arguments = (10000000,) {}
# >>>   return    = 50000005000000
# >>>   time      = 1.473084 sec
'''







import sys
import os
import linecache

def trace_line(f):
  def globaltrace(frame, why, arg):
    if why == "call":
      return localtrace
    return None
  def localtrace(frame, why, arg):
    if why == "line":
      # record the file name and line number of every trace
      filename = frame.f_code.co_filename
      if filename.startswith('C:\\Anaconda3\\'):   # Python标准库代码不输出
        return
      lineno = frame.f_lineno
      bname = os.path.basename(filename)
      report = "{}({}): {}".format(bname, lineno,
                                   linecache.getline(filename, lineno)[:-1])
                                   # getline 之后会带换行符, 需要去掉
      print(report)
    return localtrace
  def _f(*args, **kwds):
    sys.settrace(globaltrace)
    result = f(*args, **kwds)
    sys.settrace(None)
    return result
  return _f


def printcolor(msg, color=None):
  '''在 jupyter notebook 中也有效'''
  if color == "green":
    print('\033[92m%s\033[0m' % msg)
  elif color == "blue":
    print('\033[94m%s\033[0m' % msg)
  elif color == "yellow":
    print('\033[93m%s\033[0m' % msg)
  elif color == "red":
    print('\033[91m%s\033[0m' % msg)
  else:
    print(msg)










def pyshould_test_sample():
  import unittest
  # from pyshould import *
  import pyshould.patch
  from pyshould import should
  result | should.be_integer()
  (1+1) | should_not.equal(1)
  "foo" | should.equal('foo')
  len([1, 2, 3]) | should.be_greater_than(2)
  result | should.equal(1/2 + 5)
  1 | should_not.eq(2)
  # Matchers not requiring a param can skip the call parens
  True | should.be_truthy
  # Check for exceptions with the context manager interface
  with should.throw(TypeError):
    raise TypeError('foo')
  with should.not_raise:  # will report a failure
    fp = open('does-not-exists.txt')
  # Apply our custom logic for a test
  'FooBarBaz' | should.pass_callback(lambda x: x[3:6] == 'Bar')
  should.be_an_integer.or_string.and_equal(1)
  # (integer) OR (string AND equal 1)
  should.be_an_integer.or_a_float.or_a_string
  # (integer) OR (float) OR (string)
  should.be_an_integer.or_a_string.and_equal_to(10).or_a_float
  # (integer) OR (string AND equal 10) OR (float)
  should.be_an_integer.or_a_string.but_less_than(10)
  # (integer OR string) AND (less than 10)
  # Note: we can use spacing to make them easier to read
  should.be_an_integer  .or_a_string.and_equal(0)  .or_a_float
  # (integer) OR (string AND equal 0) OR (float)
  # Note: in this case we use capitalization to make them more obvious
  should.be_an_integer .Or_a_string.And_equal(1) .But_Not_be_a_float
  # ( (integer) OR (string AND equal 1) ) AND (not float)
  # Note: if no matchers are given the last one is used
  should.be_equal_to(10).Or(20).Or(30)
  # (equal 10) OR (equal 20) OR (equal 30)
  # Note: If no combinator is given AND is used by default
  should.integer.greater_than(10).less_than(20)
  # (integer) AND (greater than 10) AND (less than 20)
  # Note: But by using should_either we can set OR as default
  should_either.equal(10).equal(20).equal(30)

  class TestSequenceFunctions1(unittest.TestCase):
    def setUp(self):
      self.seq = list(range(10))
    def test_shuffle(self):
      # make sure the shuffled sequence does not lose any elements
      random.shuffle(self.seq)
      self.seq.sort()
      self.assertEqual(self.seq, list(range(10)))
      # should raise an exception for an immutable sequence
      self.assertRaises(TypeError, random.shuffle, (1,2,3))
    def test_choice(self):
      element = random.choice(self.seq)
      a = 10
      a | should.gt(20)
    def test_sample(self):
      with self.assertRaises(ValueError):
        random.sample(self.seq, 20)
      for element in random.sample(self.seq, 5):
        self.assertTrue(element in self.seq)

  unittest.main()
