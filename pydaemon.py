#! /usr/bin/env python   
#coding=utf-8   
from flask import Flask
from flask.ext.script import Manager,Command, Option
from manager.manager import Manager as jobMgr

app = Flask(__name__)
manager = Manager(app)

@manager.command
def list(opt):
    mgr = jobMgr("./manager/my.conf")    
    jobs = mgr.jobs(int(opt))
    print jobs 

@manager.command
def job(cmd, oper):
    mgr = jobMgr("./manager/my.conf")
    mgr.do(cmd,oper) 

if __name__ == "__main__":
    pass
    manager.run()

