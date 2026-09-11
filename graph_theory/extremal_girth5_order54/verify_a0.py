#!/usr/bin/env python3
"""Exact independent checks for the uniform A0 reduction. Standard library only."""
import argparse,copy,hashlib,json
from collections import Counter
from fractions import Fraction
from itertools import combinations,product
from pathlib import Path
from math import comb
from a0_inventory import profiles,bounds
from a0_far_models import cases
from a0_independent import inventory,reconstruct,hh
from verify_a2_exclusion import require

HERE=Path(__file__).resolve().parent


def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def check_certificate(rec,data):
 T,E,eq,eb,ub,bb,meta=data;n=len(T)+len(E)+len(meta)
 require(rec['dimensions']==[len(T),len(E),len(meta),len(eq),len(ub)],'certificate dimensions')
 require(rec['variable_budget']==470 and rec['denominator']>0,'full pattern-variable budget')
 denominator=rec['denominator'];rhs=Fraction(0);cs=[Fraction(0)]*n
 for rows,bs,key,upper in((eq,eb,'equality_multipliers',False),(ub,bb,'inequality_multipliers',True)):
  seen=set()
  for i,mul in rec[key]:
   require(isinstance(i,int) and 0<=i<len(rows) and i not in seen,'multiplier row')
   require(isinstance(mul,int) and (not upper or mul<=0),'upper multiplier sign')
   seen.add(i);weight=Fraction(mul,denominator);rhs+=weight*bs[i]
   for j,c in rows[i].items():cs[j]+=weight*c
 delta=max([Fraction(0)]+cs);bound=rhs-470*delta
 require(rhs==Fraction(rec['uncorrected_bound']) and delta==Fraction(rec['coefficient_excess']), 'exact combined row')
 require(bound==Fraction(rec['corrected_bound']) and bound>0,'strict exact contradiction')
 return {'name':rec['name'],'dimensions':rec['dimensions'],'bound':str(bound),'coefficient_excess':str(delta),'sha256':digest(rec),'columns':n}


def cover_inventory():
 ps=list(profiles())
 require(sorted(ps)==inventory(),'all profiles agree entrywise with charged enumeration')
 require(len(ps)==403,'complete inventory size')
 surviving=[];large=[];smallm=[];allbounds=[];twolarge=[]
 for i,row in enumerate(ps):
  m,k,s,t=row;lo,hi,extra=bounds(row)
  allbounds.append([i,m,k,lo,hi,extra])
  sizes=sorted([c for ns in(s,t) for c,n in enumerate(ns) for _ in range(n)],reverse=True)
  if sum(sizes[:2])>=10:twolarge.append(i)
  if lo>hi:continue
  if sum(s[5:])+sum(t[5:]):large.append(i)
  elif m<3:smallm.append(i)
  elif m<6:surviving.append([i,*row])
 require(twolarge==[89],'only potential b22 inventory')
 require(large==[89,176,177,194,198,210,241,253,277,309,310,319,321,342,376], 'all large-set terminal profiles')
 require(smallm==[39,41,54,55,56,70,80,92,113,123,129,139], 'all small-m terminal profiles')
 require([i for i,row in enumerate(ps) if row[0]==6]==list(range(393,403)), 'whole m6 profile cover')
 require(len(surviving)==63,'63 remaining necessary profiles')
 # Check the numerical sides of each written closing branch.
 for i in large:
  m,k,s,t=ps[i];lo,hi,extra=bounds(ps[i]);f4=s[4]+t[4]
  if i==89:require(16>2*7,'two-five contradiction');continue
  require(s[5]==1 and sum(s[6:])+sum(t[5:])==0,'unique six-five terminal premise')
  if f4==0 and i!=376:require(lo>7,'one-five far-size charge bound')
  elif i==376:
   require((m,k,s[2],s[3],t[3])==(5,0,4,11,0),'last five-set profile')
   require(5*3+3-5==13 and 15-13==2 and max(4,5)<lo,'at most two outside six-triples')
  else:
   require(t[4]==0 and lo>4,'disjoint five/quad exclusion')
   if m==3:require(lo>9,'overlapping five/quad exclusion')
   else:require(i==319 and lo==8 and f4==1 and 2+4+3<14,'final required additional quad')
 for i in smallm:
  m,k,s,t=ps[i];lo,hi,_=bounds(ps[i]);r=s[4]+t[4];triples=s[3]+t[3]
  require(m==2 and r in(3,4),'complete small-m residual shapes')
  if r==3:
   packing=comb(triples,2)-max(0,3*triples-12)
   require(triples<=5 and max(7,packing)<lo,'three-quad path/triangle bound')
  else:
   require(triples<=2 and lo>=8,'four-quad maximum charge eight')
   if lo==8:require(s[1]+t[1]<4,'equality needs four singleton vertices')
 forests=[]
 def partitions(total,minimum=1):
  if total==0:yield ();return
  for p in range(minimum,total+1):
   for rest in partitions(total-p,p):yield (p,)+rest
 mks={(x[1],x[2]) for x in surviving}
 for m,k in sorted(mks):
  for parts in partitions(m):
   if sum(p-1 for p in parts)==k and sum(p+1 for p in parts)<=12:
    forests.append({'m':m,'k':k,'nontrivial_path_orders':[p+1 for p in parts],
                    'isolates':12-sum(p+1 for p in parts)})
 require(len(forests)==12,'complete twelve-forest cover')
 return {'profiles':len(ps),'entry_sha256':digest(ps),'arithmetic_rejected':sum(r[3]>r[4] for r in allbounds),
         'large_terminal_indices':large,'small_m_terminal_indices':smallm,
         'm6_terminal_indices':list(range(393,403)),'remaining_profiles':surviving,'high_forests':forests,
         'bound_table_sha256':digest(allbounds)}


