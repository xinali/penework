# 渗透测试系统penework设计及实现

整体重构以前写的penework，并使用vue2重写前端展示

## 涉及技术

前端：

```
vue2 
vue-router
vuex
element-ui 
webpack3
```

后端

```
python
flask
masscan
nscan
```

## 前端设计

利用vue2 开发前端，element-ui做前端展示组件,vuex做数据存储交换

## 后端设计 

后端采用mongodb

新建项目时，开启一个masscan扫描，在masscan扫描结束后，利用Nscan得到banner和title

后端api返回数据格式

```
{
    'code': 2000/3000/4000/5000/
    'message': xxx,
    'data':
}
```

其中

```
2000 =>   请求成功
4000 =>   已知错误
5000 =>   {
            5001: token过期
            5002: token非法
          }
6000 =>   未知错误
```

token 设计
```
token = jwt.encode({'time': login_time}, token_key, algorithm)
```

利用一个装饰器进行token检查

```
def auth_token(func):

    def wrapper(*args, **kwargs):
        token = ''
        if request.headers['token']:
            token  =  request.headers['token']
            decode_token = jwt.decode(token, Config.TOKEN_KEY, algorithm='HS256')
            if (int(time.time()) - decode_token['time']) > Config.EXPIRE_TIME
                return jsonify({'code':5001, 'message': 'Token Expire Time!'})
        return func(*args, **kwargs)

    return wrapper
```

需要利用任务队列来管理新建项目的创建，当有masscan时，只是录入项目的信息，并更新项目的状态为未开始。但没有项目正在扫描时，开启masscan扫描.为了缓解服务器的压力，每次只是运行固定个数的项目。

任务队列，利用celery，broker使用redis

### 数据库设计

![数据库设计](https://lh3.googleusercontent.com/-7-IsjOmaxxs/WsMZfvx9oLI/AAAAAAAAHTk/qQ4ea62CG5Ab581Q59snJj_uCgkQkuQ5wCHMYCw/I/%255BUNSET%255D)


## 插件及相关扩展功能

会拥有的功能
1. masscan和nscan扫描，目前已经完成
2. 漏洞库扫描，集合各种exp/shellcode，目前exp/shellcode收集中
3. 子目录/子域名 目前基本已经完成
4. 爬虫  彻底重构，还没有开始



## 开发进度

前端 40%左右
后端 30%左右 


## 参考

[vuex理解](https://zhuanlan.zhihu.com/p/24357762)


