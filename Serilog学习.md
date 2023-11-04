## Serilog学习

### Serilog概述

- Serilog 是一个用于.NET应用程序的日志记录开源库，配置简单，接口干净，并可运行在最新的.NET平台上，与其他日志库不同, Serilog 是以功能强大的结构化事件数据为基础构建的， 支持将日志输出到控制台、文件、数据库和其它更多的方式，支持参数化日志模板，非常灵活
- Serilog使用Json格式来记录应用程序中的事件，方便快速查询、过滤日志
- Serilog 架构
  - Serilog：Serilog核心库
  - Sinks：事件接收器，通过事件接收器将日志写入到各种终端、文件、邮件、数据库或日志服务器，下面介绍常用的Sinks
    - Serilog.Sinks.Debug：将日志事件写入调试的输出窗口
    - Serilog.Sinks.Console：将Serilog事件写入控制台/终端
    - Serilog.Sinks.File：将Serilog事件写入文本文件
    - Serilog.Sinks.Http：将Serilog事件输出到REST服务
    - Serilog.Sinks.MongoDB：将日志事件写入MongoDB
    - Serilog.Sinks.EventLog：将日志事件写入系统事件中
    - Serilog.Sinks.MSSqlServer：将日志事件写入SQLServer
    - Serilog.Sinks.ElasticSearch：将日志事件写入ES
    - Serilog.Sinks.Email：将日志事件已Email的方式发送
    - Serilog.Sinks.RabbitMQ：将日志事件写入RabbitMQ

```c#
// 创建docker的seq容器
docker pull datalust/seq:latest
// 运行seq容器
// 这将在后台运行名为 "seq" 的容器，并将 Seq 的 80 端口映射到主机的 5341 端口
docker run -d --name seq -e ACCEPT_EULA=Y -p 5341:80 datalust/seq:latest
//在web访问
http://localhost:5341
```

### 从NuGet安装Serilog

1. **日志输出到控制台**，需要使用Nuget安装`Serilog`和`Serilog.Sinks.Console`两个包

2. **日志输出到文件**，需要安装`Serilog.Sinks.File`包

#### 配置Serilog
在Program的Main方法中配置Serilog

```c#
         Log.Logger = new LoggerConfiguration()
            .MinimumLevel.Information()
            .MinimumLevel.Override("Microsoft",
            LogEventLevel.Information)
            .MinimumLevel.Override("IdentityServer4",
            LogEventLevel.Information)
            .MinimumLevel.Override("Hangfire",   
            LogEventLevel.Information)
            .Enrich.FromLogContext()
            .WriteTo.Console()
            .WriteTo.Seq("http://localhost:5341")
            .CreateLogger();
```
在程序入口Program类的IHostBuilder函数启用Serilog
```C#
public static IHostBuilder CreateHostBuilder(string[] args) =>
    Host.CreateDefaultBuilder(args)
        .UseSerilog()
        .ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.UseStartup<Startup>();
        });
```

-  **MinimumLevel** 设置日志级别的最小级别为 `Debug`，这意味着 Debug、Information、Warning 和 Error 级别的日志消息都会被记录。
-  添加**MinimalLevel.Override **项，可以覆盖某些特定命名空间的最小级别。.MinimumLevel.Override("Microsoft", LogEventLevel.Information) 和.MinimumLevel.Override("Microsoft.AspNetCore", LogEventLevel.Warning)，在这种情况下，对于以 "Microsoft" 或 "Microsoft.AspNetCore" 开头的日志消息，将分别使用 Information 和 Warning 级别。
- ` .WriteTo.Console()`：将日志消息输出到控制台
-  `.WriteTo.Seq("http://localhost:5341")`：将日志消息发送到 Seq，您需要将 "http://localhost:5341" 替换为您 Seq 服务器的实际 URL。
-  ``.Enrich.FromLogContext()` 方法用于从当前日志上下文中提取附加信息，并将其添加到日志消息中,它可以自动丰富日志消息并帮助您更好地了解日志事件发生时的上下文信息。
-  事件级别

| 级别        | 说明                                     |
| ----------- | ---------------------------------------- |
| Verbos      | 第一级，记录详细的堆栈日志               |
| Debug       | 第二级，记录调试日志                     |
| Information | 第三级，记录程序执行日志                 |
| Warning     | 第四级，记录程序运行的警告日志           |
| Error       | 第五级，记录程序运行的错误日志           |
| Fatal       | 第六级，记录程序运行中发生致命错误的日志 |

