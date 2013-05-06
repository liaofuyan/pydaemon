#coding=utf-8
import sys, os, time, atexit
import signal
from threading import Timer

class Daemon:
	'''守护进程基类'''
	__metaclass__=type 
	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.pidfile = pidfile
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr

		self.exited = False
		signal.signal(signal.SIGTERM, self.sigtrem_handler)
		
		self.timer = Timer(3, self.timer_handler)


	def daemonize(self):
		'''两次fork将进程守护化'''

		#脱离父进程
		try:
			pid = os.fork()
			if pid > 0:
				#父进程退出
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
			sys.exit(1)


		os.chdir('/')
		os.setsid()
		os.umask(0)

		#脱离控制终端
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
			sys.exit(1)

		#管道重定向
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)

		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())

		atexit.register(self.delpid)
		pid = str(os.getpid())
		file(self.pidfile, "w+").write("%s\n" % pid) 

	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""
		启动守护进程
		"""
		try:
			pf = file(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()

		except IOError:
			pid = None

		if pid:
			#确认pid确实存在，而不是异常死掉
			alive = True
			try:
				os.kill(pid, 0)
			except OSError, e:
				if e.errno == 3:#process is dead
					alive = False
				elif e.errno == 1:#no permission
					pass
				else:
					raise


			if alive:
				message = "pidfile %s already exist. Daemon already runing?\n" % self.pidfile
				sys.stderr.write(message)
				sys.exit(1)

		self.daemonize()
		self.run()

	def stop(self):
		"""
		退出守护进程
		"""

		try:
			pf = file(self.pidfile, "r")
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if not pid:
			message = "pidfile %s dose not exist or destroyed. Daemon not running?\n" % self.pidfile
			sys.stderr.write(message)
			return #如果是restart，这不是个错误

		try:
			while 1:
				self.timer.cancel()
				os.kill(pid, signal.SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print str(err)
				sys.exit(1)

	def restart(self):
		"""
		重启进程
		"""
		self.stop()
		self.start()

	def run(self):
		"""
		You should override this method when you subclass Daemon. It will be called after the process has been
		daemonized by start() or restart().
		"""
        while 1:
    		pass

	def sigtrem_handler(self, signalnum, stack):
		self.timer.cancel()
		self.exited = True

	def timer_handler(self):
		'''定时flush'''
		sys.stdout.flush()
		sys.stderr.flush()
		self.timer.finished.clear()
   		self.timer.run()
