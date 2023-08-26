## ASP.NET.Core 入门

### 概念：

ASP.NET Core 是一个跨平台（Windows,macOS,Linux）的高性能开源框架，用于生成启用云且连接 Internet 的新式应用。

### 搭建项目：

- 创建Web应用项目

- 运行项目

- 运行应用

- 编辑Razor页面

```c#
//创建新Web应用
//-o aspnetcoreapp 参数使用应用的源文件创建名为 aspnetcoreapp 的目录。
dotnet new webapp -o aspnetcoreapp
```

```c#
//信任开发证书
dotnet dev-certs https --trust
```

