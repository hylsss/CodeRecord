## ASPNET.Core路由

- Routing（路由）：更准确的应该叫做Endpoint Routing，负责将HTTP请求按照匹配规则选择对应的终结点

- Endpoint（终结点）：负责当HTTP请求到达时，执行代码
   ##### 终结点有以下特点：

    -  可执行：含有RequestDelegate委托
    -  可扩展：含有Metadata元数据集合
    -  可选择：可选的包含路由信息
    -  可枚举：通过DI容器，查找EndpointDataSource来展示终结点集合。



路由是通过`UseRouting`和`UseEndpoints`两个中间件配合在一起来完成注册的：

- `UseRouting`：用于向中间件管道添加路由匹配中间件（`EndpointRoutingMiddleware`）。该中间件会检查应用中定义的终结点列表，然后通过匹配 URL 和 HTTP 方法来选择最佳的终结点。**简单说，该中间件的作用是根据一定规则来选择出终结点**
- `UseEndpoints`：用于向中间件管道添加终结点中间件（`EndpointMiddleware`）。可以向该中间件的终结点列表中添加终结点，并配置这些终结点要执行的委托，该中间件会负责运行由`EndpointRoutingMiddleware`中间件选择的终结点所关联的委托。**简单说，该中间件用来执行所选择的终结点委托**

**UseRouting`与`UseEndpoints`必须同时使用，而且必须先调用`UseRouting`，再调用`UseEndpoints**

### 路由的主要组成部分：

- **模板**：路由模板是一个预定义的URL模式，用于匹配客户端请求。例如，`/api/products/{id}` 是一个路由模板，其中 `{id}` 是一个参数。
- **处理程序**：当一个特定的路由被触发时，一个或多个处理程序（通常是控制器的动作方法）会被执行。
- **约束**：路由约束允许您限制参数的类型、范围或模式。例如，您可以指定一个参数必须是整数。
- **默认值和可选参数**：您可以为路由参数设置默认值或标记它们为可选的。
- **区域（Areas）**：在大型应用中，您可以使用区域来分组相关的控制器和视图。



### 路由的类型：

1. ##### 约定式路由：
```c#
app.UseEndpoints(endpoints =>
{
    endpoints.MapControllerRoute(
        name: "default",
        pattern: "{controller=Home}/{action=Index}/{id?}");
});

```


2. ##### 属性路由：
    通过基于属性的路由，我们可以在`控制器类和这些类的内部方法`上使用 C# 属性。 这些属性携带了告诉 ASP.NET Core 何时调用特定控制器的元数据

-  属性路由是基于约定的路由的替代方案

-  路由按照它们出现的顺序进行评估，也就是我们注册它们的顺序，映射多个路由的情况相当普遍，特别是如果我们想在 URL 中使用不同的参数或者如果要在 URL 中使用不同的文字.

```c#
[Route("api/[controller]/[action]")]
[ApiController]

public class HomeController : ControllerBase
{
    [HttpGet]
    public string Home()
    {
        return "hello world";
    }
}
```




### 基本事例

```c#
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();

//直接浏览器输入localhost:port => 页面输出 Hello World!
```
在 `ASP.NET Core` 中，`MapGet `方法用于映射 HTTP GET 请求到特定的请求处理程序（通常是一个匿名函数或委托）。这是端点路由（Endpoint Routing）的一部分，通常在` Startup.cs `文件的` Configure `方法中使用

- 当 HTTP `GET` 请求发送到根 URL`/`时：

  - 将执行请求委托。
  - `Hello World!` 会写入 HTTP 响应。

- 如果请求方法不是 `GET` 或根 URL 不是 `/`，则无路由匹配，并返回 HTTP 404。




### 配置终结点委托
- MapGet
- MapPost
- MapPut
- MapDelete
- MapHealthChecks
- 其他类似“MapXXX”的方法 

```c#
public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
{
    app.UseRouting();

    // 在执行终结点前进行授权
    app.UseAuthorization();

    app.UseEndpoints(endpoints =>
    {
        endpoints.MapGet("/", async context => await context.Response.WriteAsync("get"));
        endpoints.MapPost("/", async context => await context.Response.WriteAsync("post"));
        endpoints.MapPut("/", async context => await context.Response.WriteAsync("put"));
        endpoints.MapDelete("/", async context => await context.Response.WriteAsync("delete"));
        endpoints.MapHealthChecks("/healthChecks");
        endpoints.MapControllers();
    });

}
```





