"""
Authors : Sarah Ghiri - 000334719
          Evguéniy Starygin - 000443325
Date : 8 decembre 2017
"""

import random 
import matplotlib.pyplot as plt
import networkx as nx


def graph_generator():
    """ Génère un hypergraphe de maximum 15 vertex et 5 hyperedges
        sous forme d'un graphe d'incidence représenté par networkx.
    """
    graph = nx.Graph()
    x = random.randint(7,15)
    y = random.randint(2,5)
    for i in range(x):
        graph.add_node("v{}".format(i))
    for i in range(y):
        graph.add_node("e{}".format(i))
    for i in range(x):
        for j in range(y):
            if random.randint(0,100) <= 30:
                graph.add_edge("v{}".format(i),"e{}".format(j))

    return graph

def incidence_to_primal(g):
    """ Transforme le graphe d'incidence g
        d'un hypergraphe en graphe primal renvoyé.
    """
    G = nx.Graph()
    nodes = []
    for node in g.nodes():
        if "v" in node:
            G.add_node(node)
            nodes.append(node)
      
    for node in nodes:
        test = nodes[:]
        test.remove(node)
        for other_node in test:
            L1 = list(g.neighbors(node))
            L2 = list(g.neighbors(other_node))
            if any(edge in L1 for edge in L2):
                G.add_edge(node, other_node)
    return G

    
def berge(g):
    """ Effectue un parcours en profondeur du
        graphe d'incidence g d'un hypergraphe pour
        détecter un cycle. Renvoie True si acyclique.
    """
    stack = []
    vu = []   #Pour marquer les nodes visités
    previous = {}  
    l = [node for node in g.nodes() if len(list(g.neighbors(node))) > 1]
    #Liste des nodes du graphe
  
    while l:
        node = l[0]   #Premier noeud qu'on visite
        previous[node] = None   #Pas de previous pour celui-là

        if node not in vu:   
            stack.append(node)
      
            while stack:   
                vertex = stack.pop()   
                if vertex not in vu:
                    vu.append(vertex)   #Marque le noeud
                    if vertex in l:  #Pour pas repasser pour rien
                        l.remove(vertex) 
                    neighbors = list(g.neighbors(vertex))   #Voisins du noeud
          
                    for node in neighbors:
                        if node in vu and node != previous[vertex]:
                            #Quand on tombe sur un noeud déjà marqué non précédent, il y a un cycle
                            return False
                        elif node not in vu:
                        #On ajoute les voisins au stack sauf son précédent déjà visité
                            stack.append(node)
                            previous[node] = vertex   #Le previous des voisins est le noeud courant
                      
    return True
    
def gamma_acyclic(g):
    """ Teste la gamma-acyclicité du graphe d'incidence
        g d'un hypergraphe par élimination suivant des règles.
    """
    change = True
    G = g.copy()    
    
    while change and G.nodes():
        change = False
        
        for element in list(G.nodes()):
            if "v" in element and len(list(G.neighbors(element))) <= 1:
                #Suppression des vertex appartenant à 0 ou 1 hyperedge
                G.remove_node(element)   
                change = True 
                
            elif "e" in element:
                useless_hyperedge = True
                for other_hyperedge in G.nodes():
                    if "e" in other_hyperedge:
                        #Pour éviter d'itérer sur tous les nodes les all et any
                        if element != other_hyperedge:
                            if list(G.neighbors(element)) == list(G.neighbors(other_hyperedge)):
                                #Suppression des hyperedges exactement égales à un autre.
                                G.remove_node(element)
                                change = True
                                break
                                
                            elif not (all(neighbors in list(G.neighbors(other_hyperedge)) for neighbors in list(G.neighbors(element)))\
                                or not any(neighbors in list(G.neighbors(other_hyperedge)) for neighbors in list(G.neighbors(element)))):
                                useless_hyperedge = False
                            #Pour savoir si un hyperedge répond à la règle 2 des gammas.
                        
                if useless_hyperedge and element in G.nodes():
                    #Si suit la règle 2 --> suppression.
                    G.remove_node(element)
                    change = True
         
    return True if not G.nodes() else False


def delete_nest_point(dico,lst,node):
    """ supprime les sommets et hyper arete vide"""
    for key in lst:
        dico[key] ^= {node}
        if len(dico[key]) == 0:
            del dico[key]   

def hyperEdge(g):
    """Créer un dictionnaire contenant
    les hyper arêtes en clef et avec ses set d'arêtes
    """
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


def isNestPoint(hyperE,lst,key):
    """ Verifie si le point est bien un nest"""
    for nest in lst: # on regarde si chaque hyper edge de la liste est un sous ensemble ou key2 est un sous ensemble de ces derniers
        if abs(len(hyperE[nest]) - len(hyperE[key])) != len(hyperE[nest]^hyperE[key]): #si un des hyper edge n'est pas un sous ensemble de l'autre
            return False # pas un nest point
    return True

