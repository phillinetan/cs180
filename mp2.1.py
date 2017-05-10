from math import log
import operator
import sqlite3 as sql

class tree_builder: 		# represents the whole algo
	def __init__(self):
		self.attrs = [] 	#available attributes to be chosen from
		self.tree = []		#keeps nodes generated throughout the whole process
		self.cls =[] 		#attribute classifier (i.e. play tennis/ win) [0] attribute name [1] value [2] value
		self.leaves = []	#keeps leaves
		self.setup()

	def setup(self):		#creates temporary database
		print "setting up database"
		self.conn = sql.connect(':memory:')		#connects to sql
		#self.conn = sql.connect('train.db')
		self.c = self.conn.cursor()
		self.c.executescript("drop table if exists data;")		
		inp = open('train.txt', 'r')			#opens file containing data for training
		attr = inp.readline().strip('\n')		#gets the first line (assumed to be the column/attribute names)
		attr = attr.split(' ')
		stmt = "Create table if not exists data ("		#creates (main) data table
		cls = ''
		for i in attr:				
			if (i != attr[-1]):
				stmt += i+" text,"
				self.attrs.append(attribute(i))

			else:
				stmt += i+ " text)"
				self.cls.append(i)

		self.c.execute(stmt)
		self.get_data(inp)

	def get_data(self, inp):					#reads remaining lines (values) and adds to data table
		print "extracting data from training set"
		x = len(self.attrs)
		stmt = "insert into data values("+'?,'*x
		stmt += '?)'

		for line in inp:
			line = line.strip('\n')
			values = line.split(' ')
			self.c.execute(stmt, values)
		self.conn.commit()
		inp.close()
		cls = self.c.execute("select distinct "+self.cls[0]+" from data")		#gets the values for the classifier (i.e. yes/no)
		for i in cls:
			self.cls.append(str(i[0]))

	def trace(self, n):						#traces the finished tree
		if (n.parent == None):
			print n.attr, "->", n.value,"->",
		else:
			new = n.parent
			self.trace(new)
			print n.attr, "->",n.value, "->",

	def choose(self, root, n):			#calculates gain of available attributes, chooses the best, adds to tree
		if (root):
			self.c.execute('''create table if not exists temp as select * from data''')		#creates  another table for isolating the needed data

		for attr in self.attrs:		#calculates gain of each attribute in attributes array
			self.gain(attr)		

		self.attrs = sorted(self.attrs, key = lambda attribute: attribute.gain, reverse=True)	#sorts the attributes by gain in decreasing order
		
		print "------------computed gain---------------"
		for i in self.attrs:
			print i.value, i.gain	

		new = self.attrs.pop(0)					#pops the top (best) attribute
		self.addNode(n, new.value)
		print "best attribute:", new.value
		print "----------------------------------------"			 	

	def addNode(self, parent, attr):			#creates a node for the tree
		values = self.c.execute("select distinct "+attr+ " from data") 		#gets possible values for the chosen attribute (i.e. temp = hot/cold)
		for i in values:
			val = str(i[0])
			new = node(parent, val, attr)		#creates a node for each value of the attribute
			self.tree.append(new)				#adds the new nodes to the tree

	def entropy(self, s):						#computes entropy of given attribute
		e = 0
		stmt = "select count(*) from temp where "+self.cls[0]+"=?"		#template query for database
		if (isinstance(s,attribute)):									#computes entropy(attribute)
			p = self.c.execute(stmt, [self.cls[1]]).fetchall()			
			n = self.c.execute(stmt, [self.cls[2]]).fetchall()
			print "entropy of ", s.value

		elif (isinstance(s, node)):				#computes entropy for values of an attribute
			p = self.c.execute(stmt+" and "+s.attr+"=?", [self.cls[1],s.value]).fetchall()
			n = self.c.execute(stmt+" and "+s.attr+"=?", [self.cls[2],s.value]).fetchall()
			print "entropy of ", s.attr, '->', s.value

		p = float(p[0][0])
		n = float(n[0][0])
		total = p + n
		for i in [p,n]:				#gets overall entropy 
			if (i != 0 ):
				e -= (i/total) * log((i/total),2)
		print "entropy", e
		return e

	def majority(self, s):			#gets dominating value of the classifier attribute only called when there are no more available attributes or node can be a leaf 
		stmt = "select "+self.cls[0]+", count(*) from temp where "+s.attr+"=?"+" group by "+self.cls[0]
		result = self.c.execute(stmt,[s.value]).fetchall()
		result = sorted(result, key=lambda i:i[1], reverse=True)

		if (result != []):
			s.leaf(result[0][0])
		self.leaves.append(s)	#adds node to leaves array

	def gain(self, attr):		#computes gain of an attribute
		gain = self.entropy(attr)	#gets entropy of attribute
		total = self.c.execute("select count(*) from temp").fetchall()
		total = float(total[0][0])
		stmt = "select count(*) from temp where "
		values = self.c.execute("select distinct "+attr.value+ " from data").fetchall() # get possible values for attribute

		for i in values:
			val = str(i[0])
			prob = self.c.execute(stmt+attr.value+"=?", [val]).fetchall()
			prob = float(prob[0][0])/total
			gain -= prob * self.entropy(node(attr, val ,attr.value))
		
		attr.setGain(gain)
		print "gain of ", attr.value, attr.gain

	def isolate(self, n):		#eliminates unnecessary data from the (temp) table 
		self.c.execute("delete from temp where "+n.attr+"!=?", [n.value])
		

	def getParent(self, n):		#traces root parent of a certain node
		self.c.execute("Create table if not exists temp as select * from data where "+n.attr+"=?", [n.value])
		if (n.parent == None):
			return 0
		else:
			new = n.parent
			self.isolate(new)
			self.getParent(new)

	def build(self):
		self.choose(True, None)		#get gain of attributes and choose the "best" and sets it as the root
		print "------------------------------------"
		for n in self.tree:			#loop through each node of tree
			self.c.executescript("drop table if exists temp;")		#deletes the temp table
			self.getParent(n)
			if (self.entropy(n) == 0):		#checks if entropy of node is 0 meaning there is only one classification
				self.majority(n)			#gets the dominating value of classifier attribute
			elif (self.attrs !=[]):			#checks if there are still remaining available attributes
				self.choose(False,n)		#chooses best attribute
			elif (self.attrs == []):		#checks if there are no more available attributes
				self.majority(n)			#gets dominating value of classifier attribute 
			self.c.executescript("drop table if exists temp;")
		for i in self.leaves:				#traces finished tree
			self.trace(i)
			print i.end

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

	def leaf(self, value):
		self.end = value


tree = tree_builder()
tree.build()