#!/usr/bin/python3
#-*- coding: utf-8 -*-


import sys
import time
import random
import subprocess


titlesuffix = sys.argv[1].encode("utf-8")
timestamp = str(int(time.time())).encode("utf-8")


def gen_id():
	o = []
	for i in range(4):
		r = hex(random.randrange(0x100000000))[2:]
		o.append("0" * (8 - len(r)))
		o.append(r)
	return "".join(o).encode("utf-8")


for filename in sys.argv[2:]:
	output = []
	
	with open(filename, "rb") as feed:
		for line in feed:
			if b'"title":' in line:
				c = line.split(b"\"")
				c[3] = titlesuffix
				output.append(b"\"".join(c))
				del c
			elif b'"timestamp":' in line:
				c = line.split(b"\"")
				c[3] = timestamp
				output.append(b"\"".join(c))
				del c
			#elif b'"id":' in line:
			#	c = line.split(b"\"")
			#	c[3] = gen_id()
			#	output.append(b"\"".join(c))
			#	del c
			else:
				output.append(line)
	
	with open(filename, "wb") as feed:
		for line in output:
			feed.write(line)


subprocess.check_call("git add " + " ".join(sys.argv[2:]), shell=True)
subprocess.check_call("git commit --message='Commit by timestamp-updating script.'", shell=True)
subprocess.check_call("git push origin HEAD:bartek2", shell=True)





