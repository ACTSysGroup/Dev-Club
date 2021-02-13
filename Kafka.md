# pub-sub模型

> 当用户执行某个请求时，有可能需要后端进行数量较多的操作，或者需要进行耗时较长的操作时，在一个处理中完成所有的任务是不现实的；而且在用户数量较多的情况下，往往需要对这些请求进行排序异步处理。

> pub：发布消息（publisher）
>
> sub：订阅消息（subscriber)
>
> pub-sub模型定义了如何向***内容节点(topic)***发布和订阅消息，发布者提供一个topic，可以被多个消费者订阅

# Kafka

> 中文文档：[Kafka 中文文档 - ApacheCN](https://kafka.apachecn.org/)
>
> Kafka是最初由Linkedin公司开发的一个基于zookeeper协调的分布式消息系统，并于2010年贡献给了Apache基金会并成为顶级开源项目
>
> Apache Kafka® 是 *一个分布式流处理平台

>- Kafka作为一个集群，运行在一台或者多台服务器上.        
>- Kafka 通过 *topic* 对存储的流数据进行分类。        
>- 每条记录中包含一个key，一个value和一个timestamp（时间戳）。

> 消费者根据topic订阅消息，生产者在一个topic上发送的消息会被所有订阅这个topic的消费者收到。每个topic都具有许多分区，分区中的记录通过偏移量(offset)来区分，记录具有一个保留期限，超过期限的记录会被丢弃

---

## zookeeper

 zookeeper是一个分布式的应用程序协调服务

## 优势

 - 高吞吐量，低延迟，支持高并发
 - 集群可扩展
 - 数据持久化到磁盘，持久性，可靠性

## 分区

 相比传统的消息队列，kafka具有更严格的顺序保证。

 **传统消息队列**

 传统的队列虽然按照顺序将消息传递给消费者，但是由于这个传递过程是异步的，消息可能会到无序到达多个并行的消费者，不能保证顺序性。

 而如果想要按顺序执行的话，只能使用唯一的一个消费者，无法并行处理。

 **kafka**

 kafka的设计中，每个topic都具有一些并行的*分区(partition)*，将分区分配给消费者组中的消费者，每个分区都对应一个消费者，这保证了分区中的消息按照顺序处理，多个分区保证了负载均衡。

## **集群**

> 使用集群进行跨服务器的负载均衡，避免单节点宕机造成服务停止或数据丢失。提高可用性

**Broker**

每个Broker即是一个Kafka服务实例，多个Broker构成一个Kafka集群



## python-kafka

[kafka-python · PyPI](https://pypi.org/project/kafka-python/)

默认发送的是byte类型数据

```producer.py```

```python
from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')
for i in range(0, 100):
    producer.send('topic', b'byte string value')
    time.sleep(1)

```

```consumer.py```

```python
from kafka import KafkaConsumer

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
from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092', key_serializer=str.encode, value_serializer=str.encode)

for i in range(0, 100):
    producer.send('topic', key='key', value='string value')
    print('send '+str(i))
    time.sleep(1)

```

```consumer.py```

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer('topic',key_deserializer=lambda v: bytes.decode(v), value_deserializer=lambda v: bytes.decode(v))
for msg in consumer:
    print(msg.key, msg.value)
```

### json

通过改写序列化方法，也可以发送json数据（string 类型的key，json类型的value）

```producer.py```

```python
from kafka import KafkaProducer
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
from kafka import KafkaConsumer
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



