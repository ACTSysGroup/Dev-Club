# Web框架的设计模式

## 设计模式

https://www.runoob.com/design-pattern/design-pattern-tutorial.html

设计模式是在构件设计阶段，通过定义类或特定对象之间的结构和行为，从而解决每类设计问题的通用解决方案

是一套被反复使用、多数人知道的、经过分类编目的、代码设计经验的总结。从定义上看，它涉及到了代码级别，侧重于解决实际的现实的问题，是对代码开发经验的总结

总体来说设计模式分为：

- 创建型模式：包括工厂方法模式、抽象工厂模式、单例模式、建造者模式、原型模式。

- 结构型模式：包括适配器模式、装饰器模式、代理模式、外观模式、桥接模式、组合模式、享元模式。

- 行为型模式：包括策略模式、模板方法模式、观察者模式、迭代子模式、责任链模式、命令模式、备忘录模式、状态模式、访问者模式、中介者模式、解释器模式。

还有并发型模式和线程池模式

---

设计模式之间的关系

<img src=".\images\设计模式.png" alt="设计模式" style="zoom:80%;" />

### 设计模式的原则

- 开闭原则：在对功能扩展的时候不去修改已有的代码，实现较高的可扩展性和热插拔，易于维护和升级。通过接口和抽象类实现
- 里氏代换原则(LSP)：任何基类可以出现的地方，子类一定可以出现。是对开闭原则的补充，实现开闭原则的关键步骤就是抽象化，里氏代换原则是对实现抽象化的规范。
- 依赖倒转原则：针对接口编程，依赖于抽象而不依赖于具体
- 接口隔离原则：降低耦合度，使用多个隔离的接口，比使用单个接口要好。
- 迪米特法则（最少知道原则）：一个实体应当尽量少地与其他实体之间发生相互作用，使得系统功能模块相对独立，降低耦合度
- 合成复用原则：尽量使用合成/聚合的方式，而不是使用继承，高内聚低耦合。

### 23种设计模式

#### 工厂方法

消费者任何时候需要某种产品，只需向工厂请求即可。消费者无须修改就可以接纳新产品。缺点是当产品修改时，工厂类也要做相应的修改。如：如何创建及如何向客户端提供。

#### 建造者模式

将产品的内部表象和产品的生成过程分割开来，从而使一个建造过程生成具有不同的内部表象的产品对象。建造模式使得产品内部表象可以独立的变化，客户不必知道产品内部组成的细节。建造模式可以强制实行一种分步骤进行的建造过程。

#### 抽象工厂

核心工厂类不再负责所有产品的创建，而是将具体创建的工作交给子类去做，成为一个抽象工厂角色，仅负责给出具体工厂类必须实现的接口，而不接触哪一个产品类应当被实例化这种细节

#### 原型模式

通过给出一个原型对象来指明所要创建的对象的类型，然后用复制这个原型对象的方法创建出更多同类型的对象。原始模型模式允许动态的增加或减少产品类，产品类不需要非得有任何事先确定的等级结构，原始模型模式适用于任何的等级结构。缺点是每一个类都必须配备一个克隆方法。

#### 单态模式

单例模式确保某一个类只有一个实例，而且自行实例化并向整个系统提供这个实例单例模式。单例模式只应在有真正的 “单一实例” 的需求时才可使用。

#### 适配器模式

把一个类的接口变换成客户端所期待的另一种接口，从而使原本因接口原因不匹配而无法一起工作的两个类能够一起工作。适配类可以根据参数返还一个合适的实例给客户端。

#### ......

https://mp.weixin.qq.com/s/Wdrj5vbIKXMZ7AJORiXpEQ

### MVC

>MVC不是框架，不是设计模式，更不是架构，而是一种架构模式。它不描述系统架构，也不指定使用什么技术，仅仅是描述系统架构的一种模式

是最常用的架构模式，适用于分层架构，将应用程序分为模型、视图、控制器三层

