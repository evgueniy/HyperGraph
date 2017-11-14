import random 
import matplotlib.pyplot as plt
import networkx as nx


def graph_generator():
  graph = nx.Graph()
  x = random.randint(7,15)
  y = random.randint(2,5)
  for i in range(x):
    graph.add_node("v{}".format(i))

  for i in range(y):
    graph.add_node("e{}".format(i))

  for i in range(x):
    for j in range(y):
      if random.randint(0,100) <= 25:
        graph.add_edge("v{}".format(i),"e{}".format(j))

  return graph

def incidence_to_primal(g):
  G = nx.Graph()
  nodes = []
  for node in g.nodes():
    if "v" in node:
      G.add_node(node)
      nodes.append(node)
      
  for node in nodes:
    test = nodes[:]
    test.remove(node)
    for other in test:
      L1 = list(g.neighbors(node))
      L2 = list(g.neighbors(other))
      if any(e in L1 for e in L2):
        G.add_edge(node, other)
        
  return G

  
    
def berge(g):  
  stack = []
  vu = []   #Pour marquer les nodes visités
  previous = {}  #Pour régler le problème d'hier
  l = [node for node in g.nodes()]   #Liste des nodes du graphe
  
  while l: 
    node = l.pop()   #Premier noeud qu'on visite
    previous[node] = None   #Pas de previous pour celui-là

    if node not in vu:   #Si pas déjà visité
      stack.append(node)
      
      while stack:   #Tanqut qu'il y a des noeuds dans le stack
        v = stack.pop()   
        if v not in vu:   
          vu.append(v)   #Marque le noeud
          L = list(g.neighbors(v))   #Voisins du noeud
          
          for node in L: 
            if ((node in vu and node != previous[v]) or (node not in vu)):
              #On ajoute les voisins au stacks sauf son précedent déjà visité
              stack.append(node)
              previous[node] = v   #Le previous des voisins est le noeud courant
          
        elif v in vu:
          #Quand on tombe sur un noeud déjà marqué, il y a un cycle
          return False
        
  return True

def clicM_isHyperEdge(g,graph):
  x = {}
  prec = None
  y = [sorted(list(i)) for i in g.edges()]
  for lst in y:
    for elem in lst:
      if 'e' in elem:
        x.setdefault(elem,set())
        prec = elem
      else:
        x[prec].add(elem)
  lst = BK(set(),set(graph.nodes()),set(),graph)
  flag = [False for i in range(len(lst))]
  for i in range(len(lst)):
    for key in x:
      if x[key] == lst[i]:
        flag[i] == True
  if False in flag:
    return False
  else:
    return True
  
def alpha_acyclic(g):
  graph = incidence_to_primal(g)
  if clicM_isHyperEdge(g,graph):
    return True
  return False

def BK(r,p,x,g,sol = [],m = [0]):
  if len(p) + len(x) == 0:
    if len(r) > m[0]:
      sol.clear()
      m[0] = len(r)
      sol.append(r)
    elif len(r) == m[0]:
      sol.append(r)
    print(r)
  for v in list(p):
    BK(r | {v}, p & set(g.neighbors(v)),x & set(g.neighbors(v)),g)
    p ^= {v}
    x |= {v}  
  if len(r) + len(p) == 0:
    return sol
      
def hypercycle(g):
  if berge(g):
    print("Hypergraphe acyclique au sens de Berge et α-acyclique")
  G = incidence_to_primal(g)
  elif alpha_acyclic(G):
    print("Hypergraphe α-acyclique")
  else:
    print("Hypergraphe ni acyclique au sens de Berge et ni α-acyclique")



g = graph_generator()
hypercycle(g)

graph = nx.Graph()
for i in range(1,8):
  graph.add_node("v{}".format(i))
for i in range(1,5):
  graph.add_node("E{}".format(i))
graph.add_edge('v1', 'E1')
graph.add_edge('v2', 'E1')
graph.add_edge('v2', 'E2')
graph.add_edge('v3', 'E1')
graph.add_edge('v3', 'E2')
graph.add_edge('v3', 'E3')
graph.add_edge('v4', 'E4')
graph.add_edge('v5', 'E3')
graph.add_edge('v6', 'E3')
#print(alpha_acyclic(graph))
ng = incidence_to_primal(graph)
print(BK(set(),set(ng.nodes()),set(),ng))
nx.draw(ng, with_labels=True)
plt.show()

  
  



        

