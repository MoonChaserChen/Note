# Mac常用软件安装
## 1. brew软件包管理
可以用于命令行安装软件。
1. 安装
   直接在命令行运行 `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. 配置
   ```
   (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/akira/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
   ```
3. 查看
   ```shell
   brew info zookeeper
   ```
4. 安装
   ```shell
   brew install zookeeper
   ```
5. 开机启动
   ```shell
   brew services start zookeeper
   ```
## 2. python多版本管理工具pyenv
1. 安装 `brew install pyenv`
2. 查看当前安装的pyenv的版本 `pyenv -v`
3. 将pyenv配置到全局环境变量中
   ```
   vim  /etc/profile 
   
   export PYENV_ROOT=~/.pyenv
   export PATH=$PYENV_ROOT/shims:$PATH
   
   source /etc/profile
   ```
4. 查看所有可以安装的python版本 `pyenv install --list`
5. 安装指定版本的python
    ```
    pyenv install 3.8.9
    pyenv rehash # 在进行安装、删除指定python版本后使用，更新版本管理数据库
    ```
6. 查看所有的python版本 `pyenv versions`
7. 切换python版本 
   ```
   pyenv global 3.5.5
   python --version
   ```
8. 卸载指定的Python版本
   ```
   pyenv uninstall 3.8.9
   pyenv rehash # 在进行安装、删除指定python版本后使用，更新版本管理数据库
   ```
9. npm设置国内Registry
   ```
   npm config set registry https://registry.npm.taobao.org
   ```
## 3. jdk
https://jdk.java.net/java-se-ri/11
## 4. maven
直接在官网下载 `https://maven.apache.org/download.cgi`， 或者在 `https://archive.apache.org/dist/maven/binaries/` 下载历史版本。
### 配置说明
参见：https://www.jianshu.com/p/06f73e8cbf78
https://maven.apache.org/guides/mini/guide-multiple-repositories.html
### 配置示例
```xml
<?xml version="1.0" encoding="UTF-8"?>

<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">

   <localRepository>${user.home}/.m2/repository</localRepository>

   <mirrors>
      <mirror>
         <id>nexus-aliyun</id>
         <name>Nexus aliyun</name>
         <url>http://maven.aliyun.com/nexus/content/groups/public</url>
         <mirrorOf>central</mirrorOf>
      </mirror>
   </mirrors>

   <profiles>
      <profile>
         <id>JDK8</id>
         <properties>
            <maven.compiler.source>8</maven.compiler.source>
            <maven.compiler.target>8</maven.compiler.target>
            <maven.compiler.compilerVersion>8</maven.compiler.compilerVersion>
         </properties>
      </profile>
      <profile>
         <id>JDK11</id>
         <properties>
            <maven.compiler.source>11</maven.compiler.source>
            <maven.compiler.target>11</maven.compiler.target>
            <maven.compiler.compilerVersion>11</maven.compiler.compilerVersion>
         </properties>
      </profile>
      <profile>
         <id>Repos</id>
         <repositories>
            <repository>
               <id>central</id>
               <name>central</name>
               <url>https://repo.maven.apache.org/maven2/</url>
            </repository>
            <repository>
               <id>snatype-release</id>
               <name>snatype-release</name>
               <url>https://oss.sonatype.org/content/repositories/releases</url>
            </repository>
            <repository>
               <id>snatype-snapshots</id>
               <name>snatype-snapshots</name>
               <url>https://oss.sonatype.org/content/repositories/snapshots</url>
            </repository>
            <repository>
               <id>apache-snapshots</id>
               <name>apache-snapshots</name>
               <url>https://repository.apache.org/content/repositories/snapshots</url>
            </repository>
            <repository>
               <id>shibboleth-releases</id>
               <name>shibboleth-releases</name>
               <url>https://build.shibboleth.net/nexus/content/repositories/releases/</url>
            </repository>
            <repository>
               <id>shibboleth-snapshots</id>
               <name>shibboleth-snapshots</name>
               <url>https://build.shibboleth.net/nexus/content/repositories/snapshots/</url>
            </repository>
            <repository>
               <id>springsource-release</id>
               <name>springsource-release</name>
               <url>http://repo.spring.io/release/</url>
            </repository>
            <repository>
               <id>springsource-milestone</id>
               <name>springsource-milestone</name>
               <url>http://repo.spring.io/milestone/</url>
            </repository>
         </repositories>
      </profile>
   </profiles>

   <activeProfiles>
      <activeProfile>JDK8</activeProfile>
      <activeProfile>Repos</activeProfile>
   </activeProfiles>
</settings>
```
## 5. sublime
官网：https://www.sublimetext.com
### PackageControl
安装方式1：命令行
cmd+shift+p => Install Package Control

安装方式2：菜单
Tools => Install Package Control
## 6. gradle
## 7. node多版本管理工具nvm
依赖python
1. 安装nvm
   ```
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
   ```
2. 配置nvm
   ```
   vim /etc/profile
   
   export NVM_DIR="$HOME/.nvm"
   [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
   
   source /etc/profile
   nvm --version  # check installation
   ```
3. 查看所有可安装的node版本
   ```
   nvm ls-remote
   nvm ls-remote --lts
   ```
4. 安装指定版本的node
   ```
   nvm install v9.5.0
   nvm install stable
   ```
5. 查看已安装的node
   ```
   nvm ls
   ```
6. 切换node版本
   ```
   nvm use v6.9.0
   ```
7. 设定默认的node版本
   ```
   nvm alias default v6.9.0
   ```
8. 删除指定版本的node
   ```
   nvm uninstall v9.5.0
   ```
## 8. git
安装了 Xcode Command Line Tools 就会自带git，需要进行git初始基本配置
```
git config --global user.name "Akira"
git config --global user.email chin.kou.akira@gmail.com

git config --global http.https://github.com.proxy socks5://127.0.0.1:7890  # 为github配置代理
```

## 9. Mysql&Mysql Workbench
https://dev.mysql.com/downloads/mysql/
https://dev.mysql.com/downloads/workbench/

## 10. Redis
文档： https://redis.io/docs/  
安装： https://redis.io/docs/getting-started/installation/install-redis-on-mac-os/  

```
To start redis now and restart at login:
  brew services start redis
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/redis/bin/redis-server /opt/homebrew/etc/redis.conf
```

## 11. zookeeper
```shell
brew install zookeeper
zkServer start
zkServer stop
zkServer status
zkCli
```
## ffmpeg
用于视频处理。
```shell
# 安装
brew install ffmpeg
# 下载流媒体文件m38u
ffmpeg -i "http://host/folder/file.m3u8" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 file.mp4
# 下载流媒体文件（脚本）
ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i "$1" -c copy video.mp4
# 格式转换 mov-->mp4
ffmpeg -i source.mov -vcodec copy -acodec copy temp.mp4
# 压缩，修改帧率
ffmpeg -i temp.mp4 -r 20 des.mp4
```
