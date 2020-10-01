





# ==============================
# data processing import
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











# 作为服务器时, 丢到后台执行
# jupyter notebook --allow-root  --ip='0.0.0.0'  > jupyter.log
# nohup jupyter notebook --allow-root  --ip='0.0.0.0'  > jupyter.log &


# 安装 jupyterthemes
# pip install --upgrade jupyterthemes
'''
themes choose from
  - chesterish
  - monokai
  - oceans16
  - onedork
  - solarized-light  # Mac 上没有这个 theme

jupyterthemes coding fonts # 似乎不起作用, 也许需要强制刷新
-f arg	Monospace Font

  consolamono  Consolamono
  dejavu       DejaVu Sans Mono
  inconsolata  Inconsolata-g
  meslo        Meslo
  oxygen       Oxygen Mono
  source       Source Code Pro
  sourcemed    Source Code Pro Medium

'''


# 安装 jupyter 扩展

'''
Jupyter notebook extensions
pip install https://github.com/ipython-contrib/jupyter_contrib_nbextensions/tarball/master
or
pip install jupyter_contrib_nbextensions

pip 安装依赖包时会出错, 需要先
conda update setuptools
然后就顺利运行了
jupyter contrib nbextension install --system
jupyter contrib nbextension install --user  # Mac 不能用 --system
'''


# 启用 Sublime 风格 hotkeys

'''
把下面代码放在 C:\Users\<UserID>\.jupyter\custom\custom.js 里面

require(["codemirror/keymap/sublime", "notebook/js/cell", "base/js/namespace"],
    function(sublime_keymap, cell, IPython) {
        // setTimeout(function(){ // uncomment line to fake race-condition
        cell.Cell.options_default.cm_config.keyMap = 'sublime';
        var cells = IPython.notebook.get_cells();
        for(var cl=0; cl< cells.length ; cl++){
            cells[cl].code_mirror.setOption('keyMap', 'sublime');
        }

        // }, 1000)// uncomment  line to fake race condition
    }
);
'''



# jupyter cell 编辑 hotkeys

# Shift + Tab      光标所在对象的文档, 可以反复按, 切换更多种模式
# Ctrl + Shift + - 分割 cell
# Shift + M        Merge cell
# Esc + F          查找替换, 不会影响 outputs
# Esc + O          Toggle cell output
# D + D            (press twice) to delete the current cell





# jupyter custom.js 功能
# 如果需要对所有 notebook 有效 把下面代码放在 C:\Users\<UserID>\.jupyter\custom\custom.js 里面
'''
```javascript

require(['notebook/js/codecell'], function(codecell) {
  codecell.CodeCell.options_default.highlight_modes['magic_text/x-csharp'] = {'reg':[/^%%csharp/]} ;
  Jupyter.notebook.events.one('kernel_ready.Kernel', function(){
  Jupyter.notebook.get_cells().map(function(cell){
      if (cell.cell_type == 'code'){ cell.auto_highlight(); } }) ;
  });
});

setTimeout(function() {
    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('f5', {
        help : 'run cell',
        handler : function (event) {
            IPython.notebook.execute_cell();
            return false;}});
    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('ctrl-.', {
        help : 'run cell',
        handler : function (event) {
            IPython.notebook.execute_cell();
            return false;}});
    Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('f5', {
        help : 'run cell',
        handler : function (event) {
            IPython.notebook.execute_cell();
            return false;}});
    Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('ctrl-.', {
        help : 'run cell',
        handler : function (event) {
            IPython.notebook.execute_cell();
            return false;}});
    Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('ctrl-enter', {
        help : 'none',
        // 防止与 Sublime hotkey Ctrl+Enter 冲突
        handler : function (event) {
            return false;}});

    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('delete', {
        help : 'none',
        handler : function (event) {
            IPython.notebook.delete_cell();
            return false;}});

    // 设置 python indent 为 2 空格
    var patch = {CodeCell: {cm_config:{indentUnit: 2}}}
    Jupyter.notebook.get_selected_cell().config.update(patch)

    // 依据 ipynb 文件名, 给 cell 加上特定的背景色
    String.prototype.hashCode = function() {
      var hash = 0, i, chr;
      if (this.length === 0) return hash;
      for (i = 0; i < this.length; i++) {
        chr   = this.charCodeAt(i);
        hash  = ((hash << 5) - hash) + chr;
        hash |= 0; // Convert to 32bit integer
      }
      return hash;
    };

    function random_hue_color(label, s, l) {
      // console.log(Math.abs(label.hashCode()))
      var hash_color = (Math.abs(label.hashCode()) % 360) / 360 * 100
      return `hsl(${hash_color}, ${s}%, ${l}%)`
    }

    var notebook_path = IPython.notebook.notebook_path
    var color1 = random_hue_color(notebook_path, 20, 90)
    var color2 = random_hue_color(notebook_path, 40, 80)

    var css = document.createElement("style")
    css.type = "text/css"
    css.innerHTML = `div.cell {background-color: ${color1};}`
    css.innerHTML +=`div.running {background-color: ${color2};}`
    css.innerHTML +=`div.running.selected {background-color: ${color2};}`
    css.innerHTML +=`div.CodeMirror {font-family: "Microsoft Yahei Mono"; font-size: 20px;}`
    css.innerHTML +='.container { width:100% !important;}'
    css.innerHTML +='.prompt {min-width: 10ex;}'
    css.innerHTML +='.output_text pre, .text_cell_render pre {padding: 0.5ex;}'
    css.innerHTML +='</style>'
    document.body.appendChild(css);

}, 2000)

```
'''



# 配置 jupyter 默认浏览器
'''
shell 执行 jupyter notebook --generate-config
C:/Users/用户名/.jupyter/jupyter_notebook_config.py
将
    #c.NotebookApp.browser = ''
替换为
    import webbrowser
    webbrowser.register("Firefox", None, webbrowser.GenericBrowser("C:/Program Files/Mozilla Firefox/firefox.exe"))
    c.NotebookApp.browser = "Firefox"
'''

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
# %autoreload 2                                     # 自动重载入模块
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"   # output 显示每一行表达式的输出

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






# open doc
?str.replace()  # open doc
# Suppress the output of a final function
# By adding a semicolon at the end, the output is suppressed.
plt.hist(x);

# Executing Shell Commands
!ls *.csv
!pip install numpy





==================
# show image from local
from keras.utils.visualize_util import plot
plot(model, show_shapes=True, to_file='model.png')
from IPython.display import display, Image
display(Image('model.png', width=500))

# show SVG
from IPython.display import SVG
from keras.utils.visualize_util import model_to_dot
SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))
