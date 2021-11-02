# -- coding:utf8 --

"""
Usage:	docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Options:
      --config string      Location of client config files (default "/root/.docker")
  -c, --context string     Name of the context to use to connect to the daemon (overrides DOCKER_HOST env var
                           and default context set with "docker context use")
  -D, --debug              Enable debug mode
  -H, --host list          Daemon socket(s) to connect to
  -l, --log-level string   Set the logging level ("debug"|"info"|"warn"|"error"|"fatal") (default "info")
      --tls                Use TLS; implied by --tlsverify
      --tlscacert string   Trust certs signed only by this CA (default "/root/.docker/ca.pem")
      --tlscert string     Path to TLS certificate file (default "/root/.docker/cert.pem")
      --tlskey string      Path to TLS key file (default "/root/.docker/key.pem")
      --tlsverify          Use TLS and verify the remote
  -v, --version            Print version information and quit

Management Commands:
  builder     Manage builds
  config      Manage Docker configs
  container   Manage containers
  context     Manage contexts
  engine      Manage the docker engine
  image       Manage images
  network     Manage networks
  node        Manage Swarm nodes
  plugin      Manage plugins
  secret      Manage Docker secrets
  service     Manage services
  stack       Manage Docker stacks
  swarm       Manage Swarm
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  build       Build an image from a Dockerfile
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  images      List images
  import      Import the contents from a tarball to create a filesystem image
  info        Display system-wide information
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  login       Log in to a Docker registry
  logout      Log out from a Docker registry
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  ps          List containers
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  run         Run a command in a new container
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  search      Search the Docker Hub for images
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  version     Show the Docker version information
  wait        Block until one or more containers stop, then print their exit codes

Run 'docker COMMAND --help' for more information on a command.

docker volume

Usage:	docker volume COMMAND

Manage volumes

Commands:
  create      Create a volume
  inspect     Display detailed information on one or more volumes
  ls          List volumes
  prune       Remove all unused local volumes
  rm          Remove one or more volumes

Run 'docker volume COMMAND --help' for more information on a command.

"""
from . import image as image_util
import argparse
import os
import sys
import subprocess


def check_dir():
    dc_file = 'docker-compose.yml'
    if not os.path.exists(dc_file):
        print("执行目录错误：没有在当前目录发现docker-compose.yml！")
        exit(-1)
        
    # 检查并创建back目录d
    def check_back_dir(back_path):
        if not os.path.exists(back_path):
            run_cmd("mkdir -p  "+back_path)
    check_back_dir('./back/image')
    check_back_dir('./back/file')




def run_cmd(cmd):
    print('执行shell:'+cmd)
    p = subprocess.call(cmd, shell=True)


# def file_pack(dir_name):
#     # TODO 先检查文件夹是否存在
#     if os.path.exists(dir_name):
#       tar_file = './back/version/'+dir_name + '.tar.gz'
#       cmd = "tar -cvzf " + tar_file + " "+dir_name
#       run_cmd(cmd)
#     else:
#       print(dir_name+"不存在！")


# def file_unpack(dir_name):
#     # TODO 先检查文件是否存在
#     if os.path.exists('./back/version/'+dir_name+ '.tar.gz'):
#       tar_file = './back/version/'+dir_name + '.tar.gz'
#       cmd = "tar -xvzf " + tar_file
#       run_cmd(cmd)
#     else:
#       print("./back/version/" +dir_name + '.tar.gz'+ "不存在！")


def image(args):
    check_dir()
    # 镜像命令
    if args.pack:
        image_util.do_image_pack(args.bytes)
    if args.unpack:
        image_util.do_image_unpack()
    if args.clear:
        image_util.do_image_clear()
    if args.upgrade:
        image_util.do_image_upgrade()


# def init_data(args):
#     # init-data的命令
#     if args.pack:
#         check_dir()
#         cmd = "tar -zvcf back/version/init-data.tar.gz "
#         for root, dirs, files in os.walk('.'):
#             for file in files:
#                 if os.path.splitext(file)[1] not in ['.tar','.gz']:
#                     cmd += file + ' '
#             for dir in dirs:
#                 if dir not in ['run-data','back','temp']:
#                     cmd += dir + ' '
#             break
#         if cmd != "tar -zvcf back/version/init-data.tar.gz ":
#             run_cmd(cmd)
#         else:
#             print('没有文件需要打包！')
#     if args.unpack:
#         file_unpack('init-data')


default_dir_list = ['data','jar','conf']
def process_file(args):
    print(args)
    if args.restart:
        # TODO 先停止 'docker-compose down'，先记录当前状态，再决定是否恢复
        run_cmd('docker-compose down')
    if args.pack is not None:
        dir_list = args.pack if args.pack else default_dir_list
        for x in dir_list:
            # 检查x存在，并且是文件夹才继续，否则跳过
            if os.path.exists(x) and os.path.isdir(x):
                cmd = 'tar -zvcf back/file/' + x + '.tar.gz ' + x
                # 如果是conf文件夹,会自动包含docker-compose.xml文件
                if x == 'conf':
                    cmd = cmd + ' docker-compose.yml'
                run_cmd(cmd)
            else:
                print('文件夹不存在:' + x)


    if args.unpack is not None:
        dir_list = args.unpack if args.unpack else default_dir_list
        for x in dir_list:
            # 检查x存在，并且是文件夹才继续，否则跳过
            tar_file= 'back/file/' + x + '.tar.gz'
            if os.path.exists(tar_file) and os.path.isfile(tar_file):
                cmd = 'tar -zvxf ' + tar_file 
                run_cmd(cmd)
            else:
                print('文件不存在:' + tar_file)

    if args.restart:
        run_cmd('docker-compose up -d ')

