## c# 事件 event

事件是一种特殊的`多播委托`，仅可以从**声明事件的类或结构中对其进行调用**，事件的主要目的是允许一个类或对象通知其他类或对象发生了某种行为或状态的改变。类似一个封装机制，确保时间只能在拥有改事件的对象来触发，不会被外部对象随意触发。

在C#中，事件是一种特殊类型的委托，通常用于实现发布-订阅模式。

```c#
using System;

namespace ProjectIna
{
    public delegate void GreetingDelegate(string name); // 委托声明
   //相当于发布
    public class GreetingManager
    {
        // 定义一个事件，类型为GreetingDelegate
       //声明一个事件类似于声明一个进行了封装的委托类型的变量而已。
        public event GreetingDelegate GreetingEvent;

        // 触发事件的方法
        public void GreetingLanguage(string name)
        {
            GreetingEvent?.Invoke(name); // 如果有订阅者，则触发事件
        }
    }

    class Program
    {
        private static void GreetingEnglish(string name)
        {
            Console.WriteLine("Good morning, " + name);
        }

        private static void GreetingChinese(string name)
        {
            Console.WriteLine("早上好，" + name);
        }

        static void Main(string[] args)
        {
            GreetingManager language = new GreetingManager(); // 实例化GreetingManager类

            // 订阅事件
            language.GreetingEvent += GreetingEnglish;
            language.GreetingEvent += GreetingChinese;

            // 触发事件
            language.GreetingLanguage("Alina");

            // 输出GreetingManager对象的信息（通常不需要）
            Console.WriteLine(language);
        }
    }
}


```

`GreetingManager` 类定义了一个名为 `GreetingEvent` 的事件。然后，`Program` 类中的 `Main` 方法订阅了这个事件，并分别添加了 `GreetingEnglish` 和 `GreetingChinese` 方法作为事件处理程序。

当调用 `GreetingLanguage` 方法时，它会触发 `GreetingEvent` 事件，从而执行所有订阅了该事件的方法。

这样，可以轻松地添加或删除其他语言的问候，而不需要修改 `GreetingManager` 类的代码，实现了解耦。

