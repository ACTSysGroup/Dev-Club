# pub-sub模型

> 当用户执行某个请求时，有可能需要后端进行数量较多的操作，或者需要进行耗时较长的操作时，在一个处理中完成所有的任务是不现实的；而且在用户数量较多的情况下，往往需要对这些请求进行排序异步处理。

pub：发布消息（publisher）

sub：订阅消息（subscriber)

pub-sub模型定义了如何向***内容节点(topic)***发布和订阅消息，发布者提供一个topic，可以被多个消费者订阅

在软件架构中，**pub-sub**是一种消息范式，消息的发送者（称为发布者）不会将消息直接发送给特定的接收者（称为订阅者）。而是将发布的消息分为不同的类别，无需了解哪些订阅者（如果有的话）可能存在。同样的，订阅者可以表达对一个或多个类别的兴趣，只接收感兴趣的消息，无需了解哪些发布者（如果有的话）存在。

这种模式提供了更大的网络可扩展性和更动态的网络拓扑，同时也降低了对发布者和发布数据的结构修改的灵活性

# Kafka

> 中文文档：[Kafka 中文文档 - ApacheCN](https://Kafka.apachecn.org/)
>
> Kafka是最初由Linkedin公司开发的一个基于Zookeeper协调的分布式消息系统，并于2010年贡献给了Apache基金会并成为顶级开源项目
>
> Apache Kafka® 是一个分布式流处理平台
>
> Kafka受到Zookeeper的管理，要运行Kafka需要首先安装Zookeeper

## Zookeeper

Zookeeper是一个分布式的应用程序协调服务，其目标是封装好复杂易出错的关键服务，可以实现选举Leader、同步数据等需求

### 优点

- 分布式协调过程简单
- 同步性高
- 消息有序
- 速度较快，性能好
- 可扩展性强
- 可靠，具有原子性（一个操作只有成功失败两种状态），实时性

### 局限性

- 增加新服务节点时可能导致数据丢失
- 要实现选举过程（选举要求``可用节点数 > 总节点数/2``），所以只允许奇数个节点

## 基本概念

- Kafka作为一个集群，运行在一台或者多台服务器上.        
- Kafka 通过 *topic* 对存储的流数据进行分类。        
- 每条记录中包含一个key，一个value和一个timestamp（时间戳）。

**Producer**：生产者，发送消息

**Consumer**：消费者，消费消息

**ConsumerGroup**：消费者组，一个消费者组下的消费者可以并行消费一个topic下的消息

**Broker**：缓存代理，指Kafka集群中的一台或多台服务器节点

**topic**：消息的分类

**partition**：分区，每个toipc有许多分区，一个分区中的消息是有序的队列，用offset作为id

**offset**：消息在分区中的偏移量

> 消费者根据topic订阅消息，生产者在一个topic上发送的消息会被所有订阅这个topic的消费者收到。每个topic都具有许多分区(partition)，分区中的记录通过偏移量(offset)来区分，记录具有一个保留期限，超过期限的记录会被丢弃

## Kafka的架构

官方文档中的示例图：

<img src=".\images\kafka.png" alt="kafka" style="zoom:67%;" />

Kafka存储的消息来自任意多被称为“生产者”（Producer）的进程。数据从而可以被分配到不同的“分区”（Partition）、不同的“Topic”下。在一个分区内，这些消息被索引并连同时间戳存储在一起。其它被称为“消费者”（Consumer）的进程可以从分区查询消息。Kafka运行在一个由一台或多台服务器组成的集群上，并且分区可以跨集群结点分布。

## Kafka的优势

 - 高吞吐量，低延迟，支持高并发

   写的性能体现在以O(1)的时间复杂度进行顺序写入。读的性能体现在以O(1)的时间复杂度进行顺序读取， 对topic进行partition分区，消费者组中的消费者线程可以以很高能性能进行顺序读。

 - 集群可扩展
 - 数据持久化到磁盘，持久性，可靠性。如果正常终止，数据不会丢失；如果不正常终止，可能会使页面缓存来不及写入磁盘导致消息丢失，可以配置flush的周期来设置写磁盘的频率。

## 分区

 相比传统的消息队列，Kafka具有更严格的顺序保证，每个分区中的消息都是按顺序存放的。

 **传统消息队列**

 传统的队列虽然按照顺序将消息传递给消费者，但是由于这个传递过程是异步的，消息可能会到无序到达多个并行的消费者，不能保证顺序性。

 而如果想要按顺序执行的话，只能使用唯一的一个消费者，无法并行处理。

 **Kafka**

 Kafka的设计中，**每个topic都具有一些并行的*分区(partition)***，将分区分配给消费者组中的消费者，每个分区都对应一个消费者，这保证了分区中的消息按照顺序处理，多个分区保证了负载均衡。

**需要注意的是，一个topic内的消息是无序的，partition内的消息才是有序的**

## 重复消费

如果是处理用户缴费等任务，需要严格保证不能重复消费。

已经消费了消息，但是偏移量没有成功提交，会造成重复消费。

通常导致重复消费的原因有以下几点

- 线程被强行kill，例如消费者宕机、重启等，导致消费后的数据偏移量没来得及提交
- 设置偏移量为自动提交，关闭kafka服务时有可能有部分偏移量没有提交，重启后会重复消费
- 消费后的数据，当偏移量还没有提交时，分区就断开连接。如果消费处理时间超过了Kafka的session timeout时间，就会发生re-blance，可能会造成消费的偏移量没有提交，导致重复消费。

解决方法

- 每次消费时将每个topic和partition的offset记录在内存中 (Redis)，关闭consumer后将记录持久化到磁盘，下一次重启后根据记录去寻找下一个offset

参考 https://blog.csdn.net/zollty/article/details/53958641

## 消息丢失

通常导致消息丢失的原因有以下几点

- 设置消费端自动提交偏移量，未处理完成就到了提交间隔，此时如果消费者宕机，重启后会从下一个偏移量开始消费
- 磁盘忙，写入失败，没有消息重试，导致数据丢失或磁盘损坏
- 由于网络问题导致消息发送失败
- 数据长度超出限制

解决方法

- 设置自动提交为false，处理完成后手动提交消息
- 设置发送消息的回调函数，确保消息发送成功
- 设置多个副本
- 根据实际情况设置flush时间间隔

参考 https://www.cnblogs.com/colourness/p/12577446.html

## **集群**

> 使用集群进行跨服务器的负载均衡，避免单节点宕机造成服务停止或数据丢失。提高可用性

- Kafka集群中的Broker之间的地位是一样的，不是主从关系，可以随意增加删除节点

### Kafka Broker Leader

通过Zookeeper管理集群

所有的Kafka Broker节点一起去Zookeeper上注册一个临时节点，只有一个Kafka  Broker节点会注册成功，其他的都会失败；这个成功注册的节点称为Kafka  Broker Controller，其他的Kafka Broker叫做Kafka Broker  Follower，这个过程叫controller在Zookeeper注册Watch。这个Controller会监听其他的Kafka  Broker的所有信息。

如果这个Kafka Broker  Controller宕机了，在Zookeeper上面的那个临时节点就会消失，此时所有的Kafka  Broker又会一起去Zookeeper上注册一个临时节点，重新分配Controller和Follower。

### 集群配置

````
broker.id=0 # 参数默认值为0，设置三个kafka的配置文件分别为0,1,2
listeners=PLAINTEXT://localhost:9092 # 设置域名和端口，默认是9092
````

在同一台机器上测试的话，需要修改端口为9092,9093,9094

打开Kafka Tool可以发现连接了三个Broker

## python-Kafka

[Kafka-python · PyPI](https://pypi.org/project/Kafka-python/)

默认发送的是byte类型数据

```producer.py```

```python
from Kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')
for i in range(0, 100):
    producer.send('topic', b'byte string value')
    time.sleep(1)

```

```consumer.py```

```python
from Kafka import KafkaConsumer

consumer = KafkaConsumer('topic')
for msg in consumer:
    print(msg.value)
```

运行consumer，程序等待中，运行producer，每隔一秒收到一个消息；接收的msg是一个元组，使用.访问数据

### key value

可以发送key value

发送string类型数据

```producer.py```

```python
from Kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092', key_serializer=str.encode, value_serializer=str.encode)

for i in range(0, 100):
    producer.send('topic', key='key', value='string value')
    print('send '+str(i))
    time.sleep(1)

```

```consumer.py```

```python
from Kafka import KafkaConsumer

consumer = KafkaConsumer('topic',key_deserializer=lambda v: bytes.decode(v), value_deserializer=lambda v: bytes.decode(v))
for msg in consumer:
    print(msg.key, msg.value)
```

### json

通过改写序列化方法，也可以发送json数据（string 类型的key，json类型的value）

```producer.py```

```python
from Kafka import KafkaProducer
import time
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092', key_serializer=str.encode, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for i in range(0, 100):
    producer.send('topic', key='key', value={
        "name": "value",
        "number": str(i)
    })
    print('send '+str(i))
    time.sleep(1)
```

```consumer.py```

```python
from Kafka import KafkaConsumer
import json

consumer = KafkaConsumer('topic', key_deserializer=lambda v: bytes.decode(v), value_deserializer=lambda v: json.loads(v))
for msg in consumer:
    print(msg.key, msg.value)
```

### gzip

producer可以发送压缩后的消息，添加参数设置压缩方式为gzip

```python
producer = KafkaProducer(bootstrap_servers='localhost:9092', key_serializer=str.encode, value_serializer=lambda v: json.dumps(v).encode('utf-8'), compression_type='gzip')
```



