
''' Null Pattern
'''

class Null:
  def __init__(self, *args, **kwargs):
    "忽略参数"
    return None
  def __call__(self, *args, **kwargs):
    "忽略实例调用"
    return self
  def __getattr__(self, mname):
    "忽略属性获得"
    return self
  def __setattr__(self, name, value):
    "忽略设置属性操作"
    return self
  def __delattr__(self, name):
    '''忽略删除属性操作'''
    return self
  def __repr__(self):
    return "<Null>"
  def __str__(self):
    return "Null"

# use Null pattern
def get_test_with_null(x):
  try:
    return x.test
  except AttributeError: # 异常处理返回Null类
    return Null()

for i in [A, B]:
  # 直接调用不需要判断
  get_test_with_null(i)()





''' 嵌套 @property
可以用一个 def 解决问题 '''
def nested_property(c):
  return property(**c())

# usage
import math
class Rectangle(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
  @nested_property
  def area():
    doc = "Area of the rectangle"
    def fget(self):
      return self.x * self.y
    def fset(self, value):
      ratio = math.sqrt((1.0 * value) / self.area)
      self.x *= ratio
      self.y *= ratio
    return locals()





class Singleton(object):
  ''' 单例模式
      继承这个类之后只能创建一个实例'''
  def __new__(cls, *args, **kwargs):
    if '_inst' not in vars(cls):
      # print(super(Singleton, cls))
      cls._inst = super(Singleton, cls).__new__(cls)
      # cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
    return cls._inst



''' 自动代理
'''
class AutoDelegator(object):
  delegates = ()
  do_not_delegate = ()
  def __getattr__(self, key):
    if key not in self.do_not_delegate:
      for d in self.delegates:
        try:
          return getattr(d, key)
        except AttributeError:
          pass
    raise AttributeError(key)

# usage
class Pricing(AutoDelegator):
  def __init__(self, location, event):
    self.delegates = [location, event]
  def setlocation(self, location):
    self.delegates[0] = location