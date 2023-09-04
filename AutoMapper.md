## AutoMapper框架

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
   //或者cfg.AddProfile(new LoginMapping());
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

- `SourceMemberNamingConvention` 表示源类型命名规则 **（蛇形命名法）**

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
var configuration = new MapperConfiguration(cfg =>
{
    cfg.RecognizePrefixes("before");//前缀
    cfg.RecognizePostfixes("after");//后缀
    cfg.CreateMap<Src03,Dest03>();
});
var mapper = configuration.CreateMapper();
var dest = mapper.Map<Dest03>(new Src03() { Nameafter = "zhangsan", beforeAge = 18 });

```

```c#
cfg.ClearPrefixes();//清除所有前缀
```

##### 控制映射字段和属性范围

```c#
//ShouldMapField设置字段映射范围，ShouldMapProperty设置属性范围
var configuration = new MapperConfiguration(cfg => {
    cfg.ShouldMapField = fi => false;
    cfg.ShouldMapProperty = pi => pi.GetMethod != null && (pi.GetMethod.IsPublic || pi.GetMethod.IsPrivate);
});

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

`AutoMapper` 会自动找到相应的构造函数调用。如果在构造函数中对参数做一些改变的话，其改变会反应在映射结果中。

##### 禁用构造函数映射：

禁用构造函数映射的话，目标类要有一个无参构造函数。

```c#
var config = new MapperConfiguration(cfg => cfg.DisableConstructorMapping());
```

#### 映射

##### 数组和列表映射

```c#
public class Source  
{  
    public int Value { get; set; }  
    public int Percent { get; set; }  
}  
  
public class Destination  
{  
    public int Value { get; set; }  
}

var sources = new[]  
{  
    new Source { Value = 5, Percent = 50 },  
    new Source { Value = 6, Percent = 50 },  
    new Source { Value = 7, Percent = 50 }  
};  
  
var iEnumerableDest = mapper.Map<Source[], IEnumerable<Destination>>(sources);  
var iCollectionDest = mapper.Map<Source[], ICollection<Destination>>(sources);  
var iListDest = mapper.Map<Source[], IList<Destination>>(sources);  
var listDest = mapper.Map<Source[], List<Destination>>(sources);  
var arrayDest = mapper.Map<Source[], Destination[]>(sources);
```

支持的源集合类型包括：

- `IEnumerable`

- `IEnumerable<T>`

- `ICollection`

- `ICollection<T>`

- `IList`

- `IList<T>`

- `List<T>`

- `Arrays`

##### 字段相同的会自动映射

假如某个成员的名称为NameAAA，则名为NameAAA的field，与名为NameAAA的property，与名为GetNameAAA的方法，三者之间可以**自动相互映射**

```c#
var configuration = new MapperConfiguration(cfg =>
{
    cfg.CreateMap<Dest01, Src01>();
});
var mapper = configuration.CreateMapper();
var dest = mapper.Map<Dest01>(new Src01() { Name = "zhangsan", Age = 18 });

```

##### 字段不同要手动配置映射
同一个字段的映射，后面的会覆盖前面的，不同的字段，没有做映射的，不会进行赋值

```c#
var configuration = new MapperConfiguration(cfg =>
{
    cfg.CreateMap<Src02, Dest02>()
    .ForMember(dest => dest.NameDest, opt => opt.MapFrom(src => src.NameSrc));
});
var mapper = configuration.CreateMapper();
var dest = mapper.Map<Dest02>(new Src02() { NameSrc = "zhangsan" });
```

#####  内部类嵌套类映射

类内部嵌套一个类，需要将嵌套的类也进行映射

