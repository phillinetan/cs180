from math import log
import operator
import sqlite3 as sql

class tree_builder:
	def __init__(self):
		self.attrs = [attribute('TL'), attribute('TM'), attribute('TR'), attribute('ML'), \
					attribute('MM'), attribute('MR'), attribute('BL'), attribute('BM'), attribute('BR')]
		self.tree = []
		self.setup()

	def setup(self):
		self.conn = sql.connect(':memory:')
		#self.conn = sql.connect('train.db')
		self.c = self.conn.cursor()
		self.c.executescript("drop table if exists data;")
		self.c.executescript(''' CREATE table if not exists data(
						TL text, TM text, TR text,
						ML text, MM text, MR text,
						BL text, BM text, BR text, class text); ''')
		self.get_data()

	def get_data(self):
		inp = open('train.txt', 'r')
		for line in inp:
			line = line.strip('\n')
			line = line.replace('negative','-')
			line = line.replace('positive', '+')
			values = line.split(',')
			self.c.execute("insert into data values(?,?,?,?,?,?,?,?,?,?)", values)
		self.conn.commit()
		#print c.execute("select * from data").fetchall()
		inp.close()
	def trace(self):
		pass
	def choose(self, root, n):
		for i in self.attrs:
			print i.value,
		print '\n'
		if (root):
			self.c.execute('''create table if not exists temp as select * from data''')

		for attr in self.attrs:
			gain(self.c, attr)

		self.attrs = sorted(self.attrs, key = lambda attribute: attribute.gain, reverse=True)
		# for i in self.attrs:
		# 	print i.gain
		new = self.attrs.pop(0)
		self.addNode(n, new.value)			 #add root to tree, remove root attribute from available attributes

	def addNode(self, parent, attr):
		if (parent != None):
			print "chosen", parent.attr, parent.value,'->', attr
		for i in ['x','o','b']:
			#node(parent, value, attribute)
			new = node(parent, i, attr)
			if (parent != None):
				parent.child.append(new)
			self.tree.append(new)

	def build(self):
		self.choose(True, None)	#get gain of attributes
		print "------------------------------------"
		for n in self.tree:	#loop through each branch of tree
			#print n.attr, n.value
			self.c.executescript("drop table if exists temp;")
			getParent(self.c, n)
			if (entropy(self.c, n) == 0):
				majority(self.c, n)
			elif (self.attrs !=[]):
				self.choose(False,n)
			elif (self.attrs == []):
				#print "empty"
				majority(self.c,n)
			self.c.executescript("drop table if exists temp;")
		for i in self.tree:
			print i.attr, i.value

class attribute:
	def __init__(self, value):
		self.value = value
		self.gain = 0

	def setGain(self, val):
		self.gain = val		

class node:
	def __init__(self, parent, value, attribute):
		self.parent = parent
		self.value = value
		self.attr = attribute
		self.child = []

	def addChild(self, child):
		self.child.append(child)

	def leaf(self, value):
		self.end = value
		#print value

def entropy(c, s):
	#print 'entropy'
	e = 0
	pstmt = "select count(*) from temp where class = '+'"
	nstmt = "select count(*) from temp where class = '-'"
	if (isinstance(s,attribute)):
		#print 'attribute ako', s.value
		p = c.execute(pstmt).fetchall()
		n = c.execute(nstmt).fetchall()

	elif (isinstance(s, node)):
		#print "node ako", s.attr
		p = c.execute(pstmt+" and "+s.attr+"=?", s.value).fetchall()
		n = c.execute(nstmt+" and "+s.attr+"=?", s.value).fetchall()
	
	#print p,n
	p = float(p[0][0])
	n = float(n[0][0])
	total = p + n
	for i in [p,n]:
		if (i != 0 ):
			e -= (i/total) * log((i/total),2)
	#print s.value, " entropy=", e
	return e

def majority(c, s):
	#print 'majority'
	stmt = "select class, count(*) from temp where "+s.attr+"=?"+" group by class"
	result = c.execute(stmt,s.value).fetchall()
	result = sorted(result, key=lambda i:i[1], reverse=True)
	#print result
	if (result != []):
		s.leaf(result[0][0])
	else:
		s.leaf('-') #temporary value

def gain(c, attr):
	#print 'gain'
	gain = entropy(c,attr)
	total = c.execute("select count(*) from temp").fetchall()
	total = float(total[0][0])
	stmt = "select count(*) from temp where "
	for i in ['x','o', 'b']:
		prob = c.execute(stmt+attr.value+"=?", i).fetchall()
		prob = float(prob[0][0])/total
		gain -= prob * entropy(c, node(attr, i ,attr.value))
	
	#print attr.value, gain
	attr.setGain(gain)

def isolate(c, n):
	#print 'isolate'
	c.execute("delete from temp where "+n.attr+"!=?", n.value)
	#print c.execute("select count(*) from temp").fetchall()
	#print n.attr+'='+n.value

def getParent(c, n):
	#print 'getParent'
	c.execute("Create table if not exists temp as select * from data where "+n.attr+"=?", n.value)
	#print c.execute("select count(*) from temp").fetchall()
	if (n.parent == None):
		return 0
	else:
		new = n.parent
		isolate(c,new)
		getParent(c, new)
		#print new.attr+"="+new.value



tree = tree_builder()
tree.build()