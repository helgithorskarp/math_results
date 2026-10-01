"""Exact rational models for the two orientations of the 24-contact core.

The polynomial primitives and canonical rational-function field are reused,
with attribution, from tammes15_contact_pattern_obstruction. The perturbed
realization argument and all quantitative bounds are new in this directory.
"""
from functools import lru_cache
from fractions import Fraction as Q

LO, HI = Q(14, 25), Q(593, 1000)
PIECES = 4


class Models:
    def __init__(self, base, core):
        self.base, self.core = base, core
        R = self.R = core.Rat
        self.one, self.zero, self.t = R(base.ONE), R(), R(base.T)
        one, zero, t = self.one, self.zero, self.t
        self.H = [[one if i == j else t for j in range(3)] for i in range(3)]
        self.HI = [[(one/(one-t) if i == j else zero)-t/((one-t)*(one+2*t))
                    for j in range(3)] for i in range(3)]
        A = {i: [one if j == k else zero for j in range(3)]
             for k, i in enumerate((0, 5, 11))}
        B = {i: [one if j == k else zero for j in range(3)]
             for k, i in enumerate((1, 2, 4))}
        self.ap, self.bp, _ = base.model('asymmetric')
        r = 2*t/(one+t)
        edges = set()
        for group, steps in ((A, self.ap), (B, self.bp)):
            roots = list(group)
            edges.update(tuple(sorted((i, j))) for i in roots for j in roots if i < j)
            for n, i, j, o in steps:
                base.need(all(tuple(sorted(e)) in edges for e in ((i,j),(i,o),(j,o))),
                          'old equilateral triangle for every reflection')
                group[n] = [r*(a+b)-c for a,b,c in zip(group[i],group[j],group[o])]
                edges.update((tuple(sorted((n,i))),tuple(sorted((n,j)))))
        self.cross_edges = ((6,8),(7,12),(9,10),(9,13))
        edges.update(self.cross_edges)
        self.edges = sorted(edges)
        self.A, self.B = A, B
        self.w = self.dot(B[10], B[13])
        self.k = t*(9*t*t-2*t-3)/(one+t)**2
        self.gamma = self.k/(one+self.k)
        self.q2 = (one+2*self.k)/(one+self.k)**2
        self.mu = (t-one)*(t+one)*(2*t+one)*(3*t-one)/(9*t**3-t*t-t+one)
        self.v = [2*t/(one+self.w)*(x+y)-z for x,y,z in zip(B[10],B[13],B[2])]
        reflected = [[A[j][i] for j in (6,7,9)] for i in range(3)]
        self.ri = self.inverse(reflected)
        self.branches = {}
        for sign in (-1,1):
            C = [self.gamma*x+sign*self.mu*y
                 for x,y in zip(B[12],self.mv(self.HI,self.cross(B[12],self.v)))]
            rhs = [self.k,t,t-self.gamma*self.dot(self.v,B[12])]
            X = [[sum((z*self.H[j][i] for j,z in enumerate(V)),zero) for i in range(3)]
                 for V in (self.v,B[8],C)]
            gram = [[self.dot(x,y) for y in (self.v,B[8],C)] for x in (self.v,B[8],C)]
            aug = [row+[rhs[i]] for i,row in enumerate(gram)]+[rhs+[one]]
            xi = self.inverse(X)
            u = self.mv(xi,rhs)
            W = [self.gamma*(x+y)+sign*self.mu*z
                 for x,y,z in zip(u,self.v,self.mv(self.HI,self.cross(self.v,u)))]
            roots = [[sum((z*self.ri[j][i] for j,z in enumerate(row)),zero)
                      for i in range(3)] for row in zip(u,W,self.v)]
            model = dict(B)
            for label,av in A.items():
                model[label] = [sum((roots[i][j]*av[j] for j in range(3)),zero)
                                for i in range(3)]
            self.branches[sign] = {
                'C': C, 'X': X, 'xi': xi, 'u': u, 'W': W,
                'det': core.determinant(aug), 'model': model,
                'gramdet': core.determinant(gram),
            }

    def dot(self,x,y):
        return sum((x[i]*self.H[i][j]*y[j] for i in range(3) for j in range(3)),self.zero)

    @staticmethod
    def cross(x,y):
        return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]

    def mv(self,M,x):
        return [sum((a*b for a,b in zip(row,x)),self.zero) for row in M]

    def inverse(self,M):
        D = self.core.determinant(M)
        cof = [[(-1)**(i+j)*self.core.determinant(
                [[M[k][l] for l in range(3) if l!=j] for k in range(3) if k!=i])
                for j in range(3)] for i in range(3)]
        result = [[cof[j][i]*self.R(D.d,D.n) for j in range(3)] for i in range(3)]
        # No geometric division is inferred until the interval checks succeed.
        for i in range(3):
            for j in range(3):
                self.base.need(sum((M[i][k]*result[k][j] for k in range(3)),self.zero)
                               == (self.one if i==j else self.zero), 'exact inverse identity')
        return result

    def derivative(self,f):
        b = self.base
        return self.R(b.sub(b.mul(tuple(i*f.n[i] for i in range(1,len(f.n))),f.d),
                            b.mul(f.n,tuple(i*f.d[i] for i in range(1,len(f.d))))),
                      b.mul(f.d,f.d))

    @lru_cache(maxsize=None)
    def polynomial_range(self,p,lo,hi):
        values = self.base.bernstein(p,lo,hi)
        return min(values),max(values)

    def bound(self,f):
        if not f.n:
            return Q(0),Q(0)
        lower = upper = None
        for i in range(PIECES):
            a,b = LO+(HI-LO)*i/PIECES, LO+(HI-LO)*(i+1)/PIECES
            nl,nh = self.polynomial_range(f.n,a,b)
            dl,dh = self.polynomial_range(f.d,a,b)
            self.base.need(not dl<=0<=dh, 'denominator sign on every closed subinterval')
            values = (nl/dl,nl/dh,nh/dl,nh/dh)
            l,h = min(values),max(values)
            lower = l if lower is None else min(lower,l)
            upper = h if upper is None else max(upper,h)
        return lower,upper

    def functions(self):
        result = {'w': self.w, 'height2': self.one-2*self.t*self.t/(self.one+self.w),
                  'kappa': self.k, 'gamma': self.gamma, 'q2': self.q2,
                  'Fprime': self.R(tuple(i*self.base.F[i] for i in range(1,len(self.base.F))))}
        for sign,m in self.branches.items():
            tag = 'minus' if sign==-1 else 'plus'
            result[tag+'_gramdet'] = m['gramdet']
            result[tag+'_det'] = m['det']
            for i,row in enumerate(m['xi']):
                for j,f in enumerate(row): result[f'{tag}_xi_{i}_{j}'] = f
        result['plus_det_over_F'] = self.branches[1]['det']*self.R(self.base.ONE,self.base.F)
        for i,row in enumerate(self.ri):
            for j,f in enumerate(row): result[f'ri_{i}_{j}'] = f
        for label,row in self.A.items():
            for i,f in enumerate(row): result[f'A_{label}_{i}'] = f
        for label,row in self.branches[1]['model'].items():
            for i,f in enumerate(row): result[f's_{label}_{i}'] = f
        return result

    def manifest(self):
        return {name: {'numerator':list(f.n),'denominator':list(f.d)}
                for name,f in sorted(self.functions().items())}
