import random

data = open("data.txt", 'r')
set1 = open("set1.txt", 'w')
set2 = open("set2.txt", 'w')
set3 = open("set3.txt", 'w')
set4 = open("set4.txt", 'w')
set5 = open("set5.txt", 'w')
x = 1
for line in data:
	if (x==1):
		set1.write(line)
	elif (x==2):
		set2.write(line)
	elif (x==3):
		set3.write(line)
	elif (x==4):
		set4.write(line)
	elif (x==5):
		set5.write(line)
	x = (x+1)%6

# for line in data:
# 	x = random.choice([1,0])
# 	if (x == 1):
# 		train.write(line)
# 	else:
# 		test.write(line)

# data.close()
# train.close()
# test.close()
