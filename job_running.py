

def is_windows():
  import sys
  return sys.platform == 'win32'


import subprocess
def run_command(cmd, verbose=False):
  if verbose: print('> running: ', cmd)
  try:
    output = subprocess.check_output(
        cmd, stderr=subprocess.STDOUT, shell=True, timeout=3,
        universal_newlines=True)
  except subprocess.CalledProcessError as exc:
    if verbose: print("status: FAIL", exc.returncode, exc.output)
    raise RuntimeError(f'status: FAIL, {exc.returncode}, {exc.output}')
  else:
    if verbose: print("output: \n{}\n".format(output))
    return output





def cronjob():
    '''守护进程'''
    from apscheduler.schedulers.blocking import BlockingScheduler

    def do_job_once():
        pass

    # do_job_once()
    scheduler = BlockingScheduler()
    scheduler.add_job(do_job_once, 'cron', second='0')        # do when second == 0
    # scheduler.add_job(do_job_once, 'interval', seconds=10)  # do every 10 seconds
    # scheduler.add_job(do_job_once, 'cron', second='0,1,2,3,4,5,6')
    scheduler.start()

def check_process_running(program):
    '''检测是否有指定名称的进程'''
    import psutil
    # print(list(p.name() for p in psutil.process_iter() if program in p.name()))
    return program in (p.name() for p in psutil.process_iter())

def get_ip():
    '''取得主机IP'''
    import socket
    ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
    return ip

def execute_windows_commands():
    import subprocess
    # 不要用 import commands , 对 Windows 支持不好
    command = 'D: & cd working_folder & dir'   # 多个命令以 & 连接
    process = subprocess.Popen(command, shell=False)
    stdoutput, erroutput = process.communicate()
    print(stdoutput, erroutput)
    print(repr(process.wait()))
    if process.wait() == 0:
        print('done')

    # Python subprocess模块总结
    # http://hackerxu.com/2014/10/09/subprocess.html


# Linux以Python执行命令的返回值
# import os
# val = os.system('ls -al')
# print val #输出为0
# val = os.system('ls -al non_exist_folder')
# print val #输出为512
# val = os.system('ls -al | grep non_exist_val')
# print val #输出为256