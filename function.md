## 函数

C# 中的函数（也可以称为方法）是一段具有签名（由函数名、参数类型和参数修饰符组成的函数信息）的代码块，可以用来实现特定的功能。组成部分 `权限修饰符`，`返回值类型`,  `函数名称`, `参数列表`, `函数主体`

#### 无参数构造函数

```c#
public void HandleTxt()
{
   Console.WriteLine('没有返回值的函数');
}
```

#### 有参数没有返回值的函数

```c#
public void HandleTxt(string message)
{
   Console.WriteLine(message);
}
```

#### 有参数且有返回值的函数

```c#
/*
 * 定义一个函数，该函数可以接收一个字符串参数，
 * 并返回一个字符串
 */
public string HandleTxt(string message)
{
   string txt = message;
   return txt
}
```

#### 类中的静态函数

```c#
static string HandleTxt1(string message)
{
    string str = message;
    return str;
}

```

## 构造函数

构造函数就是与类（或结构体）具有相同名称的成员函数，它在类中的地位比较特殊，不需要我们主动调用，当创建一个类的对象时会自动调用类中的构造函数。在程序开发的过程中，我们通常使用类中的构造函数来初始化类中的成员属性。

#### 实例构造函数

构造函数是一种方法，其名称与其类型的名称相同。 其方法签名仅包含可选[访问修饰符](https://learn.microsoft.com/zh-cn/dotnet/csharp/programming-guide/classes-and-structs/access-modifiers)、方法名称和其参数列表；它不包含返回类型。 以下示例演示一个名为 `Person` 的类的构造函数。

```c#
public class Person
{
   private string last;
   private string first;

   public Person(string lastName, string firstName)
   {
      last = lastName;
      first = firstName;
   }
}
```

#### 私有构造函数

私有构造函数是一种特殊的实例构造函数。 它通常用于只包含静态成员的类中。 如果类具有一个或多个私有构造函数而没有公共构造函数，则其他类（除嵌套类外）无法创建该类的实例

```C#
class NLog
{
    // Private Constructor:
    private NLog() { }

    public static double e = Math.E;  //2.71828...
}
```

#### 静态构造函数

静态构造函数用于初始化任何[静态](https://learn.microsoft.com/zh-cn/dotnet/csharp/language-reference/keywords/static)数据，或执行仅需执行一次的特定操作。 将在创建第一个实例或引用任何静态成员之前自动调用静态构造函数。 静态构造函数最多调用一次。

```c#
class SimpleClass
{
    static readonly long baseline;

    static SimpleClass()
    {
        baseline = DateTime.Now.Ticks;
    }
}
```

有多个操作在静态初始化时执行。 这些操作按以下顺序执行：

1. 静态字段设置为 0。 这通常由运行时来完成。
2. 静态字段初始值设定项运行。 派生程度最高类型的静态字段初始值设定项运行。
3. 基类型静态字段初始值设定项运行。 以直接基开头从每个基类型到  `System.Object` 的静态字段初始值设定项。基本静态构造函数运行。 以 `Object.Object` 开头从每个基类到直接基类的任何静态构造函数。
4. 基本静态构造函数运行。 以 Object.Object 开头从每个基类到直接基类的任何静态构造函数。
5. 静态构造函数运行。 该类型的静态构造函数运行



