# Pytalk
 基于PyQt与kqueue(epoll on unix)实现的局域网聊天系统，支持好友添加，图片发送，群聊，好友添加，聊天记录查看等功能
 
## Requirement
pyqt框架,unix kqueue系统调用

## 运行方法
 先source util文件夹里的user.sql到mysql数据库。
 打开server运行kserver.py，再运行ui文件夹里的login.ui即可跑起来
