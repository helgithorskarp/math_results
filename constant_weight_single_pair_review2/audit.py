#!/usr/bin/env python3
"""six-reviewer-2: fresh pair-cover and conflict-graph audit; exact stdlib.
No researcher code imports. Inherited93-plane census explicitly hash-pinned.
"""
from pathlib import Path
from itertools import combinations, permutations
import json,time,argparse,hashlib
from collections import Counter
from functools import lru_cache

def need(ok,message="audit failed"):
 if not ok:raise ValueError(message)

N=16; ALL=(1<<N)-1

def gf(a,b):
 a0,a1=a&1,a>>1;b0,b1=b&1,b>>1
 return (a0*b0 ^ a1*b1) | ((a0*b1 ^ a1*b0 ^ a1*b1)<<1)

def mask(points):return sum(1<<p for p in points)

def pts(x):return [p for p in range(N) if x>>p&1]

P=sorted([mask(4*x+y for y in range(4)) for x in range(4)]+[mask(4*x+(gf(m,x)^b) for x in range(4)) for m in range(4) for b in range(4)])
ARCS=[mask(s) for s in combinations(range(N),4) if all((mask(s)&p).bit_count()<=2 for p in P)]
PAIRS=list(combinations(range(N),2)); PID={p:i for i,p in enumerate(PAIRS)}; FULLPAIRS=(1<<len(PAIRS))-1

def pairmask(b):return sum(1<<PID[p] for p in combinations(pts(b),2))

def covers(first, cap=200000):
 used=0
 for b in first:
  v=pairmask(b);need(used&v==0,"overlapping first-class pairs");used|=v
 candidates=[b for b in ARCS if pairmask(b)&used==0]
 cm=[pairmask(b) for b in candidates]
 incidence=[sum(1<<j for j,v in enumerate(cm) if v>>i&1) for i in range(120)]
 conflicts=[]
 for v in cm:
  row=0
  while v:
   bit=v&-v;row|=incidence[bit.bit_length()-1];v-=bit
  conflicts.append(row)
 nodes=0;found=set()
 def visit(missing,live,chosen):
  nonlocal nodes
  nodes+=1
  if nodes>cap:raise RuntimeError('INCOMPLETE direct pair-cover cap')
  if not missing:
   need(len(chosen)==16,"wrong affine completion size")
   found.add(tuple(sorted(first+[candidates[j] for j in chosen])));return
  options=None;size=999;scan=missing
  while scan:
   bit=scan&-scan;scan-=bit
   opt=live&incidence[bit.bit_length()-1];n=opt.bit_count()
   if n==0:return
   if n<size:options,size=opt,n
   if n==1:break
  while options:
   bit=options&-options;options-=bit;j=bit.bit_length()-1
   visit(missing&~cm[j],live&~conflicts[j],chosen+[j])
 visit(FULLPAIRS&~used,(1<<len(candidates))-1,[])
 return found,nodes,len(candidates)

def encdigest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def image(b,g):return mask(g[p] for p in pts(b))

