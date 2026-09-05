"""Complete exact unit/unit contact rotations for the fixed heptagon-spindle sum."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
import argparse, json, math, time
import field as F

def canonical(a,d):
 g=math.gcd(d,*a)
 return (tuple(v//g for v in a),d//g)
def multiply(x,y):return canonical(F.mul(x[0],y[0]),x[1]*y[1])
def root(k):return (F.K.POW[k%42]+F.K.ZERO,1)
def enumeration():
 H,M,d=F.construction()
 def unitdiff(X):return sorted({F.sub(a,b) for a in X for b in X if a!=b and F.norm(F.sub(a,b))==F.scale(F.ONE,d*d)})
 A,B=unitdiff(H),unitdiff(M)
 angles=Counter()
 for a in A:
  for b in B:
   ab=canonical(F.mul(a,F.conjugate(b)),d*d)
   for k in [14,28]:angles[multiply(root(k),ab)]+=1
 for r in angles:assert F.norm(r[0])==F.scale(F.ONE,r[1]**2)
 assert {F.mul(root(6)[0],h) for h in H}==set(H)
 orbits={}
 for r in angles:
  o=sorted({multiply(root(6*j),r) for j in range(7)})
  assert len(o)==7 and set(o)<=angles.keys()
  orbits[o[0]]=o
 assert sum(map(len,orbits.values()))==len(angles)
 return H,M,d,A,B,angles,orbits
def graph(r):
 H,M,d=F.construction();rn,rd=r
 H=[F.scale(a,rd) for a in H];M=[F.mul(rn,a) for a in M];d*=rd
 common=math.gcd(d,*(v for a in H+M for v in a));d//=common
 H=[tuple(v//common for v in a) for a in H];M=[tuple(v//common for v in a) for a in M]
 points=sorted({F.add(a,b) for a in H for b in M});index={a:i for i,a in enumerate(points)}
 fibres=[[] for _ in points]
 for a in range(21):
  for b in range(7):fibres[index[F.add(H[a],M[b])]].append((a,b))
 unit=F.scale(F.ONE,d*d)
 def edges(X):return [(i,j) for i,j in combinations(range(len(X)),2) if F.norm(F.sub(X[i],X[j]))==unit]
 he,me,ge=edges(H),edges(M),edges(points)
 factor={tuple(sorted([index[F.add(H[a],m)],index[F.add(H[b],m)]])) for a,b in he for m in M}
 factor|={tuple(sorted([index[F.add(h,M[a])],index[F.add(h,M[b])]])) for a,b in me for h in H}
 assert factor<=set(ge)
 return {'r':r,'denominator':d,'H':H,'M':M,'points':points,'H_edges':he,'M_edges':me,'edges':ge,'fibres':fibres,'factor_edges':sorted(factor),'extra_edges':sorted(set(ge)-factor)}

def xor(g):
 ps=json.loads((F.PARENT/'potentials.json').read_text())
 qs=[(0,)+tail for tail in product(range(4),repeat=6) if all(((0,)+tail)[a]!=((0,)+tail)[b] for a,b in g['M_edges'])]
 tried=0
 for pi,p in enumerate(ps):
  for qi,q in enumerate(qs):
   tried+=1;row=[]
   for fib in g['fibres']:
    vals={p[a]^q[b] for a,b in fib}
    if len(vals)!=1:break
    row.append(vals.pop())
   if len(row)==len(g['points']) and all(row[a]!=row[b] for a,b in g['edges']):return {'kind':'XOR','p_index':pi,'q_index':qi,'q':q,'colouring':row,'tries':tried,'M_class_size':len(qs)}
 return {'kind':'NO_SUPPLIED_XOR','tries':tried,'M_class_size':len(qs)}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
 args.out.mkdir(parents=True,exist_ok=False);start=time.perf_counter()
 H,M,d,A,B,angles,orbits=enumeration()
 rotation_rows=[{'r':r,'multiplicity':angles[r]} for r in sorted(angles)]
 rotation_raw=(json.dumps(rotation_rows,separators=(',',':'))+'\n').encode()
 (args.out/'rotations.json').write_bytes(rotation_raw)
 certificates=[];cases=[];graph_stream=sha256()
 for i,r in enumerate(sorted(orbits)):
  g=graph(r);c=xor(g);assert c['kind']=='XOR',('No certificate in supplied class',i,r)
  raw=(json.dumps(g,separators=(',',':'))+'\n').encode();graph_stream.update(raw)
  (args.out/f'{i:02d}.graph.json').write_bytes(raw)
  hcolour=json.loads((F.PARENT/'potentials.json').read_text())[c['p_index']]
  certificates.append({'r':r,'H_colouring':hcolour,'M_colouring':c['q']})
  cases.append({'index':i,'r':r,'orbit_size':len(orbits[r]),'event_multiplicity':angles[r],
    'vertices':len(g['points']),'edges':len(g['edges']),'factor_edges':len(g['factor_edges']),
    'extra_edges':len(g['extra_edges']),'collision_histogram':dict(sorted(Counter(map(len,g['fibres'])).items())),
    'H_colouring_index':c['p_index'],'M_colouring_index':c['q_index'],
    'XOR_trials_until_witness':c['tries'],'graph_sha256':sha256(raw).hexdigest()})
  print(json.dumps({'case':i,'vertices':len(g['points']),'edges':len(g['edges']),'extra_edges':len(g['extra_edges']),'status':'XOR VERIFIED'}),flush=True)
 cert_raw=(json.dumps(certificates,separators=(',',':'))+'\n').encode()
 (args.out/'certificate.json').write_bytes(cert_raw)
 result={'status':'ALL252 UNIT-CONTACT ROTATIONS ARE FOUR-CHROMATIC',
  'H_unit_differences':len(A),'M_unit_differences':len(B),'event_occurrences':sum(angles.values()),
  'rotations':len(angles),'C7_representatives':len(orbits),'normalized_spindle_colourings':96,
  'event_multiplicity_histogram':dict(sorted(Counter(angles.values()).items())),
  'rotation_denominator_histogram':dict(sorted(Counter(den for num,den in angles).items())),
  'case_histogram':[{'vertices':n,'edges':e,'extra_edges':x,'representatives':count,'rotations':count*7}
      for (n,e,x),count in sorted(Counter((c['vertices'],c['edges'],c['extra_edges']) for c in cases).items())],
  'representative_sum_pair_checks':sum(c['vertices']*(c['vertices']-1)//2 for c in cases),
  'witness_edge_checks':sum(c['edges'] for c in cases),
  'rotation_stream_sha256':sha256(rotation_raw).hexdigest(),
  'graph_stream_sha256':graph_stream.hexdigest(),'certificate_sha256':sha256(cert_raw).hexdigest(),
  'cases':cases}
 (args.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 (args.out/'timing.json').write_text(json.dumps({'seconds':time.perf_counter()-start})+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))

if __name__=='__main__':main()
