pydaemon
========

一个基于python的简单后台任务管理框架，分为三个部分：

* daemon
  
  Daemon实现了进程守护化，是所有任务的父类，它实现了守护进程的三个基本命令：start|stop|restart。

* jobs

  所有的job都继承自Daemon，只需实现run()方法来完成他们需要完成的事情。
  
* manager

  任务管理器，它维护一个任务列表，并且提供对各个任务的启动，停止，重启，重载（重新加载配置文件、资源文件等--暂未实现）等操作，只需将需要管理的任务配置到配置文件即可。

Installation
==========
