## autoMap框架

AutoMapper是一个对象-对象映射器。对象-对象映射通过将一种类型的输入对象转换为另一种类型的输出对象来工作。   
简单来说就是：基于命名约定的对象到对象的映射工具，只要2个对象的属性具有相同的名字（或者符合它规定的命名规定），`AutoMapper`就可以帮我们自动在2个对象间进行属性值的映射，
如果不符合约定的属性，就需要自定义映射行为，需要告诉`AutoMapper`,在使用`Map`进行映射之前，必须使用` CreateMap() `进行配置  
**注意：将源映射到目标时，`AutoMapper` 将忽略空引用异常，可以通过自定义解析器来更改这种设置。**     

![WechatIMG270](https://github.com/hylsss/CodeRecord/assets/62007319/6070b674-16fb-4281-8f57-acda5673cfc1)
1. Source Object:映射的原始对象
2. Destination Object:需要映射到的新对象
3. AutoMapper:执行实际映射工作的框架
4. Configuration: 在使用 `AutoMapper` 之前，您需要配置映射规则。这通常在应用程序的启动代码中完成。
