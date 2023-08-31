## ASP.NET.Core启动过程

对于ASP.NET Core应用程序来说，我们要记住非常重要的一点是：其本质上是一个独立的控制台应用，它并不是必需在IIS内部托管且并不需要IIS来启动运行（而这正是ASP.NET Core跨平台的基石）。ASP.NET Core应用程序拥有一个内置的**Self-Hosted（自托管）**的**Web Server（Web服务器）**，用来处理外部请求。

不管是托管还是自托管，都离不开**Host（宿主）**。在ASP.NET Core应用中通过配置并启动一个Host来完成应用程序的启动和其生命周期的管理（如下图所示）。而Host的主要的职责就是Web Server的配置和**Pilpeline（请求处理管道）**的构建。

### 步骤：

1.  **CreateHostBuilder(args)** ：创建IWebHostBuilder
2. **Build()** ：IWebHostBuilder负责创建IWebHost
3. **Run()** ：启动IWebHost

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