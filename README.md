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


