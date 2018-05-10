# AD_WebScanner

AD工作室精心研发漏洞安全扫描器
> 整合各大开源模块，自行加以整合
>
> python版本 ：3以上

# 开发约束
## 模块构造器
- 构造器的参数为URL+redis+模块特有参数,

```python
class demo(url,save_pool,....):
  self.module_redis = redis.Redis(connection_pool=save_pool)
  ...
  
```

- `savepool`由基础模块初始化子模块时提供，子模块可直接使用`redis.Redis(connection_pool=save_pool)`连接共用存储池
- 特有参数需指定默认参数，即只传入URL模块亦可单独执行
- 在构造函数的方法声明内注释说明特有参数的类型
- 构造器内需要包含模块的执行方法
- 从基础模块的相应键名获取各模块的特殊设置，如`hget('base','spider-threads)#获取爬虫模块的线程设置值`

## redis
- 连接redis实例的名称为模块名_redis，如`spider_redis`
- 模块中应省略创建存储池的过程，直接连接基础模块所创建的存储池
- 建议使用redis的hash存储，类型为`'模块名':'键':'值'`，如`hset('base','url',url)`
- 存储聚合数据类型时（如list/set)，使用redis的list/set存储，键名为模块名-键名，如`redis.sadd('base-input_opt','100)`
- 如果使用string\list\set存储类型，即视为共用的存储对象，各模块均有读写权限
- 进行radis的写入/读取操作的方法后注释说明传入/读取值的名称和类型

## 通用约束
- 模块内每个方法声明后注释传入参数的类型/说明，返回值的类型/说明
- 模块的关键处理步骤需进行注释
- 个人负责各自的模块，需修改他人部分的请与相应模块的负责人交流
- 模块开头用注释标明作者/修改日期
- 模块包含`is_finished()`方法，返回值为True或False，当模块的执行方法完成返回True,否则返回False
- 模块执行返回的信息应存入redis中


# 主要功能

- [x] 爬虫 (leslie)  
- [x] 目录爆破 (Mr. Guo)
- [x] 模块化设计，框架设计 (Chernobyl)
- [ ] 子域名爆破 (Chernobyl)
- [ ] 命令执行类(leslie)                                      
- [ ] 数据库漏洞扫描(13yyz)    
- [ ] 弱密码        
- [ ] XSS类        
- [ ] 敏感个人信息泄露         
- [ ] 内网渗透   
- [ ] 中间件扫描或者指纹扫描
- [ ] 无线网络扫描
- [ ] 端口扫描(Mr. Wu)
- [ ] 图形化界面
- to be continued

# 依赖

- requests
- redis
- bs4
- urllib

# 参考
https://github.com/We5ter/Scanners-Box
