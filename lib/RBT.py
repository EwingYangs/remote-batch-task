from lib import batch

class RBT:
    def __init__(self, batch_client):
        self.batch_client = batch_client
        pass

    def cmd(self, options):
        if not options.command:
            print("command is not null, please input -c ..")
            exit(0)

        # 分发远程命令
        self.batch_client.batch_cmd(options.command)

    def putfile(self, options):
        if not options.localFile:
            print("localFile is not null, please input -l ..")
            exit(0)
        if not options.remoteFile:
            print("remoteFile is not null, please input -r ..")
            exit(0)

        # 远程批量上传
        self.batch_client.batch_putfile(options.localFile, options.remoteFile)

    def getfile(self, options):
        if not options.remoteFile:
            print("remoteFile is not null, please input -r ..")
            exit(0)

        # 远程批量下载
        self.batch_client.batch_getfile(options.remoteFile)
