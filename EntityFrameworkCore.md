## EntityFrameworkCore  框架

**Entity Framework Core就是一个ORM，什么是ORM？**   
Entity Framework Core能把C#里的类映射到数据库里的表，然后属性就映射到字段上。



### 安装 Entity Framework Core

- Microsoft.EntityFrameworkCore.SqlServer （适用于EF Core SQL Server 提供程序）

- Microsoft.EntityFrameworkCore.Design（适用于EF Core .NET Core CLI 工具 ）

- Microsoft.EntityFrameworkCore.Tools（适用于 EF Core 的包管理器控制台工具）


---

### 创建实体类
数据库上下文类是为给定数据模型协调 EF Core 功能的主类。 上下文派生自`Microsoft.EntityFrameworkCore.DbContext`。 上下文指定数据模型中包含哪些实体。通过运动员,联赛,俱乐部几个类来简单表明一对多的关系

#### 一对多关系

```C#
public class League
{
    public int Id { get; set; }
    [MaxLength(100)]  //最大长度为100
    public string Name { get; set; }
    [Required,MaxLength(50)] //Required为必填
    public string Country { get; set; }
}

 public  class Player
 {
     public int Id { get; set; }

     public string Name { get; set; }

     public DateTime DateOfBirth { get; set; }

 }
//在Club看出关联
public  class Club
{
    public Club() 
    {
        Players = new List<Player>();
    }

    public int Id { get; set; }

    public string Name { get; set; }

    public string City { get; set; }
    [Column(TypeName="date")]//声明后数据库中该字段对应的类型就为date
    public DateTime DateOfEstablishment { get; set; }

    public string History { get; set; }
  
    //定义了一个名为League的League类型属性，表示与League实体的关联。//
    public League League { get; set; }
    //定义了一个名为Players的List<Player>类型属性，表示与Player实体的关联。
    public List<Player> Players { get; set; }
}

```

`Club`模型中体现出来了，足球队中有个**public League League { get; set; }** 表明一个足球队必须对应一个联赛，反过来一个联赛中也可以有多个足球队。**如果你不指定外键关联的话，EFcore会自动通过模型关系生成对应的外键关联。**

#### 多对多关系 

现在在上面的模型基础上，我们在建立一个比赛（Game）模型。一个队员可以对应多场比赛，一场比赛可以由多个队员参加，这种多对多的关系，EF Core是实现不了的，此时我们可以通过加入一个中间表`GamePlayer`来间接的去实现多对多的关系，一个队员可以参加多场比赛也就是对应多个`GamePlayer`而一场比赛又可以由多个队员参加相当于对应多个`GamePlayer`，此时就间接的实现了多对多的关系。  
```c#
 public class Game
    {
        public Game() 
        {
            GamePlayers = new List<GamePlayer>();

        }


        // 约定 取名叫ID的都是主键。或者加【key】
        public int Id { get; set; }
        [Display(Name ="场数")]
        public int Round { get; set; }
        [Display(Name = "开赛时间")]  //加问好表示对应的数据库中的字段是可空的 DateTimeOffset是值类型
        public DateTimeOffset? StarTime { get; set; }

        public List<GamePlayer> GamePlayers { get; set; }

    }

  public class GamePlayer
    {
        //GamePlayer的主键在DBContext文件中OnModelCreating方法中设置
        public int PlayerId { get; set; }

        public int GameId { get; set; }



        //在GamePlayer中体现一对多的关系   一场比赛有多个队员  一个队员参加多场比赛
        public Game Game { get; set; }

        public Player Player { get; set; }
    }

  public  class Player
    {

        public Player() 
        {
            //初始化，防止出现空引用异常
            GamePlayers = new List<GamePlayer>();
        }
        public int Id { get; set; }

        public string Name { get; set; }

        public DateTime DateOfBirth { get; set; }

        //=====导航属性
        public List<GamePlayer> GamePlayers { get; set; }

    }

```

GamePlayer添加联合主键,在DBContext文件中OnModelCreating方法中设置

```c#
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    //设置联合主键GamePlayer的主键=PlayerId+GameId
    //如果主键由多个属性组成，则指定一个匿名类型，包括属性 (post = > new {post.Title,post.BlogId}) 。
    modelBuilder.Entity<GamePlayer>().HasKey(x=>new { x.PlayerId,x.GameId});
}

```

