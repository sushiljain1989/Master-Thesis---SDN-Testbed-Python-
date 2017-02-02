#ps -ef | awk '/[m]n/{print $2}'
import os
import sys
import subprocess

cmd = 'ps -ef | awk \'/[m]n/{print $2}\'' #'lsof -t -i:{0}'.format(self.port)
pid = subprocess.check_output(cmd, shell=True)
#pid = int(pid)
killcmd2 = 'sudo kill -9 {0}'.format(pid.strip().replace('\n',' '))
os.system(killcmd2)

