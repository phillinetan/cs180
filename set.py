import random

data = open("data.txt", 'r')
train = open('train.txt', 'w')
test = open('test.txt', 'w')

for line in data:
	x = random.choice([1,0])
	if (x == 1):
		train.write(line)
	else:
		test.write(line)

data.close()
train.close()
test.close()