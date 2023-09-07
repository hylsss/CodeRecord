## Mediator.Net 框架

Mediator.Net 是一个用于.NET的简单中介器，用于发送命令、发布事件和请求响应，并支持管道。

#### Mediator Pattern（中介者模式）

- 中介者模式用于集中处理多个对象之间的交互，使对象之间的关系简化为一对多的关系，从而降低系统的复杂性。
- Mediator在这里扮演协调者和调度者的角色，处理对象间的通信和协作。

在 .NET 中，中介者模式`（Mediator Pattern）`是一种设计模式，用于减少对象之间的直接依赖关系，从而降低它们之间的耦合度。该模式通过引入一个中介者对象来协调多个对象之间的交互。

在MVC中，Controller层不直接与Services层交流，而是通过Mediator。这意味着Controller不需要直接引入其他类或知道如何调用它们，只需要通过Mediator发送请求。

**Mediator的工作原理**:

- Mediator注册了`Handler`和信息（`Message`）之间的绑定。当它收到特定的信息时，它会在注册表中查找对应的`Handler`并调用它。
- 例如，当`Controller`使用`SendAsync(command)`发送命令时，Mediator会根据命令类型找到相应的`Handler`来处理这个命令。

#### 基础用法

```c#
// 设置一个中介器构建器
var mediaBuilder = new MediatorBuilder();
var mediator = mediaBuilder.RegisterHandlers(typeof(this).Assembly).Build();

// 发送没有响应的命令
await _mediator.SendAsync(new TestBaseCommand(Guid.NewGuid()));

// 发送有响应的命令
var pong = await _mediator.SendAsync<Ping, Pong>(new Ping());

// 发送请求并获取响应
var result = await _mediator.RequestAsync<GetGuidRequest, GetGuidResponse>(new GetGuidRequest(_guid));

// 发布一个事件
await _mediator.PublishAsync(new OrderPlacedEvent);
```

### 实现步骤

1. 在 controller 使用 SendAsync(command)/RequestAsync(request) （使用了 SendMessage 来判断传来的 IMessage 是属于 command/request/event 中的哪一种类型）
2. 选择到对应的管道，寻找到对应的 handler
3. 最后 handle 执行的任务。

在`controlle`r层，我们引入一个`mediator`，`controller`发对应的信息（message contract)。

```c#
[HttpPost]
[Route("create")]
public async Task<IActionResult> CreateAsync([FromBody] CreatePeopleCommand command)
{
    var response = await _mediator.SendAsync<CreatePeopleCommand, CreatePeopleResponse>(command).ConfigureAwait(false);
            
    return Ok(response);
}
```

在管道中找到对应的handler调用	`AddPersonAsync`

```c#
public async Task<CratePeopleResponse> Handle(IReceiveContext<CreatePeopleCommand> context,  
    CancellationToken cancellationToken)  
{  
    var @event = await _personService.AddPersonAsync(context.Message, cancellationToken).ConfigureAwait(false);  
  
    await context.PublishAsync(@event, cancellationToken).ConfigureAwait(false);  
  
    return new CratePeopleResponse  
    {  
        Result = @event.Result  
    };  
}
```

**AddPersonAsync**,再在里面执行操作

```c#
public async Task<PeopleCreatedEvent> AddPersonAsync(CreatePeopleCommand command,  
    CancellationToken cancellationToken)  
{  
    return new PeopleCreatedEvent  
    {  
        result = await _personDataProvider.CreatAsync(command.person, cancellationToken).ConfigureAwait(false) > 0  
            ? "数据写入成功"  
            : "数据写入失败"  
    };  
}  
  
public async Task<int> CreatAsync(Person person, CancellationToken cancellationToken)  
{  
    await _dbContext.People.AddAsync(person, cancellationToken).ConfigureAwait(false);  
  
    return await _dbContext.SaveChangesAsync(cancellationToken).ConfigureAwait(false);  
}
```

##### 资料参考

-  [Lizzie学习笔记](https://github.com/DOGGIE4/desktop-tutorial/blob/main/Mediator%20Learn.md)
-  [Mediator.Net github](https://github.com/mayuanyang/Mediator.Net)



