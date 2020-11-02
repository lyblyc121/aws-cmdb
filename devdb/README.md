### 资产管理

> 基于Python Tornado实现的一套CMDB资产管理系统，前端使用Vue+Iview-admin




#### 部署文档

> Docker部署方式

**创建数据库**

```
create database `ui` default character set utf8mb4 collate utf8mb4_unicode_ci;
```
**修改配置**

- 修改`settings.py`配置信息
  - 注意：需要修改的信息在`settings.py`里面已经标注
  - 请确保你`settings`信息里面`mysql redis`等配置信息的准确性
- `docs/nginx_ops.conf`文件
   - 建议保持默认，毕竟都是内部通信，用什么域名都无所谓，到时候只修改前端访问的域名即可
   - 若你这里修改了，后面DNS、网关都要记得跟着修改为这个域名



**打包镜像**

```
docker build . -t ui
```

**启动Docker**

```
docker-compose up -d
```

**初始化表结构**

```
#若是在本地执行需要安装很多SDK包的依赖，建议进入容器执行
#ui_cmdb_1:是你的容器名称
docker exec -ti ui_cmdb_1 /usr/local/bin/python3 /var/www/cmdb-cmdb/db_sync.py
```

**日志文件**
- 服务日志：`/var/log/supervisor/cmdb.log`  #主程序日志
- 定时日志：`/var/log/supervisor/cmdb_cron.log` #一些后端守护自动运行的日志

**接口测试**

- 可查看日志看是否有报错
- 默认端口：8050，可直接测试Are you ok?
```
#返回200
 curl -I -X GET -m 10 -o /dev/null -s -w %{http_code} http://${cmdb_domain}:8050/are_you_ok/
```


