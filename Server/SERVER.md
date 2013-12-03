Username: rickycm@gmail.com
Password: 1qazxsw2
Public DNS: ec2-54-201-144-79.us-west-2.compute.amazonaws.com

SecureCRT 联接方式：
1、在SecureCRT中新建连接，协议选择ssh2 ，主机名填写public dns（这个地址EC2的控制台中会提供），用户名填写ec2-user 。
2、在SecureCRT连接的列表中找到刚创建的连接，右键属性，左边树中选择SSH2,然后选择右边authentication中publicKey,点属性,
在出来的对话框中选择使用身份或证书文件,通过浏览 文件指定到刚在Linux下生成的文件即可.注意xxx.pem.pub和xxx.pem要在同一文件夹下。


***
Installing MySQL on an EC2 Micro Instance
http://www.samstarling.co.uk/2010/10/installing-mysql-on-an-ec2-micro-instance/
Install / update to Python 2.7 and latest Pip on EC2 Amazon Linux
http://www.lecloud.net/post/61401763496/install-update-to-python-2-7-and-latest-pip-on-ec2