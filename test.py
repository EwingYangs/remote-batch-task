import paramiko

server = {"host":"192.168.1.222", "port":"22", "username":"root", "password":"123456"}
t = paramiko.Transport((server["host"], int(server["port"])))
t.connect(
    username = server["username"],
    password = server["password"],
)
sftp = paramiko.SFTPClient.from_transport(t)
sftp.put('/usr/local/var/www/python/remote-batch-task/app.log', '~/app.log')

