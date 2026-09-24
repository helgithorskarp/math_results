"""Exact audits for the co-sunflower Tuza certificate. Standard-library Python.
Usage: python3 audit.py EXECUTABLE FULL_REPORT
Basic palette and edge-branching helpers adapted from ../tuza_two_type_complete/audit.py.
This is an author check, not independent peer review.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import subprocess
import sys

def require(value, message):
    if not value:
        raise RuntimeError(message)


def choose2(n):
    return n * (n - 1) // 2


def palette_size(n):
    return 1 if n < 2 else n - (n % 2 == 0)


def clique(n):
    if n < 3:
        return 0
    r = n % 6
    leave = 0 if r in (1, 3) else 4 if r == 5 else n // 2 + (r == 4)
    return (choose2(n) - leave) // 3


def ceil(x):
    return -(-x.numerator // x.denominator)



def factorization(vertices):
    """Round-robin matchings, checked as actual sets of unordered pairs."""
    vertices = list(vertices)
    if len(vertices) < 2:
        return [set()]
    n = len(vertices)
    size = n if n % 2 == 0 else n+1
    result = []
    for r in range(size-1):
        matching = {(r,size-1)}
        matching |= {tuple(sorted(((r+i)%(size-1),(r-i)%(size-1))))
                     for i in range(1,size//2)}
        result.append({tuple(sorted((vertices[x],vertices[y])))
                       for x,y in matching if x<n and y<n})
    return result



def find_packing(edge_count, triangles, target):
    """Exact edge-branching search, independent of all numerical bounds."""
    @lru_cache(None)
    def solve(available, need):
        if need == 0:return ()
        if available.bit_count() < 3*need:return None
        eligible = [t for t in triangles if t & available == t]
        if len(eligible) < need:return None
        counts = {}
        for tri in eligible:
            bits = tri
            while bits:
                edge = bits & -bits
                counts[edge] = counts.get(edge,0)+1
                bits -= edge
        if not counts:return None
        edge = min(counts,key=lambda x:(counts[x],x))
        for tri in eligible:
            if tri & edge:
                tail = solve(available ^ tri,need-1)
                if tail is not None:return (tri,)+tail
        return solve(available ^ edge,need)
    result = solve((1 << edge_count)-1,target)
    require(result is not None,"no packing meeting the claimed bound")
    used = 0
    for tri in result:
        require(tri in triangles and tri.bit_count()==3 and not tri&used,"bad witness")
        used |= tri
    require(len(result)==target,"incomplete witness")


def neighborhoods(p, c):
    u=sum(p)+c
    sets=[]
    at=0
    for size in p:
        sets.append(set(range(u))-set(range(at,at+size)))
        at+=size
    return sets


def reference(p, c, d, m):
    sets=neighborhoods(p,c)
    u=sum(p)+c; k=u+d
    sizes=[len(S) for S in sets]
    x=[Q(m[i],palette_size(sizes[i])) for i in range(3)]
    independent=sum(x[i]*choose2(sizes[i]) for i in range(3))
    independent-=sum(x[i]*x[j]*choose2(len(sets[i]&sets[j])) for i,j in combinations(range(3),2))
    independent+=x[0]*x[1]*x[2]*choose2(len(set.intersection(*sets)))
    common=max(Q(sum(a[i]*choose2(sizes[i]) for i in range(3)),palette_size(u))
               for a in product(*(range(z+1) for z in m)) if sum(a)<=palette_size(u))
    h=ceil(max(independent,common)); e=choose2(k)-h
    f=h+Q(clique(k),k*(k-1)*(k-2)//6)*Q(e*(4*e-k*k),3*k)
    return h,max(h,clique(k),ceil(f)),independent,common


def literal_cover(p,c,d,m):
    sets=neighborhoods(p,c); k=sum(p)+c+d
    best=choose2(k)
    for mask in range(1<<k):
        L={v for v in range(k) if mask>>v&1}
        deleted=choose2(len(L))+choose2(k-len(L))
        deleted+=sum(m[i]*min(len(S&L),len(S-L)) for i,S in enumerate(sets))
        best=min(best,deleted)
    return best


def actual_palettes(p,c,d,m,independent,common):
    sets=neighborhoods(p,c); u=sum(p)+c
    encode=lambda pairs:sum(1<<(i*u+j) for i,j in pairs)
    choices=[]
    for i,S in enumerate(sets):
        colors=[encode(P) for P in factorization(sorted(S))]
        choices.append([sum(colors[j] for j in J) for J in combinations(range(len(colors)),m[i])])
    actual=max((a|b|cc).bit_count() for a in choices[0] for b in choices[1] for cc in choices[2])
    require(actual>=ceil(independent),'independent palette failure')
    dp={(0,0,0):0}
    for color in factorization(range(u)):
        gains=[sum(a in S and b in S for a,b in color) for S in sets]
        nxt=dict(dp)
        for counts,value in dp.items():
            for i in range(3):
                if counts[i]<m[i]:
                    key=list(counts);key[i]+=1;key=tuple(key)
                    nxt[key]=max(nxt.get(key,-1),value+gains[i])
        dp=nxt
    require(max(dp.values())>=ceil(common),'shared palette failure')


def actual_graph(p,c,d,m):
    sets=neighborhoods(p,c); k=sum(p)+c+d
    edges=set(combinations(range(k),2));vertex=k
    for S,copies in zip(sets,m):
        for _ in range(copies):
            edges.update((v,vertex) for v in S);vertex+=1
    ids={e:i for i,e in enumerate(sorted(edges))}
    triangles=[]
    for vertices in combinations(range(vertex),3):
        pairs=list(combinations(vertices,2))
        if all(e in ids for e in pairs):triangles.append(sum(1<<ids[e] for e in pairs))
    return len(edges),triangles


@lru_cache(None)
def all_core_values(p,c,d):
    """Every surviving triangle-free clique core, with exact independent sets."""
    sets=neighborhoods(p,c);k=sum(p)+c+d
    edges=list(combinations(range(k),2));ids={e:i for i,e in enumerate(edges)}
    triangles=[sum(1<<ids[e] for e in combinations(T,2)) for T in combinations(range(k),3)]
    values=[]
    for core in range(1<<len(edges)):
        if any(core&t==t for t in triangles):continue
        alpha=[]
        for S in sets:
            largest=0
            for bits in range(1<<len(S)):
                J=[v for i,v in enumerate(sorted(S)) if bits>>i&1]
                if len(J)>largest and all(not core>>ids[e]&1 for e in combinations(J,2)):
                    largest=len(J)
            alpha.append(largest)
        values.append((core.bit_count(),tuple(alpha)))
    return tuple(values)


def exact_cover(p,c,d,m):
    sets=neighborhoods(p,c);k=sum(p)+c+d
    kept=max(edges+sum(m[i]*alpha[i] for i in range(3))
             for edges,alpha in all_core_values(p,c,d))
    return choose2(k)+sum(m[i]*len(sets[i]) for i in range(3))-kept


def expected_domain(u,last):
    # Independent coordinates: decreasing neighborhood sizes. Their sum is
    # 2u+c; p_i=u-s_i, and s1<u excludes two coincident full neighborhoods.
    shapes=cells=0
    for s0 in range(2,u+1):
        for s1 in range(2,min(s0,u-1)+1):
            for s2 in range(max(2,2*u-s0-s1),s1+1):
                shapes+=1; cells+=(s0-1)*(s1-1)*(s2-1)*(last-u+1)
    return shapes,cells


def read_report(path):
    rows={}; total=None
    for line in Path(path).read_text().splitlines():
        x=line.split()
        if x[0]=='ROW':
            u=int(x[1]); require(u not in rows,'duplicate row')
            rows[u]=tuple(map(int,x[2:]))
        elif x[0]=='TOTAL':
            require(total is None,'duplicate total');total=tuple(map(int,x[1:]))
        else:raise RuntimeError('unexpected line '+line)
    require(set(rows)==set(range(3,199)),'incomplete range')
    require(all(len(row)==6 and row[-1]==0 for row in rows.values()),'failures')
    for u,row in rows.items():
        shapes,cells=expected_domain(u,198)
        require(row[:2]==(shapes,cells),'domain mismatch')
        per_outside=cells//(199-u)
        skipped=max(0,198-u-max(2,54-u))
        require(row[4]==per_outside*skipped,'analytic coverage mismatch')
        require(row[3]==2*row[2]-row[0],'binary tree count mismatch')
    require(total==tuple(sum(row[i] for row in rows.values()) for i in range(6)),'bad total')
    return total


def quartic_audit():
    # Coefficients in ascending order. Verify the displayed curvature identity,
    # not a floating point minimum of the quartic.
    g=[Q(1,12),-Q(1,2),Q(11,12),-Q(4,9),Q(2,27)]
    second=[(i+2)*(i+1)*g[i+2] for i in range(3)]
    require(second==[Q(1,18)+Q(16,9),-Q(8,3),Q(8,9)],'curvature identity')
    a=Q(9,25)
    value=sum(v*a**i for i,v in enumerate(g))
    deriv=sum(i*v*a**(i-1) for i,v in enumerate(g) if i)
    bound=value-9*deriv*deriv
    require(bound==Q(3855551,1464843750) and bound>Q(1,400),'quartic gap')
    require(Q(199**2,400)-Q(199,2)-Q(1,4)>-1,'large-order threshold')
    require(sum(v*Q(1,4)**i for i,v in enumerate(g))==Q(31,3456),'left endpoint')
    require(sum(v*Q(1,2)**i for i,v in enumerate(g))==Q(5,432),'right endpoint')
    for t,expected in [(Q(1,4),-Q(13,108)),(Q(1,2),Q(13,108))]:
        require(sum(i*v*t**(i-1) for i,v in enumerate(g) if i)==expected,'endpoint derivative')
    require(Q(1,4)*(1-Q(2,3)*Q(1,4))**2==Q(25,144),'alpha derivative constant')
    require(Q(31*55**2,3456)-Q(55,2)-Q(1,4)>-1,'outside threshold')
    require(Q(2*31*55,3456)-Q(1,2)>0,'outside monotonicity')
    return str(bound)


def main():
    require(len(sys.argv)==3,__doc__)
    exe,path=sys.argv[1:]; total=read_report(path)
    dump=subprocess.check_output([exe,'--dump','7'],text=True)
    counts={'rational_and_literal_cut_cases':0,'explicit_palette_cases':0,'actual_packing_witnesses':0,'exact_triangle_cover_cases':0,'strict_cover_improvements':0}
    seen=set()
    for line in dump.splitlines():
        fields=tuple(map(int,line.split()));require(len(fields)==11,'bad dump')
        p=fields[:3];c,d=fields[3:5];m=fields[5:8];h,bound,upper=fields[8:]
        key=fields[:8];require(key not in seen,'duplicate tuple');seen.add(key)
        hh,bb,first,second=reference(p,c,d,m)
        require((h,bound)==(hh,bb),'rational bound mismatch')
        require(upper==literal_cover(p,c,d,m),'literal cut mismatch')
        counts['rational_and_literal_cut_cases']+=1
        k=sum(p)+c+d
        if k<=6:
            actual_palettes(p,c,d,m,first,second);counts['explicit_palette_cases']+=1
        if k<=5:
            ne,triangles=actual_graph(p,c,d,m)
            find_packing(ne,triangles,bound);counts['actual_packing_witnesses']+=1
            tau=exact_cover(p,c,d,m)
            require(tau<=upper and tau<=2*bound,'actual cover/packing comparison')
            counts['exact_triangle_cover_cases']+=1
            counts['strict_cover_improvements']+=int(tau<upper)
    require(len(seen)==sum(expected_domain(u,7)[1] for u in range(3,8)),'incomplete dump')
    for n in range(199):
        palette=factorization(range(n));united=set()
        require(len(palette)==palette_size(n),'palette size')
        for matching in palette:
            require(len({v for pair in matching for v in pair})==2*len(matching),'not matching')
            require(not united&matching,'overlap');united|=matching
        require(united==set(combinations(range(n),2)),'palette missing edges')
    for args in (['2'],['199'],['-1'],['7junk'],['--dump','11'],['--dump'],['3','4']):
        require(subprocess.run([exe,*args],capture_output=True).returncode!=0,'invalid input accepted')
    quartic=quartic_audit()
    require(literal_cover((1,1,1),0,0,(1,1,1))==3,'3-sun convention')
    print(json.dumps(dict(status='VERIFIED',full_shapes=total[0],full_parameter_tuples=total[1],
         certified_rectangles=total[2],visited_rectangles=total[3],analytically_certified_tuples=total[4],**counts,
         quartic_lower_bound=quartic,dump_sha256=hashlib.sha256(dump.encode()).hexdigest()),sort_keys=True,indent=2))


if __name__=='__main__':main()