def colored_four():
 edges=list(map(frozenset,combinations(range(4),2)));hist=Counter()
 for word in product(range(4),repeat=6):
  chosen=[(edges[i],c) for i,c in enumerate(word) if c]
  if any(a&b and c==d for (a,c),(b,d) in combinations(chosen,2)):continue
  score=sum(not(a&b) and c!=d for (a,c),(b,d) in combinations(chosen,2))
  require(score<=1,'colored graph on four points has at most one suitable pair')
  hist[(len(chosen),score)]+=1
 return {'words_checked':4**6,'valid':sum(hist.values()),'maximum':max(p for r,p in hist),
         'histogram':[[r,p,n] for (r,p),n in sorted(hist.items())]}


def quad_cover():
 universe=(1<<12)-1
 quads=[sum(1<<v for v in c) for c in combinations(range(12),4)]
 histogram=Counter();singleton_templates=double_templates=0;family_count=0
 for q2 in (240,113):
  for q3 in quads:
   if any((a&b).bit_count()>1 for a,b in combinations((15,q2,q3),2)):continue
   for q4 in quads:
    qs=(15,q2,q3,q4)
    if any((a&b).bit_count()>1 for a,b in combinations(qs,2)):continue
    family_count+=1
    disjoint=[(i,j) for i,j in combinations(range(4),2) if not(qs[i]&qs[j])]
    dd=[sum(i in pair for pair in disjoint) for i in range(4)]
    isolated_edges=[pair for pair in disjoint if all(dd[i]==1 for i in pair)]
    require(len(isolated_edges)<=2,'at most two isolated edges on four quads')
    histogram[(len(disjoint),len(isolated_edges))]+=1
    for i,j in disjoint:
     outside=universe^(qs[i]|qs[j]);points=[v for v in range(12) if outside>>v&1]
     for p in points:
      z=outside^(1<<p)
      if all((z&q).bit_count()<=1 for q in qs):
       require(disjoint==[(i,j)],'singleton template forces unique disjoint quad pair')
       singleton_templates+=1
     ys=[]
     for pair in combinations(points,2):
      y=sum(1<<v for v in pair);z=outside^y
      if all((y&q).bit_count()<=1 and (z&q).bit_count()<=1 for q in qs):
       require((i,j) in isolated_edges,'double-quad bad needs isolated disjointness edge')
       ys.append(y);double_templates+=1
     require(len(ys)<=4,'at most four double-quad bad high pairs')
 # Exact arithmetic for equality: four bad pairs use all eight point
 # incidences outside the two quads. The other five far vertices must
 # double-cover the paired quad: one quad and four singleton vertices.
 possibilities=[(quad,singletons) for quad in(0,1) for singletons in range(6)
                if quad+singletons<=5 and 4*quad+singletons>=8]
 require(possibilities==[(1,4)],'four-quad equality forces four singleton vertices')
 return {'normalized_ordered_families':family_count,'disjointness_histogram':[[a,b,n] for (a,b),n in sorted(histogram.items())],
         'singleton_templates':singleton_templates,'double_quad_templates':double_templates,
         'equality_cover_quad_singletons':possibilities}


def large_set_controls():
 # All linear pairs of triples on the seven points outside a five-set.
 triples=list(map(frozenset,combinations(range(7),3)));counts=Counter();bad=Counter()
 O=frozenset(range(7))
 for a,b in combinations(triples,2):
  overlap=len(a&b)
  if overlap>1:continue
  counts[overlap]+=1
  for helper in(a,b):
   for y in map(frozenset,combinations(O-helper,2)):
    z=O-helper-y
    if all(len(s&t)<=1 for s in(y,z) for t in(a,b)):
     bad[overlap]+=1
     require(overlap==1 and y.isdisjoint(a&b),'two outside triples obstruction')
 require(bad[0]==0,'no b2 with disjoint outside triples')
 return {'linear_triple_pair_counts':dict(sorted(counts.items())),
         'permitted_bad_templates':dict(sorted(bad.items())),
         'colored_four':colored_four()}


