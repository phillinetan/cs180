from sklearn import tree
import numpy as np
import pydotplus

f = open("train1.txt")
data = np.loadtxt(f)
x = data[:,:9]
y= data[:,9]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x,y)
p = clf.predict([[1, 1, 3, 2, 2, 2, 1, 2, 1]])
print p
dot_data = tree.export_graphviz(clf, out_file=None, feature_names=['TL', 'TM', 'TR', 'ML', 'MM', 'MR', 'BL', 'BM', 'BR'])
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("iris.pdf")