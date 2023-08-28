## ASP.NET.Core概述

ASP.NET Core 是 Microsoft 推出的一个跨平台、高性能、开源的 Web 框架，用于构建现代化、云优化的 Internet 连接应用程序，如 Web 应用、API、以及即使是移动后端服务。相比传统的`ASP.NET`框架，只能在` Windows `上运行不同,`ASP.NET Core`  可以在 `Windows`、`Mac` 和` Linux `上运行。

###  ASP.NET Core 的概念

1. **跨平台**: 与传统的 ASP.NET 只能在 Windows 上运行不同，ASP.NET Core 可以在 Windows、Mac 和 Linux 上运行。
2. **模块化**: ASP.NET Core 是模块化的，这意味着你可以选择你需要的特定部分而不是整个框架，这使得应用程序更加轻量化。
3. **集成的依赖注入**: ASP.NET Core 内置了依赖注入，使得编写松耦合、可测试的代码变得简单。
4. **中间件**: 在 ASP.NET Core 中，HTTP 请求处理的组件称为中间件。这些中间件是一系列组件，用于处理请求和响应。
5. **配置系统**: ASP.NET Core 提供了一个新的、简单灵活的配置系统，支持多种配置来源，如 JSON 文件、环境变量等。
6. **Kestrel Web 服务器**: ASP.NET Core 附带了一个新的、跨平台的轻量级 Web 服务器 Kestrel，虽然通常在生产环境中与另一个服务器（如 IIS、Nginx 或 Apache）一起使用，但 Kestrel 可以独立运行。
7. **Razor Pages**: 这是一个新的页面模型，用于简化 Web UI 的创建。与 MVC 相似，但更加简化，尤其适合简单的页面。
8. **开源**: ASP.NET Core 是完全开源的，并托管在 GitHub 上。

### 创建Web应用

```c#
//创建新 Web 应用
//-o aspnetcoreapp 参数使用应用的源文件创建名为 aspnetcoreapp 的目录。
dotnet new webapp -o aspnetcoreapp
//信任证书颁发
dotnet dev-certs https --trust
//运行应用
cd aspnetcoreapp
dotnet watch run
```

### ASP.NET.Core 生命周期

##### 1.  瞬时生命周期（Transient）

每次请求 *Transient* 生命周期服务时都会创建它们。此生命周期最适合轻量级、无状态的服务。我们可以使用 **AddTransient** 方法注册 *Transient* 服务

```c#
services.AddTransient<IMyService, MyService>();
```

##### 2.  作用域生命周期（Scoped）

作用域生命周期是介于瞬时生命周期和单例生命周期之间的生命周期。**每次请求都会创建一个新的服务实例，但同一请求内的所有服务实例都是相同的**。这种生命周期适用于那些需要在请求范围内共享状态的服务，例如业务逻辑层（BLL）中的 Service、控制器（Controller）等。

```c#
services.AddScoped<IProductService, ProductService>();
```

##### 3. 单例生命周期（Singleton）

单例生命周期是**最长的生命周期**，整个应用程序只会创建**一个服务实例**。这种生命周期适用于那些需要在整个应用程序中共享状态的服务，例如配置（Configuration）类、缓存（Cache）类等。在 ASP.NET Core 中，可以通过调用 `IServiceCollection.AddSingleton<TService, TImplementation>() `方法将一个服务注册为单例生命周期。

```c#
services.AddSingleton<IMySingletonService, MySingletonService>();
```

整个应用程序**只会创建一个 MySingletonService 实例**。



### 如何选择合适的生命周期
1. 如果服务是无状态的，且不需要在不同请求之间共享状态，应该选择瞬时生命周期。
2. 如果服务需要在同一请求内共享状态，应该选择作用域生命周期。
3. 如果服务需要在整个应用程序中共享状态，应该选择单例生命周期。
4. 如果不确定服务的状态和使用场景，可以选择作用域生命周期作为默认生命周期。

