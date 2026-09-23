"""Definition-level and coverage audits. Standard-library Python 3.11+.

Usage: python3 audit.py RECTANGLE_EXECUTABLE RECTANGLE_OUTPUT LITERAL_OUTPUT
Outputs a deterministic compact JSON report; any failed check raises an error.
"""
from fractions import Fraction as Q
from itertools import combinations
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


def reference(a, b, c, d, m, n):
    k, s, t, u = a+b+c+d, a+c, b+c, a+b+c
    x, y = Q(m, palette_size(s)), Q(n, palette_size(t))
    independent = x*choose2(s)+y*choose2(t)-x*y*choose2(c)
    common = max(Q(i*choose2(s)+min(n,palette_size(u)-i)*choose2(t),
                   palette_size(u)) for i in range(min(m,palette_size(u))+1))
    h = ceil(max(independent, common))
    e, p = choose2(k)-h, clique(k)
    triangle_bound = Q(e*(4*e-k*k), 3*k)
    f = h + Q(p, k*(k-1)*(k-2)//6)*triangle_bound
    return max(p, h, ceil(f)), h


def sets(a, b, c, d):
    common = set(range(c))
    return common | set(range(c,c+a)), common | set(range(c+a,c+a+b))


def literal_cover(a, b, c, d, m, n):
    k = a+b+c+d
    S, T = sets(a,b,c,d)
    answer = choose2(k)+m*len(S)+n*len(T)
    for mask in range(1 << k):
        left = {i for i in range(k) if mask >> i & 1}
        spokes = m*min(len(S&left),len(S-left))+n*min(len(T&left),len(T-left))
        answer = min(answer, choose2(len(left))+choose2(k-len(left))+spokes)
    return answer


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


def matching_audit(k, a, b, c, d, m, n):
    S, T = sets(a,b,c,d)
    encode = lambda pairs: sum(1 << (i*k+j) for i,j in pairs)
    PS = [encode(p) for p in factorization(sorted(S))]
    PT = [encode(p) for p in factorization(sorted(T))]
    first = [sum(PS[i] for i in choice) for choice in combinations(range(len(PS)),m)]
    second = [sum(PT[i] for i in choice) for choice in combinations(range(len(PT)),n)]
    actual_independent = max((x|y).bit_count() for x in first for y in second)
    x,y = Q(m,len(PS)),Q(n,len(PT))
    require(actual_independent >= ceil(x*choose2(len(S))+y*choose2(len(T))-x*y*choose2(c)),
            "independent palette bound fails")
    # Separate exact dynamic program over disjoint shared palette assignments.
    dp = {(0,0):0}
    for matching in factorization(sorted(S|T)):
        sc = sum(i in S and j in S for i,j in matching)
        tc = sum(i in T and j in T for i,j in matching)
        nxt = dict(dp)
        for (i,j),value in dp.items():
            if i<m:nxt[i+1,j]=max(nxt.get((i+1,j),-1),value+sc)
            if j<n:nxt[i,j+1]=max(nxt.get((i,j+1),-1),value+tc)
        dp = nxt
    actual_common = max(dp.values())
    _,bound = reference(a,b,c,d,m,n)
    require(max(actual_independent,actual_common)>=bound,"centered bound fails")


def graph_triangles(a, b, c, d, m, n):
    k = a+b+c+d
    S,T = sets(a,b,c,d)
    edges = set(combinations(range(k),2))
    for v in range(k,k+m):edges |= {(x,v) for x in S}
    for v in range(k+m,k+m+n):edges |= {(x,v) for x in T}
    ids = {e:i for i,e in enumerate(sorted(edges))}
    triangles = []
    for triple in combinations(range(k+m+n),3):
        pairs = list(combinations(triple,2))
        if all(e in ids for e in pairs):
            triangles.append(sum(1 << ids[e] for e in pairs))
    return len(edges), triangles


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


def expected_domain(k):
    # Independent coordinates: s=|S| >= t=|T| and intersection c.
    shapes = cases = 0
    for s in range(k+1):
        for t in range(s+1):
            choices = t-max(0,s+t-k)+1
            shapes += choices
            cases += choices*max(1,s)*max(1,t)
    return shapes,cases


def read_report(path):
    rows = {}
    total = None
    for line in Path(path).read_text().splitlines():
        parts = line.split()
        if parts[0] == "ROW":
            k = int(parts[1]); require(k not in rows,"duplicate row")
            rows[k] = tuple(map(int,parts[2:]))
        elif parts[0] == "TOTAL":
            require(total is None,"duplicate total")
            total = tuple(map(int,parts[1:]))
        else:raise RuntimeError("unexpected report line: "+line)
    require(set(rows)==set(range(3,113)),"incomplete finite range")
    require(all(len(row)==5 and row[-1]==0 for row in rows.values()),"reported failures")
    require(total==tuple(sum(row[i] for row in rows.values()) for i in range(5)),"wrong total")
    for k,row in rows.items():require(row[:2]==expected_domain(k),"domain count disagreement")
    return rows,total


def main():
    require(len(sys.argv)==4,__doc__)
    executable,first_file,second_file = sys.argv[1:]
    first,first_total = read_report(first_file)
    second,second_total = read_report(second_file)
    require(first_total[:2]==second_total[:2],"full traversals disagree")
    dump = subprocess.check_output([executable,"--dump","8"],text=True)
    entries = matching_cases = packing_cases = cut_cases = 0
    seen = set()
    for line in dump.splitlines():
        fields = tuple(map(int,line.split()))
        require(len(fields)==9,"bad dump")
        a,b,c,d,m,n,p,upper,h = fields
        k = a+b+c+d
        require((a,b,c,d,m,n) not in seen,"duplicate tuple")
        seen.add((a,b,c,d,m,n))
        require(reference(a,b,c,d,m,n)==(p,h),"rational reference disagreement")
        require(literal_cover(a,b,c,d,m,n)==upper,"literal cut disagreement")
        entries += 1;cut_cases += 1
        if k<=6:
            matching_audit(k,a,b,c,d,m,n);matching_cases+=1
        if k<=5:
            edges,triangles = graph_triangles(a,b,c,d,m,n)
            find_packing(edges,triangles,p);packing_cases+=1
    require(entries==sum(expected_domain(k)[1] for k in range(3,9)),"dump incomplete")
    for size in range(13):
        palette = factorization(range(size))
        all_edges = set()
        require(len(palette)==palette_size(size),"wrong palette size")
        for matching in palette:
            require(len({v for e in matching for v in e})==2*len(matching),"not a matching")
            require(not all_edges&matching,"color collision")
            all_edges |= matching
        require(all_edges==set(combinations(range(size),2)),"missing clique edges")
    for args in (["2"],["113"],["-1"],["8junk"],["--dump","13"]):
        require(subprocess.run([executable,*args],capture_output=True).returncode!=0,"bad input accepted")
    # Negative controls for the literal graph checker and reference conventions.
    require(graph_triangles(0,0,0,3,0,0)[1]==[7],"K3 convention")
    require(literal_cover(0,0,0,4,0,0)==2 and clique(4)==1,"tight K4 control")
    report = dict(status="VERIFIED",full_shapes=first_total[0],full_parameter_tuples=first_total[1],
                  producer_rectangles=first_total[2],literal_rectangles=second_total[2],
                  entrywise_rational_comparisons=entries,literal_cut_cases=cut_cases,
                  explicit_matching_cases=matching_cases,definition_level_packing_cases=packing_cases,
                  dump_sha256=hashlib.sha256(dump.encode()).hexdigest())
    print(json.dumps(report,sort_keys=True,indent=2))


if __name__ == "__main__":
    main()
