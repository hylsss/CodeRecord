## c# 委托

委托（Delegate）特别用于实现事件和回调方法。所有的委托（Delegate）都派生自** **System.Delegate** **类。

#### 声明委托（Delegate）

委托声明决定了可由该委托引用的方法，委托可指向一个与其具有相同标签的方法。

```c#
// 声明委托的语法：
// return type：这是委托指向的方法的返回类型。
// delegate-name：这是委托的名称。
// parameter list：这是委托指向的方法的参数列表。
delegate <return type> <delegate-name> <parameter list>
```

##### 如何理解委托指向一个与委托具有相同标签的方法
委托可以指向一个与其具有相同标签的方法时，我们是指该方法的**返回类型和参数列表**必须与委托的声明**相匹配**。换句话说，**方法的签名必须与委托的签名相匹配**。

```c#
// 委托声明
public delegate void MyDelegate(int a, string b);
// 声明的委托可以指向SomeMethod方法
SomeMethod
public void SomeMethod(int number, string text) { ... }
//不能指向AnotherMethod方法，
public void AnotherMethod(string text, int number) { ... }
```



#### 实例化委托

实例化一个委托就是创建一个该委托类型的对象,用于封装特定的方法。

实例化委托通常有两种方式:

- 使用新的关键字直接创建:delegate int MyDelegate(string s);
- 使用已有的方法来初始化:MyDelegate md = new MyDelegate(Method);

```c#
   //委托声明
    delegate string printString(string s);
    static string WriteToScreen(string txt)
    {
        Console.WriteLine(txt);
        return txt;
    }
    
    static void Main()
    {
       //实例化委托，该委托可用于引用带有一个string类型的WriteToScreen
        printString ps1 = new printString(WriteToScreen);
        ps1("打印一下实例化委托方法");
    }
    //终端打印
    // 打印一下实例化委托方法
```

#### 委托多播

委托对象可使用 **"+" **运算符进行合并。一个合并委托调用它所合并的两个委托。只有相同类型的委托可被合并。**"-"** 运算符可用于从合并的委托中移除组件委托。可以创建一个委托被调用时要调用的方法的调用列表。这被称为委托的 **多播（multicasting）**，也叫组播。

```C#
 delegate string printString(string s);
 static string WriteToScreen(string txt)
 {
     Console.WriteLine(txt+"WriteToScreen");
     return txt;
 }
 
 static string WriteToNum(string txt)
 {
     Console.WriteLine(txt+"WriteToNum");
     return txt;
 }
 
 static void Main()
 {
     printString obj;
     printString ps1 = new printString(WriteToScreen);
     printString ps2= new printString(WriteToNum);
     obj = ps1;
     obj += ps2;
     obj("打印一下实例化委托方法");
 }

//终端打印
//打印一下实例化委托方法WriteToScreen
//打印一下实例化委托方法WriteToNum
```

