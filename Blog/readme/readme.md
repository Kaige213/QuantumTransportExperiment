# 网页部署



## 一、为什么用这种方式

我一直有用Typora写工作总结的习惯，Typora是目前市面上最强最优雅的markdown编辑器。我一般是先写工作总结，然后考虑是否可以发布。所以不想再重写一次博客，用来发布到网上，于是写了deploy.py和web_tool.py，两个工具用来实现markdown=>html=>网页部署，整个过程的自动化。这样，博客建设就不需要花费更多的精力。



## 二、添加新博文的步骤：

运行webPage_produce.py文件，执行下面操作：

- 询问是否添加新的markdown文件，新md文件的路径和文件名被存放到md_record.txt中；
- 根据md_record.txt文件，检查是否将md文件转换为html文件；
- 对html文件进行如下处理：

   - 为页面添加home建，指向我的博客首页
   - 修改title为head1，而不是与文件名相同
   - 删除第5行的链接，该链接不影响网页加载效果，但由于网络问题，有时会影响加载时间
   - 删除文件中的根目录：`http://www.yxkblog.com`，flask会自动补全，在本地和云端，根目录是不一样的
   - 修改其中的图片缩放格式，typora中图片缩放格式为`style="zoom:80%;"`，转成html文件，在chrome中能正常显示，但firefox中缩放失败。所以需要根据图片尺寸，改为`width="100" height="100"`的缩放格式
   - 图片src改为base64的数据，直接放到html文件中，封装起来，就不需要额外建文件夹来放图片
- 将网页项目发送到服务器，并重启supervisor，完成部署；



**Notes:**

- 执行webPage_produce.py时，由于程序中有些操作是通过模拟键盘输入来实现的，所以除了必要的输入，其余时间都不能接触键盘和鼠标，

- 网页部署的前后，最好使用git status检查md文件是否被修改





## 三、补充说明

- 平时使用Typora时，使用的字体大小是22px，但输出网页文件时，需要改为20px

- 加载静态网页时，只根据html的文件名判断，不考虑文件路径

- 服务器重置后，大致的设置步骤：

  Ref：[flask的web部署云服务器——史上最详细小白教程没有之一](https://blog.csdn.net/qq_40831778/article/details/104639076)

  - 进入root，`vi /etc/ssh/sshd_config`，添加
    `ClientAliveInterval 30`
    `ClientAliveCountMax 300`

  - `sudo apt-get install python3-venv`

  - `python3 -m venv Env` #创建虚拟环境

  - pip安装flask、gunicorn

  - `sudo apt-get install supervisor`

  - ` echo_supervisord_conf > /etc/supervisor/supervisord.conf`

  - ` vim  /etc/supervisor/supervisord.conf`  

  - #去掉末尾的两个";"

    [include]

    files = /flask/root/demoapp/demoapp_supervisor.conf

  - 修改supervisor.conf文件
  
  - 添加supervisor_err.log，supervisor.log文件
  
  - `supervisord -c /etc/supervisor/supervisord.conf`
  
  - `supervisorctl -c /etc/supervisor/supervisord.conf status demoapp`



**Log** 

-  [2021.2.4] 鲁迅图片的markdown代码放在了html框中，typora输出html文件后，该图片不以'/>'结尾，而是以'>'结尾。所以修改了html_modify函数中，图片查找的re规则；
-  [2021.6.15] pip安装pykeyboard后，并不能直接使用，还需要安装PyUserInput；