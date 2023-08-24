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


**如果创建有返回值的Task** 



![WechatIMG243](https://github.com/hylsss/CodeRecord/assets/62007319/0ca37bac-048b-49c9-a09d-3e42e96d5a1d)



注意**task.Resut**获取结果时会**阻塞线程**，即如果task没有执行完成，会等待task执行完成获取到Result，然后再执行后边的代码

### 同步执行Task任务

```c#
static void UseRunchronously()
{
    Task task = new Task(() =>
    {
        Thread.Sleep(1000);
        Console.WriteLine("执行Task结束！");
    });
    task.RunSynchronously();
    Console.WriteLine("执行主线程结束");
    Console.ReadKey();
}

//执行Task结束！
//执行主线程结束
```

### Task 的阻塞线程方法

1.用 `Thread` 也是可以实现阻塞线程的方法

```c#
 
 Thread th1 = new Thread(() => { 
     Thread.Sleep(500); 
     Console.WriteLine("线程1执行完毕！"); 
 }); 
 th1.Start(); 
 Thread th2 = new Thread(() => { 
     Thread.Sleep(1000); 
     Console.WriteLine("线程2执行完毕！"); 
 }); 
 th2.Start(); 
 //阻塞主线程 
 th1.Join(); 
 th2.Join(); 
 Console.WriteLine("主线程执行完毕！"); 
 Console.ReadKey(); 


//执行结果
//线程1执行完毕！
//线程2执行完毕！
//主线程执行完毕！
```

##### 缺点：

- 实现很多线程的阻塞时，每个线程都要调用一次Join方法;

- 所有的线程执行完毕(或者任一线程执行完毕)时，立即解除阻塞，使用Join方法不容易实现。

2. Task的Wait/WaitAny/WaitAll方法

**Task.WaitAll(Task[] tasks)**  表示只有所有的task都执行完成了再解除阻塞; 
**Task.WaitAny(Task[] tasks) ** 表示只要有一个task执行完毕就解除阻塞;

```c#
 Task task1 = new Task(() => 
 { 
     Thread.Sleep(500); 
     Console.WriteLine("线程1执行完毕！"); 
 }); 
 task1.Start(); 
 Task task2 = new Task(() => 
 { 
     Thread.Sleep(1000); 
     Console.WriteLine("线程2执行完毕！"); 
 }); 
 task2.Start(); 
 //阻塞主线程。task1,task2都执行完毕再执行主线程 
 //执行【task1.Wait();task2.Wait();】可以实现相同功能 
 Task.WaitAll(new Task[]{ task1,task2}); 
 Console.WriteLine("主线程执行完毕！"); 
 Console.ReadKey();

```

### Task 的延续操作 **WhenAny/WhenAll**

1. WhenAny：其中一个任务执行完，就可以操作后续任务
2. WhenAll：所有任务执行完才会去执行后续任务

```c#
//task1 task2执行完之后再去执行后续操作
Task.WhenAll(task1, task2).ContinueWith((t) =>
{
    Thread.Sleep(100);
    Console.WriteLine("执行后续操作完毕！");
});
```

### Task 任务取消

```c#
static void UseCancelTask()
{ 
    CancellationTokenSource source = new CancellationTokenSource(); 
    //注册任务取消的事件 
    source.Token.Register(() => 
    { 
        Console.WriteLine("任务被取消后执行xx操作！"); 
    }); 
 
    int index = 0; 
    //开启一个task执行任务 
    Task task1 = new Task(() => 
    { 
        while (!source.IsCancellationRequested) 
        { 
            Thread.Sleep(1000); 
            Console.WriteLine($"第{++index}次执行，线程运行中..."); 
        } 
    }); 
    task1.Start(); 
    //延时取消，效果等同于Thread.Sleep(5000);source.Cancel(); 
    source.CancelAfter(5000); 
    Console.ReadKey(); 
} 
```

## Thread 和 Task的区别

1. 定义方式不同:
   - Thread 通过继承 Thread 类或参数传递启动信息来定义线程。
   - Task 通过 TaskFactory.StartNew 或 Task.Run 等方法来创建。

2. 线程管理不同:
   - Thread 需要手动控制线程的启动、暂停、恢复和停止。
   - Task 系统自动管理线程的生命周期。

3. 返回结果不同:
   - Thread 不直接支持返回结果。需要通过共享变量、传参等方式获取结果。
   - Task 支持通过 Task.Result 属性或 async/await 获取结果。

4. 异常处理不同:
   - Thread 通过 Try/Catch 处理异常。但不方便传递异常。
   - Task 用 Try/Catch 也可以处理异常。也可以通过返回的 Task 获取异常。

5. 取消机制不同:
   - Thread 不直接支持取消。需要通过设置标志位、中断等方式实现取消。
   - Task 内置支持取消,可以通过 CancellationToken 取消任务。

6. 继续执行不同:
   - Thread 继续执行需要手动管理,比较复杂。
   - Task 可以通过 ContinueWith 直接连续执行。

7. 调度机制不同:
   - Thread 默认使用线程池线程。
   - Task 默认使用线程池线程,也可以指定特定的调度器。

8. 使用场景不同:
   - Thread 更底层,适用于要完全控制线程的场景。
   - Task 更高层,适用于大多数异步编程场景。

总结:
Task 在线程管理、同步、任务调度等方面提供了更多高级功能,使用更加方便,适合大多数异步编程场景。Thread 则提供底层的线程控制,适用于要完全控制线程的复杂场景。
