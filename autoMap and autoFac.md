## autoMap框架

AutoMapper是一个对象-对象映射器。对象-对象映射通过将一种类型的输入对象转换为另一种类型的输出对象来工作。  基于命名约定的对象到对象的映射工具，只要2个对象的属性具有相同的名字（或者符合它规定的命名规定），`AutoMapper`就可以帮我们自动在2个对象间进行属性值的映射。  
简单来说：`AutoMapper` 是一个对象-对象映射器，可以将一个对象映射到另一个对象。  

如果不符合约定的属性，就需要自定义映射行为，需要告诉`AutoMapper`,在使用`Map`进行映射之前，必须使用` CreateMap() `进行配置  
**注意：将源映射到目标时，`AutoMapper` 将忽略空引用异常，可以通过自定义解析器来更改这种设置。**     

![WechatIMG270](https://github.com/hylsss/CodeRecord/assets/62007319/6070b674-16fb-4281-8f57-acda5673cfc1)
1. Source Object:映射的原始对象
2. Destination Object:需要映射到的新对象
3. AutoMapper:执行实际映射工作的框架
4. Configuration: 在使用 `AutoMapper` 之前，您需要配置映射规则。这通常在应用程序的启动代码中完成。

***

##### demo

```c#
public class Foo
{
    public int ID { get; set; }

    public string Name { get; set; }
}

public class FooDto
{
    public int ID { get; set; }

    public string Name { get; set; }
}


```

注意:**经验法则是一个应用程序域AppDomian只需要一个AutoMapper配置对象**，简单来说就是`Startup.cs` 文件的 `ConfigureServices` 方法中，或在控制台应用的 `Main` 方法中）创建和配置一个 `MapperConfiguration` 实例，并将这个实例在应用程序的其他部分中重用

### 注册

`MapperConfiguration` 配置映射规则

```c#
public void Map()
{
  //使用Map方法之前，首先要告诉AutoMapper是从什么类映射到什么类
  //Foo 类型的对象转换为 FooDto 类型的对象。
    var config = new MapperConfiguration(cfg => cfg.CreateMap<Foo, FooDto>());

    var mapper = config.CreateMapper();
   //进行对象的转换
    Foo foo = new Foo { ID = 1, Name = "Tom" };

    FooDto dto = mapper.Map<FooDto>(foo);
}
```

#### Profile

`Profile` 是组织映射的另一种方式。新建一个类，继承 `Profile`，并在构造函数中配置映射。

```c#
//Mappings文件下的LoginMapping
public class LoginMapping : Profile
{
    public LoginMapping()
    {
        CreateMap<UserAccount, LoginDto>();
    }
}
//注册
var config = new MapperConfiguration(cfg =>
{
  //将LoginMapping添加到MapperConfiguration的配置中
    cfg.AddProfile<LoginMapping>();
});
```

将映射关系添加到`Profile`，再加载`Profile`，类似于模块化分割业务，让项目结构更加清晰

```c#
var config = new MapperConfiguration(cfg =>
{
    // 扫描当前程序集
    cfg.AddMaps(System.AppDomain.CurrentDomain.GetAssemblies());
    
    // 也可以传程序集名称（dll 名称）
    cfg.AddMaps("LibCoreTest");
});
```

AutoMapper 也可以在指定的程序集中扫描从 `Profile` 继承的类，并将其添加到配置中。

***

### 配置

##### 命名约定

默认情况下，`AutoMapper` 基于相同的字段名映射，并且是 **不区分大小写** 的。

- `SourceMemberNamingConvention` 表示源类型命名规则**（蛇形命名法）**

- `DestinationMemberNamingConvention` 表示目标类型命名规则 **（驼峰命名法）**

需要指定命名规则，使其能正确映射。

##### 配置可见性

默认情况下，AutoMapper 仅映射 `public` 成员，但其实它是可以映射到 `private` 属性的。

```c#
var config = new MapperConfiguration(cfg =>
{
    cfg.ShouldMapProperty = p => p.GetMethod.IsPublic || p.SetMethod.IsPrivate;
    cfg.CreateMap<Source, Destination>();
});
```

##### 全局属性/字段过滤

AutoMapper 尝试映射每个公共属性/字段。以下配置将忽略字段映射。

```c#
var config = new MapperConfiguration(cfg =>
{
	cfg.ShouldMapField = fi => false;
});
```

##### 替换字符

```c#
var config = new MapperConfiguration(cfg =>
{
    cfg.ReplaceMemberName("Ä", "A");
});
```

##### 识别前缀和后缀

```c#
var config = new MapperConfiguration(cfg =>
{
    cfg.RecognizePrefixes("My");
    cfg.RecognizePostfixes("My");
}
```

##### 调用构造函数

有些类，属性的 `set` 方法是私有的。

```c#
public class Commodity
{
    public string Name { get; set; }

    public int Price { get; set; }
}

public class CommodityDto
{
    public string Name { get; }

    public int Price { get; }

    public CommodityDto(string name, int price)
    {
        Name = name;
        Price = price * 2;//映射后 Price会乘 2。
    }
}
```

AutoMapper 会自动找到相应的构造函数调用。如果在构造函数中对参数做一些改变的话，其改变会反应在映射结果中。

##### 禁用构造函数映射：

禁用构造函数映射的话，目标类要有一个无参构造函数。

```c#
var config = new MapperConfiguration(cfg => cfg.DisableConstructorMapping());
```

