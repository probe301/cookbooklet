
import os
import re
import sys
import fnmatch
import shutil
import difflib
from collections import OrderedDict as odict


class FileReplacer:

    def __init__(self, root, file_pattern='*.txt', black_list=None):
        self.root = root
        self.file_pattern = file_pattern
        self.black_list = tuple(black_list) or tuple([])
        self.rules = odict()

    def __str__(self):
        return (f"<self.__class__.__name__ root={self.root} file_pattern={self.file_pattern} \n"
                f"    black_list={self.black_list} \n"
                f"    rules_count={len(self.rules)} rules >")

    def add_rule(self, match_text, replacer):
        self.rules[match_text] = replacer

    def walk_on_files(self, root, patterns='*', single_level=False, yield_folders=False):
        ''' 取得文件夹下所有文件
            single_level 仅处理 root 中的文件(文件夹) 不处理下层文件夹
            yield_folders 也遍历文件夹'''
        patterns = patterns.split(';')
        for path, subdirs, files in os.walk(root, topdown=True):
            subdirs[:] = [d for d in subdirs if d not in ('.git', '__pycache__', '.ipynb_checkpoints')]
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

    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    def write_file(self, file_path, text):
        # 存文件, 顺带解决一下 CRLF -> LF 的问题
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        return True

    def can_match_patterns(self, text):
        for pat, repl in self.rules.items():
            if re.search(pat, text, flags=re.S):
                return True
        else:
            return False

    def compare_text(self, old_code, new_code, verbose=2):
        old_code = old_code.strip().split('\n')
        new_code = new_code.strip().split('\n')
        # diff = ndiff(old_code.splitlines(1), new_code.splitlines(1))   # splitlines(1) 保留行尾的换行
        changes = [l for l in difflib.unified_diff(old_code, new_code, n=verbose)]
        changes = [c for c in changes if c.strip() and not(c.startswith('@@') or c=='+++ \n' or c=='--- \n')]
        return changes

    def replace_patterns(self, text):
        for pat, replacer in self.rules.items():
            text = re.sub(pat, replacer, text, flags=re.S)
        return text

    def preview(self):
        return self.replace(dryrun=True)

    def replace(self, dryrun=False):
        for file_path in self.walk_on_files(self.root, patterns=self.file_pattern):
            if file_path.endswith(self.black_list):
                print(f'detect file `{file_path}` should not execute replacing')
                continue

            old_text = self.read_file(file_path)
            if self.can_match_patterns(old_text):
                new_text = self.replace_patterns(old_text)
                print(f'>>> change on file {file_path}')

                if dryrun:
                    # 只做预览
                    for diff_line in self.compare_text(old_text, new_text):
                        print(diff_line)
                else:
                    # 确实没有问题了, 再执行这一个write_file, 之前注意备份, 注意保持 git status目录清洁
                    self.write_file(file_path, new_text)






class ExcelReplacer(FileReplacer):

    def __init__(self, excel_file, excel_range='A1:A2'):
        # 需要 win32com, 或者别的什么能操作 excel 的 API
        import win32com.client

        self.excel_file = excel_file
        app = win32com.client.Dispatch("KET.Application")
        app.Visible = True
        doc = app.Workbooks.Open(excel_file)
        self.sheet = doc.ActiveSheet
        self.excel_range = excel_range
        self.rules = odict()

    def __str__(self):
        return (f"<self.__class__.__name__ excel_file={self.excel_file} {self.excel_range} \n"
                f"    rules_count={len(self.rules)} rules >")

    def read_cell(self, cell):
        v = cell.Value
        return str(v)

    def write_cell(self, cell, text):
        cell.Value = text
        self.cell_set_color(cell, '浅浅红')
        return True

    def cell_set_color(self, cell, color):
        data = {
            '浅浅红': 14083324.0, '浅浅黄': 13431551.0, '浅浅蓝': 15917529.0, '浅浅绿': 14348258.0, '浅浅灰': 15592941.0, '浅浅青': 16247773.0, '浅浅灰蓝': 14998742.0,
            '浅红': 11389944.0, '浅黄': 10086143.0, '浅蓝': 15189684.0, '浅绿': 11854022.0, '浅灰': 14408667.0, '浅青': 15652797.0, '浅灰蓝': 13285804.0,
            '红': 8696052.0, '黄': 6740479.0, '蓝': 14395790.0, '绿': 9359529.0, '灰': 13224393.0, '青': 15123099.0, '灰蓝': 11573124.0,
        }
        if color in data:
            cell.Interior.Color = data[color]
        else:
            raise ValueError(f'Invalid color {color}')


    def replace(self, dryrun=False):
        for cell in self.sheet.Range(self.excel_range):
            old_text = self.read_cell(cell)
            if self.can_match_patterns(old_text):
                new_text = self.replace_patterns(old_text)
                print(f'>>> change on cell {cell.Address}')
                if dryrun:
                    # 只做预览
                    for diff_line in self.compare_text(old_text, new_text):
                        print(diff_line)
                else:
                    # 确实没有问题了, 再执行这一个
                    self.write_cell(cell, new_text)






if __name__ == '__main__':

    # 文件内容替换
    # ROOT = r'C:/myproject_folder'
    # # BLACK_LIST 表示属于这个 ROOT 路径, 但是不想被替换的文件
    # BLACK_LIST = ('_replacer.py', 'some_file_do_not_want_to_replace.py', )
    # # 文件替换器, 输入项目主目录, 扫描和替换其中的文件
    # rplc = FileReplacer(root=ROOT, file_pattern='*.py', black_list=BLACK_LIST)


    # Excel替换器, 输入excel文件名和指定 Range (Range 形如 A23:C56), 扫描和替换其中的 cell
    rplc = ExcelReplacer(excel_file='C:/Downloads/test.xlsx', excel_range='N16:N46')

    # 接下来指定替换规则, rplc.add_rule(match_text, replacer)
    # match_text 是匹配到的文字,
    # replacer 是对匹配到的文字, 怎样处理, replacer 可以是字符串, 但是一般是函数, 更方便

    match_text = r'(@steps: 步骤\s*?)(\d+?\n)'
    def replacer(mat):
        step_index = int(mat.group(2)) + 100
        print(step_index)
        return mat.group(1) + str(step_index)
    rplc.add_rule(match_text, replacer) # 一个无聊的示例, 把 @steps: 换行后的步骤号 "1." 转成 "101."

    match_text = r'count=(\d+)'
    def replacer(mat):
        number = int(mat.group(1))
        if number > 200000:
            return f'count={number//10}'
        else:
            return f'count={number+500}'
    rplc.add_rule(match_text, replacer) # 一个更无聊的示例, 如果 "count=数字" 里的数字较大就缩到 1/10, 否则加上 500

    match_text = r'.+'
    def replacer(mat):
        cell_content = mat.group(0)
        result = []
        for line in cell_content.splitlines():
            if re.search(r'^\d+\.', line):
                result.append(line)
            else:
                last_line = result[-1] if result else ''
                result[-1] = last_line.rstrip() + ' ' + line
        return '\n'.join(result)
    rplc.add_rule(match_text, replacer) # 一个有点用的示例, 如果步骤中有 "不带序号的行", 则并入前一行

    # add_rule() 可以执行多次
    # 至此定义完成, 打印这个实例看看
    print(rplc)

    # 预览将被替换的文本
    rplc.preview()

    # 首先预览好了, 都没问题了, 再启动实际的替换
    # rplc.replace()
