#! /usr/bin/env python   
#coding=utf-8   
import os
import sys
from cfg import Config

class Manager(object):
    '''后台任务管理器'''
    def __init__(self, cfgfile):
        pass
        self.init_config(cfgfile)

    def init_config(self, cfgfile):
       self.cfg = Config(cfgfile)

    def do(self, job, operation):
        pass
        if job in self.cfg.programs:
            pass
            obj = self.get_obj(job) 
            
            {
                'start': lambda : obj.start(),        
                'stop': lambda : obj.stop(),        
                'restart': lambda : obj.restart(),        
            }.get(operation, self.emptyoper)()

    def get_obj(self, program):
        '''
        根据模块、类名，创建类对象
        注意：所有的类必须继承于Daemon类
        '''
        sm = self.cfg.programs[program]['module'] 
        sc = self.cfg.programs[program]['class'] 

        module_path = self.cfg.programs[program]['module_path'] 
        sys.path.insert(0, os.path.abspath(module_path))

        pidfile = os.path.join(self.cfg.pidpath, program)
        
        m = __import__(sm, globals(), locals(),[sc])
        c = getattr(m, sc) 
        obj = c(pidfile)
        return obj
    
    def emptyoper(self):
        print "emptyoper"

    def jobs(self, flag = 0):
        '''列出任务，flag表示列出状态:
            0: 所有
            1：活的
            2：死的
        '''
        pidpath = self.cfg.pidpath
        files = os.listdir(pidpath)
        jobs = {}
        for job in self.cfg.programs:
            jobs[job] = {'pid': None, 'alive': False} 

        for f in files:
            fullname = os.path.join(pidpath, f)
            if os.path.isfile(fullname):
                try:
                    pf = file(fullname, "r")
                    pid = int(pf.read().strip())
                    pf.close()
                    jobs[f] ={}
                    jobs[f]['pid'] = pid
                    alive = self.check_pid(pid) 
                    jobs[f]['alive'] =alive 

                except IOError:
                    pass

        for job in jobs.keys():
            if flag == 1 and not jobs[job]['alive']:
                del jobs[job]
            elif flag == 2 and jobs[job]['alive']:
                del jobs[job]
        return jobs 

    def check_pid(self, pid):
        '''检查给定的pid是否存活''' 
        alive = True
        try:
            os.kill(pid, 0)
        except OSError, e:
            if e.errno == 3:
                alive = False
            elif e.errno == 1:
                pass
            else:
                raise
        return alive 


if __name__ == "__main__":
    pass
    cfgfile = os.path.abspath(os.path.join(os.path.dirname(__file__), "./my.conf")) 
    print cfgfile
    print '----'
    mgr = Manager(cfgfile)
    mgr.do('job1','restart')
    #print mgr.jobs()
