## AutoFac框架

- Autofac是第三方IOC容器，是当前最流行的IOC容器。
- 功能强大，比asp.netcore内置容器强大得多，支持属性注入和方法注入，支持AOP。
- 官网地址：http://autofac.org/
- 源码下载地址：https://github.com/autofac/Autofac


1. Autofac是什么?
   说到Autofac，我们就要首先了解依赖注入（Dependency Injection，简称DI）1.1节介绍。DI不是什么技术，而是一种设计模式，是用来降低计算机程序之间的耦合的。在.net平台，有很多依赖注入工具，比较于其他的IOC框架，如Spring.NET，Unity，Castle等等所包含的，Autofac是一款较为轻量级的、性能优异的、支持xml配置的依赖注入工具
    - 依赖注入（DI）
    DI是一种软件设计模式，用来允许我们开发松耦合代码。DI是一种很好的方式去减少软件模块之间的紧耦合关心。DI帮助更好的去管理软件中的功能更新和复杂度。DI的目的是让代码可维护。
    - 控制反转（IOC）
    　IOC控制反转模式是对DIP(依赖倒置原则)的一种实现。IOC指的是一种框架或运行时的编程风格，用来控制程序流程。

---

#### 容器创建对象

```c#
//创建一个容器建造者
ContainerBuilder containerBuilder = new ContainerBuilder();
//注册普通类
containerBuilder.RegisterType<Honer>();
//build一下，得到一个容器
IContainer container = containerBuilder.Build();
//可以基于容器来获取对象的实例
Honer phone = container.Resolve<Honer>();
```

#### 注册普通类

```c#
ContainerBuilder containerBuilder = new ContainerBuilder();
containerBuilder.RegisterType<Honer>();

IContainer container = containerBuilder.Build();
Honer phone = container.Resolve<Honer>();
```

#### 注册抽象与实现

```c#
ContainerBuilder containerBuilder = new ContainerBuilder();
containerBuilder.RegisterType<Honer>().As<IPhone>();
IContainer container = containerBuilder.Build();
IPhone phone = container.Resolve<IPhone>();
```

#### 注册程序集

- RegisterAssemblyTypes() ：接收包含一个或多个程序集的数组作为参数
- RegisterAssemblyModules() : 接收模块作为参数，进行模块扫描注册
- PublicOnly() ：指定公有方法被注册
- Where() ：要过滤注册的类型
- Except() ：要排除的类型
- As() ：反射出其实现的接口
- AsImplementedInterfaces() ： 自动以其实现的所有接口类型暴露（包括IDisposable接口）

```c#
var assemblies = Assembly.GetExecutingAssembly();

builder.RegisterAssemblyTypes(assemblies)//程序集内所有具象类 
.Where(c => c.Name.EndsWith("Service"))
.PublicOnly()//只要public访问权限的
.Where(cc => cc.IsClass)//只要class型（主要为了排除值和interface类型） 
.AsImplementedInterfaces();//自动以其实现的所有接口类型暴露（包括IDisposable接口）

```
---

###   注入方式

##### 1.  构造函数注入
默认支持，无法用特性进行筛选，默认选参数最多的构造函数进行注入
```c#
ContainerBuilder containerBuilder = new ContainerBuilder();
containerBuilder.RegisterType<Honer>().As<IPhone>();
containerBuilder.RegisterType<Teacher>().As<ITeacher>();
containerBuilder.RegisterType<Student>().As<IStudent>();
IContainer container = containerBuilder.Build();
ITeacher teacher = container.Resolve<ITeacher>();
```

##### 2.  全部属性注入
关键词`PropertiesAutowired`，这个对象所有属性全部注入
```c#
ContainerBuilder containerBuilder = new ContainerBuilder();
containerBuilder.RegisterType<Honer>().As<IPhone>();
containerBuilder.RegisterType<Teacher>().As<ITeacher>().PropertiesAutowired();
containerBuilder.RegisterType<Student>().As<IStudent>();
IContainer container = containerBuilder.Build();
ITeacher teacher = container.Resolve<ITeacher>();
```

##### 3.  标记特性的属性注入
关键词`PropertiesAutowired`，定义特性选择器`CustomPropertySelector`
```c#
ContainerBuilder containerBuilder = new ContainerBuilder();
containerBuilder.RegisterType<Honer>().As<IPhone>();
containerBuilder.RegisterType<Teacher>().As<ITeacher>().PropertiesAutowired(new CustomPropertySelector());
containerBuilder.RegisterType<Student>().As<IStudent>();
IContainer container = containerBuilder.Build();
ITeacher teacher = container.Resolve<ITeacher>();
```
##### 4.  方法注入
关键词`OnActivated`，指定调用方法
```c#
ContainerBuilder containerBuilder = new ContainerBuilder();
containerBuilder.RegisterType<Honer>().As<IPhone>();
containerBuilder.RegisterType<Teacher>().As<ITeacher>()
    .OnActivated(p =>
    {
        p.Instance.SetStudent1(p.Context.Resolve<IStudent>());
    });
containerBuilder.RegisterType<Student>().As<IStudent>();
IContainer container = containerBuilder.Build();
ITeacher teacher = container.Resolve<ITeacher>();
```

### 生命周期

![image-20210410161115561](https://github.com/hylsss/CodeRecord/assets/62007319/e8cac6b5-aa8a-4692-bac7-4c9ab81c22cc)