def symmetries():
 maps=[]
 def scale(a,p):return 4*gf(a,p//4)+gf(a,p%4)
 for origin in range(16):
  for u in range(1,16):
   span={scale(a,u) for a in range(4)}
   for v in range(1,16):
    if v in span:continue
    for power in (False,True):
     perm=[]
     for p in range(16):
      x,y=divmod(p,4)
      if power:x,y=gf(x,x),gf(y,y)
      perm.append(origin^scale(x,u)^scale(y,v))
     perm=tuple(perm)
     need(len(set(perm))==16 and sorted(image(l,perm) for l in P)==P,'invalid affine frame map')
     maps.append(perm)
 need(len(maps)==len(set(maps))==5760,'frame-map census')
 need({(g[0],image(15,g)) for g in maps}=={(x,l) for l in P for x in pts(l)},'flag transitivity')
 return sorted(maps)

def normalization():
 squares=[]
 def build(rows):
  if len(rows)==4:squares.append(tuple(sum((list(r) for r in rows),[])));return
  for row in permutations(range(4)):
   if all(row[c]!=old[c] for c in range(4) for old in rows):build(rows+[row])
 build([tuple(range(4))])
 triples=[t for t in combinations(squares,3) if all(len(set(zip(a,b)))==16 for a,b in combinations(t,2))]
 need(len(squares)==24 and len(triples)==2,'Latin/MOLS completeness')
 grid=[mask(4*r+c for c in range(4)) for r in range(4)]+[mask(4*r+c for r in range(4)) for c in range(4)]
 designs=[sorted(grid+[mask(i for i in range(16) if a[i]==z) for a in t for z in range(4)]) for t in triples]
 maps=[]
 for Q in designs:
  found=None
  for rows in permutations(range(4)):
   for cols in permutations(range(4)):
    g=tuple(4*rows[x//4]+cols[x%4] for x in range(16))
    if sorted(image(l,g) for l in Q)==P:found=g;break
   if found:break
  need(found is not None,'unnormalized order4 affine design');maps.append(list(found))
 return {'latin_squares':24,'orthogonal_triples':2,'all_grid_planes':designs,'normalization_maps':maps}

def carrier_classes(L):
 complement=ALL^L;by_point={p:[a for a in ARCS if a>>p&1 and not a&L] for p in range(16)};out=set()
 def rec(left,chosen):
  if not left:out.add(tuple(sorted([L]+chosen)));return
  bit=left&-left;p=bit.bit_length()-1
  for b in by_point[p]:
   if b&left==b:rec(left^b,chosen+[b])
 rec(complement,[])
 return out

def check_plane(Q):
 need(len(Q)==len(set(Q))==20 and all(0<b<1<<16 and b.bit_count()==4 for b in Q),'invalid plane lines')
 paircounts=Counter(p for b in Q for p in combinations(pts(b),2))
 need(paircounts==Counter({p:1 for p in PAIRS}),'invalid complete pair coverage')

def alpha(words,cap=500000):
 need(len(words)==len(set(words)),'duplicate conflict vertices');n=len(words)
 adj=[sum(1<<j for j,b in enumerate(words) if j!=i and (a&b).bit_count()>2) for i,a in enumerate(words)]
 return independent(adj,cap),adj

def independent(adj,cap=500000):
 n=len(adj);need(cap>0,'INCOMPLETE nonpositive state cap');nodes=0
 @lru_cache(None)
 def solve(U):
  nonlocal nodes;nodes+=1
  if nodes>cap:raise RuntimeError('INCOMPLETE conflict-state cap')
  if not U:return ()
  ids=[i for i in range(n) if U>>i&1];isolates=[i for i in ids if not(adj[i]&U)]
  if isolates:
   rem=U
   for i in isolates:rem^=1<<i
   return tuple(isolates)+solve(rem)
  v=max(ids,key=lambda i:((adj[i]&U).bit_count(),-i))
  left=solve(U&~(1<<v));right=(v,)+solve(U&~((1<<v)|adj[v]))
  return left if len(left)>=len(right) else right
 answer=solve((1<<n)-1)
 need(all(not(adj[a]>>b&1) for a,b in combinations(answer,2)),'invalid independent witness')
 return (answer,nodes)

def validate_code(words,dx=20,dy=20,pair=1):
 need(len(words)==len(set(words)) and all(type(w) is int and 0<w<1<<18 and w.bit_count()==5 for w in words),'invalid five-word input')
 need(all((a&b).bit_count()<=2 for a,b in combinations(words,2)),'code intersection violation')
 degrees=[sum((w>>p)&1 for w in words) for p in range(18)]
 need(degrees[17]==dx and degrees[16]==dy and sum((w>>16&3)==3 for w in words)==pair,'center hypothesis mismatch')
 return degrees

def residual(stars):
 return [mask(s) for s in combinations(range(16),5) if all((mask(s)&w).bit_count()<=2 for w in stars)]

def fresh_cases(maps):
 stabilizer=[g for g in maps if g[0]==0 and image(15,g)==15]
 need(len(stabilizer)==72 and {g[4] for g in stabilizer}==set(range(4,16)),'second-anchor cover')
 rows=[];cases=[];carriers=[]
 for b in (0,4):
  L=mask([1,2,3,b]);G=[g for g in stabilizer if g[b]==b];classes=carrier_classes(L)
  need(len(classes)==(600 if b==0 else 537) and len(G)==(72 if b==0 else 6),'carrier baseline')
  remaining=set(classes);representatives=[]
  while remaining:
   A=min(remaining);orbit={tuple(sorted(image(l,g) for l in A)) for g in G}
   need(orbit<=remaining,'carrier orbit overlap or omission');remaining-=orbit;representatives.append((A,len(orbit)))
  need(len(representatives)==(14 if b==0 else 92),'carrier orbit count')
  seen=set()
  for A,size in representatives:
   Qs,n,k=covers(list(A));rows.append({'anchor':b,'first_class':list(A),'orbit_size':size,'pair_cover_states':n,'candidate_lines':k,'planes':len(Qs)})
   for Q in Qs:check_plane(Q);seen.add(Q)
  for Q in sorted(seen):
   need({(l,q) for l in P for q in Q if (l&q).bit_count()>2}=={(15,L)},'one-exception cross-line condition')
   stars=[l|(1<<17) for l in P if l!=15]+[l|(1<<16) for l in Q if l!=L]+[mask([1,2,3,16,17])]
   validate_code(stars);words=residual(stars);(ids,n),adj=alpha(words);chosen=[words[i] for i in ids]
   full=sorted(stars+chosen);degrees=validate_code(full)
   # Completed degree19 star uses P whole and removes only the Q exception.
   d19stars=[l|(1<<17) for l in P]+[l|(1<<16) for l in Q if l!=L]
   w19=[w for w in words if (w&15).bit_count()<=2]
   need(w19==residual(d19stars),'degree19 nonarc universe mismatch')
   (id19,n19),_=alpha(w19);full19=sorted(d19stars+[w19[i] for i in id19]);validate_code(full19,20,19,0)
   cases.append({'anchor':b,'second_plane':list(Q),'common_five_arcs':words,'maximum':len(chosen),'independence_states':n,'attaining_words':chosen,'degrees':degrees,'nonarc19_candidates':len(w19),'nonarc19_maximum':len(full19),'nonarc19_states':n19,'nonarc19_attaining_words':full19})
  carriers.append({'anchor':b,'all_first_classes':len(classes),'stabilizer':len(G),'orbit_representatives':len(representatives),'selected_planes':len(seen)})
 need(len(rows)==106 and len(cases)==29,'fresh complete case cover')
 return rows,cases,carriers

ABSENT_SHA='46dd2aa871cd825130474fb32e6a7ffa9debdb0263e4f059f3998f3118fa5806'
def degree19_arc(path,maps):
 data=path.read_bytes();need(hashlib.sha256(data).hexdigest()==ABSENT_SHA,'previous independent census differs')
 old=json.loads(data);need(old['plane']==P and len(old['cases'])==93 and old['restricted_maximum']==56,'previous census interface')
 first=[mask(s) for s in combinations(range(16),5) if all((mask(s)&l).bit_count()<=2 for l in P)]
 stream=hashlib.sha256();hist=Counter();states=0;maxstates=0;equality=[];allwords=[]
 for Q in sorted(tuple(sorted(c['second_plane'])) for c in old['cases']):
  check_plane(Q);need(all((q&p).bit_count()<=2 for q in Q for p in P),'inherited nonorthogoval plane')
  for L in Q:
   stars=[l|(1<<17) for l in P]+[l|(1<<16) for l in Q if l!=L]
   words=[w for w in first if all((w&q).bit_count()<=2 for q in Q if q!=L)]
   (ids,n),_=alpha(words);chosen=[words[i] for i in ids];full=sorted(stars+chosen);degrees=validate_code(full,20,19,0)
   size=len(full);hist[size]+=1;states+=n;maxstates=max(maxstates,n)
   stream.update(json.dumps([Q,L,words,len(chosen),chosen],separators=(',',':')).encode()+b'\n')
   if size==59:
    need(len(words)==20 and len(chosen)==20 and sorted(degrees)==[15]*4+[16]*8+[17]*4+[19,20],'59 equality profile/unicity')
    need({p for p in range(16) if degrees[p]==17}==set(pts(L)),'degree17 line recovery')
    equality.append({'second_plane':list(Q),'missing_line':L,'all20forced_residual_words':words,'degrees':degrees})
    allwords.append(full)
 need(sum(hist.values())==1860 and max(hist)==59 and len(equality)==8,'degree19 sharp census')
 # Full collineation completeness is a written inherited elementary lemma;
 # every map is freshly generated/checked. Degrees intrinsically fix centers.
 types=[];remaining=list(range(len(equality)))
 while remaining:
  i=remaining[0];row=equality[i];Q=row['second_plane'];L=row['missing_line']
  orbit={(tuple(sorted(image(l,g) for l in Q)),image(L,g)) for g in maps}
  members=[j for j in remaining if (tuple(equality[j]['second_plane']),equality[j]['missing_line']) in orbit]
  for j in members:remaining.remove(j)
  stabilizers=[g for g in maps if (tuple(sorted(image(l,g) for l in Q)),image(L,g))==(tuple(Q),L)]
  need(len(orbit)*len(stabilizers)==5760,'orbit/stabilizer mismatch')
  transform=lambda code,g: sorted(image(w&ALL,g)|(w&~ALL) for w in code)
  need(all(transform(allwords[i],g)==allwords[i] for g in stabilizers),'full code stabilizer mismatch')
  for j in members:
   destination=(tuple(equality[j]['second_plane']),equality[j]['missing_line'])
   transporter=next(g for g in maps if (tuple(sorted(image(l,g) for l in Q)),image(L,g))==destination)
   need(transform(allwords[i],transporter)==allwords[j],'full code isomorphism mismatch')
  types.append({'representative':row,'covered_normalized_cases':members,'labeled_plane_line_orbit_size':len(orbit),'full_code_automorphism_order':len(stabilizers),'attaining_code':allwords[i]})
 return {'inherited_census_sha256':ABSENT_SHA,'inherited93plane_census_rerun':False,'old_first_five_arcs':len(first),'all_missing_line_cases':1860,'full_maximum_histogram':dict(sorted(hist.items())),'complete_case_stream_sha256':stream.hexdigest(),'independence_states':states,'maximum_instance_states':maxstates,'exact_arc_branch_maximum':59,'equality_normalized_cases':equality,'equality_isomorphism_types':types}

def tests():
 # Exhaust every simple graph through five vertices against literal subsets.
 count=0
 for n in range(6):
  edges=list(combinations(range(n),2))
  for em in range(1<<len(edges)):
   adj=[0]*n
   for j,(u,v) in enumerate(edges):
    if em>>j&1:adj[u]|=1<<v;adj[v]|=1<<u
   answer,states=independent(adj)
   truth=max(U.bit_count() for U in range(1<<n) if all(not(U>>i&1 and adj[i]&U) for i in range(n)))
   need(len(answer)==truth,'small graph exactness');count+=1
 need(count==1100,'graph census')
 # First-class exact-cover results are also checked directly by all pair sums.
 # Malformed/capped controls never establish mathematical nonexistence.
 bad=[lambda:validate_code([31,31]),lambda:validate_code([3]),lambda:independent([0],0),lambda:covers([15,15]),lambda:covers([15,816,12480,52224],0)]
 for f in bad:
  try:f()
  except (ValueError,RuntimeError):pass
  else:raise ValueError('malformed/capped control accepted')
 return {'all1100small_graphs_verified':count,'malformed_or_zero_cap_controls_rejected':len(bad)}

def main():
 root=Path(__file__).resolve().parent.parent;p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--absent-census',type=Path,default=root/'constant_weight_absent_pair_review1'/'expected.json')
 p.add_argument('--compare-author',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
 check_plane(P);need(len(ARCS)==840,'complete four-arc census');maps=symmetries();norm=normalization();rows,cases,carriers=fresh_cases(maps);arc=degree19_arc(a.absent_census,maps)
 comparison=None
 if a.compare_author:
  old=json.loads((a.compare_author/'expected.json').read_text())
  mine={(c['anchor'],tuple(c['second_plane'])):(set(c['common_five_arcs']),c['maximum']) for c in cases}
  theirs={(c['anchor'],tuple(sorted(c['second_plane']))):(set(c['common_five_arcs']),c['maximum']) for c in old['cases']}
  need(mine==theirs,'target entry-level cases/residuals/maxima differ')
  theirsrows={(r['anchor'],tuple(r['first_class'])):(r['orbit_size'],r['compatible_planes']) for r in old['rows']}
  minerows={(r['anchor'],tuple(r['first_class'])):(r['orbit_size'],r['planes']) for r in rows}
  need(minerows==theirsrows,'target carrier row cover differs')
  witness=json.loads((a.compare_author/'witness56.json').read_text());validate_code(witness['words']);need(len(witness['words'])==56,'original witness cardinality')
  comparison={'all29plane_residual_lists_and_maxima_equal':True,'all106carrier_rows_equal':True,'original56word_witness_verified':True}
 hist={str(b):dict(sorted(Counter(39+c['maximum'] for c in cases if c['anchor']==b).items())) for b in (0,4)}
 need(hist['0']=={56:3} and hist['4']=={49:2,50:3,51:7,52:9,53:5},'sharp single-pair histograms')
 result={'agent':'six-reviewer-2','role':'independent mathematical reviewer','researcher_modules_imported':False,'normalization':norm,'all5760maps_checked':len(maps),'carrier_cover':carriers,'all106pair_cover_rows':rows,'pair_cover_states_total':sum(r['pair_cover_states'] for r in rows),'all29selected_cases':cases,'single_pair_full_maximum_histograms':hist,'nonarc19_full_maximum_histogram':dict(sorted(Counter(c['nonarc19_maximum'] for c in cases).items())),'sharp59and_equality':arc,'small_controls':tests()}
 # Optional comparison does not alter the deterministic proof record.
 text=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(text)
 else:print(text,end='')
 if comparison:__import__('sys').stderr.write(json.dumps(comparison)+'\n')
if __name__=='__main__':main()
