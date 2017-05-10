import random

a=[223, 568, 452, 466, 331, 400, 620, 720, 295, 597, 766, 659, 342, 211, 651, 441, 763, 228, 400, 134]


data = open("train1.txt", 'r')
out = open("noisy.txt", 'w')
x = 0
for line in data:
	if x in a:
		new=line.replace("positive", "negative")
		if (new == line):
			new=line.replace("negative", "positive")
		out.write(new)
	else:
		out.write(line)
	x+=1
out.close()
data.close()
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
# out = open("train1.txt", 'w')
# out.write("TL TM TR ML MM MR BL BM BR CLASS\n")
# for fname in fnames:
# 	with open(fname) as infile:
# 		for line in infile:
# 			out.write(line)

# out.close()
#1 train: train1 test:set1
#2  train: train2 test:set2
#3 train:train3 testLset3
#4