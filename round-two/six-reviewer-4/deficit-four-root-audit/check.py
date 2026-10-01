#!/usr/bin/env python3
"""Independent deficit-four Book22 audit, six-reviewer-4, reviewer.

The complete raw incidence census is a credited dependency of REVIEW 8808;
we check the deficit-zero/two/four row-domain transfer explicitly. The
completion proof uses literal neighborhoods and path consistency, without
branching or imports of researcher/reviewer executable modules.
"""
from itertools import combinations
from collections import Counter
import argparse, json, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
PAIRS=tuple(combinations(range(10),2))
ALL=1023
LABELS=tuple(combinations(range(5),2))
IMAGE=(0,7,8,9,3,6,1,2,4,5)
BETA=((0,6),(0,7),(0,8),(0,9),(1,6),(1,7),(1,8),(1,9),
      (2,7),(2,9),(3,6),(3,8),(4,8),(4,9),(5,6),(5,7))
ALPHA=(-4,-4)+(-2,)*8
CENSUS_SHA='95b5e500fb3c9f05257b7083ecfa3da25974031ac5ae8cfa94cb91aba98b75ce'

def need(value,message):
 if not value: raise ValueError(message)

def indices(mask,n):
 return tuple(i for i in range(n) if mask&(1<<i))

def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def local_graph():
 p=tuple(sum(1<<j for j in range(10) if not(set(LABELS[IMAGE[i]])&set(LABELS[IMAGE[j]]))) for i in range(10))
 need(p[0]&(1<<1),'Deleted pair is not a Petersen edge')
 a=list(p);a[0]^=1<<1;a[1]^=1
 need(tuple(q.bit_count() for q in a)==(2,2)+(3,)*8,'Local degrees')
 need(indices(a[0],10)==(2,3) and indices(a[1],10)==(4,5),'Local labels')
 mask=sum(1<<bit for bit,(i,j) in enumerate(combinations(range(2,10),2)) if a[i]&(1<<j))
 need(mask==51317328,'Geometric core versus published labels')
 return tuple(a)
LOCAL=local_graph()
H=tuple(q.bit_count() for q in LOCAL)
CAP=tuple(H[i]+H[j]-(5 if LOCAL[i]&(1<<j) else 2)-(LOCAL[i]&LOCAL[j]).bit_count() for i,j in PAIRS)

def row_domains():
 need(88+sum(ALPHA[i]*(H[i]+2) for i in range(10))+sum(CAP[PAIRS.index(p)] for p in BETA)==0,'Integer cut upper bound')
 result=[];positive=[]
 for d in range(5):
  zero=[];scores=Counter()
  for z in range(1024):
   k=z.bit_count()
   if not 4+d<=k<=8:continue
   if any(((z>>low)&1 and z&((1<<j)|(1<<q))) or (not((z>>low)&1) and not z&((1<<j)|(1<<q))) for low,j,q in [(0,2,3),(1,4,5)]):continue
   if any(cap<1 and z&(1<<i) and z&(1<<j) for (i,j),cap in zip(PAIRS,CAP)):continue
   if any(k>(LOCAL[i]&z).bit_count()+5+d for i in range(10) if not z&(1<<i)):continue
   if any((LOCAL[i]&z).bit_count()<k-7 for i in indices(z,10)):continue
   score=8+sum(ALPHA[i] for i in indices(z,10))+sum(bool(z&(1<<i) and z&(1<<j)) for i,j in BETA)
   need(score>=0,'Negative cut score')
   scores[score]+=1
   if not score:zero.append(z)
  result.append(tuple(zero));positive.append(dict(sorted(scores.items())))
 need(set().union(*map(set,result[:3]))==set().union(*map(set,result)), 'New deficits enlarge imported census domain')
 return tuple(result),positive

