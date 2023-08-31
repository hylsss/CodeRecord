## ASP.NET.Core启动过程

对于ASP.NET Core应用程序来说，我们要记住非常重要的一点是：其本质上是一个独立的控制台应用，它并不是必需在IIS内部托管且并不需要IIS来启动运行（而这正是ASP.NET Core跨平台的基石）。ASP.NET Core应用程序拥有一个内置的**Self-Hosted（自托管）**的**Web Server（Web服务器）**，用来处理外部请求。

不管是托管还是自托管，都离不开**Host（宿主）**。在ASP.NET Core应用中通过配置并启动一个Host来完成应用程序的启动和其生命周期的管理（如下图所示）。而Host的主要的职责就是Web Server的配置和**Pilpeline（请求处理管道）**的构建。

### 步骤：

1.  **CreateHostBuilder(args)** ：创建IWebHostBuilder
2. **Build()** ：IWebHostBuilder负责创建IWebHost
3. **Run()** ：启动IWebHost

![启动进程图](https://github.com/hylsss/CodeRecord/assets/62007319/2c0c5037-fab1-4a5f-b0fd-fcc231812a15)


```c#
 public class Program
 { 
     //应用程序的入口点，它负责创建、构建和运行宿主
     public static void Main(string[] args)
     { 
         //配置 Web 宿主的默认设置
         CreateHostBuilder(args).Build().Run();
     }
     public static IHostBuilder CreateHostBuilder(string[] args) =>
       //创建一个预配置的宿主构建器，该构建器包括默认的日志记录、配置。
         Host.CreateDefaultBuilder(args)
             .ConfigureWebHostDefaults(webBuilder =>
             {   
                 //指定Startup为启动类
                 webBuilder.UseStartup<Startup>();
             });
 }
```

### 宿主构造器

WebHost的创建，又可以划分为三个部分：

1. 构建依赖注入容器，初始通用服务的注册：BuildCommonService();
2. 实例化WebHost：var host = new WebHost(...);
3. 初始化WebHost，也就是构建由中间件组成的请求处理管道：host.Initialize();
![宿主构造器](https://github.com/hylsss/CodeRecord/assets/62007319/7da39033-dfa2-4233-99d3-c45618050c34)



### 注册初始通用服务

`BuildBuildCommonService`方法主要做了两件事：

1. 查找`HostingStartupAttribute`特性以应用其他程序集中的启动配置
2. 注册通用服务
3. 若配置了启动程序集，则发现并以`IStartup`类型注入到IOC容器中

### 构建请求处理管道
1. 注册Startup中绑定的服务；
2. 配置IServer；
3. 构建管道

![请求处理管道](https://github.com/hylsss/CodeRecord/assets/62007319/0ab7945c-37d9-4ced-98b7-6c35af71cd6a)


### 启动WebHost

WebHost的启动主要分为两步：

1. 再次确认请求管道正确创建
2. 启动Server以监听请求
3. 启动 HostedService

![启动WebHost](https://github.com/hylsss/CodeRecord/assets/62007319/20bfb345-3b92-4a42-b0f2-3700a334e335)


### 总结
1. 负责创建IWebHost的宿主构造器IWebHostBuilder
2. 代表宿主的IWebHost接口
3. 用于构建请求管道的IApplicationBuilder
4. 中间件衔接而成的RequestDelegate
5. 代表Web Server的IServer接口
6. 贯穿请求处理管道的请求上下文HttpContext
7. 可以用来注册后台服务的IHostedService接口






