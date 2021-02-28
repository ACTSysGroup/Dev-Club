# Websocket

GET、POST等请求，只能由客户端发起服务端回应，想要用请求实现数据的实时更新，只能通过轮询、长轮询等技术

 - 轮询：客户端每隔固定的时间发送一次请求

 - 长轮询：客户端发送请求，服务端如果没有消息就一直阻塞，知道有消息再返回，之后客户端再次发送请求

 这种方式对网络和服务器的资源消耗较大，并发性不高

 - Websocket：支持长连接，经过一次握手建立连接，可以由服务端主动推送消息给客户端，实现低延时的双向通信

 网络环境不好的话会造成不断的重连

---

**HTTP**

HTTP的生命周期通过Request来界定，也就是一个Request 一个Response，那么在HTTP/1.0中，这次HTTP请求就结束了

在HTTP/1.1中进行了改进，使得有一个keep-alive，也就是说，在一个HTTP连接中，可以发送多个Request，接收多个Response。

HTTP协议是被动的，不能主动发起

---

**Websocket**

Websocket是基于HTTP协议实现的，通过借用HTTP的协议来完成一部分握手

在握手阶段，Websocket握手请求会多出请求头

```
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
Sec-WebSocket-Protocol: chat
Sec-WebSocket-Version: 13
```

表明发起的是Websocket握手请求而不是普通的HTTP请求

``Sec-WebSocket-Key``是客户端随机生成的一个Base64值，用来验证服务端识别的是否是Websocket协议

``Sec-WebSocket-Protocol``用来区分同一协议下不同服务需要的协议

``Sec-WebSocket-Version``注明协议版本

服务端会返回``Switching Protocols``表示收到请求，成功建立连接



## Flask-Sockets

是flask对websocket的原始封装，功能较少