- 模型 (Model) : 存取数据的对象
- 视图 (View) : 用户界面，将控制器返回的数据显示在用户界面上
- 控制器 (Controller) : 作用于模型和视图之间，根据用户的操作调用模型进行操作或获取数据，返回给视图

### 前后端分离

最开始，MVC是后端的一种设计模式。绝大部分后端服务器，都做一件事情：接收用户发来的请求，返回一段响应内容。根据不同的URL，Router调用不同的Controller来处理。Router的作用就是让每个URL都有一段代码来负责响应

现在最常用的开发方式是前后端分离，将浏览器视为前端，而服务器视为后端，使用RESTful API进行交互，后端只需要关注api的实现 

|            | 前端                                              | 后端                                       |
| ---------- | ------------------------------------------------- | ------------------------------------------ |
| model      | JSON、XML、HTML数据等                             | 数据库、文件等                             |
| view       | 模板引擎、模板片段等                              | HTML模板                                   |
| controller | JS业务逻辑、HTTP请求交互（Ajax, JSONP, Websocket) | HTTP请求路由、搜索引擎、数据分析、文件服务 |

前端MVC需要向服务器端传递和接收的数据量都少很多，前端要做的等待和渲染工作也少很多，这意味着更好、更快的用户体验和更低的服务器端负载

## Flask项目结构

## Flask

>Flask适合开发者用最快的速度做一个简单的，Python做后端的网站。
>
>它适合一些一次性的工具，或者一些基于 现有API的简单web应用。
>
>需要实现一个简单的Web接口时，Flask可以开发的很快。例如想要将Python开发的深度学习算法对外开放Web api，使用Flask会比较方便。

Flask项目较为灵活，没有固定的目录结构，实际上使用Flask在单文件中即可实现简单的Web接口，但是对于开发一个较为复杂的项目，将全部代码写在一个文件中是不现实的，所以需要有一定的文件结构。

### 按照类型

> ~~import flask as django~~

目录结构：

```
myapp
│  manage.py
│          
├─myapp
│  │  config.py
│  │  extensions.py
│  │  create_app.py
│  │  
│  ├─api
│  │  │  articles.py
│  │  │  authors.py
│  │  │  __init__.py
│  │          
│  ├─models
│  │  │  models.py
│  │  │  __init__.py
```

```manage.py```

```python
from myapp.create_app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

# 生成app
app = create_app()

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

```myapp/config.py```

```python
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '123456'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 数据库配置
    # mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/dev-database'
    # postgre sql
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/dev-database'

    # token
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_SECRET_KEY = 'SECRET key!'

    # 额外的初始化操作
    @staticmethod
    def init_app(app):
        pass

```

```myapp/extensions.py```数据库等配置

```python
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate(db=db)


def config_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    # cache.init_app(app,config={'CACHE_TYPE':'redis'})
```

```myapp/create_app.py```

```python
from flask import Flask
from myapp.extensions import config_extensions
from myapp.api import config_blueprint
from myapp.config import Config


# 将创建app的动作封装成一个函数
def create_app(config_name):
    # 创建app实例对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(Config)

    app.debug=True

    # 加载扩展
    config_extensions(app)

    # 配置blueprint
    config_blueprint(app)

    # 返回app实例对象
    return app

```

```myapp/api/```目录下存放接口文件，使用blueprint配置路径

```myapp/api/__init__.py```

```python
from .authors import authors
from .articles import articles

DEFAULT_BLUEPRINT = (
    (authors, '/authors'),
    (articles, '/articles')
)


def config_blueprint(app):
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
```

```myapp/api/authors.py```一些对author的操作示例，路径需要加上blueprint配置的前缀，示例：```http://localhost:5000/authors/1```

```python
from flask import Blueprint, jsonify
from myapp.models.models import Authors, Articles, Publish

authors = Blueprint('authors', __name__)


@authors.route('/<int:id>', methods=['GET'])
def get_author_info(id):
    u = Authors.query.filter_by(id=id).first_or_404()
    return jsonify(u.serialize())


@authors.route('/<int:id>/articles', methods=['GET'])
def get_author_articles(id):
    res = []
    l = Publish.query.filter_by(author_id=id)
    return jsonify([i.serialize() for i in l])

```

