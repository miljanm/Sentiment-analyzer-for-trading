#!/usr/bin/python
'''
Created on 4 Dec 2013

@author: miljan
'''

import subprocess
import atexit, time

# proc = subprocess.Popen(
#             "./StreamingAPI.py",             #call something with a lot of output so we can see it
#             shell=True,
#             stdout=subprocess.PIPE
#         )
# for line in iter(proc.stdout.readline,''):
#     print line

# proc1 = subprocess.call('python test4.py', shell=True)
# def test1():
#     proc1 = subprocess.Popen('python test4.py', shell=True, stdout=subprocess.PIPE)
#     for line in proc1.stdout:
#         print line
# 
# test1()
# 


# 
# def inner():
#     proc = subprocess.Popen(
#         ['python','test4.py'],             #call something with a lot of output so we can see it
#         shell=True,
#         stdout=subprocess.PIPE
#     )
# 
#     for line in iter(proc.stdout.readline,''):
#         time.sleep(1)                           # Don't need this just shows the text streaming
#         print line.rstrip() + '<br/>\n'
# 
# inner()
# procs = []
# @atexit.register
# def kill_subprocesses():
#     for proc in procs:
#         proc.kill()
import sys
for i in xrange(4):
    time.sleep(1)
    print i
    sys.stdout.flush()