import optparse
from lib import RBT

# 允许执行的task命令
task_type_list = ['cmd', 'getfile', 'putfile']

# 主程序入口
def run():
    op = optparse.OptionParser()
    op.add_option("-t", "--task", dest="task")
    op.add_option("-c", "--command", dest="command")
    op.add_option("-l", "--localFile", dest="localFile")
    op.add_option("-r", "--remoteFile", dest="remoteFile")
    options, args = op.parse_args()

    task_type = options.task
    if task_type not in task_type_list:
        print("invalid task params, please input %s" %(",".join(task_type_list)))
        exit(0)

    # 反射执行类的方法
    if hasattr(RBT.RBT, task_type):
        func = getattr(RBT.RBT, task_type)
        rbt_obj = RBT.RBT()
        func(rbt_obj, options=options)
    else:
        print("has no %s method, please input %s" % (task_type, ",".join(task_type_list)))
        exit(0)