```myapp/models/models.py```数据库模板

```python
from myapp.extensions import db


class Authors(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, name, email, password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password_hash': self.password_hash
        }


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, title, year):
        self.title = title
        self.year = year

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year
        }


class Publish(db.Model):
    __tablename__ = 'publish'
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True)
    authors = db.relationship('Authors', backref=db.backref('authors', lazy='dynamic'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'), primary_key=True)
    articles = db.relationship('Articles', backref=db.backref('articles', lazy='dynamic'))

    rank = db.Column(db.Integer)

    def __init__(self, author_id, article_id, rank):
        self.author_id = author_id
        self.article_id = article_id
        self.rank = rank

    def serialize(self):
        return {
            'author_id': self.author_id,
            'name': self.authors.name,
            'email': self.authors.email,
            'password_hash': self.authors.password_hash,
            'article_id': self.article_id,
            'title': self.articles.title,
            'year': self.articles.year
        }

    def authors_serialize(self):
        return {
            'id': self.author_id,
            'name': self.authors.name,
            'email': self.authors.email,
            'password_hash': self.authors.password_hash
        }

    def articles_serialize(self):
        return {
            'id': self.article_id,
            'title': self.articles.title,
            'year': self.articles.year
        }
```

#### 命令

```bash
python manage.py db init    # 初始化 生成migrations文件夹 第一次创建表的时候运行
python manage.py db migrate # 生成迁移文件
python manage.py db upgrade # 执行迁移
python manage.py downgrade  # 回退操作
python manage.py # 运行项目
```

### 按照功能模块

对于功能模块较多的项目，可以根据功能模块分开，每个功能模块一个包

例如

```
myapp
│  manage.py
│          
├─myapp
│  │  config.py
│  │  extensions.py
│  │  create_app.py
│  │  
│  ├─authors
│  │  │  api.py
│  │  │  authors.py
│  │  │  __init__.py
│  │          
│  ├─articles
│  │  │  api.py
│  │  │  __init__.py
|  |
|  ├─tools
|  |  |  api.py
|  |  |  __init__.py
```

### cookiecutter

可以使用```cookiecutter-flask-api```模板创建基于Flask的RESTful api项目

> ```bash
> pip install cookiecutter # 安装
> cookiecutter https://github.com/karec/cookiecutter-flask-restful # 创建项目
> ```
>
> 地址：
>
> https://github.com/karec/cookiecutter-flask-restful

## 常用模块

### 基于Token的RESTful接口

通过Token过滤非法请求，保证服务器和数据的安全

在用户登录时申请一个Token，Token设定有一定的有效期限，一般为1-2小时，登录后的请求都需要传递Token，服务器根据Token判断是否合法。每次请求都会刷新Token

#### JWT

JWT(json web token)是一种token规范，包含header, payload, signature三个部分之间用```.```分隔开，一般使用base64编码

>一个典型的token

> ```
> eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTEyNDAxMjUsIm5iZiI6MTYxMTI0MDEyNSwianRpIjoiZmNlMTMyMDYtNjJiZi00MWVmLWEwMjEtODM4YmEyMTkwNWZjIiwiZXhwIjoxNjExMjQzNzI1LCJpZGVudGl0eSI6eyJ1aWQiOjEyMzQsInVzZXJuYW1lIjoibm5ubiIsInBob25lIjoiMTAwMDEifSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.zRXeI7jb6xsm8p-Y_2W9-e9jqFmdlwGAd0K9MfZNij4
> ```

前端可以将token保存在local storage、cookie中

需要将```Authorization: JWT <token>```加入到请求头中

使用```flask_jwt_extended```模块实现

flask

 ```python
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
 ```

