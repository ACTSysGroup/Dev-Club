# RESTful

> Representational State Transfer（表现层状态转化）
>
> 一种软件架构风格，设计风格而不是标准，只是提供了一组设计原则和约束条件。它主要用于客户端和服务器交互类的软件。基于这个风格设计的软件可以更简洁，更有层次，更易于实现缓存等机制。
>
> 
>
> **URI**：统一资源标识符，表示Web中的每一种可用的资源
>
> Web上可用的每种资源：HTML文档、图像、视频片段、程序等，由一个通用资源标识符（Uniform Resource Identifier, 简称"URI"）进行定位。
>
> **URL**：统一资源定位符，是URI概念的一个实现方式
>
> 使用基于IP的协议来定位因特网上的主机的URL方案：//<用户名>:<密码>@<主机>:<端口>/<url路径>
>
> 可能会省略“<用户名>:<密码>@”，“ :<密码>”，“ :<端口>”，和“/<url路径>”这些部分的某些或者全部
>
> - 用户名：任意的用户名称。有些方案（例如：ftp）允许使用用户名称的描述。
> - 密码：任意的密码。如果存在的话，它紧跟在用户名后面并用一个冒号隔开。

## 设计原则

1. Uniform Interface：统一的接口，服务端客户端统一接口

   客户端只需要关注接口即可，接口的可读性更强

2. Stateless：无状态，让客户端对服务端的操作完全通过表现层来进行

   客户端和服务器之间的交互在请求之间是无状态的。从客户端到服务器的每个请求都必须包含理解请求所必需的信息。如果服务器在请求之间的任何时间点重启，客户端不会得到通知。此外，无状态请求可以由任何可用服务器回答，这十分适合云计算之类的环境。客户端可以缓存数据以改进性能。

3. Cacheable：可缓存的

4. Client-Server：服务端客户端分离，客户端不包括数据，服务端不包括用户状态

5. Layered System：分层系统，客户端可不直接连接服务端，客户端通常无法表明自己是直接还是间接与端服务器进行连接，需要考虑安全策略。

6. Code on Demand：按需编码（可选），服务端可以返回一些 JavaScript 代码让客户端执行，去实现某些特定的功能

## 设计理念

RESTful是一种开发理念，每个URL代表一种资源

使用RESTful架构，格式统一，有利于团队并行开发，RESTful api可以为web、iOS、Android提供一套统一的接口

| 项目 | 内容                                                         |
| ---- | :----------------------------------------------------------- |
| 协议 | HTTP                                                         |
| 域名 | 专用域名：https://api.xxx.com/，或添加到主域名：http://xxx.com/api/ |
| 版本 | 放入url：https://api.xxx.com/v1/，或放入http头：Accept: version=1 |
| 名称 | url代表获取的资源，所以不在url中使用动词，一般使用名词；名词大多为复数形式，往往和数据库表对应；命名中使用```-```或```_```使得url更容易理解 |

## HTTP方法类型

使用HTTP方法区分不同类型的请求

安全：不论访问多少次，都不会改变服务器状态。如GET和HEAD

幂等：相同的请求后面的不会比第一次产生更多的影响。如GET、HEAD、PUT和DELETE

| HTTP方法 (数据库操作) | 作用                                           | 是否安全 | 是否幂等 |
| --------------------- | ---------------------------------------------- | -------- | -------- |
| GET (SELECT)          | 从服务器取出资源，从服务器获取数据             | 是       | 是       |
| POST (CREATE)         | 在服务器新建资源，传送数据到服务器             | 否       | 否       |
| PUT (UPDATE)          | 在服务器更新资源，客户端需要提供全部数据       | 否       | 是       |
| PATCH (UPDATE)        | 在服务器更新资源，客户端提供需要修改的部分数据 | 否       | 是       |
| DELETE (DELETE)       | 从服务器删除数据                               | 否       | 是       |

## RESTful命名规范

> **在此以Flask框架为例讨论接口规范**

- 用```/```来表示资源之间的层级关系
- 用请求的类型表示操作类型
- 用params表示过滤数据的条件
- URL中使用名词，大多为复数，不能使用动词词组
- URL请求采用小写字母，数字，部分特殊符号（非制表符）组成。
- URL请求中不采用大小写混合的驼峰命名方式，尽量采用全小写单词，如果需要连接多个单词，则采用连接符“_”连接单词

例如获取id为1234的用户数据，使用GET

非RESTful风格

 ```http
GET http://localhost:5000/getUserData?uid=1234
 ```

