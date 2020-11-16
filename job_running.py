

def is_windows():
  import sys
  return sys.platform == 'win32'

'''paramiko demo'''
import paramiko
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机，否则可能报错：paramiko.ssh_exception.SSHException:
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname=host_ip, username='root')
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout = cmd_output.read().decode()
ssh.close()



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





# 简便的多远程节点的运行命令方式, 适合在 jupyter 里做控制板
import paramiko
import time
from itertools import zip_longest
class RemoteNode:
    def __init__(self, ip, port, user, pw, label=''):
        self.ip = ip
        self.port = port
        self.user = user
        self.pw = pw
        self.label = label or f'{self.ip}:{self.port}'

    def connect(self, verbose=False):
        remote_node = paramiko.SSHClient()
        remote_node.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_node.connect(self.ip, self.port, self.user, self.pw)
        if verbose:
            print(f'connect RemoteNode {self.ip}:{self.port} done')
        return remote_node

    def test(self):
        self.connect(verbose=True)

    def __gt__(self, cmd):
        start_time = time.time()
        ret_status = 'done'
        print(f'>>> {cmd} (on {self.label})')
        remote_node = self.connect()  # reconnect everytime
        stdin, stdout, stderr = remote_node.exec_command(cmd)
        for line in iter(stdout.readline, ''):  # 实时显示出 stdout, 不使用 iter 会导致执行完了一并显示
            print('    ' + line.rstrip('\n'))
        for line in iter(stderr.readline, ''):
            print('  x ' + line.rstrip('\n'))
            fail = 1
        print(f'<<< {ret_status} in {(time.time() - start_time):.2f}s\n')
        remote_node.close()

# usage
# vmA = RemoteNode('ip', 22, 'root', 'password', label='vmA')
# vmB = RemoteNode('ip', 22, 'root', 'password', label='vmB')
# vmA > 'ls'
# vmB > 'ls -alh'

# 实时标准输出和标准错误的样例
# cmd = '''
# echo "1in stdout";      sleep 4;
# echo "2in stdout";      sleep 4;
# echo "3in stderr" 1>&2; sleep 2;
# echo "4in stdout";      sleep 4;
# echo "5in stderr" 1>&2; sleep 2;
# echo "6in stdout";      sleep 4;
# echo "7in stdout"
# '''
# vmA > cmd.replace('\n', ' ')  # 因为缓冲区, 不太能保证顺序, 但差不太多

# TODO vmB >> 表示仅执行, 无输出, 或者丢到后台执行?

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



'''线程执行的基本模式'''
import threading
import time
def jn_exec(name, n=10):
  for i in range(n):
    time.sleep(1)
    print(f'jn_exec: {i+1}/{n} seconds')

def jro_exec(name, n=12):
  for i in range(n):
    time.sleep(1)
    print(f'jro_exec: {i+1}/{n} seconds')

def vd_init(wait_time=5, n=3):
  time.sleep(wait_time)
  for i in range(n):
    time.sleep(1)
    print(f'    vd_init: {i+1}/{n} seconds')

def vd_delete(n=5):
  for i in range(n):
    time.sleep(1)
    print(f'    vd_delete: {i+1}/{n} seconds')

def jn_and_jro_and_delete():

  jn_exec('name', )
  print('>>> jn completed, running jro')
  jro_exec('name', )
  print('>>> jro completed, running delete')
  vd_delete()
  print('>>> all done')

t1 = threading.Thread(target=jn_and_jro_and_delete, args=())
t2 = threading.Thread(target=vd_init, args=(5, ))
t1.start()
t2.start()
t1.join()
t2.join()

# jn_exec: 1/10 seconds
# jn_exec: 2/10 seconds
# jn_exec: 3/10 seconds
# jn_exec: 4/10 seconds
# jn_exec: 5/10 seconds
#     vd_init: 1/3 seconds
# jn_exec: 6/10 seconds
#     vd_init: 2/3 seconds
# jn_exec: 7/10 seconds
#     vd_init: 3/3 seconds
# jn_exec: 8/10 seconds
# jn_exec: 9/10 seconds
# jn_exec: 10/10 seconds
# >>> jn completed, running jro
# jro_exec: 1/12 seconds
# jro_exec: 2/12 seconds
# jro_exec: 3/12 seconds
# jro_exec: 4/12 seconds
# jro_exec: 5/12 seconds
# jro_exec: 6/12 seconds
# jro_exec: 7/12 seconds
# jro_exec: 8/12 seconds
# jro_exec: 9/12 seconds
# jro_exec: 10/12 seconds
# jro_exec: 11/12 seconds
# jro_exec: 12/12 seconds
# >>> jro completed, running delete
#     vd_delete: 1/5 seconds
#     vd_delete: 2/5 seconds
#     vd_delete: 3/5 seconds
#     vd_delete: 4/5 seconds
#     vd_delete: 5/5 seconds
# >>> all done

# join的原理就是依次检验线程池中的线程是否结束，没有结束就阻塞直到线程结束，如果结束则跳转执行下一个线程的join函数

# 1. 阻塞主进程，专注于执行多线程中的程序
# 2. 多线程多join的情况下，依次执行各线程的join方法，前头一个结束了才能执行后面一个
# 3. 无参数，则等待到该线程结束，才开始执行下一个线程的join
# 4. 参数timeout为线程的阻塞时间，如 timeout=2 就是罩着这个线程2s 以后，就不管他了，继续执行下面的代码