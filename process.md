## 进程和线程

这里是C#线程和进程的基本概念:

进程(Process)是操作系统资源分配的基本单位,每个进程有自己独立的内存空间。线程(Thread)是进程中的基本执行单位,一个进程可以包含多个线程。

- 进程有自己的独立内存空间,不同进程之间数据不共享,线程可以访问归属进程的内存空间。
- 线程比进程更轻量级,创建和销毁线程的开销比进程小很多。
- 一个进程默认至少有一个线程,称为主线程,进程结束时主线程结束。
- 一个进程中的多个线程可以并发执行,这对于提高程序的执行效率是很有帮助的。
- 线程之间的通信和协作依赖于同一个进程中的共享内存。进程间的通信需要借助IPC(Inter-process communication)。
- 线程执行是无序的,线程同步和互斥机制(比如锁)可以保证线程间的有序访问。
- 线程可以拥有自己的栈空间和程序计数器,但线程之间会共享进程的堆空间和方法区。
- 在C#中,System.Threading命名空间中提供了线程相关的类,如Thread、Mutex等。程序可以通过创建Thread实例并启动来创建新线程。

总之,理解进程和线程的区别,以及线程之间如何协作是掌握多线程编程的基础。

### C#中使用线程的常见方式有以下几种:

1. 直接使用Thread类，可以创建Thread类的实例,并通过Start方法启动线程执行。

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
   Thread t1 = new Thread(x => 
   {
       Work(1);
   });
   t1.Start();

   Thread t2 = new Thread(x => 
   {
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

2. 使用线程池(ThreadPool),线程池维护着一组线程,避免过度创建线程。可以通过`ThreadPool.QueueUserWorkItem` 添加任务.
```c#
ThreadPool.QueueUserWorkItem(Work);
```

3. 使用任务(Task)
```c#
Task t = new Task(Work);
t.Start();
```

4. 使用异步编程(async/await),使用 `async` 方法和`await` **可实现异步编程,底层会使用线程池:**
```c#
async Task DoWorkAsync()
{
  await Task.Run(() => 
  {
    //执行任务
  });
}
```

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