class Frame:
    """Actual whole-vertex neighborhoods as arbitrary-precision binary integers."""
    def __init__(self, local, rows):
        self.a, self.n = len(local), len(rows)
        self.offset = self.a + 1
        self.universe = (1 << (self.offset + self.n)) - 1
        self.rows = tuple(rows)
        self.a_red = tuple(1 | (local[i] << 1)
                           | sum(1 << (self.offset + b) for b, z in enumerate(rows)
                                 if not z & (1 << i)) for i in range(self.a))
        self.a_blue = tuple(self.universe ^ r ^ (1 << (i + 1))
                            for i, r in enumerate(self.a_red))
        self.base_b_red = tuple((((1 << self.a) - 1) ^ z) << 1 for z in rows)

    def neighborhoods(self, b, star):
        red = self.base_b_red[b] | (star << self.offset)
        return red, self.universe ^ red ^ (1 << (self.offset + b))

    def ab_pages(self, b, star, i):
        red, blue = self.neighborhoods(b, star)
        return ((blue & self.a_blue[i]).bit_count() if self.rows[b] & (1 << i)
                else (red & self.a_red[i]).bit_count())

    def pair_pages(self, b, x, c, y):
        red = bool(x & (1 << c))
        if red != bool(y & (1 << b)):
            return None
        rb, bb = self.neighborhoods(b, x); rc, bc = self.neighborhoods(c, y)
        return red, ((rb & rc) if red else (bb & bc)).bit_count()

    def compatible(self, b, x, c, y):
        result = self.pair_pages(b, x, c, y)
        return result is not None and result[1] <= (3 if result[0] else 6)

    def domains(self, deficits):
        need(len(deficits) == self.n, "deficiency vector length")
        result = []
        for b, (z, delta) in enumerate(zip(self.rows, deficits)):
            degree = z.bit_count() - delta
            need(0 <= degree < self.n, "impossible prescribed outside degree")
            pool = []
            for choice in combinations(tuple(c for c in range(self.n) if c != b), degree):
                star = sum(1 << c for c in choice)
                if all(self.ab_pages(b, star, i) <= (6 if z & (1 << i) else 3)
                       for i in range(self.a)):
                    pool.append(star)
            result.append(tuple(sorted(pool)))
        return tuple(result)


def small_whole_graph_controls():
    # Exhaust all 1024 six-point graphs with N(0)={1,2,3}, B={4,5}.
    free = tuple(combinations(range(1, 6), 2)); checks = asymmetric = 0
    for bits in range(1 << len(free)):
        adj = [[False] * 6 for _ in range(6)]
        for i in (1, 2, 3): adj[0][i] = adj[i][0] = True
        for t, (i, j) in enumerate(free): adj[i][j] = adj[j][i] = bool(bits & (1 << t))
        local = tuple(sum(1 << j for j in range(3) if adj[i + 1][j + 1]) for i in range(3))
        rows = tuple(sum(1 << i for i in range(3) if not adj[b + 4][i + 1]) for b in range(2))
        actual = tuple(sum(1 << c for c in range(2) if adj[b + 4][c + 4]) for b in range(2))
        frame = Frame(local, rows)
        for b in range(2):
            for i in range(3):
                u, v = b + 4, i + 1; color = adj[u][v]
                pages = sum(adj[u][t] == color and adj[v][t] == color for t in range(6) if t not in (u, v))
                need(frame.ab_pages(b, actual[b], i) == pages, "whole-graph A/B control")
                checks += 1
        color = adj[4][5]
        pages = sum(adj[4][t] == color and adj[5][t] == color for t in range(4))
        need(frame.pair_pages(0, actual[0], 1, actual[1]) == (color, pages), "whole-graph B/B control")
        need(frame.pair_pages(0, actual[0] ^ 2, 1, actual[1]) is None, "asymmetric star accepted")
        checks += 1; asymmetric += 1
    return {"whole_graphs": 1024, "literal_spine_checks": checks, "asymmetric_stars_rejected": asymmetric}



