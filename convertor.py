
# SVG 转换 ICO
# 首先安装 ImageMagick https://imagemagick.org/script/download.php#windows
# 完后要添加环境变量 MAGICK_HOME = C:\Program Files\ImageMagick-7.0.10-Q16
# 然后 pip install Wand
from wand.image import Image
import os

INPUT_PATH = r'C:/Users/Probe/Downloads/folder_svg_in'
OUTPUT_PATH = r'C:/Users/Probe/Downloads/folder_ico_out'

def EnumPathFiles(path, callback):
    if not os.path.isdir(path):
        print('Error:"', path, '" is not a directory or does not exist.')
        return
    list_dirs = os.walk(path)

    for root, dirs, files in list_dirs:
        for d in dirs:
            EnumPathFiles(os.path.join(root, d), callback)
        for f in files:
            callback(root, f)

def svg2ico(path, filename):
    filename=str(filename)
    i = filename.index('.')
    fname = filename[:i]
    fext = filename[i:]
    if fext !='.svg': return

    input_file = str(path+'\\'+filename)
    output_file = OUTPUT_PATH + '\\' + fname + '.ico'
    print(output_file)
    with Image(width=128, height=128, filename=input_file) as ico:
        with Image(width=64, height=64, filename=input_file) as sico:
            ico.sequence.append(sico)
        with Image(width=48, height=48, filename=input_file) as sico:
            ico.sequence.append(sico)
        with Image(width=32, height=32, filename=input_file) as sico:
            ico.sequence.append(sico)
        with Image(width=16, height=16, filename=input_file) as sico:
            ico.sequence.append(sico)
        ico.save(filename=output_file)






# ipynb to markdown

import functools
import json
import os
import re
import sys
sys.path.append('../../')

from sein import log


# todo 现在 的 code 和 output 都是缩进 4 空格, 应该区别开
# 比如 code 是用 ```python ... ```, output 用 4 空格



def pre_text(lines):
    # 用来输出 output txt 的数据, 需要高亮的代码区分
    return '<pre>\n' + indent_join(lines) + '\n</pre>'


def highlight_code(source):
    # write("{% highlight ipython %}")
    # write(source)
    # write("{% endhighlight %}")
    return '```python\n' + source.replace('```', '\`\`\`') + '\n```'


def strip_colors(string):
    ansi_escape = re.compile(r'\x1b[^m]*m')
    return ansi_escape.sub('', string)


def embed_image(base64code, ref_id=None, alt_text=None, title=None):
    # 如果提供 ref_id 则使用 Reference-style, 否则使用 Inline-style
    # Inline-style:
    # ![alt text](https://github.com/.../images/icon48.png "Logo Title Text 1")
    # Reference-style:
    # ![alt text][logo]
    # [logo]: https://github.com/.../images/icon48.png "Logo Title Text 2"

    # # this is a markdown file with an image
    # <img src="data:image/png;base64,iVBORw0...ABJRU5ErkJggg==" />
    base64code = base64code.replace('\n', '')

    if ref_id:
        alt_text = alt_text or ref_id
        title = title or alt_text or ref_id
        return '![{}][{}]'.format(alt_text, ref_id), '[{}]: data:image/png;base64,{} "{}"'.format(ref_id, base64code, title)
    else:
        alt_text = alt_text or 'image'
        title = title or alt_text
        return '![{}](data:image/png;base64,{} "{}")'.format(alt_text, base64code, title)

def indent_join(lines, indent=4):
    return ''.join(' '*indent + l for l in lines)


