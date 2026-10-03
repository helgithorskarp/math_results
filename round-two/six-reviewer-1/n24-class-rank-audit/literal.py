"""Independent definition-level n8 control: all actual vertices and empty loop."""
from fractions import Fraction as Q
from math import comb
from exact import need, pack
from model import parameters, choose, sector


def literal_control():
    n = 8
    sizes, counts, N, s = parameters(n)
    B = [[Q(0) for b in range(n-1)] for a in range(n-1)]
    for a, d in [(2,Q(0)),(3,Q(1,2)),(4,Q(2,3))]:
        B[a][n-a] = B[n-a][a] = s-d
    B[3][3] = Q(1,17)
    for a in sizes[1:]:
        B[1][a] = B[a][1] = s-sum(choose(n-a-1,b-1)*B[a][b] for b in sizes[1:])
    B[1][1] = s-sum(choose(n-2,b-1)*B[1][b] for b in sizes[1:])
    vertices = [v for v in range(1<<n) if v.bit_count() <= n-2]
    need(len(vertices) == N, 'literal original vertex census')
    row_empty = {a:Q(N-s)-sum(choose(n-a,b)*B[a][b] for b in sizes) for a in sizes}
    loop = N-sum(comb(n,a)*row_empty[a] for a in sizes)
    L = [[(loop if a == b == 0 else row_empty[(a or b).bit_count()])
          if a == 0 or b == 0 else Q(s)*(a == b)+(B[a.bit_count()][b.bit_count()] if a&b == 0 else 0)
          for b in vertices] for a in vertices]
    C = [[v-1 for v in row[1:]] for row in L[1:]]
    U = [[Q(N)*(i == k)-1-C[i][k] for k in range(N-1)] for i in range(N-1)]
    rowU = [sum(row,Q(0)) for row in U]
    for i, a in enumerate(vertices):
        for k, b in enumerate(vertices):
            target = Q(N)*(i == k)-L[i][k]
            lift = (sum(rowU,Q(0)) if not i and not k else
                    -rowU[k-1] if not i else -rowU[i-1] if not k else U[i-1][k-1])
            need(target == lift, 'every literal original upper-lift entry')
            if a&b:
                need(L[i][k] == (s if a == b else 0), 'literal intersection support')
        need(sum(L[i],Q(0)) == N, 'literal original row')
        for point in range(n):
            need(sum((L[i][k] for k,b in enumerate(vertices) if b&(1<<point)),Q(0)) == s,
                 'literal point-star row including empty')
    # Pair-difference harmonics from the definition, not an irreducible module import.
    operators = []
    for j in range(n//2+1):
        I = list(range(max(1,j), min(n-2,n-j)+1))
        def f(a):
            v = 1
            for point in range(j):
                v *= bool(a&(1<<(2*point)))-bool(a&(1<<(2*point+1)))
            return int(v)
        lifted = [[f(v) if v.bit_count() == b else 0 for v in vertices] for b in I]
        g = [choose(n-2*j,a-j) for a in I]
        for a, v in zip(I, lifted):
            need(sum(t*t for t in v) == (2**j)*g[I.index(a)], 'literal harmonic norm')
        H = [[sum((lifted[k][i]*sum((C[i-1][ell-1]*lifted[m][ell]
                    for ell in range(1,N)),Q(0)) for i in range(1,N)),Q(0))
              for m in range(len(I))] for k in range(len(I))]
        direct = [[Q((2**j)*g[k])*(s*(a == b)-(comb(n,b) if not j else 0)
                   +(-1)**j*B[a][b]*choose(n-a-j,b-j))
                  for b in I] for k,a in enumerate(I)]
        need(H == direct, 'entire literal harmonic energy matrix')
        if not j:
            # Actual centered original layer indicators retain the empty coefficient.
            R = [[Q(counts[a-1])*(a == b)-Q(counts[a-1]*counts[b-1],N) for b in I] for a in I]
            energy = [[sum((L[i][k] for i,v in enumerate(vertices) if v.bit_count()==a
                           for k,w in enumerate(vertices) if w.bit_count()==b),Q(0))
                       -counts[a-1]*counts[b-1] for b in I] for a in I]
            need(energy == H, 'actual centered original mean lower energy')
            metric = [[sum((Q((v.bit_count()==a))-Q(counts[a-1],N))
                           *(Q((v.bit_count()==b))-Q(counts[b-1],N)) for v in vertices)
                       for b in I] for a in I]
            need(metric == R, 'actual centered original mean metric with empty')
        operators.append({'j':j,'sizes':I,'entire_literal_energy':H,'physical_norm':g})
    return pack({'n':n,'actual_vertices':N,'all_lift_entry_checks':N*N,
                 'all_original_point_star_checks':N*n,'original_loop':loop,
                 'full_table':B,'operators':operators})
