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
##### 在Program的Main方法中配置Serilog

日志输出到控制台

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
输出本地日志文件

```c#
Log.Logger = new LoggerConfiguration()
  .MinimumLevel.Debug()
  .WriteTo.Console()
  .WriteTo.File("00_Logs//log.log",
                rollingInterval: RollingInterval.Day,
                outputTemplate: SerilogOutputTemplate,
                retainedFileCountLimit: 31,
                retainedFileTimeLimit: TimeSpan.FromDays(2),
                rollOnFileSizeLimit: true,
                fileSizeLimitBytes: 52428800 // 50MB
                )
  .CreateLogger();

//简洁版本
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
            .WriteTo.File("00_Logs//log.log", rollingInterval: RollingInterval.Day)
            .CreateLogger();
```

WriteTo.File详解（日志默认路径为当前程序路径）

- path：默认路径是程序的bin目录+path参数，当然也可以写绝对路径，只需要写入参数就可以了
- rollingInterval：创建文件的类别，可以是分钟，小时，天，月。 此参数可以让创建的log文件名 + 时间。例如log20191219.log
- outputTemplate：日志模板，可以自定义
- retainedFileTimeLimit：日志保存时间，删除过期日志
- retainedFileCountLimit：设置日志文件个数最大值，默认31，意思就是只保留最近的31个日志文件,等于null时永远保留文件
- rollOnFileSizeLimit： 是否限制单个文件的最大大小
- fileSizeLimitBytes： 单个文件最大长度

##### 在程序入口Program类的IHostBuilder函数启用Serilog

```C#
public static IHostBuilder CreateHostBuilder(string[] args) =>
    Host.CreateDefaultBuilder(args)
        .UseSerilog()
        .ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.UseStartup<Startup>();
        });
```
##### 还有一个Startup.cs，用于配置中间件管道，Configure如下所示

RequestLoggingMiddleware被包含在Serilog.AspNetCore中，可以被用于为每个请求添加一个单一的“摘要”日志消息。如果您已经完成了上一节中的步骤，则添加这个中间件将变得很简单。在您的Startup类中，在您想要记录日志的位置使用UseSerilogRequestLogging()进行调用

```c#
    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        app.UseHttpsRedirection();
        app.UseStaticFiles();
        app.UseSerilogRequestLogging();
        app.UseRouting();
        app.UseAuthentication();
        app.UseAuthorization();
        app.UseEndpoints(enpoint => enpoint.MapControllers());
    }
```
与ASP.NET Core的中间件管道一样，顺序很重要。当请求到达RequestLoggingMiddleware中间件时，它将启动计时器，并将请求传递给后续中间件进行处理。当后面的中间件最终生成响应（或抛出异常），则响应通过中间件管道传递回到请求记录器，并在其中记录了结果并写入概要日志信息。

Serilog只能记录到达中间件的请求。在上面的例子中，我已经在StaticFilesMiddleware之后添加了RequestLoggingMiddleware 。因此如果请求被UseStaticFiles处理并使管道短路的话，日志将不会被记录。鉴于静态文件中间件非常嘈杂，而且通常这是人们期望的行为（静态文件进行短路，不需要进行记录），但是如果您也希望记录对静态文件的请求，则可以在管道中serilog中间件移动到更早的位置。


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

#### appsettings.json的配置
修改`appsettings.json`，向 WriteTo 下的 RollingFile 对象节点的 Args 添加一个 outputTemplate 选项，以 自定义输出消息模板 ：
```c#
 "Args": {
    "pathFormat": "Logs\\{HalfHour}.log",
    "outputTemplate": "{Timestamp:o} [{Level:u3}] ({MachineName}/{ProcessId}/{ProcessName}/{ThreadId}) {Message}{NewLine}{Exception}"
  }
```
向 Serilog 配置对象添加 Enrich 配置节点，以丰富日志事件的信息.
```c#
"Enrich": [
  "WithMachineName",
  "WithProcessId",
  "WithProcessName",
  "WithThreadId"
]
```

将日志保存到数据库
修改 appsettings.json，在 Serilog 配置中的 WriteTo 节点下添加以下配置节点，以向 SQLite 输出日志：

```c#
 "Args": {
    "sqliteDbPath": "Logs\\log.db",
    "tableName": "Logs",
    "maxDatabaseSize": 1,
    "rollOver": true
  }
```
-  sqliteDbPath： SQLite 数据库的路径。
-  tableName： 用于存储日志的 SQLite 表的名称。
-  maxDatabaseSize： 数据库的最大文件大小，可以以 MB 为单位增加。默认为 10MB，最大为 20GB。为了方便测试，我在这里将其设置为 1MB。
-  rollOver： 如果文件大小超过最大数据库文件大小，则创建滚动备份，默认为 true。



浏览器log 出来的记录
![673bdf873ef864657c08c994eceae04](https://github.com/hylsss/CodeRecord/assets/62007319/f08f14f0-ea19-47bc-b6f8-3e0d114a34b1)

输出本地日志文件
![1699172049516](https://github.com/hylsss/CodeRecord/assets/62007319/9b2158cf-2b10-4fa7-a078-9a2d70a84fdc)
