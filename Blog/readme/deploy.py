#!/home/yxk/Software/anaconda3/lib/python3.8
import web_tools

#===============================================================================
#----------------------------------------------------
#询问是否添加md文件
print("是否添加新文件(default:no)？(yes|no)")
input_str = input()
if input_str == "yes": web_tools.add_markdownFile()

#----------------------------------------------------
#查看md文件是否被修改，如果有，则更新对应的html文件
try:
  with open("md_record.txt", "r") as read_file:
    md_record = read_file.readlines()
except: md_record=[]

for pathAndFile_of_md in md_record:
  pathAndFile_of_md = pathAndFile_of_md.rstrip('\n')
  if (web_tools.check_ifUpdate_html(pathAndFile_of_md) == True ):
    #1. 用typora打开md文件，输出html文件
    web_tools.convert_md_html(pathAndFile_of_md)
    #2. 对html文件做一些必要处理
    web_tools.html_modify(pathAndFile_of_md)
    #3. 移动html文件并将其mtime改为md文件的mtime
    web_tools.mv_and_mtime(pathAndFile_of_md)
    
#----------------------------------------------------
#部署到服务器端
print("是否部署(default:yes)？(yes|no)")
input_str = input()
if input_str != "no": web_tools.web_deploy()
