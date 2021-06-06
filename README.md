## okta-cmd

### Introduction
docker-compose 辅助脚本

### 安装
```bash
$ git clone https://github.com/perfectstorm88/dc-help
# init okta
$ python setup.py install
# 进入一个docker-compose.yml所在目录，执行对涉及的镜像自动打包
$ dc-help image --pack 
# add user file to group
```
### 
在docker-compose.yml所在目录，执行`dc-help -h`
```
usage: dc-help COMMAND

docker-compose辅助工具,帮助管理镜像、版本文件

optional arguments:
  -h, --help            show this help message and exit

COMMAND:
  {image,init-data,run-data}
    image               管理docker-compose.yml中的镜像，打包、装载
                        、清理、升级
    init-data           init-data的压缩和解压缩
    run-data            run-data的压缩和解压缩2
```

其中`dc-help image -h`

```
usage: dc-help COMMAND image [-h] (--pack | --unpack | --clear | --upgrade)

optional arguments:
  -h, --help  show this help message and exit
  --pack      对镜像进行自动打包
  --unpack    对镜像进行自动装载
  --clear     对镜像文件进行清理
  --upgrade   对镜像文件进行自动装载，然后升级`
```

### Advanced Features
### Features
*  [x] add group
*  [x] add user file to group
*  [x] copy group to other group
*  [x] group list
*  [x] user list
*  [x] download user list file
*  [x] download group list file

### TODO
*  [ ] Delete matching users
*  [ ] Delete matching groups

### Notes
* If you have new features or questions, you can write issues