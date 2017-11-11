from random import randint
import networkx as nx

graph = nx.Graph()
x = randint(7,15)
y = randint(2,5)
for i in range(x):
  graph.add_node("v{}".format(i))

for i in range(y):
  graph.add_node("e{}".format(i))

for i in range(x):
  for j in range(y):
    if randint(0,100) <= 25:
      graph.add_edge("v{}".format(i),"e{}".format(j))

      
