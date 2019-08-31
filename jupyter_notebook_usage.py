




# ==============================
# ==============================
# data processing import

######   ##### ####### #####
##   ## ##   ##   ##  ##   ##
##   ## #######   ##  #######
##   ## ##   ##   ##  ##   ##
######  ##   ##   ##  ##   ##

######  ######   #####   ###### #######  ###### ###### ###### ##   ##  ######
##   ## ##   ## ##   ## ###     ##      ##     ##        ##   ###  ## ##
######  ######  ##   ## ##      ######   #####  #####    ##   ## # ## ##  ###
##      ##  ##  ##   ## ###     ##           ##     ##   ##   ##  ### ##   ##
##      ##   ##  #####   ###### ####### ###### ######  ###### ##   ##  #####

 ###### ##   ## ######   #####  ###### #######
   ##   ### ### ##   ## ##   ## ##   ##   ##
   ##   ## # ## ######  ##   ## ######    ##
   ##   ##   ## ##      ##   ## ##  ##    ##
 ###### ##   ## ##       #####  ##   ##   ##
# ==============================
# ==============================

import json
import yaml
import csv
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl import load_workbook


import tablib
dataset = tablib.Dataset()
dataset.xlsx = open('testdata.xlsx', 'rb').read()
print(dataset)



















## jupyter notebook matplotlib
# 这些得放在 jupyter notebook 里, 放在 py 文件里让 jupyter 调用就没用
import numpy as np
import pandas as pd
pd.set_option('display.width', 200)   # 每行最大字符
pd.set_option('precision', 3)         # 显示数字精度
pd.set_option('display.max_rows', 10) # 预览时最多显示行数
pd.set_option('display.float_format', lambda x : '%.2f' % x)  # 不使用科学计数法

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

plt.rcParams['figure.figsize'] = 18, 9
plt.rcParams['axes.unicode_minus'] = False     # 显示数字负号
plt.rcParams['font.sans-serif'] = ['SimHei']   # 显示中文字体
mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['savefig.dpi'] = 100
mpl.rcParams['font.size'] = 12
mpl.rcParams['legend.fontsize'] = 'large'
mpl.rcParams['figure.titlesize'] = 'medium'
plt.style.use('seaborn-whitegrid')

import seaborn as sns
# sns.set(style="white")  # 不显示背景 grid, 有时候带一些浅灰 grid 更好

def explore(df):
  print('==== row, col ====', df.shape)
  print('==== columns ====')
  print('\t'.join(df.columns))

  print('==== describe ====')
  print(df.describe())
  print('==== info ====')
  print(df.info())
  print('==== sample ====')
  return df.sample(n=5, random_state=100)

def find_in(df, col, pat):
  ''' 在 col 中 查找命中 pat 的数据
      如果 pat 是 字符串, 视为模糊查找 
      如果 pat 是 list, 或者非字符串型, 视为精确查找 '''
  if isinstance(pat, str):
    return df[df[col].str.contains(pat)]
  if not isinstance(pat, (list, set)):
    pat = [pat]
  return df[df[col].isin(pat)]


def join_sample():
  smoking_df = smoking_df[['state_county', 'smok']]
  m = pd.merge(cancer_df, smoking_df, how='left', on=None, 
          left_on='County', right_on='state_county',  
          left_index=False, right_index=False, sort=True,  
          suffixes=('_x', '_y'), copy=True, indicator=False)

  m.head(10)



### jupyter magic

# %matplotlib inline
# %load_ext autoreload
# %autoreload 2
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"  # 在 output 显示多个表达式

# jupyter notebook css fix

# %%html
# <style>
# .output_text {font-size: 12px; }
# .output_text pre {line-height: 12px; font-family: "Monaco";}

# .text_cell_render pre {line-height: 11px;}
# .rendered_html pre {line-height: 11px; }
# .text_cell_render pre code {font-size: 12px;}
# .rendered_html pre code {font-size: 12px;}

# .output_text pre, .text_cell_render pre {padding: 0.5ex;}
# .container { width:100% !important;}
# .prompt {min-width: 10ex;}
# </style>


from IPython.display import Image
import os
def display_image(paths, labels=None):
  if isinstance(paths, str):
    paths = [paths]
  if isinstance(labels, str):
    labels = [labels]

  for i, path in enumerate(paths):
    display(Image(filename=path))
    # display(Image(filename=path, width=200, height=200))
    if labels:
      print(labels[i])
    else:
      print(os.path.basename(path))
    print()

from IPython.display import display, Markdown
display(Markdown(text))




## file method


