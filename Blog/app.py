from flask import Flask, render_template, request
from flask import escape
from flask import render_template_string
import os
import time


#===============================================================================  
def record(html_fileName, ip):
  #Notes:
  #  日志记录格式为：访问时间 | 访问者ip（实际为区域运营商的ip） | 访问的文件名 
  #  ip的长度固定为15位，不足的话就在右边补空格
  localtime = time.asctime( time.localtime(time.time()) )
  data_str = "%s | %s | %s\n"%(localtime, ip.ljust(15,' '), html_fileName)
  try:
    with open("./log/record.txt", "a") as file:
      file.write(data_str) 
  except:
    with open("./log/record.txt", "w") as file:
      file.write(data_str) 

#===============================================================================
app = Flask(__name__)

#===============================================================================
@app.route("/")
def index():
    return render_template('index/index.html')

#===============================================================================
@app.route('/<path:dummy>')
def all_subpage(dummy):
    #找到html的文件名
    for html_fileName in dummy.split('/'):
      if ('.html' in html_fileName): break

    #查看所有的静态html文件
    #-------------------------------------------
    #如果有，则返回相应静态网页，并记录时间，ip，以及网页
    #Notes: 这里记录的应该是访问者使用的网络运营商的ip
    for root, dirs, files in os.walk("templates"):
      for name in files:
        if (name == html_fileName): 
          path_and_file = os.path.join(root, name).replace('templates','')
          record(html_fileName,  request.remote_addr)
          return render_template(path_and_file)
    #-------------------------------------------
    #如果没有，则返回404页面
    return render_template_string('<center><h1> 欧欧 </h1><h2>啥也没有</h2>')
    
#=============================================================================== 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)#80, debug=True )