def ipynb_json_to_markdown(path, print_code='follow_metadata'):
    # print_code = 'all' | 'none' | 'follow_metadata'
    filename = path
    notebook = json.load(open(filename, encoding='utf-8'))
    out_filename = os.path.splitext(filename)[0] + '.markdown'
    out = open(out_filename, 'w', encoding='utf-8')
    write = functools.partial(print, file=out) # this function contains newline

    def should_print_code(cell):
        # 先接受整体的 "metadata": "hide_input": true 控制, 然后是每个 cell 自己的控制, 有点像 css
        # 实际上在 notebook 里观察到这俩同时设置时有冲突
        # 还是只调节单独 cell 的显示, 把全部 cell 显示调成一直开启比较好
        if print_code == 'all':
            return True
        if print_code == 'follow_metadata':
            if cell.get('metadata') and 'hide_input' in cell['metadata'].keys():
                return not(cell['metadata']['hide_input'])
            elif notebook.get('metadata') and 'hide_input' in notebook['metadata'].keys():
                return not(notebook['metadata']['hide_input'])
            else:
                return True   # notebook 里没写, cell 也没写, 默认返回 true
        if print_code == 'none':
            return False
        raise ValueError


    cells = notebook['cells']

    image_counter = 0
    image_footer_refs = []

    for cell in cells:
        if cell['cell_type'] == 'markdown':
            # Easy
            write(''.join(cell['source']))

        elif cell['cell_type'] == 'code':
            # 先抓出 code, 再抓出 output
            # Can't use ``` or any shortcuts as markdown fails for some code
            source = ''.join(cell['source'])
            if source and should_print_code(cell):
                # print('write highlight_code', )
                write(highlight_code(source))
                write()

            for output in cell['outputs']:
                if output['output_type'] == 'stream':
                    if output['text'] and ''.join(output['text']).strip():
                        write('({})\n'.format(output['name']))
                        write(indent_join(output['text']))
                        write()
                    else:
                        pass
                elif output['output_type'] in ('display_data', 'execute_result'):
                    # display_data: 这时 data 可能是 text/plain text/markdown image/png 等等
                    # execute_result: 当 code 最后一句是表达式时
                    if output['data'].get('image/png'):
                        image_counter += 1
                        # html_code = embed_image(output['data']['image/png'])  # inline style
                        html_code, footer_ref = embed_image(output['data']['image/png'], ref_id='image{:03d}'.format(image_counter))
                        write(html_code)
                        image_footer_refs.append(footer_ref)
                    elif output['data'].get('text/markdown'):
                        write(pre_text(output['data']['text/markdown']))
                    elif output['data'].get('text/plain'):
                        write(pre_text(output['data']['text/plain']))
                    else:
                        raise ValueError('cannot read one of the output type', list(output['data'].keys()))
                elif output['output_type'] == 'error':
                    # 这里可能需要处理 pyerr pywarn 的情况, 原来是这么处理的
                    # elif output['output_type'] == 'pyerr':
                    #     write('\n'.join(strip_colors(o)
                    #                     for o in output['traceback']))
                    write('({})\n'.format(output['ename']))
                    write('({})\n'.format(output['evalue']))
                    write()

                else:
                    raise ValueError('cannot read output type', output['output_type'])
                write()
        write('\n'*2)

    if image_footer_refs:
        for ref in image_footer_refs:
            write(ref)
            write()

    print("{} created".format(out_filename))



def preview_ipynb_json(path):
    jso = json.loads(open(path, encoding='utf-8').read())

    # log.config(output_paths=['test.log'])
    log.config(max_depth=5)


    # 整体结构
    # {
    #   cells: [..., ..., ..., ..., ..., ..., ..., ...] <-- list length 39
    #   metadata: {
    #     toc: ...
    #     hide_input: ...
    #     language_info: ...
    #     kernelspec: ...
    #   }
    #   nbformat: 4
    #   nbformat_minor: 2
    # }

    # 其中 cell 分为 cell_type=code cell_type=md 这两种

    # cell_type=code 结构
    # {
    #   cell_type: code
    #   execution_count: 1
    #   outputs: []
    #   metadata: {
    #     hide_input: False
    #     ExecuteTime: {
    #       start_time: ...
    #       end_time: ...
    #     }
    #   }
    #   source: code lines...
    # }

    # 其中 outputs list 结构, 目前看来有
    # output_type=stream
    # output_type=display_data
    # output_type=execute_result (当 code 最后一句是表达式时) 三种
    # [{
    #   output_type: stream
    #   text: [..., ..., ..., ..., ..., ..., ..., ...] <-- list length 36
    #   name: stdout
    # },
    # {
    #   output_type: display_data
    #   data: {
    #     text/plain: [<matplotlib.figure.Figure at 0x1b78c978>]
    #     text/markdown: [mdcode list...]
    #     image/png: iVBORw0KGgoAAAANSUEFUeJ... (162090 chars)
    #   }
    #   metadata:       { }
    # },
    # {
    #   output_type: stream
    #   text: [...]
    #   name: stdout
    # }]
    log('notebook hide_input:', jso['metadata'].get('hide_input'))
    # print(jso['metadata'])
    log('cells:')

    for cell in jso['cells']:
        log(cell['cell_type'], cell['metadata'].get('hide_input'))




# if __name__ == '__main__':
#     # 或者这样也很好 html_embed base64 嵌入图片
#     # jupyter nbconvert --to=html_embed --no-prompt --template=nbextensions "dev.ipynb"
#     path = r'D:\Coding\...\data_process.ipynb'
#     preview_ipynb_json(path)
#     ipynb_json_to_markdown(path, print_code='follow_metadata')

# if __name__ == '__main__':
#     EnumPathFiles(INPUT_PATH, svg2ico)