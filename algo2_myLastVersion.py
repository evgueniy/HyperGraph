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
    

def alpha_acyclic(g):
    i = 0
    max_cliques = []
    G = incidence_to_primal(g)
    #nx.draw(G, with_labels=True)
    #plt.show()
    nodes = [node for node in G.nodes() if len(list(G.neighbors(node))) > 1]
    previous_len = len(nodes)
    
    while nodes:
        
        v = nodes[i]
        neighbors = [neighbor for neighbor in G.neighbors(v) if neighbor in nodes]
    
        if detect_clique(neighbors, G):
            nodes.remove(v)
            neighbors.append(v)
            if not max_cliques or len(max_cliques[0]) == len(neighbors):
                max_cliques.append(neighbors)
            elif len(max_cliques[0]) < len(neighbors):
                del max_cliques[:]
                max_cliques.append(neighbors)
        i += 1
        if i >= len(nodes) and len(nodes) == previous_len:
            return False

        elif i >= len(nodes) and len(nodes) != previous_len:
            previous_len = len(nodes)
            i = 0
    
    return True if check_max_cliques(g, max_cliques) else False


def detect_clique(neighbors, G):
    for neighbor in neighbors:
        if not all(node in list(G.neighbors(neighbor)) for node in neighbors if node != neighbor):
            return False
    return True
        
    
def check_max_cliques(g, max_cliques):
    hyperaretes = [sorted(list(g.neighbors(node))) for node in g.nodes() if "e" in node]
    for clique in max_cliques:
        if sorted(clique) not in hyperaretes:
            return False
        
    return True    
    
                                    
def hypercycle(g):
    if berge(g):
        print("Hypergraphe acyclique au sens de Berge et α-acyclique")

    elif alpha_acyclic(g):
        print("Hypergraphe α-acyclique")
                                      
    else:
        print("Hypergraphe ni acyclique au sens de Berge et ni α-acyclique")

def hyperEdge(g):
    x = list(g.edges())
    d = {}
    for i in x:
        prec = ''
        for j in sorted(i):
            if 'e' in j:
                d.setdefault(j,set())
                prec = j
            else:
                d[prec].add(j)
    return d
def alphac(g):
    d = hyperEdge(g)
    x = incidence_to_primal(g)
    if nx.is_chordal(x):
        l = [list(i) for i in nx.chordal_graph_cliques(x)]
        t = 0
        mx = []
        for i in l:
            if len(i) > t:
                t = len(i)
        if t in (0,1):
            return True
        for i in l:
            if len(i) == t:
                mx.append(i)
        flag = [False for i in mx]
        for i in range(len(mx)):
            for j in d:
                if sorted(mx[i]) == sorted(d[j]):
                    flag[i] = True
                    continue
        return False if False in flag else True
    else:
        return False

def delete_nest_point(dico,lst,node):
    for key in lst:
        dico[key] ^= {node}
        if len(dico[key]) == 0:
            del dico[key]
    
def beta(g):
    source = hyperEdge(g)
    copy = hyperEdge(g)
    delete = True
    while delete and len(copy) != 0:
        delete = False
        for key in source:
            if key not in copy:
                continue
            for node in source[key]:
                if key not in copy or node not in copy[key]:
                    continue
                contenu = []
                ok = True
                contenu.append(key)
                for key2 in source:
                    if key == key2 or key2 not in copy:
                        continue
                    if node in source[key2]:
                        for nest in contenu:
                            if abs(len(copy[nest]) - len(copy[key2])) != len(copy[nest]^copy[key2]):
                                ok = False
                                break
                        if not ok:
                            break
                        else:
                            contenu.append(key2)
                if ok:
                    delete = True
                    delete_nest_point(copy,contenu,node)
    return len(copy) == 0


            
g = graph_generator()

meme = []
while True:
    g = graph_generator()
    if beta(g):
        if not alphac(g):
            print('lul')
            break
        else:
            print('ok')




        