#### 一对一关系

```c#
 public class Resume
 {
     public int Id { get; set; }

     public string Description { get; set; }
     //相当于球员表的外建，与Player类的Id字段关联。
     public int PlayerId { get; set; }
     //导航属性
     public Player Player { get; set; }

 }


public class Player
{
    public int Id { get; set; }
    public string Name { get; set; }
    public int Age { get; set; }

    // 导航属性
    public Resume Resume { get; set; }
}

protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Resume>()
        .HasOne(p => p.Player)//这句话意思就是一份简历对应一个球员
        .WithOne(r => r.Resume)//一个球员又带着一份简历
        .HasForeignKey<Resume>(r => r.PlayerId);//这句话意思就是一份简历有一个外键关联着PlayerId
}
```

这里`Entity`里面依赖的实体不管是`Resume`还是`Player`都可以，如果是`Player`把对应的关系换一下就可以。这样一对一的关系就建立完成。



### 创建上下文类

##### `ApplicationDbContext `类必须公开具有 `DbContextOptions` 参数的公共构造函数。 这是将` AddDbContext `的上下文配置传递到 DbContext 的方式。

```c#
public BloggingContext(DbContextOptions<BloggingContext> options) : base(options)
{
        
}

//BloggingDbContext可以通过构造函数注入在 ASP.NET Core 控制器或其他服务中使用
[ApiController]
[Route("api/[controller]")]
public class HomeController : Controller
{

    private readonly BloggingContext _context;
            
    public  HomeController(BloggingContext context)
    {
        _context = context;
    }
}



```

通过上下文中的`DbSet`属性将我们的模型加入上下文中，并且暴露成`DbSet类型`

```c#
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options) { }
    public DbSet<League> Leagues { get; set; }
    public DbSet<Club> Clubs { get; set; }
    public DbSet<Player> Players { get; set; }
}
```
###### 映射数据库
``` c#
"ConnectionStrings": {
   //两种连接方式都可以  一种weindows验证  一种是sa用户
 //"DefaultConnection": "Server=.;Database=EFCoreDb;Trusted_Connection=True;MultipleActiveResultSets=true"
    "DefaultConnection": "Server=127.0.0.1; Database=EFCoreDb; Persist Security Info=True;User ID=sa;Password=123;Packet Size=512;"
  }
```
######  在Startup类的ConfigureServices方法下注入数据库上下文依赖

```c#
services.AddDbContext<AppDbContext>(optionsAction => 
      optionsAction.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));
```



## 使用 fluent API 配置模型

可在派生上下文中替代 `OnModelCreating` 方法，并使用 Fluent API 来配置模型。 此配置方法最为有效，并可在不修改实体类的情况下指定配置。 Fluent API 配置具有最高优先级，并将替代约定和数据注释。 配置按调用方法的顺序应用，如果存在任何冲突，最新调用将替代以前指定的配置。

```c#
using Microsoft.EntityFrameworkCore;

namespace EFModeling.EntityProperties.FluentAPI.Required;

internal class MyContext : DbContext
{
    public DbSet<Blog> Blogs { get; set; }

    #region Required
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Blog>()
            .Property(b => b.Url)
            .IsRequired();
    }
    #endregion
}

public class Blog
{
    public int BlogId { get; set; }
    public string Url { get; set; }
}
```





### 学习资料

- [EntityFrameworkCore的使用教程](https://huaweicloud.csdn.net/63357939d3efff3090b58448.html?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Eactivity-1-121281103-blog-117927907.235%5Ev38%5Epc_relevant_default_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Eactivity-1-121281103-blog-117927907.235%5Ev38%5Epc_relevant_default_base3&utm_relevant_index=2)
- [EntityFrameworkCore应用举例](https://blog.csdn.net/gy0124/article/details/117927907?spm=1001.2101.3001.6650.4&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-4-117927907-blog-111246549.235%5Ev38%5Epc_relevant_default_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-4-117927907-blog-111246549.235%5Ev38%5Epc_relevant_default_base3&utm_relevant_index=5)
- [EFCore 6.0入门](https://www.cnblogs.com/Mamba8-24/p/16098812.html)
- [EFCore 创建并配置模型](https://learn.microsoft.com/zh-cn/ef/core/modeling/)