RESTful风格

 ```http
GET http://localhost:5000/users/1234
 ```

如果两个资源类型属于从属关系，在url中传值，例如某个id为````1234````的用户 发表的某一篇id为```0001```的文章：

 ```http
GET http://localhost:5000/users/1234/articles/0001
 ```

接收：

 ```python
@app.route('/users/<string:uid>/articles/<string:aid>')
def get_user(uid, aid):
    # ...
 ```

如果两个资源类型属于平行关系，或者说属于检索过滤的操作，使用params传参，例如某个id为```1234```的用户发表的标题为 ```t```，年份为```y```的文章：

 ```http
GET http://localhost:5000/users/1234/articles?title=t&year=y
 ```

接收：

 ```python
@app.route('/users/<string:uid>/articles')
def get_articles(uid):
    title = request.args.get('title')
    year = request.args.get('year')
    # ...
 ```

### GET

**从服务器获取资源**

例如获取id为1234的用户数据，使用GET

 ```http
GET http://localhost:5000/users/1234
 ```

flask

```python
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/users/<string:uid>')
def get_user(uid):
 	# 处理数据，从数据库找数据
 	return jsonify('data': {'uid': uid}), 200


if __name__ == '__main__':
 app.run(host='localhost', port=5000, debug=True)

```

对于不写methods的情况，默认接收GET (HEAD, OPTIONS 不常用)

可以自己写一个返回的工具模板

### POST

**给服务器发送数据**

例如用户注册，需要发送用户的数据，假设只有用户名和密码（加密过的）

```http
POST http://localhost:5000/users
```

发送``JSON``格式数据，写在body里面

```json
{
    "username": "nnnn",
    "password": "password"
}
```

flask

```python
@app.route('/users', methods=['post'])
def user_register():
    username = request.json.get('username')
    password = request.json.get('password')
    # 处理数据
    print(username, password)
    return jsonify(), 200
```

或者使用```form-data```发送数据

| key      | value    |
| -------- | -------- |
| username | nnnn     |
| password | password |

flask

```python
@app.route('/users', methods=['post'])
def user_register():
    username = request.form.get('username')
    password = request.form.get('password')
    # 处理数据
    print(username, password)
    return jsonify(), 200
```

### PUT

**更新数据，需要发送给后端全部数据**

例如更新某个id为1234的用户数据，假设用户数据有用户名和电话

```http
PUT http://localhost:5000/users/1234?username=nnnn&phone=10001
```

flask

```python
@app.route('/users/<string:uid>', methods=['put'])
def update_user(uid):
    username = request.args.get('username')
    phone = request.args.get('phone')
    print('update', uid, username, phone)
    return jsonify(), 200
```

### PATCH

**更新数据，发送需要更新的数据**

有时候只需要改动一个字段的数据时，使用PUT会对资源造成不必要的浪费，如网络带宽、数据库等，可以使用PATCH仅更新有变动的字段

例如更新某个id为1234的用户的用户名

```http
PATCH http://localhost:5000/users/1234/username/nnnn
```

```python
@app.route('/users/<string:uid>/username/<string:username>', methods=['patch'])
def update_user_name(uid, username):
    print('update', uid, username)
    return jsonify(), 200
```

### DELETE

删除某个id为1234的用户

```http
DELETE http://localhost:5000/users/1234
```

flask

```python
@app.route('/users/<string:uid>', methods=['delete'])
def delete_user(uid):
    print('delete', uid)
    return jsonify(), 200
```

### 状态码

| 状态码 | 含义                                           |
| ------ | ---------------------------------------------- |
| 200    | 已在响应中发出，或资源已被修改，或资源已被删除 |
| 201    | 新资源被创建                                   |
| 202    | 已接收处理但请求未完成                         |
| 203    | 成功返回资源的副本                             |
| 204    | 资源有空表示                                   |
| 301    | 资源的URI已被更新                              |
| 303    | 其它，如负载均衡                               |
| 304    | 资源未更改，缓存                               |
| 400    | 坏请求，如参数错误                             |
| 404    | 资源不存在                                     |
| 406    | 服务端不支持所需表示                           |
| 409    | 通用冲突                                       |
| 412    | 前置条件失败                                   |
| 415    | 接受到的表示不受支持                           |
| 500    | 通用错误相应                                   |
| 503    | 服务端无法处理请求                             |

- POST和PUT的区别：如果客户端指定创建资源的名称，一般使用PUT；如果服务端指定创建资源的名称，一般使用POST