def beta_acyclic(g):
    """ Teste la beta-acyclicité du graphe d'incidence
        g d'un hypergraphe par élimination suivant des règles.
    """
    source = hyperEdge(g) # dico à itérer 
    copy = hyperEdge(g) # dico servant à vider si beta acyclique
    delete = True # tant qu'au moins un éléments a été supprimé
    while delete and len(copy) != 0: # et qu'on possède toujours une hyper edge
        delete = False
        for key in source: #pour les hyper edges dans le dico
            if key in copy: #si  pas supprimer on passe à la suivante
                for node in source[key]: #les sommets dans l'hyper arête
                    if key in copy and node in copy[key]: #si plus d'hyper arrête ou de sommets on passe à la suivante
                        contenu = [] #liste des différents hyper edge contenant le sommet node
                        ok = True # si chaque hyper arête contenant node est un sous ensemble 
                        contenu.append(key)
                        for key2 in source: #2 eme parcours du dico pour comparer
                            if key != key2 and key2 in copy: #idem
                                if node in source[key2]: #si le sommets est contenu dans l'hyper arête key2
                                    ok = isNestPoint(copy,contenu,key2)
                                    if not ok: #on sort
                                        break
                                    else:
                                        contenu.append(key2) #on ajoute l'hyper edge à la liste
                        if ok:
                            delete = True #au moin un sommet a été supprimé
                            delete_nest_point(copy,contenu,node) # on enlève l'élement du dico copy
    return len(copy) == 0 



def alpha_acyclic(g):
    """ Renvoie True si le graphe g est alpha-acyclique.
    """
    
    i = 0
    max_cliques = []
    G = incidence_to_primal(g)
    nodes = [node for node in G.nodes() if len(list(G.neighbors(node))) >= 1]
    #Liste de noeuds appartenant à au moins une hyperedge.
    previous_len = len(nodes)  
    
    while nodes:
        
        vertex = nodes[i]  
        neighbors = [neighbor for neighbor in G.neighbors(vertex) if neighbor in nodes]
        #liste des voisins non supprimés de ce vertex.
        
        if detect_clique(neighbors, G):
            #Elimination simpliciale, suppression noeud formant clique avec ses voisins.
            nodes.remove(vertex)
            neighbors.append(vertex)

            #Ajout des cliques si maximales dans max_cliques
            if not max_cliques or len(max_cliques[0]) == len(neighbors):
                max_cliques.append(neighbors)
            elif len(max_cliques[0]) < len(neighbors):
                del max_cliques[:]
                max_cliques.append(neighbors)
        i += 1
        if i >= len(nodes) and len(nodes) == previous_len:
            #Parcouru toute la liste sans changement graphe non cordal.
            return False

        elif i >= len(nodes) and len(nodes) != previous_len:
            #Parcouru toute la liste avec changement
            previous_len = len(nodes)
            i = 0

    # Return true si les cliques maximales sont des hyperedges.
    return True if check_max_cliques(g, max_cliques) else False


def detect_clique(neighbors, G):
    """ Renvoie True si les noeuds de la liste neighbors
        forment une clique tous ensemble dans le graphe primal G.
    """
    for neighbor in neighbors:
        #Pour une clique les voisins doivent posséder les autres en voisin.
        if not all(node in list(G.neighbors(neighbor)) for node in neighbors if node != neighbor):
            return False
    return True
        
    
def check_max_cliques(g, max_cliques):
    """ Return True si les cliques maximales sont bien
        des hyperarètes de l'hypergraphe g.
    """
    hyperaretes = [sorted(list(g.neighbors(node))) for node in g.nodes() if "e" in node]
    for clique in max_cliques:
        if sorted(clique) not in hyperaretes:
          #Une clique maximale n'est pas un hyperedge
            return False
        
    return True    

                                    
def bipartite_draw(g):
    """ Fonction qui dessine les noeuds et hyperarêtes
        du graphe d'incidence de l'hypergraphe séparément.
    """
    pos = {}
    l = 0
    r = 0
    for elem in list(g.nodes()):
        
        if "v" in elem:  
            pos.update({elem: (1, l)})
            l += 1
        else:
            pos.update({elem: (2, r)})
            r += 2

    nx.draw(g, with_labels = True, pos=pos)
    plt.show()
                                    
def hypercycle(g):
    """ Fonction qui teste les différentes acyclicités
        possibles sur le graphe g et affiche le résultat.
    """
    if berge(g):
        print("Hypergraphe acyclique au sens de Berge, gamma-acyclique,\
              \n beta-acyclique et alpha-acyclique.")
               
    elif gamma_acyclic(g):
        print("Hypergraphe gamma-acyclique, beta-acyclique et alpha-acyclique.")
             
    elif beta_acyclic(g):
        print("Hypergraphe beta-acyclique et alpha-acyclique.")
        
    elif alpha_acyclic(g):
        print("Hypergraphe alpha-acyclique.")
                              
    else:
        print("Hypergraphe ni acyclique au sens de Berge, ni gamma-acyclique,\
               \n ni beta-acyclique et ni alpha-acyclique !")

def main():
    g = graph_generator()
    hypercycle(g)
    bipartite_draw(g)
    
          
if __name__ == "__main__":
    main()
    
