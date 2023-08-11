# [server](http://nginx.org/en/docs/http/ngx_http_core_module.html#server)
nginx代理中比较重要的配置，管理了nginx如何进行请求转发。
## [server_name](http://nginx.org/en/docs/http/ngx_http_core_module.html#server_name)
http://nginx.org/en/docs/http/server_names.html
可以配置多个server，每个server都有个server_name配置，此配置来判断某个请求会命中哪个server。
1. server_name可以配置多个，使用通配符以及正则，例如：
    ```
    server {
        listen       80;
        server_name  example.org  www.example.org;
        ...
    }
    
    server {
        listen       80;
        server_name  *.example.org;
        ...
    }
    
    server {
        listen       80;
        server_name  mail.*;
        ...
    }
    
    server {
        listen       80;
        server_name  ~^(?<user>.+)\.example\.net$;
        ...
    }
    ```
2. 通配符只能位于起始或结束位置并跟随着`.`分隔符出现。例如 `www.*.example.org` 和 `w*.example.org`就是不合法的
3. `*.example.org` 可以匹配到 `www.example.org` 以及 `www.sub.example.org`
4. 正则配置需要以 `~` 开头，而且通常带有 `^` 与 `&`
5. 如果正则配置中带有`{}`，则需要使用引号。例如：`server_name  "~^(?<name>\w\d{1,3}+)\.example\.net$";`
6. 正则中的变量也可以在后续进行使用，例如：
   ```
   server {
       server_name   ~^(www\.)?(?<domain>.+)$;
   
       location / {
           root   /sites/$domain;
       }
   }
   
   
   server {
       server_name   ~^(www\.)?(.+)$;
   
       location / {
           root   /sites/$2;
       }
   }
   ```

匹配优先级：
1. the exact name
2. the longest wildcard name starting with an asterisk, e.g. “*.example.com”
3. the longest wildcard name ending with an asterisk, e.g. “mail.*”
4. the first matching regular expression (in order of appearance in the configuration file)

不知道是不是通过域名进行匹配，还是仅仅是个名称。猜测原理是：nginx在http这个context下可以配置多个server，
每个server可以有不同的配置，因此需要先命中server，再根据server判定命中的location等。
但是奇怪：
1. server_name配置为life.akira.ink，但实际上通过ip访问（发现请求中的Host也是IP）也能命中
2. 两个文件 file.conf life.conf都通过域名配置，但实际上通过Ip访问直接命中了第一个文件


## [location](http://nginx.org/en/docs/http/ngx_http_core_module.html#location)
根据request的uri进行路径匹配，有三种设置方式：前缀匹配、~*标志的区分大小写的正则、~标志的不区分大小写的正则

匹配规则：
1. 先进行所有的前缀匹配，以选中最长匹配；
    1. 在匹配过程中，如果发现配置以 `=` 开头，且精确匹配上，则选中此配置并直接结束
    2. 选出最长匹配后，如果配置前缀以 `^~` 开头，则选中此配置并直接结束
2. 再按配置顺序进行正则匹配
    1. 正则匹配命中一个则选中此配置并直接结束
    2. 若正则匹配均未命中，则选中前面获取到的最长前缀匹配
```
Let’s illustrate the above by an example:

location = / {
    [ configuration A ]
}

location / {
    [ configuration B ]
}

location /documents/ {
    [ configuration C ]
}

location ^~ /images/ {
    [ configuration D ]
}

location ~* \.(gif|jpg|jpeg)$ {
    [ configuration E ]
}
The “/” request will match configuration A, 
the “/index.html” request will match configuration B, 【这里命中了B，且没有后续的正则命中，所以最终选取了B】
the “/documents/document.html” request will match configuration C, 【这里同时命中了B和C，但C更长，所以选取了C】
the “/images/1.gif” request will match configuration D, 【这里理论上会命中D和E，但命中的D带有^~，因此未进行后续的正则匹配，也就不会命中E，直接选取D】
the “/documents/1.jpg” request will match configuration E. 【这里可以看出，同时命中了前缀的C和正则的E，最后选取了正则匹配E】
```

### [proxy_pass](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass)
标明请求转发到哪个服务器，也可配合[upstream](upstream.md)以实现负载均衡。
1. proxy_pass后若带URI，则不带匹配部分
2. proxy_pass后若不带URI，则带匹配部分（也可通过[rewrite](#rewrite)改写匹配部分）

```
Let’s illustrate the above by an example:

location /name/ {
    proxy_pass http://127.0.0.1/remote/;
}

location /some/path/ {
    proxy_pass http://127.0.0.1;
}

请求 /name/1234 会转发到 http://127.0.0.1/remote/1234
请求 /some/path/1234 会转发到 http://127.0.0.1/some/path/1234
```
建议proxy_pass后面的转发服务器均不使用IP，而是使用[upstream](upstream.md)。

### [rewrite](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html#rewrite)
语法： `rewrite regex replacement break;`
```
Let’s illustrate the above by an example:

location /name/ {
    rewrite    /name/([^/]+) /users?name=$1 break;
    proxy_pass http://127.0.0.1;
}

请求 /name/akira 会转发到 http://127.0.0.1/users?name=akira
```

### [proxy_set_header](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_set_header)
使用nginx反向代理后，如果要使服务获取真实的用户信息，通常用请求头携带
```
location /api {
    proxy_pass  http://192.168.0.1;
    #不修改被代理服务器返回的响应头中的location头
    proxy_redirect off;
    #使用nginx反向代理后，如果要使服务获取真实的用户信息，通常用请求头携带
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

### if
可以在配置中增加条件判断
```
# 匹配到携带example字符串的请求 将请求转发到其他HOST并携带path
location ~ /example/ {
    proxy_set_header Host example.example.top;
    if ($request_uri ~*  [.]*?/example/(.*)){
       set $path $1;
       proxy_pass http://127.0.0.1/$path;
     }
}
```

### [root](http://nginx.org/en/docs/http/ngx_http_core_module.html#root)&[alias](http://nginx.org/en/docs/http/ngx_http_core_module.html#alias)
可用于代理静态文件（root会带上匹配部分，alias不会带上匹配部分）。
```
location /i/ {
    root /data/w3;
}


请求 /i/top.gif 会返回 /data/w3/i/top.gif 文件
```

```
location /i/ {
    alias /data/w3/images/;
}

请求 /i/top.gif 会返回 /data/w3/images/top.gif 文件
```

官网建议，如果能匹配上最后部分，建议使用root，即：
```
location /images/ {
    alias /data/w3/images/;
}
建议改成如下：
location /images/ {
    root /data/w3;
}
```

### 其它
#### 流量镜像功能
```
location / {
    mirror /mirror;
    proxy_pass http://backend;
}

location = /mirror {
    internal;
    proxy_pass http://test_backend$request_uri;
}
```

#### 重定向配置
```
location / {
   return 404; #直接返回状态码
}
location / { 
   return 404 "pages not found"; 
   #返回状态码 + 一段文本
}
location / { 
   return 302 /blog ; 
   #返回状态码 + 重定向地址
}
location / { 
   return https://www.mingongge.com ; 
   #返回重定向地址
}
```
