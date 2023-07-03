import paramiko
import time
import itertools


def line_buffered(out):
    line_buf = ""
    while not out.channel.exit_status_ready():
        line_buf += out.read(1)
        if line_buf.endswith('\n'):
            yield line_buf
            line_buf = ''

def roundrobin(*iterables):
    '''轮询

    :param iterables: 一个或多个可迭代对象
    :rtype: iterator
    >>> list(roundrobin('ABC', 'D', 'EF'))
    ['A', 'D', 'E', 'B', 'F', 'C']
    '''
    num_active = len(iterables)
    nexts = itertools.cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            num_active -= 1
            nexts = itertools.cycle(itertools.islice(nexts, num_active))

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
vmA = RemoteNode('192.168.1.72', 22, 'root', 'vm', label='vmA')
# vmB = RemoteNode('ip', 22, 'root', 'password', label='vmB')
# vmA > 'ls'
# vmB > 'ls -alh'

# 实时标准输出和标准错误的样例
cmd = '''
echo "1in stdout";      sleep 1; 
echo "2in stdout";      sleep 1; 
echo "3in stderr" 1>&2; sleep 1; 
echo "4in stdout";      sleep 1; 
echo "5in stderr" 1>&2; sleep 1; 
echo "6in stdout";      sleep 1; 
echo "7in stdout"
'''
vmA > cmd.replace('\n', ' ')  # 因为缓冲区, 不太能保证顺序, 但差不太多