# def run_data(args):
#     # check_dir()
#     # run-data的命令
#     if args.pack:
#         # TODO 先停止 'docker-compose down'，先记录当前状态，再决定是否恢复
#         run_cmd('docker-compose down')
#         file_pack('run-data')
#         run_cmd('docker-compose up -d ')
#     if args.unpack:
#         # TODO 先停止 'docker-compose down'，先记录当前状态，再决定是否恢复
#         result = os.popen("docker-compose ps")
#         if len(result.read().strip()) == 61:
#             file_unpack('run-data')
#         else:
#             run_cmd('docker-compose down -v')
#             file_unpack('run-data')
#             run_cmd('docker-compose up -d ')

def daemon(args):
    def check_status():
        if os.path.exists('.dc-help.lock'):
            with open('.dc-help.lock', 'rt') as f:
                lines = f.readlines()
                if lines:
                    result = os.popen("ps -ef|grep " + lines[0].replace('\n','') + " |grep -v grep").read().strip()
                    if result:
                        return True
        return False
    check_dir()
    if args.status:
        if check_status():
            print('running') 
        else:
            print('not running')
    if args.start:
        if check_status():
            print('自动升级服务已启动！')
        else:
            cmd = "nohup sh -c ' while true; do dc-help image --upgrade; sleep 60; done > dc-help.log' &"
            run_cmd(cmd)
            result = os.popen("ps -ef|grep while |grep -v grep").read().strip().split()[1]
            with open('.dc-help.lock','w') as f:
                f.write(result)
            print('自动升级服务启动成功！')

    if args.stop:
        if check_status():
            with open('.dc-help.lock', 'rt') as f:
                lines = f.readlines()
            run_cmd('kill -9 ' + lines[0])
            print("自动升级服务已停止！")
        else:
            print('未启动自动升级服务！')


def main_cli():
    # 创建解析对象
    parser = argparse.ArgumentParser(
        usage="dc-help COMMAND", description="docker-compose辅助工具,帮助管理镜像、版本文件")
    # 获取第一层子命令操作对象
    sub_parsers = parser.add_subparsers(title="COMMAND",)
    # 创建一个子命令
    p1 = sub_parsers.add_parser("image",
                                usage='dc-help COMMAND image [-h] (--pack | --unpack | --clear | --upgrade)',
                                help="管理docker-compose.yml中的镜像，打包、装载、清理、升级")
    p2 = sub_parsers.add_parser("file",
                                usage="dc-help file [-h] (--pack | --unpack)",
                                help="对文件夹进行压缩和解压缩,默认是conf、log之外的所有文件夹")
    # p3 = sub_parsers.add_parser("run-data",
    #                             usage="dc-help run-data [-h] (--pack | --unpack)",
    #                             help="run-data的压缩和解压缩2", add_help=True)
    p4 = sub_parsers.add_parser("daemon",
                                usage="dc-help daemon [-h] (--status | --start | --stop)",
                                help="daemon的状态、启动和停止", add_help=True)
    # 互斥，且至少需要一个参数
    p1.add_argument('-b', '--bytes', help='设置分包大小', default= '', nargs='?')
    group = p1.add_mutually_exclusive_group(required=True)
    group.add_argument('--pack', action='store_true', help="对镜像进行自动打包")
    group.add_argument('--unpack', action='store_true', help="对镜像进行自动装载")
    group.add_argument('--clear', action='store_true', help="对镜像文件进行清理")
    group.add_argument('--upgrade', action='store_true',
                       help="对镜像文件进行自动装载，然后升级")
    p1.set_defaults(func=image)  # 将函数 与子解析器绑定

    group = p2.add_mutually_exclusive_group(required=True)
    group.add_argument('--pack', type=str, nargs='*', help="对文件夹进行自动打包")
    group.add_argument('--unpack', type=str, nargs='*',
                       help="对文件夹进行自动解包")
    p2.add_argument('--restart', action='store_true',help="是否重启服务,默认不重启")
    p2.set_defaults(func=process_file)   # 将函数 与子解析器绑定

    # group = p3.add_mutually_exclusive_group(required=True)
    # group.add_argument('--pack', action='store_true', help="对run-data进行自动打包")
    # group.add_argument('--unpack', action='store_true', help="对run-data进行自动解包")
    # p3.set_defaults(func=run_data)  # 将函数 与子解析器绑定

    group = p4.add_mutually_exclusive_group(required=True)
    group.add_argument('--status', action='store_true', help="查看自动升级服务的状态，running 或 not running")
    group.add_argument('--start', action='store_true', help="启动自动升级服务")
    group.add_argument('--stop', action='store_true', help="停止自动升级服务")
    p4.set_defaults(func=daemon)  # 将函数 与子解析器绑定

    import sys
    # 先检查目录

    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main_cli()
