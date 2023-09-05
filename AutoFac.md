## AutoFac框架

- Autofac是第三方IOC容器，是当前最流行的IOC容器。
- 功能强大，比asp.netcore内置容器强大得多，支持属性注入和方法注入，支持AOP。
- 官网地址：http://autofac.org/
- 源码下载地址：https://github.com/autofac/Autofac


1. Autofac是什么?<br/>
   说到Autofac，我们就要首先了解依赖注入（Dependency Injection，简称DI）1.1节介绍。DI不是什么技术，而是一种设计模式，是用来降低计算机程序之间的耦合的。在.net平台，有很多依赖注入工具，比较于其他的IOC框架，如Spring.NET，Unity，Castle等等所包含的，Autofac是一款较为轻量级的、性能优异的、支持xml配置的依赖注入工具
    - 依赖注入（DI）<br/>
      DI是一种软件设计模式，用来允许我们开发松耦合代码。DI是一种很好的方式去减少软件模块之间的紧耦合关心。DI帮助更好的去管理软件中的功能更新和复杂度。DI的目的是让代码可维护。<br/>
      **Dependency Injection 依赖注入**，将对象依赖的其他对象，通过注入的方式进行初始化。
    - 控制反转（IOC）<br/>
    IOC控制反转模式是对DIP(依赖倒置原则)的一种实现。IOC指的是一种框架或运行时的编程风格，用来控制程序流程。<br/>
     **Inversion of Control 控制反转**，将控制权进行反转，将本由自身控制的对象初始化交由外部IoC容器进行初始化；

**现在我们使用其他的IoC容器框架来替换默认的内置IoC，这里选择使用Autofac框架**

.net core 2.x和3.x 使用`Autofac`注入方式不一样，针对.net core 3.x的使用。首先,我们需要从nuget引用相关的包`Autofac.Extensions.DependencyInjection`(这个包扩展了一些微软提供服务的类.来方便替换`Autofac`)

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

##### 暂时性
每次在向服务容器进行请求时都会创建新的实例，相当于每次都new出一个。
注册方式：使用`InstancePerDependency()`方法标注，如果不标注，这也是默认的选项。
```c#
//不指定，默认就是瞬时的
builder.RegisterType<TransientService>().As<ITransientService>();

//指定其生命周期域为瞬时
builder.RegisterType<TransientService>().As<ITransientService>().InstancePerDependency();
```



##### 作用域内
在每次Web请求时被创建一次实例，生命周期横贯整次请求。即在每个生命周期作用域内是单例的。
注册方式：使用`InstancePerLifetimeScope()`方法标识：
```c#
builder.RegisterType<ScopedService>().As<IScopedService>().InstancePerLifetimeScope();
```

##### 匹配作用域内
即每个匹配的生命周期作用域一个实例。该类型其实是上面的“作用域内”的其中一种，可以对实例的共享有更加精准的控制.。我们通过允许给域“打标签”，只要在这个特定的标签域内就是单例的。
注册方式：使用`InstancePerMatchingLifetimeScope(string tagName)`方法注册：
```c#
//当你开始一个生命周期时, 提供的标签值和它就关联起来了。
var builder = new ContainerBuilder();
builder.RegisterType<Worker>().InstancePerMatchingLifetimeScope("myrequest");
```



##### 全局单例
即全局只有一个实例，即每一个后续请求都使用同一个实例。
注册方式：使用`SingleInstance()`方法标识：

```c#
 builder.RegisterType<SingletonService>().As<ISingletonService>().SingleInstance()
```

### Demo:

* 定义一个Container容器。
* 创建builder，并在builder中注册类型。
* 实例化容器。
* 在需要使用接口的地方，通过container来解析得到一个接口的实例。

```c#
//定义一个接口
public interface IAnimal
{
    void DogCall();
    void CatCall();
}

//写一个类去继承
public class AnimalsClass : IAnimal
{
    public void CatCall()
    {
        Console.WriteLine("test1");
    }

    public void DogCall()
    {
        Console.WriteLine("test2");
    } 
}


static void Main(string[] args)
{
    //创建一个IOC容器
    var builder = new ContainerBuilder();
    //通过AS可以让AnimalsClass类中通过构造函数依赖注入类型相应的接口。
    builder.RegisterType<AnimalsClass>().As<IAnimal>();
    //Build()方法生成一个对应的Container实例，这样，就可以通过Resolve解析到注册的类型实例。
    using (var container = builder.Build())
    {
        //当注册的类型在相应得到的容器中可以Resolve你的AnimalsClass类中所有实例。
        var call = container.Resolve<IAnimal>();
        call.DogCall();
        call.CatCall();
    }

    Console.ReadLine();
}

//终端打印
//test1
//test2
```





### 参考资料

1. [AutoFac思维导图](https://www.processon.com/view/link/6072ed8863768912ae50b483#map)
2. [AutoFac 框架初识与应用](https://www.cnblogs.com/i3yuan/p/14654547.html)
3. [Autofac详解](https://admans.blog.csdn.net/article/details/125736127?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-2-125736127-blog-79784947.235%5Ev38%5Epc_relevant_default_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-2-125736127-blog-79784947.235%5Ev38%5Epc_relevant_default_base3&utm_relevant_index=3)
4. [什么是依赖注入(DI)和控制反转(IOC)](https://www.cnblogs.com/sheng-jie/p/6512909.html)
5. [.Net Core中Autofac的使用方法](https://blog.csdn.net/xiaouncle/article/details/88701770?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-88701770-blog-125736127.235%5Ev38%5Epc_relevant_default_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-88701770-blog-125736127.235%5Ev38%5Epc_relevant_default_base3&utm_relevant_index=2)