flask-sockets : [GitHub - heroku-python/flask-sockets: Elegant WebSockets for your Flask apps.](https://github.com/heroku-python/flask-sockets)

### 运行

```python
from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/test')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send('received' + message)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
```

JavaScript (vue) : 

连接：

```js
let wsuri = "ws://localhost:5000/test"
this.websock = new WebSocket(wsuri);
this.websock.onmessage = this.websocketonmessage; // 接收消息
this.websock.onopen = this.websocketonopen;
this.websock.onerror = this.websocketonerror;
this.websock.onclose = this.websocketclose;
```

发送消息：

```js
this.websock.send("message");
```

接收：

```js
websocketonmessage(response){ //数据接收
	console.log('websocket收到消息', response.data);
},
```



## Flask-SocketIO

> socket.io是基于websocket协议的一套成熟的解决方案
>
> SocketIO将WebSocket、AJAX和其它的通信方式全部封装成了统一的通信接口，兼容性较好，在使用socketIO时底层会自动选用最佳的通信方式，WebSocket是SocketIO的一个子集
>
> 需要注意：SocketIO传输的数据并不完全遵循Websocket协议，后端使用SocketIO协议不能兼容前端的Websocket协议，这就要求客户端和服务端都必须使用socketIO解决方案

flask-socketio包封装了flask对socketio的支持，可以配合js端的socket.io实现前后端交互方案

flask-socketio文档：[Welcome to Flask-SocketIO’s documentation! — Flask-SocketIO documentation](https://flask-socketio.readthedocs.io/en/latest/)

JavaScript socket.io文档：[The Socket instance (client-side) | Socket.IO](https://socket.io/docs/v3/client-socket-instance/)

## 版本匹配

| JavaScript Socket.IO version | Socket.IO protocol revision | Engine.IO protocol revision | python-socketio version |
| ---------------------------- | --------------------------- | --------------------------- | ----------------------- |
| 0.9.x                        | 1, 2                        | 1, 2                        | Not supported           |
| 1.x and 2.x                  | 3, 4                        | 3                           | 4.x                     |
| 3.x                          | 5                           | 4                           | 5.x                     |

### 运行flask_socketio

```python
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' # 可以定期更换密钥
socketio = SocketIO(app, cors_allowed_origins='*') # 设置跨域

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000) # 可以设置ip地址和端口号
```

JavaScript (vue)：

```js
import {io} from 'socket.io-client';
```

连接：

```js
this.socket = io('ws://localhost:5000/');
this.socket.on("connect", this.socketconnect);
```

```js
socketconnect(){
	console.log('connect', this.socket);
},
```

查看输出，connected为true，disconnected为false说明连接成功

### 传递数据

**命名空间：**

可以不指定命名空间，所有消息共用一个命名空间```/```

如果需要在一组客户端和服务端之间传递多种类型的数据，可以使用命名空间来做区分，例如使用/chat命名空间

JavaScript :

```js
this.socket = io('ws://localhost:5000/chat');
```

客户端使用chat命名空间，flask接收消息的时候需要指明```namespace='/chat'```

发送消息时默认使用接收消息的命名空间，可以指定另外的命名空间

如果使用默认的命名空间，namespace可以省略

**房间：**

可以将连接到同一个命名空间的几个客户端分到同一个房间，实现房间内的消息共享，如聊天室等应用

**事件：**

使用```send```发送未命名消息，不指定event；使用```emit```发送命名消息，指定event

使用```@socketio.on()```注释接收命名和未命名消息，括号中写明消息类型，保留字有```message, json, connect, disconnect```，不能用于event的命名

connect : 建立连接调用

disconnect : 关闭连接调用

message : 接收使用send发送的未命名消息，字符串类型

json : 接收使用send发送的未命名消息，json类型

event的名字 : 接收使用emit发送的命名消息

#### 连接

```python
@socketio.on('connect', namespace='/chat')
def handle_connect():
    print('Client connected')
```

#### 关闭

```python
@socketio.on('disconnect', namespace='/chat')
def handle_disconnect():
    print('Client disconnected')
```

#### 未命名

接收客户端使用send发送的未指定event的消息

JavaScript :

发送：

```js
this.socket.send('message');
```

json

```js
this.socket.send({"message": 123});
```

接收：

```js
this.socket.on('message', (msg) => {
	console.log(msg);
})
```

```js
this.socket.on('json', (msg) => {
	console.log(msg);
})
```

flask :

```python
@socketio.on('message', namespace='/chat')
def handle_message(data):
    print('received message: ' + data)
    send('received message.')
```

```python
@socketio.on('json', namespace='/chat')
def handle_json(json):
    print('received json: ' + str(json))
    send('received json.', json=True)
```

#### 命名

 接收前端使用emit发送的指定event的消息，例如客户端指定event为```my event```

 JavaScript :

 发送：

 ```js
 this.socket.emit('my event', 'message');
 ```

 接收：

 ```js
 this.socket.on('my event', (msg) => {
 	console.log(msg);
 })
 ```

 flask :

 ```python
 @socketio.on('my event', namespace='/chat')
 def handle_my_custom_event(data):
     print('received data: ' + data)
     emit('my event', 'received data.')
 ```

#### 多个参数

 可以用```,```将需要发送的多个参数隔开，发送的参数数量和接收的需要对应起来

 如果服务端接收的参数少于客户端发送的，服务端会抛异常```TypeError: my_event() takes 1 positional argument but 3 were given```，如果服务端接收的参数多于客户端发送的，服务端会抛异常```TypeError: my_event() missing 2 required positional arguments: 'm2' and 'm3'```

 JavaScript :

 发送：

 ```js
 this.socket.emit('my event', 'msg1', 'msg2', 'msg3')
 ```

 接收：

 ```js
 this.socket.on('my event', (msg1, msg2, msg3) => {
 	console.log(msg1, msg2, msg3);
 })
 ```

 flask : 使用元组的形式发送多个参数

 ```python
 @socketio.on('my event', namespace='/chat')
 def handle_my_custom_event(data1, data2, data3):
     print('received data: ', data1, data2, data3)
     emit('my event', (data1, data2, data3))
 ```

#### 使用函数名

 如果event名称和python关键字不冲突，是一个合法的python标识符，可以使用函数名表示event名称

 JavaScript :

 ```js
 this.socket.emit('my_event', 'message')
 ```

 flask :

 ```python
 @socketio.event(namespace='/test')
 def my_event(msg):
     print(msg)
 ```

#### 广播

 设置```broadcast=True```字段可以发送广播消息

 连接到**同一个命名空间**的所有客户端都会收到消息

 ```python
 @socketio.on('chatting', namespace='/chat')
 def handle_response(msg):
     send('broadcast message!')
 ```

 使用多个客户端连接/chat命名空间，其中一个发送一条事件名为chatting的消息，所有的客户端都会收到广播消息

#### 房间

 如果需要让连接到同一个命名空间下的**某些**客户端共享数据，命名空间的broadcast无法实现，需要使用房间。

 使用emit发送join消息的方式进入房间

 JavaScript : 

 进入房间：

 ```javascript
 this.socket.emit('join', {"username": "user1", "room": "room1"});
 ```

 离开房间：

 ```js
 this.socket.emit('leave', {"username": "user1", "room": "room1"});
 ```

 flask :

 ```python
 from flask_socketio import join_room, leave_room
 
 @socketio.on('join')
 def on_join(data):
     username = data['username']
     room = data['room']
     join_room(room)
     send(username + ' has entered the room.', room=room)
 
 @socketio.on('leave')
 def on_leave(data):
     username = data['username']
     room = data['room']
     leave_room(room)
     send(username + ' has left the room.', room=room)
 ```

 当客户端进入或离开房间时，房间中的其它客户端都能收到消息

 一个客户端可以进入多个房间

#### 服务端推送

要实现实时更新的任务，服务端还需要具有推送消息的能力，根据客户端的id来推送消息

可以使用room来实现

每个客户端连接后，都具有一个sid，后端可以使用```sid = request.sid```获取这个sid，在发送消息的语句中写明```room=sid```可以实现对此客户端单独的消息推送

对于一般的业务场景，一个用户连接后，需要将用户id和这个sid作为key-value存入数据库（redis）中，当需要对某个用户推送消息时，根据用户id找出对应的sid来发送消息

```python
sid = request.sid
send({"message": "123"}, namespace='/test', room=sid)
```

### 项目配置

在项目中使用时，可以使用命名空间类来绑定事件，可以在初始化的时候加载命名空间

如果使用socketio.on绑定命名空间，则需要将代码写在运行的文件里面，否则会导致命名空间无效

在```myapp/extensions.py```中添加socketio配置

```python
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate(db=db)
socketio = SocketIO()


def config_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    socketio.init_app(app, cors_allowed_origins='*')
    # cache.init_app(app,config={'CACHE_TYPE':'redis'})
```

在myapp中新建socketio包，创建```test.py```文件

```myapp/__init__.py```

```python
from .test import TestNamespace
from myapp.extensions import socketio


def config_socketio():
    socketio.on_namespace(TestNamespace('/socketTest'))
```

```myapp/test.py```

```python
from flask import request
from flask_socketio import join_room, leave_room, send, emit, Namespace


class TestNamespace(Namespace):
    def on_connect(self):
        print('connected', request.sid)
        send('class conected!')

    def on_disconnect(self):
        print('disconnected')

    def on_message(self, msg):
        print('recv message', msg)
        send('received message')

    def on_chat(self, msg):
        print('recv chat', msg)
        emit('chat', 'received chat')

    def on_join(self, data):
        username = data['username']
        room = data['room']
        join_room(room)
        print(username + ' has entered the room.')
        send(username + ' has entered the room.', room=room)

    def on_leave(self, data):
        username = data['username']
        room = data['room']
        leave_room(room)
        print(username + ' has left the room.')
        send(username + ' has left the room.', room=room)

```

在```myapp/create_app.py```中调用```config_socketio```配置

在```manage.py```中配置socketio运行方式，重写manager的run命令

```python
manager.add_command('run', socketio.run(app=app, debug=True, host="0.0.0.0", port=5000))
```

使用命令运行

```bash
python manage.py runserver
```

# HTTP/2

 相比HTTP 1.1 性能更好，兼容大部分HTTP 1. 1 的操作

- **二进制分帧**：HTTP/2 采用二进制格式传输数据，而非 HTTP 1.x 的文本格式，二进制协议解析起来更高效。HTTP/2 中，同域名下所有通信都在单个连接上完成，该连接可以承载任意数量的双向数据流。每个数据流都以消息的形式发送，而消息又由一个或多个帧组成。多个帧之间可以乱序发送，根据帧首部的流标识可以重新组装。
- **多路复用**：HTTP 1.x 中，如果想并发多个请求，必须使用多个 TCP 链接，且浏览器为了控制资源，还会对单个域名有 6-8个的TCP链接请求限制。在HTTP/2中，同域名下所有通信都在单个连接上完成，可以承载任意数量的双向数据流，数据流以消息的形式发送，而消息又由一个或多个帧组成，多个帧之间可以乱序发送，因为根据帧首部的流标识可以重新组装。提高了性能。
- **服务器推送**：服务端可以在发送页面HTML时主动推送其它资源，而不用等到浏览器解析到相应位置，发起请求再响应。
- **头部压缩**：HTTP/2对消息头采用HPACK（专为http/2头部设计的压缩格式）进行压缩传输，能够节省消息头占用的网络的流量

## 优点

- 性能高，加载速度快，节省流量
- 更加安全

## 缺点

- TCP 以及 TCP+TLS建立连接的延时
- TCP的队头阻塞并没有彻底解决

# GraphQL

> ask exactly what you want

文档：[GraphQL 入门 | GraphQL 中文文档](https://graphql.bootcss.com/learn/)

GraphQL是一种API查询语言

- 可以从一个查询API中获取前端需要的部分数据，只需要传送前端需要的部分数据，避免了冗余数据的传输
- 一次请求可以获取多个API的信息，更加灵活，提高了系统吞吐量、服务端响应效率

使用Flask_GraphQL实现一个简单的接口

- resolve_user的user字段和类Query的user字段对应
- 设置url为```/test```
- 通过设置```graphiql=True```使用graphiql来调试GraphQL接口

```python
from flask_graphql.graphqlview import GraphQLView
from graphene import ObjectType, Int, String, Field, Schema, List
from flask import Flask


app = Flask(__name__)


class Query(ObjectType):
    ans = String(a=String(), b=Int())

    def resolve_ans(self, info, a, b):
        print(a,b)
        return {
            'a': a,
            'b': b
        }

view_func = GraphQLView.as_view('test', schema=Schema(query=Query), graphiql=True)
app.add_url_rule('/test', view_func=view_func)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

```

运行后进入```http://localhost:5000/test```来调试接口

输入

```json
{
  ans(a: "str", b: 3)
}
```

查询结果

```json
{
  "data": {
    "ans": "{'a': 'str', 'b': 3}"
  }
}
```

## 项目配置

一般使用在根据数据库模型查询的场景

Query类的属性不能直接映射数据库模型，需要使用```SQLAlchemyObjectType```连接，Field对应```SQLAlchemyObjectType```对象，返回```models```对象

在myapp下新建graphql包，创建```graphql.py```文件

配置文件

```myapp/graphql/__init__.py```

```python
from flask_graphql import GraphQLView
from graphene import Schema
from myapp.graphql.graphql import Query


def config_graphql(app):
    view_func = GraphQLView.as_view('test', schema=Schema(query=Query), graphiql=True)
    app.add_url_rule('/test', view_func=view_func)

```

```myapp/__init__.py```的```create_app```中添加配置

```
# 配置graphql
config_graphql(app)
```



```graphql.py```

```python
from flask import jsonify
from graphene import ObjectType, Int, String, Field, List, relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from myapp.api.articles import get_article_info
from myapp.api.authors import get_author_info, get_author_articles
from myapp.models.models import Authors, Articles, Publish


class AuthorsNode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node,)
        model = Authors


class ArticlesNode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node,)
        model = Articles


class PublishNode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node,)
        model = Publish


class Query(ObjectType):

    authors = Field(type=AuthorsNode, id=Int())
    articles = Field(type=ArticlesNode, id=Int())

    author_articles = Field(type=PublishNode, id=Int())

    @staticmethod
    def resolve_authors(self, info, id):
        return Authors.query.filter_by(id=id).first_or_404()

    @staticmethod
    def resolve_author_articles(self, info, id):
        return Publish.query.filter_by(author_id=id)

    @staticmethod
    def resolve_articles(self, info, id):
        return Articles.query.filter_by(id=id).first_or_404()
```

### 查询示例

输入

```
{
  authors(id: 1) {
    name
    email
  }
}
```

查询结果

```json
{
  "data": {
    "authors": {
      "name": "Li Ming",
      "email": "Li@gmail.com"
    }
  }
}
```

- 根据查询条件返回特定的字段


如果前端的多个接口，有的需要对象的全部数据，有的只需要对象的某几个字段数据，就可以根据需要来请求数据，后端不需要构造多个接口，也不需要每次都传输所有的数据。

- 对于查询列表同样适用
- 对于外键字段可以嵌套```{}```查询

输入

```
{
  authorArticles(id: 2){
    authors{
      name
    }
    articles{
      title
    }
    rank
	}
}
```

查询结果

```json
{
  "data": {
    "authorArticles": [
      {
        "authors": {
          "name": "Wang Ming"
        },
        "articles": {
          "title": "这是第一本书"
        },
        "rank": 2
      },
      {
        "authors": {
          "name": "Wang Ming"
        },
        "articles": {
          "title": "这是第二本书"
        },
        "rank": 1
      },
      {
        "authors": {
          "name": "Wang Ming"
        },
        "articles": {
          "title": "这是第三本书"
        },
        "rank": 1
      },
      {
        "authors": {
          "name": "Wang Ming"
        },
        "articles": {
          "title": "这是第四本书"
        },
        "rank": 1
      }
    ]
  }
}
```

### 查询多个接口数据

- 可以通过一个请求返回多个接口的数据

输入

```
{
  authors(id: 1){
    name
  }
  articles(id: 2){
    title
  }
}
```

查询结果

```json
{
  "data": {
    "authors": {
      "name": "Li Ming"
    },
    "articles": {
      "title": "这是第二本书"
    }
  }
}
```

可以发现查询结果的数据结构和请求的数据结构是相同的，便于前端处理数据

### 别名

- 可以在字段前加```name:```来重命名返回的字段名称，便于前端命名

输入

```
{
  user:authors(id: 1){
    id:name
  }
}
```

查询结果

```json
{
  "data": {
    "user": {
      "id": "Li Ming"
    }
  }
}
```

### 变量和指令

使用```$varName```表示变量，后加```!```表示是必要的变量，反之表示是可选的变量，类似于函数的输入参数

使用```@include、@skip```指令可以对查询添加条件

使用变量查询：

query: 

```
query Author($id: Int, $b: Boolean!){
  authors(id: $id){
    name
    email @include(if: $b)
  }
}
```

variables:

```json
{
  "id": 3,
  "b": false
}
```

结果

```json
{
  "data": {
    "authors": {
      "name": "Zhang Ming"
    }
  }
}
```

将b的值改成true后，查询结果

```json
{
  "data": {
    "authors": {
      "name": "Zhang Ming",
      "email": "Zhang@gmail.com"
    }
  }
}
```

### 变更

类似于RESTful，改变数据和查询数据最好使用不同的类型，查询数据的query可以省略

变更数据一般使用mutation

需要在```__init__.py```中添加Schema对mutation的配置

```
view_func = GraphQLView.as_view('test', schema=Schema(query=Query, mutation=Mutation), graphiql=True)
```

在```graphql.py```中新建类Mutation

```python
class Mutation(ObjectType):
    addArticle = Field(type=ArticlesNode, title=String(), year=Int())

    @staticmethod
    def resolve_addArticle(self, info, title, year):
        a = Articles(title, year)
        db.session.add(a)
        db.session.commit()
        return a
```

输入

```
mutation addArticle($title: String, $year: Int){
  addArticle(title: $title, year: $year){
    title,
    id
  }
}
```

变量

```json
{
  "title": "new Article",
  "year": 2020
}
```

结果

```json
{
  "data": {
    "addArticle": {
      "title": "new Article",
      "id": "QXJ0aWNsZXNOb2RlOjg="
    }
  }
}
```

此处id使用了base64编码，明文是```ArticlesNode:8```，查看数据库这条数据的id是8

# hoppscotch(Postwoman)

 支持**Request**、**Websocket**、**Server Sent Events**、**Socket.IO**、**MQTT**、**GraphQL**等操作，一个方便免费的调试工具，用来代替postman

[hoppscotch/hoppscotch: 👽 A free, fast and beautiful API request builder used by 120k+ developers. https://hoppscotch.io](https://github.com/hoppscotch/hoppscotch)

