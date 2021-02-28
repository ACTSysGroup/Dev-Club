# Redis

[Redis 教程 | 菜鸟教程](https://www.runoob.com/redis/redis-tutorial.html)

> REmote DIctionary Server 是一个key-value存储系统，跨平台的非关系数据库

- 整个数据库都加载在内存中，性能较强，每秒可以处理超过10万次读写操作
- 支持数据的持久化，可以将内存中的数据保存在磁盘，重启时再次加载
- 数据结构还支持list, set, zset, hash等类型

安装后默认显示16个数据库，使用0~15编号，之间的数据是隔离的，可以更改配置文件修改这个值

默认使用0号数据库，使用```SELECT 1```命令切换到1号数据库

## Redis键的命令

```SET key value```, ```GET key```, ```DEL key```, ```EXISTS key``` 等

用来对redis键进行操作

## Python

```bash
pip install redis
```

```python
import redis
# r = redis.Redis(host='localhost', port=6379, db=0)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
```

> StrictRedis的函数名称和redis命令行使用的命令基本相同，而Redis在使用一些函数时，参数的顺序会和redis命令行不一样

# 数据结构

## 字符串

按照键值对的形式存储，一个key对应一个value

string 类型是二进制安全的，因此可以存储任何数据，一条数据最大为512MB

```python
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
r.delete('k')
r.set('k', 'string value')
print(r.get('k'))
```

```
string value
```

默认获取的是byte类型的字符串，添加decode_responses=True自动将结果转为utf-8格式

set的参数：

```
ex 过期时间（s）
px 过期时间（ms）
nx 为True时，当key不存在的时候执行（存入）
xx 为True是，当Key存在的时候才执行（更新）
```

这些参数只能在set函数中添加，hmset等无法添加

可以使用函数设置

```
r.setex('k', 'string value', 1)     # 过期时间，秒
r.psetex('k', 'string value', 1000) # 过期时间，毫秒
r.setnx('k', 'string value')        # 
```

## Hash

一个key对应一个哈希表，哈希表使用字符串类型的field和value存储，适合存储对象数据

```python
r.delete('k')
r.hmset('k', mapping={'name': 'my name', 'email': 'my email'})
print(dict(r.hgetall('k')))
```

```
{'name': 'my name', 'email': 'my email'}
```

## 列表

一个列表最多可以包含 2^32 - 1 个元素，约40亿个

```python
r.delete('k')
r.lpush('k', 'item1')
r.lpush('k', 'item2')
r.lpush('k', 'item3')
r.lpush('k', 'item4')
print(r.llen('k'))  # 列表长度
print(r.lrange('k', 0, 10))  # 获取0到10的元素，忽略超出的部分
```

```
4
['item4', 'item3', 'item2', 'item1']
```

## 集合

集合成员是唯一的

集合的添加、删除、查找复杂度都是O(1)

一个集合最多存放 2^32 - 1 个元素

```python
r.delete('k')
r.sadd('k', 'item1')
r.sadd('k', 'item2')
r.sadd('k', 'item3')
r.sadd('k', 'item4')
r.sadd('k', 'item5')
print(r.scard('k'))    # 集合元素个数
print(r.smembers('k')) # 获取集合元素 乱序
```

```
5
{'item5', 'item4', 'item2', 'item1', 'item3'}
```

## 有序集合

添加、删除、查找的复杂度都是O(1)，最大数量是 2^32-1 

每个集合成员都具有一个score，通过score对成员实现排序，score可以重复

```python
r.delete('k')
r.zadd('k', 1, 'item1')
r.zadd('k', 2, 'item2')
r.zadd('k', 3, 'item3')
r.zadd('k', 4, 'item4')
print(r.zcard('k'))
print(r.zrange('k', 1, 10))
```

如果使用Redis构造，score需要写在后面

```python
r.delete('k')
r.zadd('k', 'item1', 1)
r.zadd('k', 'item2', 2)
r.zadd('k', 'item3', 3)
r.zadd('k', 'item4', 4)
print(r.zcard('k'))
print(r.zrange('k', 1, 10))
```

```
4
['item2', 'item3', 'item4']
```

> redis.exceptions.ResponseError: WRONGTYPE Operation against a key holding the wrong kind of value
>
> 异常表示想要存入的数据value值和已经有的不是同一个类型，可以删除数据后再存入```r.delete('k')```

# HyperLogLog

实现大量数据的基数统计（数据集去重后的数量）功能

```python
r.pfadd('k', '1')
r.pfadd('k', '1')
r.pfadd('k', '2')
r.pfadd('k', '1')
r.pfadd('k', '1')
r.pfadd('k', '1')

print(r.pfcount('k'))
```

```
2
```

# pub sub

类似消息队列，pub（发送者）发送消息，sub（接收端）接收消息

首先运行接收端

```python
import redis

r = redis.StrictRedis(host='localhost', port='6379', db=0, decode_responses=True)
p = r.pubsub()
p.subscribe('msg')

for item in p.listen():
    if item['type'] == 'message':
        print(item['channel'], item['data'])

```

运行发送端

```python
import redis
import time

rc = redis.StrictRedis(host='localhost', port='6379', db=0, decode_responses=True)
for i in range(0, 10):
    rc.publish("msg", str(i))
    time.sleep(1)

```

接收端输出

```
msg 0
msg 1
msg 2
msg 3
msg 4
msg 5
msg 6
msg 7
msg 8
msg 9
```



# flask项目中使用

- **可以使用flask_redis**

```myapp/extensions.py```中添加redis初始化

```python
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

db = SQLAlchemy()
migrate = Migrate(db=db)
socketio = SocketIO()
jwt = JWTManager()
redis_client = FlaskRedis()


def config_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    socketio.init_app(app, cors_allowed_origins='*')
    jwt.init_app(app)
    redis_client.init_app(app, decode_responses=True)
```

```myapp/config.py```中添加数据库地址

```python
REDIS_URL = "redis://localhost:6379/0"
```

flask-redis是对python redis库的封装，存取数据的时候使用的函数名基本相同

- **也可以使用python的redis库实现**

```myapp/extensions.py```中初始化

```python
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import redis

db = SQLAlchemy()
migrate = Migrate(db=db)
socketio = SocketIO()
jwt = JWTManager()

redis_client = redis.StrictRedis()


def config_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    socketio.init_app(app, cors_allowed_origins='*')
    jwt.init_app(app)

    redis_client.__init__(**app.config['REDIS_URL'])

```

```myapp/config.py```中添加配置

```python
REDIS_URL = {
    'host': 'localhost',
    'port': '6379',
    'db': 0,
    'decode_responses': True
}
```

# Redis集群

单个Redis：

1. 不稳定，redis服务器宕机后没有可用的服务
2. 读写性能有限

redis集群可以提高redis的性能和可用性

redis集群中，包括一个主节点(Master)和多个从节点(slave)，基于主从复制实现redis集群的数据同步，通过哨兵模式监控主节点的状态，当主节点宕机后选举出新的主节点。

主节点：执行读、写任务

从节点：只读节点

因此可以应对需要大量读数据的任务

## 主从复制

> Ubuntu配置文件一般位于```/etc/redis/redis.conf```

> 修改从数据库的配置文件，增加配置

> ```
> salveof <Master的ip> <Master的端口>
> ```

> 修改配置文件后重启redis服务
>
> 通过开放端口等操作，确保从数据库可以访问主数据库所在服务器的端口

> ```bash
> /etc/init.d/redis-server stop
> /etc/init.d/redis-server start
> /etc/init.d/redis-server restart
> ```

以下在本机(windows)上测试，复制redis整个文件夹并命名为redis-slave1, redis-slave2

修改redis-salve1的配置文件，设置端口为6378，redis-slave2的配置文件设置端口为6377，均添加```slaveof 127.0.0.1 6379```配置

使用命令行进入目录，```redis-server.exe redis.windows.conf```启动

向master存入数据

```python
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
r.delete('k')
r.set('k', 'k value')
print(r.get('k'))
```

连接slave查看

```python
import redis
r = redis.StrictRedis(host='localhost', port=6378, db=0, decode_responses=True)
print(r.get('k'))
```

向slave中尝试写入，出现redis.exceptions.ReadOnlyError

关闭主数据库服务后，从数据库服务会不断向Master发送连接请求，此时可以读取数据，无法写入数据

为了避免主库服务器宕机使得整个集群无法使用，可以使用哨兵模式选举出新的主数据库

## 哨兵

需要启动三个哨兵进程

三个数据库安装目录下新建配置文件sentinel.conf

主数据库sentinel.conf配置

```
port 26379
sentinel monitor mymaster 127.0.0.1 6379 2
```

从数据库1配置

```
port 26378
sentinel monitor mymaster 127.0.0.1 6379 2
```

从数据库2配置

```
port 26377
sentinel monitor mymaster 127.0.0.1 6379 2
```

首先按照主从复制的方式启动三个redis服务

进入目录下，使用命令

```
redis-server.exe sentinel.conf --sentinel
```

启动三个哨兵进程

进入安装目录下，使用

```
redis-cli -h 127.0.0.1 -p 6379
```

连接客户端，使用```info replication```命令查看服务状态

Master

```
# Replication
role:master
connected_slaves:2
slave0:ip=127.0.0.1,port=6378,state=online,offset=114963,lag=0
slave1:ip=127.0.0.1,port=6377,state=online,offset=114963,lag=0
master_replid:75b93e076204443536253ef8ec546e9ab7407a83
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:114963
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:114963
```

Slave1

```redis-cli -h 127.0.0.1 -p 6378```

```
# Replication
role:slave
master_host:127.0.0.1
master_port:6379
master_link_status:up
master_last_io_seconds_ago:0
master_sync_in_progress:0
slave_repl_offset:135452
slave_priority:100
slave_read_only:1
connected_slaves:0
master_replid:75b93e076204443536253ef8ec546e9ab7407a83
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:135452
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:135452
```

Slave2

```redis-cli -h 127.0.0.1 -p 6377```

```
# Replication
role:slave
master_host:127.0.0.1
master_port:6379
master_link_status:up
master_last_io_seconds_ago:1
master_sync_in_progress:0
slave_repl_offset:140947
slave_priority:100
slave_read_only:1
connected_slaves:0
master_replid:75b93e076204443536253ef8ec546e9ab7407a83
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:140947
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:43
repl_backlog_histlen:140905
```

查看sentinel状态

```redis-cli -h 127.0.0.1 -p 26379```

```info sentinel```

```
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=127.0.0.1:6379,slaves=2,sentinels=3
```

**关闭Master服务**

查看Slave的状态

Slave1

```redis-cli -h 127.0.0.1 -p 6378```

```
# Replication
role:slave
master_host:127.0.0.1
master_port:6377
master_link_status:up
master_last_io_seconds_ago:1
master_sync_in_progress:0
slave_repl_offset:186645
slave_priority:100
slave_read_only:1
connected_slaves:0
master_replid:024c2342c5d1d6a7492bde764521c1aa2a5eb7de
master_replid2:75b93e076204443536253ef8ec546e9ab7407a83
master_repl_offset:186645
second_repl_offset:178853
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:186645
```

Slave2

```redis-cli -h 127.0.0.1 -p 6377```

```
# Replication
role:master
connected_slaves:1
slave0:ip=127.0.0.1,port=6378,state=online,offset=189452,lag=1
master_replid:024c2342c5d1d6a7492bde764521c1aa2a5eb7de
master_replid2:75b93e076204443536253ef8ec546e9ab7407a83
master_repl_offset:189452
second_repl_offset:178853
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:43
repl_backlog_histlen:189410
```

发现原先的slave2变为Master

> 哨兵进程启动后会修改sentinel.conf配置文件，将配置写入硬盘上持久化，可以方便地重启而不会丢失配置

## redis-cluster

> redis 3.0以后支持cluster
>
> cluster将数据分散在几个节点，并支持动态扩充

1. 所有节点两两相连（PING-PANG机制），内部使用二进制协议优化传输速度和带宽每个节点都保存整个集群状态

2. 客户端连接其中一个节点即可

3. 节点的失效需要被集群中超过半数的节点检测到才能被认定
4. 集群将所有的节点映射到0-16383的slot上，存入数据时，根据CRC16(key)对16384取模的值来确定放入的节点

- 根据slot分好节点后，如果有新增的节点，则已有的所有节点选取一部分slot给新增节点
- 如果集群的某个节点挂掉后，集群就无法被访问。因此redis-cluster也可以配置主从模式，提高可用性。主从模式下，所有主节点分配slot，每个主节点可以有几个从节点同步数据，某个主节点宕机后相应的从节点可以来充当主节点

此处配置三个主节点分配slot（7001,7002,7003），每个主节点分配一个从节点（7004,7005,7006），需要复制6份redis数据库

需要安装Ruby环境，Redis的Ruby驱动gem文件，创建集群的redis-trib.rb

windows下参考：https://www.cnblogs.com/yy3b2007com/p/11033009.html



所有的redis数据库添加配置文件，设置端口为7001~7006

```redis-cluster.conf```

```
port 7001
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 15000
appendonly yes
bind 127.0.0.1
```

使用```redis-server redis-cluster.conf```运行6个redis服务

使用

```
redis-trib.rb create --replicas 1 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 127.0.0.1:7006
```

命令创建集群，```--replicas 1```表示每个主节点配有一个从节点，会自动分配主节点，从节点和slot

可以看出slot的分配范围

127.0.0.1:7001  slots:0-5460 (5461 slots)

127.0.0.1:7002  slots:5461-10922 (5462 slots)

127.0.0.1:7003  slots:10923-16383 (5461 slots)

使用```redis-cli -c -p 7001```命令连接7001

输入```set k kvalue```，显示```Redirected to slot [7629] located at 127.0.0.1:7002```，根据计算所得的hash值，放入了7002节点

重新连接到7001，输入```get k```，显示

```
-> Redirected to slot [7629] located at 127.0.0.1:7002
"kvalue"
```



手动关闭7001服务，```redis-trib.rb check 127.0.0.1:7004```，发现7004变为主节点，分配到了7001的slot

重启后如果发现```Error writing to socket fd xx```删掉生成的node.conf配置文件即可

