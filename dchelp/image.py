# -- coding:utf8 --
import os,sys,subprocess
import datetime

img_back_path = './back/image/'
temp_path = './temp/'
def run_cmd(cmd):
  print('执行shell:'+cmd)
  p = subprocess.call(cmd, shell=True)
  return p

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

def do_image_pack(split_size):
  #打包镜像
  # docker save IMAGE > xxx.tar #  或者 docker save -o xxx.tar IMAGE
  # gizp xxx.tar.gz xxx.tar  # 可以压缩为原来为三分之一
  imgs = read_images()
  for i in imgs:
    print('打包镜像:'+i)
    result = os.popen("docker inspect -f '{{ .Created }}' "+i)
    res = result.read().strip()
    if not res:
      print(i+'镜像不存在！')
      continue
    dt = datetime.datetime.strptime(res[:26],"%Y-%m-%dT%H:%M:%S.%f")+datetime.timedelta(hours=8)
    time = dt.strftime("%Y%m%d%H%M%S")
    if not os.path.exists(img_back_path+ i.split("/")[-1].replace(":","___")+"_"+time+'.tar.gz') and not os.path.exists(img_back_path+ i.split("/")[-1].replace(":","___")+"_"+time+'.tar.gz.part-00'):
      cmd = "docker save "+ i +" > " +img_back_path+ i.split("/")[-1].replace(":","___")+"_"+time+'.tar'
      run_cmd(cmd)
      cmd = "gzip "+ img_back_path +i.split("/")[-1].replace(":","___")+"_"+time+'.tar'
      run_cmd(cmd)
      if split_size:
        cmd = "split -b "+split_size + ' -d '+ img_back_path +i.split("/")[-1].replace(":","___")+"_"+time+'.tar.gz' + ' ' + img_back_path +i.split("/")[-1].replace(":","___")+"_"+time+'.tar.gz.part-'
        run_cmd(cmd)
    else:
      print(i.split("/")[-1]+"_"+time+'.tar 已存在!')


