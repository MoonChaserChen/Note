## 官方文档
http://nginx.org/en/docs/

## nginx安装
nginx有很多种安装方式，同时不同的系统也有不同的安装方式。详见[官方文档](http://nginx.org/en/docs/install.html)。
这里记录RHEL版本通过yum安装，详见[官方文档](http://nginx.org/en/linux_packages.html#RHEL)。
```
[]# yum install yum-utils
[]# /etc/yum.repos.d/nginx.repo
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true

[nginx-mainline]
name=nginx mainline repo
baseurl=http://nginx.org/packages/mainline/centos/$releasever/$basearch/
gpgcheck=1
enabled=0
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true

[]# yum install -y nginx
```
## nginx启动
`nginx -c /usr/nginx/conf/nginx.conf`
## nginx重启
`nginx -s reload`

## 查看nginx当前使用的配置文件
```
[root@iZ2vcigu2y18c53vilsgfxZ local]# nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
## 检查指定的配置文件
`nginx -t -c /usr/nginx/conf/nginx.conf`

## nginx作用
1. 静态文本服务器
2. 代理服务器
3. 负载均衡