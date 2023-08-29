### ASP.NET.Core控制器 （Controller）

在 ASP.NET Core 中，控制器（Controller）是** MVC（Model-View-Controller）** 架构中的一个关键组成部分，负责处理来自客户端的请求并返回响应。控制器是一个包含一组方法（通常称为“操作”或“动作”）的 C# 类，这些方法用于处理不同类型的**HTTP请求 ** （如 GET、POST、PUT、DELETE 等）。

#### MVC框架概述

`ASP.NET Core MVC` 是使用模型-视图-控制器`（Model-View-Controller）`设计模式构建网页应用与 API 的丰富的框架。

- 模型（Model）：模型是应用程序的数据访问层，负责与数据库交互、执行业务逻辑、以及数据验证。
- 视图（View）：视图是用户界面的表示，通常是 HTML、CSS 和 JavaScript 的组合。在 ASP.NET Core MVC 中，视图通常使用 Razor 语法来动态生成 HTML。
- 控制器（Controller）：控制器是 MVC 架构中的中央协调者，负责接收 HTTP 请求、处理用户输入、与模型交互，并返回视图或数据。




```c#
using Microsoft.AspNetCore.Mvc;

namespace Practise.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}

```

1. **继承自 `Controller` 类**：在 ASP.NET Core 中，控制器通常继承自 `Microsoft.AspNetCore.Mvc.Controller` 类。
2. **命名约定**：控制器的类名通常以 "Controller" 结尾（如 `HomeController`、`AccountController` 等）。



### 控制器的种类

1. **API 控制器**：用于构建 RESTful API，通常继承自 `ControllerBase` 类而不是 `Controller` 类。
2. **视图控制器**：用于构建返回 HTML 视图的 Web 应用程序。
3. **混合控制器**：既可以返回 API 响应也可以返回视图，通常继承自 `Controller` 类。
