## ASP.NET.Core-Startup

### Startup类

##### 结构

- 构造函数
- `Configuration`属性
- `ConfigureServices`方法
- `Configure`方法

```c#
public class Startup
{
    public Startup(IConfiguration configuration)
    {
        Configuration = configuration;
    }

    public IConfiguration Configuration { get; }
    // 该方法由运行时调用，使用该方法向DI容器添加服务
    public void ConfigureServices(IServiceCollection services)
    {
    }
    // 该方法由运行时调用，使用该方法配置HTTP请求管道
    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
    }
}
```

### ConfigureServices

- 该方法是**可选**的
- 该方法用于添加服务到DI容器中
- 该方法在 **`Configure`方法之前被调用**
- 该方法要么无参数，要么只能有一个参数且类型必须为`IServiceCollection`
- 该方法内的代码大多是形如`Add{Service}`的扩展方法

常用的服务有（部分服务框架已默认注册）：

- `AddControllers`：注册Controller相关服务，内部调用了`AddMvcCore`、`AddApiExplorer`、`AddAuthorization`、`AddCors`、`AddDataAnnotations`、`AddFormatterMappings`等多个扩展方法
- `AddOptions`：注册Options相关服务，如`IOptions<>`、`IOptionsSnapshot<>`、`IOptionsMonitor<>`、`IOptionsFactory<>`、`IOptionsMonitorCache<>`等。很多服务都需要Options，所以很多服务注册的扩展方法会在内部调用`AddOptions`
- `AddRouting`：注册路由相关服务，如`IInlineConstraintResolver`、`LinkGenerator`、`IConfigureOptions<RouteOptions>`、`RoutePatternTransformer`等
- `AddAddLogging`：注册Logging相关服务，如`ILoggerFactory`、`ILogger<>`、`IConfigureOptions<LoggerFilterOptions>>`等
- `AddAuthentication`：注册身份认证相关服务，以方便后续注册JwtBearer、Cookie等服务
- `AddAuthorization`：注册用户授权相关服务
- `AddMvc`：注册Mvc相关服务，比如Controllers、Views、RazorPages等
- `AddHealthChecks`：注册健康检查相关服务，如`HealthCheckService`、`IHostedService`等

### Configure

- 该方法是**必须**的
- 该方法用于配置HTTP请求管道，通过向管道添加中间件，应用不同的响应方式。
- 该方法在**`ConfigureServices`方法之后被调用**
- 该方法中的参数可以接受任何已注入到DI容器中的服务
- 该方法内的代码大多是形如`Use{Middleware}`的扩展方法
- **该方法内中间件的注册顺序与代码的书写顺序是一致的，先注册的先执行，后注册的后执行**

常用的中间件有

- `UseDeveloperExceptionPage`：当发生异常时，展示开发人员异常信息页
- `UseRouting`：路由中间件，根据Url中的路径导航到对应的Endpoint。必须与`UseEndpoints`搭配使用。
- `UseEndpoints`：执行路由所选择的Endpoint对应的委托。
- `UseAuthentication`：身份认证中间件，用于对请求用户的身份进行认证。比如，早晨上班打卡时，管理员认出你是公司员工，那么才允许你进入公司。
- `UseAuthorization`：用户授权中间件，用于对请求用户进行授权。比如，虽然你是公司员工，但是你是一名.NET开发工程师，那么你只允许坐在.NET开发工程师区域的工位上，而不能坐在老总的办公室里。
- `UseMvc`：Mvc中间件。
- `UseHealthChecks`：健康检查中间件。
- `UseMiddleware`：用来添加匿名中间件的，通过该方法，可以方便的添加自定义中间件。