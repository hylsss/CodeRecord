## ASP.NET.Core依赖注入

ASP.NET Core 的依赖注入（Dependency Injection, DI）是一个用于实现控制反转（Inversion of Control, IoC）的技术，它有助于提高代码的可维护性和可测试性。

-  ASP.NET Core 支持依赖关系注入` (DI) 软件设计模式`，这是一种在类及其依赖关系之间实现[控制反转 (IoC)](https://learn.microsoft.com/zh-cn/dotnet/standard/modern-web-apps-azure-architecture/architectural-principles#dependency-inversion) 的技术。

### 一、定义接口或者抽象类，来描述依赖对象具备的属性和功能。

```c#
//定义接口
public interface ILogger
{
    void Log(string message);
}

//定义抽象类
public abstract class LoggerBase
{
    public abstract void Log(string message);
    
    public void LogInformation(string info)
    {
        // Some default implementation
        Log($"Information: {info}");
    }
}


```

### 二、实现接口或者接口类

```c#
//实现接口
public class ConsoleLogger : ILogger
{
    public void Log(string message)
    {
        Console.WriteLine(message);
    }
}

// 实现抽象类
public class FileLogger : LoggerBase
{
    public override void Log(string message)
    {
        // Write to a file
    }
}

```

### 三、注册依赖

在 `Startup.cs` 文件的 `ConfigureServices` 方法中，注册依赖。

```c#
public void ConfigureServices(IServiceCollection services)
{
    services.AddTransient<IGreetingService, GreetingService>();
    // 其他服务注册
}
```

这里，`AddTransient` 方法表示每次请求都会创建一个新的 `GreetingService` 实例。除了 `AddTransient`，还有其他方法如 `AddScoped` 和 `AddSingleton`，用于控制依赖对象的生命周期。

### 四、注入依赖

在需要使用该服务的地方（如控制器、视图、其他服务等）通过构造函数注入依赖。

```c#
public class HomeController : Controller
{
    private readonly IGreetingService _greetingService;

    public HomeController(IGreetingService greetingService)
    {
        _greetingService = greetingService;
    }

    public IActionResult Index()
    {
        var greeting = _greetingService.Greet("John");
        return View("Index", greeting);
    }
}

```

####  依赖注入方式
- 构造函数注入（Constructor Injection）
  这是最常用的依赖注入方式。在这种方式中，依赖项通过类的构造函数传入。
```c#
public class HomeController : Controller
{
    private readonly IGreetingService _greetingService;

    public HomeController(IGreetingService greetingService)
    {
        _greetingService = greetingService;
    }
}

```


- 属性注入（Property Injection）

这种方式不如构造函数注入常用，但在某些特定场景下可能会用到。在这种方式中，依赖项通过属性设置。

```c#
public class HomeController : Controller
{
    [FromServices]
    public IGreetingService GreetingService { get; set; }
}

```

- 方法注入（Method Injection）
在这种方式中，依赖项通过方法参数传入。这通常用于 Action 方法。
```c#
public class HomeController : Controller
{
    public IActionResult Index([FromServices] IGreetingService greetingService)
    {
        var greeting = greetingService.Greet("John");
        return View("Index", greeting);
    }
}

```

- 服务定位器（Service Locator）
虽然这不是一种推荐的依赖注入方式，但在某些特定情况下，您可能需要在运行时动态地获取依赖项。这可以通过 IServiceProvider 实现。
```c#
public class HomeController : Controller
{
    private readonly IServiceProvider _serviceProvider;

    public HomeController(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public IActionResult Index()
    {
        var greetingService = _serviceProvider.GetService<IGreetingService>();
        var greeting = greetingService.Greet("John");
        return View("Index", greeting);
    }
}

```

-  使用 IOptions 注入配置

如果您需要将配置信息注入到应用程序中，可以使用 `IOptions` 或 `IOptionsSnapshot`。

```c#
public class HomeController : Controller
{
    private readonly MyConfig _config;

    public HomeController(IOptions<MyConfig> options)
    {
        _config = options.Value;
    }
}

```



### 五、使用依赖

在应用程序的逻辑中，您现在可以使用注入的依赖。

```c#
public IActionResult Index()
{
    var greeting = _greetingService.Greet("John");
    return View("Index", greeting);
}
```

