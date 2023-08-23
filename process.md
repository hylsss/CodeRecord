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

