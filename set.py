import random

a=[]
for i in range(20):
	a.append(random.randrange(0,193))
print a
# data = open("data.txt", 'r')
# set1 = open("set1.txt", 'w')
# set2 = open("set2.txt", 'w')
# set3 = open("set3.txt", 'w')
# set4 = open("set4.txt", 'w')
# set5 = open("set5.txt", 'w')
# x = 0
# for line in data:
# 	if (x==0):
# 		set1.write(line)
# 	elif (x==1):
# 		set2.write(line)
# 	elif (x==2):
# 		set3.write(line)
# 	elif (x==3):
# 		set4.write(line)
# 	elif (x==4):
# 		set5.write(line)
# 	x = (x+1)%5
# fnames = ['set2.txt','set3.txt', 'set4.txt','set5.txt']
# out = open("test.txt", 'w')
# out.write("TL TM TR ML MM MR BL BM BR CLASS\n")
# for fname in fnames:
# 	with open(fname) as infile:
# 		for line in infile:
# 			out.write(line)

# out.close()