
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210607195419420.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpY2hhbmd6aGVuMjAwOA==,size_16,color_FFFFFF,t_70)

@[TOC]

参考博文：

[docker部署规范-目录结构与辅助工具](https://blog.csdn.net/lichangzhen2008/article/details/117672233?spm=1001.2014.3001.5501)

本规范根据多个项目实践总结，通过**目录结构规范化，结合辅助工具**，可以降低在多节点、新环境部署中的重复工作与沟通工作量，大幅提供部署效率。

## 规范部署目录结构

目录结构的规划基于下面几点考虑：

- 一个主机上可以部署多套系统
- 一个系统应该是”自洽“的，具有完整的逻辑性，系统涉及的所有文件是自包含的
- 目录结果尽量简单，便于管理(不再执行dockcer-compose up --build命令)，本地的配置修改通过volumes文件夹或文件挂载的方式进行容器内文件覆盖完成

目录结构如下所示:

- [产品]-deplopy:
  - **docker-compose.yml**: 主文件
  - **conf**： 配置文件，如nginx配置，mysql配置文件等
    - `web/nginx.conf`: nginx的配置文件夹，例如路由配置，安全设置等。
    - `web/ca/` :nginx的证书文件目录。
    - `mysql/` :msql的配置文件等
  - **data**: 运行过程中的数据，如数据库存储目录，程序的临时文件目录
    - `mysql/` :msql的数据库文件目录
    - `mongo/` :mongodb的数据库文件目录
  - **jar**: 包含服务用的jar文件、或者其他格式的代码打包文件等
  - **log**: 程序日志目标
  - **back**: 程序备份目录

## 辅助工具解决
辅助工具参考：[github代码 dc-help](https://github.com/perfectstorm88/dc-help)
工具安装

```bash
git clone https://github.com/perfectstorm88/dc-help
cd dc-help
python setup.py install
```

在docker-compose.yml所在目录，执行`dc-help -h`

```txt
usage: dc-help COMMAND

docker-compose辅助工具,帮助管理镜像、版本文件

optional arguments:
  -h, --help           show this help message and exit

COMMAND:
  {image,file,daemon}
    image              管理docker-compose.yml中的镜像，打包、装载、清理、升级
    file               对文件夹进行压缩和解压缩,默认是conf、data、jar等文件夹
    daemon             daemon的状态、启动和停止
```

其中`dc-help image -h`

```log
usage: dc-help COMMAND image [-h] (--pack | --unpack | --clear | --upgrade)

optional arguments:
  -h, --help  show this help message and exit
  --pack      对镜像进行自动打包
  --unpack    对镜像进行自动装载
  --clear     对镜像文件进行清理
  --upgrade   对镜像文件进行自动装载，然后升级`
```

## 功能介绍

*  [x] `dc-help image --pack`：对项目的镜像进行自动打包
*  [x] `dc-help image --unpack`：对项目的镜像进行自动装载
*  [x] `dc-help image --clear`：对项目的镜像进行清理
*  [x] `dc-help image --upgrade`：扫描备份目录，判断是否有镜像更新，进行自动装载，更新集群服务
*  [x] `dc-help file --pack`：对项目的配置和数据文件进行自动打包压缩
*  [x] `dc-help file --unpack`：对项目的配置和数据文件进行自动解压缩
*  [x] `dc-help daemon --status`：查看自动升级服务的状态，running 或 not running
*  [x] `dc-help daemon --start`：启动自动升级服务
*  [x] `dc-help daemon --stop`：停止自动升级服务

# 安装部署
## pip安装
```
pip install dc-help
```
## 源代码安装
```
git clone https://github.com/perfectstorm88/dc-help.git
cd dc-help
python setup.py install 
```
## 离线安装(docker,推荐)
如果部署在客户内网，离线建议采用docker方式，在容器内执行docker命令

1. 首先下载源代码，构建docker镜像：
```bash
git clone https://github.com/perfectstorm88/dc-help.git
cd dc-help
docker build -t dc-help . # 构建docker
docker save dc-help >dc-help-docker-image.tar
gzip dc-help-docker-image.tar
```

2. 在内网主机，把dc-help-docker-image.tar.gz上传到部署主机,还原镜像：
```bash
docker  load -i dc-help-docker-image.tar
```
3. 配置alias,在~/.bashrc中增加alias：（通过 vim ~/.bashrc编辑后，执行 source ~/.bashrc后生效）
```bash
alias dc-help='docker run --rm -t -u root  -v $(which docker):/usr/bin/docker  -v $(which docker-compose):/usr/bin/docker-compose  -v /var/run/docker.sock:/var/run/docker.sock  -v /usr/lib64/libltdl.so.7:/usr/lib/x86_64-linux-gnu/libltdl.so.7 -v $(pwd):$(pwd)  -w $(pwd) dc-help dc-help'
```


## 离线源码安装dc-help工具(centos7)
● (安装setuptools（若没有的话需要安装，视centos的版本，有的环境不需要这一步）
https://pypi.org/project/setuptools/36.5.0/
下载setuptools-36.5.0.tar.gz
不能下过高版本，因为python2语法不支持

```bash
tar -zxvf setuptools-36.5.0.tar.gz 
#若外网下载zip格式，则 unzip setuptools-36.5.0.zip
cd setuptools-36.5.0
python setup.py install
```
源代码安装步骤同上

## 	离线源码安装dc-help工具(centos8)
centos8已经默认不自带python版本，需要先安装python2，参见[VirtualBox CentOS8 挂载iso镜像](https://juejin.cn/post/6937962931212517406)

源代码安装步骤同上

## 参考

- [How to get exact date for docker images?如何抽取镜像时间](https://stackoverflow.com/questions/32705176/how-to-get-exact-date-for-docker-images)
- [Declare default environment variables in file 通过文件声明默认环境变量](https://docs.docker.com/compose/env-file/)
- [COMPOSE_PROJECT_NAME](https://docs.docker.com/compose/reference/envvars/#compose_project_name)
- [如何从容器内部执行宿主机的docker命令](https://www.jianshu.com/p/8b72eece7df8)



