
# remote executor
# 基于 paramiko 的多远程节点的命令管理

import paramiko
import time
from itertools import zip_longest
import socket
import logging


class RemoteNode:
    def __init__(self, ip, port, user, pw, label='', run_params=None):
        self.ip = ip
        self.port = port
        self.user = user
        self.pw = pw
        self.label = label or f'{self.ip}:{self.port}'
        self.run_params = run_params or self.get_run_params()

    def clone(self, label_surfix='', overwrite_params=None):
        run_params = self.get_run_params()
        if overwrite_params:
            run_params.update(overwrite_params)
        return RemoteNode(ip=self.ip, port=self.port, user=self.user, pw=self.pw,
                          label=self.label+'; '+label_surfix, run_params=run_params)

    def get_run_params(self):
        return {'timeout': 60, 'loop': 1, 'interval': 1}

    def connect(self, verbose=False):
        remote_node = paramiko.SSHClient()
        remote_node.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_node.connect(self.ip, self.port, self.user, self.pw)
        if verbose:
            print(f'connect RemoteNode {self.ip}:{self.port} done')
        return remote_node

    def test(self):
        self.connect(verbose=True)

    def run(self, cmd):
        return self.run_once(cmd)

    def run_once(self, cmd):
        timeout = self.run_params['timeout']
        start_time = time.time()
        ret_status = 'done'
        print(f'>>> running `{cmd}` (on {self.label})')
        remote_node = self.connect()  # reconnect everytime
        try:
            stdin, stdout, stderr = remote_node.exec_command(cmd, timeout=timeout)
            for line in iter(stdout.readline, ''):  # 实时显示出 stdout, 不使用 iter 会导致执行完了一并显示
                print('    ' + line.rstrip('\n'))
            for line in iter(stderr.readline, ''):
                log.error('  x ' + line.rstrip('\n'))
                fail = 1
        except Exception as e:
            if type(e) == socket.timeout:
                print(f'!   socket.timeout on {self.ip} executing `{cmd}`')
                ret_status = 'timeout'
            else:
                raise e
        print(f'<<< {ret_status} in {(time.time() - start_time):.2f}s\n')
        remote_node.close()

    def __gt__(self, cmd):
        return self.run(cmd)

    def loop(self, count, interval):
        return self.clone(label_surfix='loop mode', overwrite_params={'count': count, 'interval': interval})

    def timeout(self, n):
        return self.clone(label_surfix=f'timeout {n}', overwrite_params={'timeout': n})

node = RemoteNode('10.2.xx.xx', '22', 'root', 'password', 'test 10.2.xx.xx')
node.test()