def path_exclusion(frame,domains,observe=None):
 """Synchronous path consistency: retain each actual pair's actual third star."""
 n=frame.n
 if any(not d for d in domains):return {'rounds':0,'empty_vertex':next(b for b,d in enumerate(domains) if not d),'removed_pairs':0,'trace_sha256':digest([])}
 current={}
 for b,c in combinations(range(n),2):
  forward=[sum(1<<j for j,y in enumerate(domains[c]) if frame.compatible(b,x,c,y)) for x in domains[b]]
  current[b,c]=forward
  current[c,b]=[sum(1<<i for i,x in enumerate(domains[b]) if forward[i]&(1<<j)) for j in range(len(domains[c]))]
 def empty_pair(tables):return next(((b,c) for b,c in combinations(range(n),2) if not any(tables[b,c])),None)
 if observe is not None:observe(current)
 first=empty_pair(current)
 if first is not None:return {'rounds':0,'empty_pair':first,'removed_pairs':0,'trace_sha256':digest([])}
 trace=[];removed=0
 for round_number in range(1,100):
  following={p:list(v) for p,v in current.items()};round_trace=[]
  for b,c in combinations(range(n),2):
   for i in range(len(domains[b])):
    for j in indices(current[b,c][i],len(domains[c])):
     witness=next((q for q in range(n) if q!=b and q!=c and not(current[b,q][i]&current[c,q][j])),None)
     if witness is not None:
      following[b,c][i]^=1<<j;following[c,b][j]^=1<<i
      round_trace.append([b,domains[b][i],c,domains[c][j],witness])
  need(round_trace,'Path-consistent residual; no exclusion established')
  trace.append(round_trace);removed+=len(round_trace);current=following
  if observe is not None:observe(current)
  empty=empty_pair(current)
  if empty is not None:return {'rounds':round_number,'empty_pair':empty,'removed_pairs':removed,'trace_sha256':digest(trace)}
 raise RuntimeError('INCOMPLETE: path consistency round guard')

def primary_control():
    fixture = json.loads((HERE / 'primary21.json').read_text())
    need(fixture['order'] == 21, 'primary fixture order')
    edges = fixture['red_edges']
    need(len(edges) == len({tuple(e) for e in edges}) == 93, 'primary edge list')
    adj = [0] * 21
    for u, v in edges:
        need(type(u) is int and type(v) is int and 0 <= u < v < 21, 'primary edge')
        adj[u] |= 1 << v; adj[v] |= 1 << u
    blue = tuple(((1 << 21) - 1) ^ a ^ (1 << i) for i, a in enumerate(adj))
    red_pages = [(adj[u] & adj[v]).bit_count() for u, v in combinations(range(21), 2) if adj[u] & (1 << v)]
    blue_pages = [(blue[u] & blue[v]).bit_count() for u, v in combinations(range(21), 2) if not adj[u] & (1 << v)]
    need(max(red_pages) == 3 and max(blue_pages) == 6, 'primary ordinary book caps')
    roots = [i for i, a in enumerate(adj) if a.bit_count() == 10]
    need(len(roots) == 1, 'primary degree-ten root')
    root = roots[0]; a = indices(adj[root], 21); b = indices(blue[root], 21)
    local = tuple(sum(1 << j for j, v in enumerate(a) if adj[u] & (1 << v)) for u in a)
    rows = tuple(sum(1 << i for i, v in enumerate(a) if not adj[u] & (1 << v)) for u in b)
    stars = tuple(sum(1 << j for j, v in enumerate(b) if adj[u] & (1 << v)) for u in b)
    deficits = tuple(10 - adj[u].bit_count() for u in b)
    frame = Frame(local, rows); domains = frame.domains(deficits)
    need(all(stars[i] in domains[i] for i in range(10)), 'primary actual star')
    need(all(frame.compatible(i, stars[i], j, stars[j]) for i, j in combinations(range(10), 2)),
         'primary actual reciprocal completion')
    damaged = 0
    for i in range(10):
        for remove in indices(stars[i], 10):
            for add in range(10):
                if add == i or stars[i] & (1 << add): continue
                changed = stars[i] ^ (1 << remove) ^ (1 << add)
                need(any(not frame.compatible(i, changed, j, stars[j]) for j in range(10) if j != i),
                     'primary degree-preserving asymmetric star')
                damaged += 1
    return {'red_edges': 93, 'blue_edges': 117, 'max_red_pages': 3, 'max_blue_pages': 6,
            'actual_stars_accepted': 10, 'actual_completion_accepted': 1,
            'degree_preserving_asymmetric_damages_rejected': damaged}