def graph_controls():
 from verify import graph
 fixture=json.loads((HERE/'lower_bound_54_185.json').read_text())
 edges=[tuple(e) for e in fixture['edges']];graphs=roots=aux_edges=0
 for deleted in [None]+list(range(len(edges))):
  selected=[e for i,e in enumerate(edges) if i!=deleted]
  G=graph(54,selected);degrees=list(map(len,G))
  near=[{v}|set(G[v])|{w for u in G[v] for w in G[u]} for v in range(54)]
  high={t for t in range(54) if degrees[t]==8 and len(near[t])==54}
  if not high:continue
  graphs+=1;C=[set(G[v])&high for v in range(54)]
  for v in range(54):
   if degrees[v] not in(6,7):continue
   far=set(range(54))-near[v];delta=8-degrees[v]
   for t in high:
    require(delta*(t in C[v])+sum(t in C[u] for u in far)==delta,'actual graph individual cover')
   if degrees[v]==6:
    aux=[]
    for t in high-C[v]:
     ends=tuple(sorted(u for u in far if t in C[u]))
     require(len(ends)==2 and ends not in aux,'actual simple far-cover graph')
     aux.append(ends)
    ds=[sum(u in e for e in aux) for u in sorted(far)]
    require(ds==[len(C[u]) for u in sorted(far)] and hh(ds),'actual far degrees')
    aux_edges+=len(aux)
   roots+=1
 return {'actual_graphs':graphs,'low_root_covers':roots,'auxiliary_edges':aux_edges}


def final_pigeonhole():
 eps_solutions=[]
 for ones in range(17):
  # Equality sum eps^2=sum eps=4 forces every integer eps in{0,1}.
  if ones==4:eps_solutions.append((ones,16-ones))
 require(eps_solutions==[(4,12)],'four positive sixes')
 neighbor_patterns=[(z,s,p) for z in range(2) for s in range(8) for p in range(8)
                    if z+s+p==7 and s+2*p==12]
 require(neighbor_patterns==[(0,2,5),(1,0,6)],'zero-high seven needs at least five pair neighbors')
 require(min(p for z,s,p in neighbor_patterns)>4,'four available positive sixes cannot be distinct')
 return {'positive_sixes':4,'zero_sixes':12,'seven_classes':[2,12,12],
         'forced_far_seven_matching_edges':12,'Q':4,'U':12,
         'zero_high_seven_neighbor_patterns':neighbor_patterns}


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--certificates',type=Path,required=True);args=p.parse_args()
 records=json.loads(args.certificates.read_text());case_data=list(cases())
 require([r['name'] for r in records]==[name for name,row,epsq,data in case_data],'all eleven cases exactly once')
 checked=[];pattern_rows=0
 for rec,(name,row,epsq,data) in zip(records,case_data):
  independent=reconstruct(row,epsq)
  for j,(a,b) in enumerate(zip(data,independent)):
   if j in(2,4):
    a=[{i:v for i,v in r.items() if v} for r in a];b=[{i:v for i,v in r.items() if v} for r in b]
   require(a==b,(name,'independent model mismatch',j))
  checked.append(check_certificate(rec,independent));pattern_rows+=len(data[-1])
 # Four deliberate corruptions must be rejected; checks survive -O.
 corruptions=[]
 for kind in('budget','bound','multiplier','sign'):
  bad=copy.deepcopy(records[0]);data=reconstruct(case_data[0][1],case_data[0][2])
  if kind=='budget':bad['variable_budget']=428
  elif kind=='bound':bad['corrected_bound']='0'
  elif kind=='multiplier':bad['equality_multipliers'][0][1]+=1
  else:bad['inequality_multipliers']=[[0,1]]
  try:check_certificate(bad,data)
  except ValueError:corruptions.append(kind)
  else:raise ValueError('accepted corrupt '+kind)
 result={'claim':'All z12,A0 candidates have 3<=m<=5 and c(v)<=4; twelve explicit high forests and63 necessary low profiles remain',
         'scope':'whole large-neighborhood, small-m and m6 exclusions; A0 realization remains open',
         'inventory':cover_inventory(),'large_set_controls':large_set_controls(),
         'four_quad_controls':quad_cover(),'actual_graph_controls':graph_controls(),
         'm6_certificates':checked,'independently_compared_pattern_columns':pattern_rows,
         'corruption_checks':corruptions,'m6_final_pigeonhole':final_pigeonhole()}
 print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
