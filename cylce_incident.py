def primal(graph):
	x = {} 
	prec = None
	y = [list(i) for i in graph.edges()]
	for i in y:
		i.sort()
	for lst in y:
		for elem in lst:
			if 'e' in elem:
				x.setdefault(elem,set())
				prec = elem
			else:
				x[prec].add(elem)
	keys = list(x.keys())
	for key in x:
		if len(x[key]) == 1:
			continue
		s = set()
		del keys[0]
		for k in keys:
			