```c#
public class SrcOuter
{
    public string OutName { get; set; }
    public int OutAge { get; set; }
    public SrcInner Inner { get; set; }
}
public class SrcInner
{
    public string Name { get; set; }
    public int Age { get; set; }
}
public class DestOuter
{
    public string OutName { get; set; }
    public int OutAge { get; set; }
    public DestInner Inner { get; set; }
}
public class DestInner
{
    public string Name { get; set; }
    public int Age { get; set; }
}

var configuration = new MapperConfiguration(cfg =>
{
    cfg.CreateMap<SrcOuter, DestOuter>();
    cfg.CreateMap<SrcInner, DestInner>();
});
var mapper = configuration.CreateMapper();
var dest = mapper.Map<DestOuter>(new SrcOuter(){OutName = "zhangsan",OutAge = 18,Inner = new SrcInner() { Name = "lisi", Age = 20 }});

```

##### 条件映射

符合某些条件时才映射Condition方法会在MapFrom方法后判断,PreCondition会在MapFrom前判断。

```c#
var configuration = new MapperConfiguration(cfg =>
{
    cfg.CreateMap<SrcCondition, DestCondition>()
    //src.Name.Length>=3&&(src.Name+"XXX").Length >= 5 两个条件都满足才映射
    .ForMember(dest => dest.Name, opt => opt.PreCondition(src => src.Name.Length >= 3))
    .ForMember(dest => dest.Name, opt => opt.MapFrom(src => src.Name + "XXX"))
    .ForMember(dest => dest.Name, opt => opt.Condition(src => src.Name.Length >= 5))
    //src.Age <= 15&&src.Age * 3>=30 两个条件都满足才映射
    .ForMember(dest => dest.Age, opt => opt.PreCondition(src => src.Age <= 15))
    .ForMember(dest => dest.Age, opt => opt.MapFrom(src => src.Age * 3))
    .ForMember(dest => dest.Age, opt => opt.Condition(src => src.Age >= 30));
});
var mapper = configuration.CreateMapper();
var dest = mapper.Map<DestCondition>(new SrcCondition() { Name = "zhangsan", Age = 18 });

```

##### 空值处理

```c#
//给个默认值 
cfg.CreateMap<Src01, Dest01>()
    .ForMember(dest => dest.Name, opt => opt.NullSubstitute("XXX"));
```

##### 映射反转

ReverseMap一般在Create[Map方法](https://so.csdn.net/so/search?q=Map方法&spm=1001.2101.3001.7020)或者ForMember等方法之后，相当于src和dest根据你自己的配置反向映射

```c#
cfg.CreateMap<Order, OrderDto>().ReverseMap();
//等同于以下两句
cfg.CreateMap<Order,OrderDto>();
cfg.CreateMap<OrderDto,Order>();

//反向映射可以用ForPath配置
cfg.CreateMap<Order, OrderDto>()
  .ForMember(d => d.CustomerName, opt => opt.MapFrom(src => src.Customer.Name))
  .ReverseMap()
  .ForPath(s => s.Customer.Name, opt => opt.MapFrom(src => src.CustomerName));

```



- `VO`(`View Object`)：视图对象，用于展示层，它的作用是把某个指定页面(或组件)的所有数据封装起来。
- `DTO`(`Data Transfer Object`)：数据传输对象，泛指用于展示层与服务层之间的数据传输对象。
- `DO`(`Domain Object`)：领域对象，就是从现实世界中抽象出来的有形或无形的业务实体。
- `PO`(`Persistent Object`)：持久化对象，它跟持久层(通常是[关系型数据库](https://cloud.tencent.com/product/cdb-overview?from_column=20065&from=20065))的数据结构形成一一对应的映射关系，如果持久层是关系型[数据库](https://cloud.tencent.com/solution/database?from_column=20065&from=20065)，那么，数据表中的每个字段(或若干个)就对应`PO`的一个(或若干个)属性。
- `DAO`(`Data Access Object`):数据访问对象，主要用来封装对数据库的操作。



### 参考资料

[映射框架AutoMapper](https://www.cnblogs.com/bigbox777/p/14414594.html)
[AutoMapper](https://blog.csdn.net/liyou123456789/article/details/125222690?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522169379076516800197063596%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=169379076516800197063596&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-125222690-null-null.142^v93^insert_down1&utm_term=AutoMapper&spm=1018.2226.3001.4187)
