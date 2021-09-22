import os
from pykeyboard import PyKeyboard
import time
import re
import base64
from   PIL import Image
import multiprocessing
import getpass

#===============================================================================
#函数说明：根据md文件的路径，得到html文件的目标位置。文件中其他函数基本都会调用该函数，获取
#html文件的位置
#变量说明：
#  md_fileName: markdown文件的文件名
#  md_path：markdown文件的路径（相对本文件）
def get_html_pathAndFile(pathAndFile_of_md):
  md_fileName   = pathAndFile_of_md.split('/')[-1]
  md_path       = pathAndFile_of_md.replace(md_fileName,'')  
  html_fileName = md_fileName.replace('.md', '.html')
  #html文件放在templates文件夹中
  #去掉路径中的'../'和'./'，保证html文件在templates文件夹中
  html_path     = '../templates/'+ md_path.replace('../','').replace('./','')
  return [md_fileName, md_path, html_fileName, html_path]
  
#===============================================================================
#向md_record.txt文件中添加新的md文件
def add_markdownFile():
  #读取md_record.txt文件，如果读取失败，则初始化为空list 
  try:
    with open("md_record.txt", "r") as read_file:
      md_record = read_file.readlines()
  except: md_record=[]
  
  #询问，输入添加的markdown文件的所在的文件夹
  #如果输入为空，则结束添加
  while True:
    print("请输入md文件所在文件夹（相对路径，回车退出）：")
    input_str = input()
    
    if len(input_str)==0: break
    try: 
      files = os.listdir(input_str)
      for file in files:
        path_and_file = input_str+'/'+file+'\n'
        if   path_and_file in md_record: continue
        elif file.endswith('.md'): 
          print('    Add file: %s'%file)          
          md_record.append(path_and_file)
    except: print("No such dir!")
    
  #保存md_record的内容
  outputFile = open('md_record.txt', 'w')
  for line in md_record:
      outputFile.write(line)
  outputFile.close()
    
  print('new_markdownFile: DONE!');
  print('---------------------------\n')

#===============================================================================
#检查html文件和markdown文件的mtime，如果两者不一样，则返回True，要求更新html文件
def check_ifUpdate_html(pathAndFile_of_md):
  #获取html文件的文件名以及路径
  [_, _, html_fileName, html_path] = get_html_pathAndFile(pathAndFile_of_md)
  pathAndFile_of_html = html_path+html_fileName
    
  #检查其mtime
  #有可能不存在html文件，所以使用try结构
  try:
    md_mtime   = os.path.getmtime(pathAndFile_of_md)
    html_mtime = os.path.getmtime(pathAndFile_of_html)
    if (abs(html_mtime - md_mtime)>1): return True     
    else: return False
  except: return True
  
#===============================================================================
#使用typora将markdown转换为html文件
def convert_md_html(pathAndFile_of_md):
  #获取md、html文件的文件名以及路径
  [md_fileName, md_path, _, _] = get_html_pathAndFile(pathAndFile_of_md)
  
  #用typora打开文件，并等待4s
  for file in os.listdir(md_path):
    if '.html' in file: 
      os.system('cd %s; rm *.html &'%md_path);time.sleep(0.1) 
      #保证md文件夹中没有html文件，然后打开typora，并输入html文件
  os.system('cd %s; typora %s &'%(md_path, md_fileName));time.sleep(4)

  #模拟键盘按键，输出html文件
  k = PyKeyboard()
  k.tap_key(k.alt_key);time.sleep(0.2)
  k.tap_key(k.enter_key);time.sleep(0.2)
  k.tap_key('e');time.sleep(0.2) 
  k.tap_key(k.enter_key);time.sleep(0.2)
  k.tap_key('h');time.sleep(0.2)
  k.tap_key(k.enter_key);time.sleep(0.3)
  k.tap_key(k.enter_key);time.sleep(1) 

  #ctrl+w 关闭typora
  k.press_key(k.control_key);time.sleep(0.1)
  k.tap_key('w');time.sleep(0.1)
  k.release_key(k.control_key)

