

# 检查包版本
# pip list | grep arrow
# >>> arrow     0.14.2
# 安装包的特定版本
# pip install arrow==0.14.2


# 安装 requirements.txt 中的包
# pip install -r requirements.txt


# 检测 项目中用到的包
# pip install pipreqs
# pipreqs ./ --encoding=utf8 --use-local --print
# >>> py_gfm==0.1.4
# >>> feedgen==0.7.0
# >>> ...
# >>> Jinja2==2.10.1
# >>> pyfiglet==0.8.post1
# >>> Flask==1.0.3


import sys
import os
from cx_Freeze import setup, Executable


path_platforms = ( "C:\Python33\Lib\site-packages\PyQt5\plugins\platforms\qwindows.dll", "platforms\qwindows.dll" )



included = (
  "test/msvcp100.dll",
  "test/msvcr100.dll",
  'Qt5UI.ui',
  'Other.py',
  'templates',
  'doc'
)


version = '1.5'
build_path = 'D:/builds/App_v' + version

build_exe_options = {
  "packages": ["os"],
  "excludes": ["tkinter"],
  "includes" : [ "re", "atexit"],
  "icon": 'icon.ico',
  "build_exe": build_path,
  "include_files" : included

}







setup(name = "App.exe",
      version = version,
      description = "description",
      options = {"build_exe": build_exe_options},
      executables = [Executable("App.py", base="Win32GUI", icon = 'icon.ico')])


os.remove(build_path + '/Qt5WebKit.dll')