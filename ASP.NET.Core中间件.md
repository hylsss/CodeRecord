## ASP.NET.Core中间件

### 什么是ASP.NETCore的中间件？

1. 中间件是ASP.NET.Core的核心组件
2. 中间件相当于一个管道，，整个`ASP.NET Core`的执行过程就是`HTTP请求和响应`按照中间件组装的顺序在中间件之间流转的过程。

3. 使用`WebApplication`创建中间件管道，`ASP.NET Core` 请求管道包含一系列请求委托，每个委托均可在下一个委托前后执行操作。每个`HTTP请求`都要经历一系列中间件的处理，每个中间件对于请求进行特定的处理后，再转到下一个中间件，最终的业务逻辑代码执行完成后，响应的内容也会按照处理的相反顺序进行处理，然后形成`HTTP响应`报文返回给客户端。
4. 中间件是一种装配到应用管道以处理请求和响应的软件。 每个中间件执行以下任务：
   - 选择是否将请求传递到管道中的下一个组件。
   - 可在管道中的下一个组件前后执行工作。



### 在ASP.NET Core中执行顺序

在ASP.NET Core中,中间件可以访问到的HTTP请求和HTTP响应，所以可以用来：

1. 通过生成一个HTTP响应来处理HTTP请求
2. 处理并可以修改HTTP请求，然后将该HTTP请求传给管道上的下一个中间件
3. 处理并可以修改HTTP响应，并将HTTP响应传递给管道上的下一个中间件或ASP.NET Core应用





### ASP.NET Core 中间件的三个概念

`Map`、`Use`和`Run`。`Map`用来定义一个管道可以处理哪些请求，`Use`和`Run`用来定义管道，一个管道由`若干个Use和一个Run`组成，每个`Use`引入一个中间件，而Run是用来执行最终的核心应用逻辑。

1. 用Use将多个请求委托链接在一起。 next参数表示管道中的下一个委托。 可通过不调用next参数使管道短路。

2. Run 委托不会收到 next 参数。 第一个 Run 委托始终为终端，用于终止管道。 Run 是一种约定。 某些中间件组件可能会公开在管道末尾运行的 Run[Middleware]

3. Map*扩展用作分支管道的约定。

   

```C#
var builder = WebApplication.CreateBuilder(args);
 
var app = builder.Build();

app.Use(async (context, next) =>
{
    await context.Response.WriteAsync("First Start");
    await next.Invoke();
    await context.Response.WriteAsync("First End");
});

app.Run(async context =>
{
    await context.Response.WriteAsync("Second Start");
    await context.Response.WriteAsync("Second End");
});
 
app.Run();

//First Start
//Second Start
//Second End
//First End
```



### ASP.NET Core 常用内置中间件

1. 异常/错误处理
   - 当应用在开发环境中运行时：
     - 开发人员异常页中间件 (UseDeveloperExceptionPage) 报告应用运行时错误。
     - 数据库错误页中间件 (UseDatabaseErrorPage) 报告数据库运行时错误。
   - 当应用在生产环境中运行时：
     - 异常处理程序中间件 (UseExceptionHandler) 捕获以下中间件中引发的异常。
     - HTTP 严格传输安全协议 (HSTS) 中间件 (UseHsts) 添加 Strict-Transport-Security 标头。
2. HTTPS 重定向中间件 (UseHttpsRedirection) 将 HTTP 请求重定向到 HTTPS。
3. 静态文件中间件 (UseStaticFiles) 返回静态文件，并简化进一步请求处理。
4. Cookie 策略中间件 (UseCookiePolicy) 使应用符合欧盟一般数据保护条例 (GDPR) 规定。
5. 用于路由请求的路由中间件 (UseRouting)。
6. 身份验证中间件 (UseAuthentication) 尝试对用户进行身份验证，然后才会允许用户访问安全资源。
7. 用于授权用户访问安全资源的授权中间件 (UseAuthorization)。
8. 会话中间件 (UseSession) 建立和维护会话状态。 如果应用使用会话状态，请在 Cookie 策略中间件之后和 MVC 中间件之前调用会话中间件。

```C#
var builder = WebApplication.CreateBuilder(args);
 
var app = builder.Build();
  
if (app.Environment.IsDevelopment())
{ 
    app.UseDeveloperExceptionPage();//开发人员异常页中间件
    app.UseDatabaseErrorPage();//数据库错误页中间件
}
else
{
    app.UseExceptionHandler("/Error");//异常处理程序中间件
    app.UseHsts();//HTTP 严格传输安全协议 (HSTS) 中间件
}
app.UseHttpsRedirection();//HTTPS 重定向中间件
app.UseStaticFiles();//静态文件中间件
app.UseCookiePolicy();// Cookie 策略中间件
app.UseRouting();//用于路由请求的路由中间件
app.UseAuthentication();//身份验证中间件
app.UseAuthorization();//用于授权用户访问安全资源的授权中间件
app.UseSession();//会话中间件
  
app.Run();

```