#===============================================================================  
#在md文件夹中，对html文件进行处理
def html_modify(pathAndFile_of_md):
    #获取md、html文件的文件名以及路径
    [_, md_path, html_fileName, _] = get_html_pathAndFile(pathAndFile_of_md)
    
    #读取html文件
    inputFile = open(md_path+html_fileName, 'r')
    line_vec   = inputFile.readlines()
    inputFile.close()
    #----------------------------------------------------------------
    #1. 为页面添加home建，主页不添加
    if (not "index.html" in html_fileName):
      home_button = "<p><a href='/'><span>Home</span></a></p>"
      for n_line in range( len(line_vec)):
          line    = line_vec[n_line]      
          if ("<body class='typora-export'>" in line):
            break
      line_vec.insert(n_line, home_button)

    
    #----------------------------------------------------------------
    #2.修改title为head1，而不是与文件名相同
    for n_line in range( len(line_vec)):
        line    = line_vec[n_line]      
        h1_name = re.findall(r'<span>(.+?)</span></h1>',line)
        if (len(h1_name) > 0 ):
            h1_name = h1_name[0]
            break
    for n_line in range( len(line_vec)):
        line  = line_vec[n_line]      
        title = re.findall(r'<title>(.+?)</title>',line)
        if (len(title) > 0 ):
            titleStr_old = '<title>%s</title>'%title[0]
            titleStr_new = '<title>%s</title>'%h1_name
            line  = line.replace(titleStr_old, titleStr_new,1);
            #修改line_vec
            line_vec[n_line] = line
            break
            
            
    
    #逐行判断是否需要修改
    for n_line in range( len(line_vec)):
        line = line_vec[n_line]      

        #----------------------------------------------------------------
        #3. 删除第5行的连接     
        link_str = "<link href='https://fonts.loli.net/css?family=Open+Sans:400italic,700italic,700,400&subset=latin,latin-ext' rel='stylesheet' type='text/css' />"
        if (link_str in line): 
            line=line.replace(link_str, "",1)
        
        #----------------------------------------------------------------
        #4. 修改根目录
        link_str = 'http://www.yxkblog.com'
        if (link_str in line): 
            line=line.replace(link_str, ""); #全部删除

        #----------------------------------------------------------------
        #5. 修改其中的图片格式
        output = re.findall(r'<img src=(.+?)>',line)
        for figure_str in output:
            #找到图片文件名和缩放尺寸
            figure_name = re.findall(r'"(.+?)" style',figure_str)
            zoom_ratio  = re.findall(r'zoom:(.+?)%;',figure_str)
            
            #判断是否找到正确的文件名和缩放尺寸
            if (len(figure_name) != 1 or len(zoom_ratio) != 1 ): continue
            pathAndFile_of_fig = md_path+figure_name[0]
            
            #如果上面运行正确，则进行下面修改图片格式的代码    
            #----------------------------------------------------------------
            #a. 修改缩放格式
            im         = Image.open(pathAndFile_of_fig) #返回一个Image对象
            zoom_ratio = float(zoom_ratio[0])
            #得到缩放后的width &height
            width  = im.size[0]
            height = im.size[1]
            width  = width  * zoom_ratio/100
            height = height * zoom_ratio/100     
            #修改缩放格式
            zoomStr_old   = 'style'+re.findall(r'" style(.+?)%;',figure_str)[0]+'%;"'
            zoomStr_new   = 'width="%.2f" height="%.2f"'%(width,height)
            figureStr_new = figure_str.replace(zoomStr_old,zoomStr_new,1)
            
            #----------------------------------------------------------------
            #b. 将图片src改为base64的数据，进行封装
            #图片修改为base64的格式
            with open(pathAndFile_of_fig, 'rb') as f:
               image_base64 = str(base64.b64encode(f.read()))[2:]
            src_new       = "'data:img/png;base64, " + image_base64
            src_old       = '"' + figure_name[0] + '"'
            figureStr_new = figureStr_new.replace(src_old, src_new,1)

            #----------------------------------------------------------------
            #c. 将前面的修改写进line数据中
            line=line.replace(figure_str, figureStr_new, 1)
            
        #修改line_vec
        line_vec[n_line] = line

    ##将修改后的数据覆盖html文件
    outputFile = open(md_path+html_fileName, 'w')
    for line in line_vec:
        outputFile.write(line)
    outputFile.close()

#===============================================================================
#将经过处理的html移动到相应文件夹，并修改mtime
def mv_and_mtime(pathAndFile_of_md):
  #获取md、html文件的文件名以及路径
  [md_fileName, md_path, html_fileName, html_path] = \
      get_html_pathAndFile(pathAndFile_of_md)
    
  #将html文件移动到相应位置
  if (os.path.exists(html_path) == False): os.makedirs(html_path)
  os.system('mv %s %s'%(md_path+html_fileName,html_path+html_fileName))
  
  #根据md文件的mtime，修改html的mtime
  md_mtime = os.path.getmtime(md_path+md_fileName)
  os.utime(html_path+html_fileName,(0,md_mtime)) #第2个参数为访问时间，不重要，设置为0
  
#===============================================================================
#将本地的项目发送到服务器端
#过程中涉及到三次密码输入，所以使用PyKeyboard()&子进程来模拟密码的输入
def web_deploy():
  #子进程用于模拟键盘，输入密码
  def enter_passwd(passwd):
    time.sleep(2)  #2s，等待执行shell命令
    k = PyKeyboard()
    k.type_string('%s'%passwd);time.sleep(0.1)
    k.tap_key(k.enter_key);time.sleep(0.1)
    k.tap_key(k.enter_key);time.sleep(0.3)


  #输入密码  
  passwd = getpass.getpass("Server Password:")  

  #让服务器端的记录文件复制到本地，并覆盖旧日志文件
  mp1 = multiprocessing.Process(target=enter_passwd,args=(passwd,))
  mp1.start()
  os.system('scp  ubuntu@101.32.204.72:Blog/Blog/log/record.txt ../log')

  #将新的Blog项目发送到服务器端
  mp1 = multiprocessing.Process(target=enter_passwd,args=(passwd,))
  mp1.start()
  #os.system('scp -n -r ../../Blog  ubuntu@101.32.204.72:Blog')
  os.system('rsync -avzu --progress ../../Blog  ubuntu@101.32.204.72:Blog')

  #重启supervisor
  cmd_str = 'ssh ubuntu@101.32.204.72 -tt <<EOT \n\
    sudo su \n\
    supervisorctl shutdown \n\
    supervisord   -c /etc/supervisor/supervisord.conf \n\
    supervisorctl -c /etc/supervisor/supervisord.conf status Blog \n\
	  exit \n\
	  exit \n\
  EOT'
  mp1 = multiprocessing.Process(target=enter_passwd,args=(passwd,))
  mp1.start()
  os.system(cmd_str)
