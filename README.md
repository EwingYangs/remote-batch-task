# 远程批量分发命令，上传文件，下载文件

> 第一次写python项目，有不好的地方请多多指正交流，背景是由于遇到项目上线时，需要登录多台服务器重启对战服务器，webhook不合适，所以开发了一个小型的远程命令分发工具，在配置文件中配置服务器列表执行命令就可以把命令远程分发到每台服务器，并在日志中记录命令执行的结果

- 部署
        
        git clone https://github.com/EwingYangs/remote-batch-task
        cd remote-batch-task
        pip3 install -r requirements.txt
                
- 配置服务器文件在lib/config.py，本程序保证不会保存配置文件的服务器信息，放心使用

        Server = [
            {"host":"192.168.1.222", "port":"22", "username":"root", "password":"123456"},
            {"host":"192.168.10.10", "port":"22", "username":"root", "password":"123456"},
            {"host":"192.168.33.10", "port":"22", "username":"vagrant", "password":"vagrant"},
        ]

- 命令

      -h, --help            show this help message and exit
      -t TASK, --task=TASK  任务类型，cmd,getfile,putfile
      -c COMMAND, --command=COMMAND 命令，用引号，-c 'ls -al'
      -l LOCALFILE, --localFile=LOCALFILE 上传本地文件路径
      -r REMOTEFILE, --remoteFile=REMOTEFILE 远程文件路径，上传或下载文件都必须传
 
- demo

    - 重启所有服务器的swoole服务器
    
            python rbt.py -t cmd -c 'kill -USR2 `cat \tmp\socket.pid`'
            
    - 上传本地文件/usr/local/test.py到所有服务器的/tmp/test.py
    
            python rbt.py -t putfile -l '/usr/local/test.py' -r '/tmp/test.py'
            
    - 下载所有服务器文件/tmp/test.py到本地
    
            python rbt.py -t getfile -r '/tmp/test.py'
            
           
- 运行结果

        2019-02-01 12:10:38 batch.py[line:84] DEBUG 
        -------------------------------------
        任务id[CWVMenTrbsKcgOBP] 服务器[192.168.33.10]输出结果是:
        Filesystem              1K-blocks      Used Available Use% Mounted on
        /dev/mapper/centos-root   8775680   2471612   6304068  29% /
        devtmpfs                   228052         0    228052   0% /dev
        tmpfs                      234316         0    234316   0% /dev/shm
        tmpfs                      234316      4412    229904   2% /run
        tmpfs                      234316         0    234316   0% /sys/fs/cgroup
        /dev/sda1                  508588     84492    424096  17% /boot
        none                    244912536 126445848 118466688  52% /vagrant
        none                    244912536 126445848 118466688  52% /home/wwwroot
        
        -------------------------------------
                            
        2019-02-01 12:10:38 batch.py[line:84] DEBUG 
        -------------------------------------
        任务id[CWVMenTrbsKcgOBP] 服务器[192.168.1.222]输出结果是:
        Filesystem           1K-blocks    Used Available Use% Mounted on
        /dev/mapper/vg_localhost-lv_root
                               6795192 5456372    986976  85% /
        tmpfs                   379976       0    379976   0% /dev/shm
        /dev/sda1               487652   35907    426145   8% /boot
        
        -------------------------------------
                            
        2019-02-01 12:10:43 batch.py[line:84] DEBUG 
        -------------------------------------
        任务id[CWVMenTrbsKcgOBP] 服务器[192.168.10.10]输出结果是:
        timed out
        -------------------------------------
            
- 作为第三方库调用

        from remote-batch-task.lib.batch
        batch_client =  batch.BatchTask()
        # 命令分发，在日志中查看结果，没有返回
        batch_client.batch_cmd('ls -al') 
        # 文件上传
        batch_client.batch_putfile('/usr/local/test.py', '/tmp/test.py')
        # 文件下载
        batch_client.batch_getfile('/tmp/test.py')