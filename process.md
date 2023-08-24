## 进程和线程

1. **进程** 是一种正在执行的程序，是操作系统的一个基本概念，可以简单理解为“正在运行的程序”。进程之间是相互独立的，利用[Process类](https://so.csdn.net/so/search?q=Process类&spm=1001.2101.3001.7020)可启动、停止本机或远程进程，进程有着「**运行 - 暂停 - 运行**」的活动规律，暂停时会记录**当前进程中运行的状态信息，以备下次切换回来的时候可以恢复执行。**

2. **线程** 上下文包含线程顺畅继续执行所需的全部信息，包括线程的一组 CPU 寄存器和堆栈。 多个线程可在进程上下文中运行。 进程的所有线程共享其虚拟地址空间。线程可执行任意部分的程序代码，包括其他线程正在执行的部分。

3. **利用Process类**，可以启动和停止本机进程，获取或设置进程优先级、确定进程状态，获取进程列表和各进程的资源占用情况等。
   使用`Process`需要先引入`System.Diagnostics`命名空间：`using System.Diagnostics`;

```c#
//进程查看
Process[] myProcesses = Process.GetProcesses();   //本机的进程列表
foreach(Process p in myProcesses)
{
	Console.WriteLine(p.Id);
}
Console.ReadKey();
```

### 启动进程

1. 需要创建Process类的实例
2. 设置Starlnfo属性（(程序名称+传递参数)
3. 调用Start方法启动该进程
4. 等待启动成功

```c#
Process p1 = new Process();
p1.StartInfo.FileName = "Notepad.exe";  //准备执行记事本
p1.StartInfo.Arguments = "Test1234.txt";  //创建或打开的文档
p1.StartInfo.WindowStyle = ProcessWindowStyle.Minimized;//打开方式为图形化界面   最小化
p1.Start();

```

### 同步

优点：代码简单

缺点：串行执行，相互阻塞

```c#
public static void Standard()
{
    Work(1);
    Work(2);
}
```



### 异步

异步的好处在于非阻塞(调用线程不会暂停执行去等待子线程完成)，因此我们把一些不需要立即使用结果、较耗时的任务设为异步执行，可以提高程序的运行效率。

Task：表示一个异步操作

优点：线程开销减少，异步方法内部可以使用外部变量

```C#
    public static void UseTask()
    {
        var id1 = 1;
        var t1 = Task.Run(() =>
        {
            Work(id1);
        });

        var id2 = 2;
        var t2 = Task.Run(() =>
        {
            Work(id2);
        });
    }
```

### 线程
线程：创建和控制线程，设置其优先级并获取其状态。
优点：可以并行
缺点：开销大

```c#
//模拟高耗时任务
public static void Work(int id)
{
    Console.WriteLine($"{id} Begin");
    char[] chars = new char[4] { 'A', 'B', 'C', 'D' };
    foreach (var item in chars)
     {
         Thread.Sleep(1000);
         Console.WriteLine($"{id} {item}");
      }
      Console.WriteLine($"{id} End");
    }

public static void UserThread() 
{
   Thread t1 = new Thread(x => {
       Work(1);
    });
   t1.Start();

   Thread t2 = new Thread(x => {
       Work(2);
    });
    t2.Start();
}

//2 A
//1 A
//1 B
//2 B
//1 C
//2 C
//1 D
//1 End
//2 D
//2 End

```



## Task

`Task` 是在 `ThreadPool` 的基础上推出的，我们简单了解下 `ThreadPool`。`ThreadPool` 中有若干数量的线程，如果有任务需要处理时，会从线程池中获取一个空闲的线程来执行任务，任务执行完毕后线程不会销毁，而是被线程池回收以供后续任务使用。当线程池中所有的线程都在忙碌时，又有新任务要处理时，线程池才会新建一个线程来处理该任务，如果线程数量达到设置的最大值，任务会排队，等待其他任务释放线程后再执行。线程池能减少线程的创建，节省开销，看一个ThreadPool的例子吧

```c#
static void UserThreadPool()
{
    for (int i = 1; i < 5; i++)
    {
        ThreadPool.QueueUserWorkItem(new WaitCallback((obj) =>
        {
            Console.WriteLine($"第{obj}个执行任务");
        }), i);
    }
}


//第4个执行任务
//第2个执行任务
//第1个执行任务
//第3个执行任务


```

`ThreadPool `相对于 `Thread` 来说可以**减少线程的创建，有效减小系统开销**;但是 `ThreadPool` 不能控制线程的执行顺序，我们也**不能获取线程池内线程取消/异常/完成的通知**，即我们**不能有效监控和控制线程池中的线程。**

### Task创建和执行

1.  new方式实例化一个Task，需要通过Start方法启动 
```c#
Task task = new Task(() => 
{ 
    Thread.Sleep(100); 
    Console.WriteLine($"hello, task1的线程ID为{Thread.CurrentThread.ManagedThreadId}"); 
}); 
task.Start();       

```

2. Task.Factory.StartNew(Action action)创建和启动一个Task 

```c#
 Task task2 = Task.Factory.StartNew(() => 
{ 
    Thread.Sleep(100); 
    Console.WriteLine($"hello, task2的线程ID为{ Thread.CurrentThread.ManagedThreadId}");
}); 
```

3. Task.Run(Action action)将任务放在线程池队列，返回并启动一个Task 

```c#
Task task3 = Task.Run(() => 
{ 
    Thread.Sleep(100); 
    Console.WriteLine($"hello, task3的线程ID为{ Thread.CurrentThread.ManagedThreadId}"); 
}); 
```

运行结果：
![WechatIMG242](https://github.com/hylsss/CodeRecord/assets/62007319/c89c77a5-dcb9-431a-9c7e-21f60cd6a3d2)





先打印"执行主线程"，然后再打印各个任务，说明了**Task不会阻塞主线程**

如果创建有返回值的**Task** 





注意task.Resut获取结果时会阻塞线程，即如果task没有执行完成，会等待task执行完成获取到Result，然后再执行后边的代码
