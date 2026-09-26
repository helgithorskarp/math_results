"""Exact incidence matrix for the complete 71-point reduction."""
from itertools import combinations_with_replacement


def system(spectra, n=71):
    lower = n-64
    parallel = [p for p in combinations_with_replacement(range(lower,17),5)
                if sum(p)==n]
    pencils = [(k,p) for k in range(5)
               for p in combinations_with_replacement(range(max(lower,n+5*k-80),17),6)
               if sum(p)==n+5*k]
    columns = [('s',s) for s in spectra] + [('p',p) for p in parallel] + [('l',p) for p in pencils]
    names, matrix, rhs = [], [], []
    def row(name, coefficient, value):
        names.append(name)
        matrix.append([coefficient(kind,x) for kind,x in columns])
        rhs.append(value)
    row('planes',lambda t,x:int(t=='s'),155)
    row('plane_points',lambda t,x:x[0] if t=='s' else 0,31*n)
    row('plane_pairs',lambda t,x:x[0]*(x[0]-1)//2 if t=='s' else 0,3*n*(n-1))
    row('parallel_classes',lambda t,x:int(t=='p'),31)
    for m in range(lower,17):
        row(f'parallel_size_{m}',lambda t,x:int(x[0]==m) if t=='s' else (-x.count(m) if t=='p' else 0),0)
    for k in range(5):
        for m in range(lower,17):
            row(f'pencil_{k}_size_{m}',lambda t,x:(x[1+k] if x[0]==m else 0) if t=='s'
                else (-x[1].count(m) if t=='l' and x[0]==k else 0),0)
    row('lines',lambda t,x:int(t=='l'),775)
    row('line_points',lambda t,x:x[0] if t=='l' else 0,31*n)
    row('line_pairs',lambda t,x:x[0]*(x[0]-1)//2 if t=='l' else 0,n*(n-1)//2)
    return columns,names,matrix,rhs