def network_controls():
 """All 4096 binary three-variable networks, checked by eight literal tuples."""
 from itertools import product
 sat=unsat=retained=0
 class Network:
  n=3
  def __init__(self,relations):self.relations=relations
  def compatible(self,b,x,c,y):
   if b>c:b,c,x,y=c,b,y,x
   return bool(self.relations[((0,1),(0,2),(1,2)).index((b,c))]&(1<<(2*x+y)))
 for masks in product(range(16),repeat=3):
  frame=Network(masks)
  solutions=tuple(t for t in product(range(2),repeat=3) if all(frame.compatible(b,t[b],c,t[c]) for b,c in combinations(range(3),2)))
  def observe(tables):
   nonlocal retained
   for t in solutions:
    need(all(tables[b,c][t[b]]&(1<<t[c]) for b,c in combinations(range(3),2)), 'Actual solution pair deleted in small network')
    retained+=1
  try:
   path_exclusion(frame,((0,1),)*3,observe)
   need(not solutions,'Satisfiable network excluded')
   unsat+=1
  except ValueError as e:
   if str(e)!='Path-consistent residual; no exclusion established':raise
   need(bool(solutions),'Unsatisfiable three-variable network not excluded')
   sat+=1
 need(sat+unsat==4096,'Incomplete network control enumeration')
 return {'all_binary_three_variable_networks':4096,'satisfiable':sat,'unsatisfiable':unsat,'actual_solution_preservation_checks':retained}


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');args=parser.parse_args()
 by_delta,scores=row_domains()
 rows=json.loads((HERE/'CENSUS.json').read_text())
 need(type(rows) is list and len(rows)==135 and rows==sorted(rows),'Imported complete census normalization')
 need(len({tuple(r) for r in rows})==135,'Duplicate imported incidence')
 need(hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()==CENSUS_SHA,'Imported reviewed census bytes differ')
 universe=set().union(*map(set,by_delta));records=[];cases=Counter();rounds=Counter();sum_removed=0
 for r in rows:
  need(type(r) is list and len(r)==11 and r==sorted(r) and all(type(z) is int and z in universe for z in r),'Malformed row multiset')
  need(all(sum(bool(z&(1<<i)) for z in r)==H[i]+2 for i in range(10)),'Wrong column margin')
  need(all(sum(bool(z&(1<<i) and z&(1<<j)) for z in r)<=cap for (i,j),cap in zip(PAIRS,CAP)),'Wrong pair cap')
  ds=tuple(z.bit_count()-4 for z in r)
  need(sum(ds)==4 and all(0<=d<=4 for d in ds),'Unique deficit tagging')
  frame=Frame(LOCAL,r);domain=frame.domains(ds)
  need(all(q.bit_count()==10 for q in frame.a_red),'Fixed full degrees')
  need(not all(domain) or all(z in by_delta[d] for z,d in zip(r,ds)),'Actual domains violate necessary row gates')
  fixed=(1023<<1,)+frame.a_red
  blue=tuple(frame.universe ^ x ^ (1<<i) for i,x in enumerate(fixed))
  need(all(((fixed[u]&fixed[v]).bit_count()<=3 if fixed[u]&(1<<v) else (blue[u]&blue[v]).bit_count()<=6) for u,v in combinations(range(11),2)),'Literal fixed spines')
  result=path_exclusion(frame,domain)
  pattern=','.join(str(d) for d in sorted(ds) if d)
  if all(domain):cases[pattern]+=1
  rounds[result['rounds']]+=1;sum_removed+=result['removed_pairs']
  records.append({'rows':r,'deficits':ds,'domain_sizes':list(map(len,domain)),'domain_sha256':digest(domain),'exclusion':result})
 result={'actual_reviewer':'six-reviewer-4','role':'independent mathematical reviewer',
         'scope':'New deficit-four completion proof of 8828; complete raw incidence census explicitly imported from reviewed 8808.',
         'census_count':len(rows),'census_sha256':CENSUS_SHA,'zero_rows_by_deficit':list(map(len,by_delta)),
         'cut_score_histograms':scores,'surviving_cases':dict(sorted(cases.items())),
         'path_round_counts':dict(sorted(rounds.items())),'removed_pairs':sum_removed,
         'records':records,'whole_graph_controls':small_whole_graph_controls(),
         'network_controls':network_controls(),'primary_control':primary_control()}
 if args.emit:print(json.dumps(result,separators=(',',':'),sort_keys=True));return
 expected=json.loads((HERE/'expected.json').read_text())
 need(json.loads(json.dumps(result))==expected,'Whole exact expected record mismatch')
 print('PASS')
if __name__=='__main__':main()
