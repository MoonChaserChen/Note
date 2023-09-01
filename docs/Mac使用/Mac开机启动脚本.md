# Mac开机启动脚本
## 1) 创建脚本
```shell
$ sudo vim /usr/local/bin/kafka_start
#!/bin/bash
cd ~/Software/kafka
bin/kafka-server-start.sh config/server.properties & 
```

## 2) 开机启动
`设置 > 通用 > 登录项 > 登录时打开`

将上面创建的脚本加入到这里。