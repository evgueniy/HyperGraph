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
