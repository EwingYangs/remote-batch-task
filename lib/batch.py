from concurrent.futures import ThreadPoolExecutor
from . import config
import paramiko
import logging
import os
import random
import string

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = config.AppLog,
    filemode = 'a'
)

class BatchTask:
    def __init__(self):
        pass

    def generate_task_id(self):
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        return ran_str

    def batch_cmd(self, cmd):
        if not cmd:
            return
        self.cmd = cmd
        self.batch_with_thred(type='cmd')

    def batch_putfile(self, local_file, remote_file):
        if not local_file or not remote_file:
            return
        self.local_file = local_file
        self.remote_file = remote_file
        self.batch_with_thred(type='putfile')

    def batch_getfile(self, remote_file):
        if not remote_file:
            return
        self.remote_file = remote_file
        self.batch_with_thred(type='getfile')

    def batch_with_thred(self, type=''):
        pool = ThreadPoolExecutor(config.ThreadPoolNum)
        self.task_id = self.generate_task_id()
        print("task %s running.." %(self.task_id))
        if type == 'cmd':
            server_list = config.Server
            for server in server_list:
                pool.submit(self.cmd_task, server)


    def cmd_task(self, server):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                hostname = server["host"],
                port = server["port"],
                username = server["username"],
                password = server["password"],
                timeout = 5
            )
            stdin, stdout, stderr = ssh.exec_command(self.cmd)
            stdout_res = stdout.read()
            stderr_res = stderr.read()

            ssh_res = (stdout_res + stderr_res).decode('utf-8')

        except Exception as e:
            ssh_res = e

        result = """
-------------------------------------
任务id[%s] 服务器[%s]输出结果是:
%s
-------------------------------------
                    """ % (self.task_id, server["host"], ssh_res)

        print(result)

        if config.LogApp:
            logging.debug(result)

        ssh.close()