def do_image_unpack():
  imgs = read_images()
  unpack_list = {}
  error = 0
  if os.path.exists(img_back_path):
    for root, dirs, files in os.walk(img_back_path):  
      for file in files:
        if os.path.splitext(file)[1] == '.part-00':
          file1 = os.path.splitext(file)[0]
          if os.path.splitext(file1)[1] == '.gz':
            file_name = '_'.join(os.path.splitext(file1)[0].split('_')[:-1]).replace("___", ":")
            file_time = os.path.splitext(file1)[0].split('_')[-1].split('.')[0]
            if file_name and file_time.isdigit():
              if file_name in unpack_list:
                if int(file_time) > int(unpack_list[file_name][0]):
                  unpack_list[file_name] = [file_time,1]#0表示该镜像为完整镜像，1表示为分包文件
              else:
                unpack_list[file_name] = [file_time,1]
        elif os.path.splitext(file)[1] == '.gz':
          file_name = '_'.join(os.path.splitext(file)[0].split('_')[:-1]).replace("___",":")
          file_time = os.path.splitext(file)[0].split('_')[-1].split('.')[0]
          if file_name and file_time.isdigit():
            if file_name in unpack_list:
              if int(file_time) > int(unpack_list[file_name][0]):
                unpack_list[file_name] = [file_time,0]
            else:
              unpack_list[file_name] = [file_time,0]
  else:
    print("back/image文件夹不存在！")
    error = 1
  for image in imgs:
    pair_name = image.split("/")[-1]
    if pair_name in unpack_list:
      result = os.popen("docker inspect -f '{{ .Created }}' "+image)
      res = result.read().strip()
      if res:
        dt = datetime.datetime.strptime(res[:26],"%Y-%m-%dT%H:%M:%S.%f")+datetime.timedelta(hours=8)
        time = dt.strftime("%Y%m%d%H%M%S")
        if int(unpack_list[pair_name][0]) > int(time):
          if not os.path.exists(temp_path):
            run_cmd("mkdir "+temp_path)
          if unpack_list[pair_name][1]:#分包文件，需合并
            cmd = 'cat '+ img_back_path + pair_name.replace(":","___") + "_" + unpack_list[pair_name][0] + '.tar.gz.part-* > ' + temp_path +pair_name + "_" + unpack_list[pair_name][0] + ".tar.gz"
            run_cmd(cmd)
            r = run_cmd("gzip -dc "+ temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar.gz > "+ temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar")
            if r:
              print(image+'文件异常！')
              error = 1
              break
            p = "docker load < " + temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar"
            r = run_cmd(p)
            if r:
              print(image+'镜像加载异常！')
              error =1
              break
          else:
            r = run_cmd("gzip -dc " + img_back_path + pair_name.replace(":", "___") + "_" + unpack_list[pair_name][
              0] + ".tar.gz > " + temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar")
            if r:
              print(image + '文件异常！')
              error = 1
              break
            p = "docker load < " + temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar"
            r = run_cmd(p)
            if r:
              print(image + '镜像加载异常！')
              error = 1
              break
        else:
          print(image +"镜像已为最新!")
      else:
        if not os.path.exists(temp_path):
          run_cmd("mkdir "+temp_path)
        if unpack_list[pair_name][1]:  # 分包文件，需合并
          cmd = 'cat ' + img_back_path + pair_name.replace(":", "___") + "_" + unpack_list[pair_name][0] + '.tar.gz.part-* > ' + temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar.gz"
          run_cmd(cmd)
          r = run_cmd("gzip -dc "+ temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar.gz" +" > "+ temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar")
          if r:
            print(image + '文件异常！')
            error = 1
            break
          p = "docker load < " + temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar"
          r = run_cmd(p)
          if r:
            print(image + '镜像加载异常！')
            error = 1
            break
        else:
          r = run_cmd("gzip -dc " + img_back_path + pair_name.replace(":", "___") + "_" + unpack_list[pair_name][
            0] + ".tar.gz" + " > " + temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar")
          if r:
            print(image + '文件异常！')
            error = 1
            break
          p = "docker load < " + temp_path + pair_name + "_" + unpack_list[pair_name][0] + ".tar"
          r = run_cmd(p)
          if r:
            print(image + '镜像加载异常！')
            error = 1
            break
  if os.path.exists(temp_path):
    p = "rm -rf "+temp_path
    run_cmd(p)
  else:
    error = 1#不存在temp文件夹表示所有镜像都为最新，返回1让upgrade不执行up操作
  return error
def do_image_clear():
  """对进行进行清理
  """
  imgs = read_images()
  imgs1=[]
  for i in imgs:
    imgs1.append(i.split('/')[-1].replace(':','___'))
  img_list = {}
  for root, dirs, files in os.walk(img_back_path):
    for file in files:
      if os.path.splitext(file)[1] == '.gz':
        name = "_".join('.'.join(file.split('.')[:-2]).split('_')[:-1])
        time = '.'.join(file.split('.')[:-2]).split('_')[-1]
        if not name or not time.isdigit():
          os.remove(img_back_path + file)
          print("删除" + file)
          continue
        if name not in imgs1:
          os.remove(img_back_path + name + "_" + time + ".tar.gz")
          print("删除" + name + "_" + time + ".tar.gz")
          continue
        if name in img_list:
          if img_list[name] <= time:
            os.remove(img_back_path+name+"_"+img_list[name]+".tar.gz")
            print("删除"+name+"_"+img_list[name]+".tar.gz")
            img_list[name]=time
          else:
            os.remove(img_back_path+name+"_"+time+".tar.gz")
            print("删除"+name+"_"+time+".tar.gz")
        else:
          img_list[name] = time
      else:
        os.remove(img_back_path + file)
        print("删除" + file)

def do_image_upgrade():
  error = do_image_unpack()
  if error == 0:
    run_cmd('docker-compose up -d')