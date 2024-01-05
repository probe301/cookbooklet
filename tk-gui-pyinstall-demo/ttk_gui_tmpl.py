# -*- coding:utf-8 -*-


import os
import sys
import logging
import base64
# Logging configuration
logging.basicConfig(filename=__file__.replace('.py', '.log'),
                    level=logging.DEBUG,   # choose debug will show all logs
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))


try:
    import Tkinter as tkinter   # python2
    import ttk                  # 更好看的样式, 把 tkinter.Radiobutton 改成 ttk.Radiobutton
    import Tix as tix
    from tkinter.ScrolledText import ScrolledText

except ImportError:
    import tkinter              # python3
    from tkinter import ttk     # 更好看的样式, 把 tkinter.Radiobutton 改成 ttk.Radiobutton
    from tkinter import tix
    from tkinter.scrolledtext import ScrolledText


from tkinterdnd2 import TkinterDnD


'''
简化的 python GUI
只支持 windows 版, 能打包 pyinstaller 在无编程环境运行即可
GUI 支持拖放, 记录日志就行

复杂 UI 应该考虑 web, gradio, streamlit 等
'''

class TextHandler(logging.Handler):
  def __init__(self, widget):
    logging.Handler.__init__(self)
    self.setLevel(logging.DEBUG)
    self.widget = widget
    self.widget.config(state='disabled')
    self.widget.tag_config("INFO", foreground="black")
    self.widget.tag_config("DEBUG", foreground="grey")
    self.widget.tag_config("WARNING", foreground="orange")
    self.widget.tag_config("ERROR", foreground="red")
    self.widget.tag_config("CRITICAL", foreground="red", underline=1)
    self.red = self.widget.tag_configure("red", foreground="red")
  def emit(self, record):
    self.widget.config(state='normal')
    # Append message (record) to the widget
    self.widget.insert(tkinter.END, self.format(record) + '\n', record.levelname)
    self.widget.see(tkinter.END)  # Scroll to the bottom
    self.widget.config(state='disabled')
    self.widget.update() # Refresh the widget




class GUI(tkinter.Frame):

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.root = master
        self.widget_dict = dict()
        self.build_gui()
        # ESC退出
        self.root.bind('<Escape>', lambda x: sys.exit())

    def build_gui(self):
        self.root.title('TITLE')
        self.option_add('*tearOff', 'FALSE')
        label = ttk.Label(self.root, text='text')
        label.grid(column=0, row=0)

        folders = ['folderA', 'folderB', 'folderC']
        self.folder_var = tkinter.StringVar()
        menu = ttk.OptionMenu(self.root,
                              self.folder_var,
                              *folders,
                              command=self.handle_cmd
                              )
        menu.config(width=50)
        menu.grid(column=1, row=0, sticky='we')

        end_row = self.build_radios(start_row=1)


        label_entry_info = [('local file path', '...this entry support drag file in'),
                            ('run command', 'C:\\notepad2\\notepad2.exe'),
                            ]
        for text, default_value in label_entry_info:
            label, entry = self.build_label_value_block(text, default_value,
                                                        position=(end_row, 0), entry_size=30)
            self.widget_dict[text] = entry
            end_row += 1

        # 给 widget 添加拖放方法
        local_path_entry = self.widget_dict['local file path']
        self.add_drop_handle(local_path_entry, self.handle_drop_on_local_path_entry)

        self.main_button = ttk.Button(self.root, text='text',
                                      command=self.print_main_button_method
                                      )
        self.main_button.grid(row=end_row+1, column=0, columnspan=2, sticky='we')

        self.build_logger_panel(end_row+2)





    ##########################
    ##########################
    # handlers
    ##########################
    ##########################



    def print_main_button_method(self):
        logger.info('print_main_button_method')
        logger.debug('dubug print_main_button_method')
        logger.warn('folder choose {}'.format(self.folder_var.get()))
        logger.error('radio choose {}'.format(self.radio_var.get()))


    def handle_cmd(self, value):
      logger.debug('choose %s' % self.folder_var.get())


    def add_drop_handle(self, widget, handle):
        widget.drop_target_register('DND_Files')

        def drop_enter(event):
            event.widget.focus_force()
            print('Entering widget: %s' % event.widget)
            return event.action
        def drop_position(event):
            print('Position: x %d, y %d' % (event.x_root, event.y_root))
            return event.action
        def drop_leave(event):
            # leaving 应该清除掉之前 drop_enter 的 focus 状态, 怎么清?
            print('Leaving %s' % event.widget)
            return event.action

        widget.dnd_bind('<<DropEnter>>', drop_enter)
        widget.dnd_bind('<<DropPosition>>', drop_position)
        widget.dnd_bind('<<DropLeave>>', drop_leave)
        widget.dnd_bind('<<Drop>>', handle)


    def handle_drop_on_local_path_entry(self, event):
        if event.data:
            logger.debug('Dropped data: %s' % event.data)
            # => ('Dropped data:\n', 'C:/tkDND.htm C:/TkinterDnD.html')
            # event.data is a list of filenames as one string;
            files = event.widget.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    print('Dropped file: "%s"' % f)
                    event.widget.delete(0, 'end')
                    event.widget.insert('end', f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f)
        return event.action


    ##########################
    ##########################
    # build UI
    ##########################
    ##########################


    def build_radios(self, start_row):
        label = ttk.Label(self.root, text='text')
        label.grid(column=0, row=start_row)

        self.radio_var = tkinter.StringVar()
        for radio_text in ['radioA', 'radioB', 'radioC']:
            radio = ttk.Radiobutton(self.root, text=radio_text,
                                    variable=self.radio_var,
                                    value=radio_text,
                                    # command=self.choose_templates_group
                                    )

            radio.grid(column=1, row=start_row, sticky='w', padx=15)
            start_row += 1
        return start_row

    def build_label_value_block(self, label, default_value, position=(0, 0), entry_size=20):
        label = ttk.Label(self.root, text=label)
        label.grid(row=position[0], column=position[1], sticky='we', padx=3, pady=1)
        entry = ttk.Entry(self.root, width=entry_size)
        entry.grid(row=position[0], column=position[1]+1, sticky='we', padx=3, pady=1)
        entry.insert(0, default_value)
        return label, entry

    def build_button(self, label, command, position=(0, 0), span=(1, 1)):
        if isinstance(span, str):
            span = [int(part) for part in span.split('x')]
        button = ttk.Button(self.root, text=label, command=command)
        button.grid(row=position[0], column=position[1], sticky='eswn',
                    padx=3, pady=1, rowspan=span[0], columnspan=span[1])
        return button

    def build_logger_panel(self, row):
        st = ScrolledText(self.root, state='disabled', width=30, height=20)
        st.configure(font='TkFixedFont', width=70)
        st.grid(column=0, row=row, sticky='we', columnspan=2)
        # Create textLogger
        text_handler = TextHandler(st)

        logger.addHandler(text_handler)



