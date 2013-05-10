#coding=utf-8
from ConfigParser import ConfigParser

class Config():
    '''配置文件解析器'''
    def __init__(self, cfgfile):
        pass
        self.cfg = ConfigParser()
        self.cfg.read(cfgfile)
        self._parse()
    def _get_section(self):
        sections = self.cfg.sections()
        return sections
    def _get_option(self, sec):
        return self.cfg.options(sec)
    def _parse(self):
        sections = self.cfg.sections()
        programs = {}
        for sec in sections:
            if sec.startswith('program'):
                try:
                    pname = sec.split(':')[1] 
                    pmodule = self.cfg.get(sec,'module')
                    pclass= self.cfg.get(sec,'class')
                    pmodule_path= self.cfg.get(sec,'module_path')
                    programs[pname] = {'module': pmodule, 'class': pclass, 'module_path':pmodule_path}
                except Exception, e:
                    print e
                    pass
            elif sec == "general":
                try:
                    pidpath= self.cfg.get(sec, 'pidpath')
                    self.pidpath = pidpath
                except Exception, e: 
                    self.pidpath = "/var/tmp"
                    print e
        self.programs = programs
if __name__ == "__main__":
   cfgfile = "./my.conf" 
   cfg = Config(cfgfile)
   print cfg.programs
