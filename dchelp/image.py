# -- coding:utf8 --
import os,sys,subprocess
import datetime

img_back_path = './back/image/'
def run_cmd(cmd):
	print('执行shell:'+cmd)
	p = subprocess.call(cmd, shell=True)

def read_images():
  dc_file = 'docker-compose.yml'
  imgs =[]
  with open(dc_file,'rt') as f:
    lines = f.readlines()

  for l in lines:
    l = l.strip()
    if 'image:' in l and l[0] !='#':
        imgs.append(l.split()[1])
  return list(set(imgs))

def do_image_pack():
  imgs = read_images()
  #打包镜像
  # docker save IMAGE > xxx.tar #  或者 docker save -o xxx.tar IMAGE
  # gizp xxx.tar.gz xxx.tar  # 可以压缩为原来为三分之一
  for i in imgs:
    print('打包镜像:'+i)
    result = os.popen("docker inspect -f '{{ .Created }}' "+i)
    res = result.read().strip()
    dt = datetime.datetime.strptime(res[:26],"%Y-%m-%dT%H:%M:%S.%f")
    time = dt.strftime("%Y%m%d%H%M%S")
    if not os.path.exists(img_back_path+ i.split("/")[-1]+"_"+time+'.tar.gz'):
      cmd = "docker save "+ i +" > " +img_back_path+ i.split("/")[-1]+"_"+time+'.tar'
      run_cmd(cmd)
      cmd = "gzip "+ img_back_path +i.split("/")[-1]+"_"+time+'.tar'
      run_cmd(cmd)
    else:
      print(i.split("/")[-1]+"_"+time+'.tar 已存在!')


def do_image_unpack():
  pass

def do_image_clear():
  """对进行进行清理
  """
  img_list = {}
  for root, dirs, files in os.walk(img_back_path):
    for file in files:
      name = "_".join(''.join(file.split('.')[:-2]).split('_')[:-1])
      time = file.split('.')[0].split('_')[-1]
      if name in img_list:
        if img_list[name] <= time:
          os.remove(path+name+"_"+img_list[name]+".tar.gz")
          img_list[name]=time
        else:
          os.remove(path+name+"_"+time+".tar.gz")
      else:
        img_list[name] = time

def do_image_upgrade():
  do_image_unpack()
  run_cmd('docker-compose up -d')