def make_stringify_ico(icopath):
    # ico to b64 解决 tk 运行后只有默认叶子图标问题
    # 与 pyinstaller 打包的文件 ico 无关
    # https://blog.csdn.net/PengDW12/article/details/121401871
    with open(icopath, "rb") as i:
        b64str = base64.b64encode(i.read())
    with open("icon.py", "w") as f:
        f.write('class Icon(object):\n')
        f.write('    def __init__(self):\n')
        f.write(f"        self.img='{bytes.decode(b64str)}'")
    print(f'ico {icopath} => icon.py done')
# make_stringify_ico('card.ico')


if __name__ == '__main__':
    # root = tkinter.Tk()

    # 如果需要文件拖放的话
    # TkDND (Tcl Plugin) tkdnd2.8-win32-x86_64.tar
    # https://sourceforge.net/projects/tkdnd/files/Windows%20Binaries/TkDND%202.8/
    # TkinterDnD2 (Python bindings)
    # https://sourceforge.net/projects/tkinterdnd/files/TkinterDnD2/
    root = TkinterDnD.Tk()

    root.lift()                         # 窗口置顶
    root.attributes('-topmost', True)   # 窗口置顶

    from icon import Icon
    with open('tmp.ico','wb') as tmp:
        tmp.write(base64.b64decode(Icon().img))
    root.iconbitmap('tmp.ico')
    os.remove('tmp.ico')

    if os.path.exists('icon.ico'):
        root.iconbitmap('icon.ico')  # 运行后 显示在左上角 ico

    gui = GUI(master=root)
    gui.mainloop()

# pyinstaller 打包
# pyinstaller -F -w -i card.ico ttk_gui_tmpl.py --additional-hooks-dir=.


# note

# tkinterdnd2 with pyinstaller
# 钩子文件 https://github.com/Eliav2/tkinterdnd2/blob/master/hook-tkinterdnd2.py
# If you want to use pyinstaller, you should use the hook-tkinterdnd2.py file included.
# Copy it in the base directory of your project, then:
# `pyinstaller -F -w myproject/myproject.py --additional-hooks-dir=.`

# pyinstaller 打包报错
# win32ctypes.pywin32.pywintypes.error: (225, '', '无法成功完成操作，因为文件包含病毒或潜在的垃圾软件。')
# 将pyinstaller 6.3.0，卸载后，安装6.2.0重新打包即可
# pip uninstall pyinstaller
# pip install pyinstaller==6.2.0