配置过期时间和密钥，为保证安全，可以定期更新密钥

 ```python
app = Flask(__name__)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
app.config['JWT_SECRET_KEY'] = 'secret-key'
jwt = JWTManager(app)
 ```

获取token

 ```python
@app.route('/login')
def user_login():
    user = {
        'uid': 1234,
        'username': 'nnnn',
        'phone': '10001'}
    # 假设user是一个用户类的实例
    t = create_access_token(identity=user)
    return jsonify({'token': t})
 ```

使用token

```python
@app.route('/token-test')
@jwt_required
def token_test():
    # 获取当前用户
    user = get_jwt_identity()
    print(user.get('uid'), user.get('username'), user.get('phone'))

    # 更新token
    token = create_access_token(user)
    return jsonify({'token': token}), 200
```

#### 项目配置

将token引入项目，需要在```myapp/config.py```中添加配置

```python
# token
JWT_ACCESS_TOKEN_EXPIRES = 3600
JWT_SECRET_KEY = 'SECRET key!'
```

在```myapp/extensions.py```中添加

```python
jwt = JWTManager()
```

```config_extensions```函数中添加

```python
jwt.init_app(app)
```

### Flask-Login模块

> [Flask-Login — Flask-Login 0.4.1 documentation](https://flask-login.readthedocs.io/en/latest/#your-user-class)

Flask-Login为Flask提供用户会话管理。它处理登录、注销和长时间记住用户会话的常见任务。

- 通过在会话中存储活动用户的Id来实现登录或者注销功能

- 可以限制某些接口为登录后才能访问

- 可以实现记住用户的功能。

- 帮助保护用户会话不被窃取。

```myapp/extensions.py```中添加配置

```python
login_manager = LoginManager()
```

```python
def config_extensions(app):
    # ...
    login_manager.init_app(app)
    # ...
```

#### login_required

> 使用session存储授权数据

通过@login_manager.user_loader加载对象，在需要登录才能访问的接口函数前加@login_required

使用login_user(user)将当前用户加入到session中，使用logout_user将当前用户移出

```myapp/api/login.py```

```python
from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user

from myapp.models.models import Authors
from myapp.extensions import redis_client
from myapp.extensions import login_manager

login = Blueprint('login', __name__)


@login_manager.user_loader
def load_user(userId):
    return Authors.query.filter_by(id=userId).first()


@login.route('/login', methods=['GET'])
def author_login():
    user_email = request.args.get('email')
    password_hash = request.args.get('password')
    a = Authors.query.filter_by(email=user_email).filter_by(password_hash=password_hash).first_or_404()
    login_user(a)
    return jsonify(), 200


@login.route('/logout', methods=['GET', 'POST'])
@login_required
def author_logout():
    logout_user()
    return jsonify(), 200


@login.route('/redis', methods=['POST'])
@login_required
def set_value():
    key = request.json.get('key')
    value = request.json.get('value')

    redis_client.set(key, value)
    return jsonify(), 200


@login.route('/redis/<string:key>', methods=['GET'])
@login_required
def get_value(key):
    i = redis_client.get(key)
    return jsonify({'value': i})

```

```myapp/models/models.py```中的Authors类中添加方法

```python
def is_authenticated(self):
    return True

def is_active(self):
    return True

def is_anonymous(self):
    return False

def get_id(self):
    return str(self.id)
```

测试：

向```http://localhost:5000/redis```发送请求，显示```401 Unauthorized```

发送登录请求，再次发送```POST http://localhost:5000/redis```请求，携带json数据

```json
{
    "key": "key",
    "value": "key value"
}
```

发送```GET http://localhost:5000/redis/key```请求查询数据成功

向```http://localhost:5000/logout```发送请求，用户登出，再次发送查询数据请求，显示401

#### request_loader

> 使用api key的授权登

将@login_manager.user_loader回调函数改为@login_manager.request_loader回调函数

```python
@login_manager.request_loader
def load_user_from_request(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = Authors.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = Authors.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None

```

