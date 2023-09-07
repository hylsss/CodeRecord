## docker创建mysql容器

#### 创建并启动一个容器

```
docker run --name test-mysql -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 -d mysql:5.7
//653ae2cc6f174f820c41ab48f8208b1babd4319ad69422c628c7e3072e0603fc

```

- `-name`: 给新创建的[容器](https://cloud.tencent.com/product/tke?from_column=20065&from=20065)命名，此处命名为`test-mysql`
- `-e`: 配置信息，此处配置 [mysql](https://cloud.tencent.com/product/cdb?from_column=20065&from=20065) 的 root 用户的登录密码
- `-p`: 端口映射，此处映射主机的3306端口到容器`test-mysql`的3306端口
- -d: 成功启动同期后输出容器的完整ID
- 最后一个`mysql:5.7`指的是`mysql`镜像

bdfb0ec4d54ad6c6f51e03ce444f792731ac97d79c4575ee74e291b01b6a4bed

#### 查看容器运行状态

```
docker ps
```

#### 进入容器

```
docker exec -it test-mysql /bin/bash
```

#### 进入容器连接

```
mysql -u root -p
```

#### 查看所有容器

```
docker ps -a
```

#### 启动和关闭容器

```
docker start test-mysql # 指定容器名称
docker start 73f8811f669e # 指定容器ID
```

```
docker start test-mysql # 指定容器名称
docker start 73f8811f669e # 指定容器ID
```

