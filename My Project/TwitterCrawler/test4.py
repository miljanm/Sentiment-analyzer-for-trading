#!/usr/bin/python
'''
Created on 4 Dec 2013

@author: miljan
'''
# import time
# def test3():
#     for i in xrange(5):
#         yield i
#  
# if __name__ == '__main__':
#     a = test3()
#     for i in a:
#         print i

# for i in xrange(5):
#     yield i
import subprocess, sys
 
proc = subprocess.Popen(
            ['python','./StreamingAPI.py'],
            shell=False,
            stdout=subprocess.PIPE
        )
# for line in iter(proc.stdout.readline,''):

# proc = subprocess.Popen(
#             ['python','./test3.py'],
#             shell=False,
#             stdout=subprocess.PIPE)

for line in iter(proc.stdout.readline,''):
    print line
# 
# print subprocess.check_output(
#             ['python','./test3.py'],
#             shell=False)

# print subprocess.check_output(
#             ['python','./StreamingAPI.py'],
#             shell=False)