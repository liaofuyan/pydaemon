#! /usr/bin/env python
#coding=utf-8

from daemon.daemon import Daemon
import logging

class MyDaemon(Daemon):
    """"""
    def __init__(self, pidfile ="/var/tmp/mydaemon.pid"):
        super(MyDaemon, self).__init__(pidfile)

    def run(self):
        while not self.exited:
            pass
            #do your work 
            self.logger.info("this is a test.")  
    def _init_logger(self):
        pass
        logger = logging.getLogger('daemon')
        formatter = logging.Formatter('%(name)-12s %(asctime)s %(process)d %(message)s')
        logfile =  "/opt/envpy27/app/platform/jobs/data/log/daemon.log"
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        self.logger = logger 
if __name__ == "__main__":
    MyDaemon().start()
