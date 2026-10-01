"""Separate raw-label, free-renaming, cell-isomorphism and arithmetic audit.
Only prior published audit primitives are imported, never production predicates,
schemas, enumeration, forcing, or canonical-map algorithms. Same author.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter,deque
import hashlib,importlib.util,json
s=Path(__file__).resolve().parent;source=s.parent/'tammes15_ordinary_five_four_one_exclusion/audit.py'
if hashlib.sha256(source.read_bytes()).hexdigest()!='f9d4ebbab1316f68e4dffdec8375ad158203c3cf2fd0627d90da68dee019eabb':raise RuntimeError('Prior published separate audit changed')
loader=importlib.util.spec_from_file_location('prior_separate_audit',source);a=importlib.util.module_from_spec(loader);loader.loader.exec_module(a)
old_check=a.check
ROLES={
 'D_one_X_one':(('E','G','B','C'),('D','X','E','G','B','C'),('X','D','E','G','B','C')),
 'D_one_Z_one':(('E','G','B','C'),('D','Z','E','G','B','C'),('Z','D','E','G','B','C')),
 'D_one_both_one':(('E','G','B'),('D','X','Z','E','G','B'),('X','Z','D','E','G','B')),
}
REPRESENTATIVES={
 'D_one_X_one':[(('E','G','B'),4),(('X','E','G'),6),(('D','E','G'),6),(('X','D','E'),4)],
 'D_one_Z_one':[(('E','G','B'),4),(('Z','E','G'),6),(('D','E','G'),6),(('Z','D','E'),4)],
 'D_one_both_one':[(('E','G','B'),1),(('X','E','G'),3),(('Z','E','G'),3),(('D','E','G'),3),
                   (('X','Z','E'),3),(('X','D','E'),3),(('Z','D','E'),3),(('X','Z','D'),1)],
}
def specification(role,contacts):
 extra,ones,deficient=ROLES[role];originals=a.ANCHORS+extra;names=originals+('L','K','M','P','Q');words=a.BASE
 if 'X' in ones:names+=('AX',);words+=(('X','P','AX','D'),)
 else:words+=(('X','P','D'),)
 if 'Z' in ones:names+=('AZ',);words+=(('Z','D','AZ','Q'),)
 else:words+=(('Z','D','Q'),)
 number={n:i for i,n in enumerate(names)}
 return {'names':names,'words':words,'faces':tuple(tuple(number[n] for n in w) for w in words),
  'mode':'full','maxima':{},'exact':{0:4,1:0,**{number[n]:1 for n in ones}},'distinct':(),
  'initial':tuple(range(len(originals))),'contact_edges':tuple((1,number[n]) for n in contacts)}
def check(labels,spec,use_orientability=True):
 if len(set(labels))>15:return False
 positions={n:i for i,n in enumerate(spec.get('names',()))}
 if sum(t==1 for t in spec['exact'].values())==6 and all(n in positions and positions[n]<len(labels) for n in ('L','K','M')):
  l,c,r=[a.actual_role(labels,spec,labels[positions[n]]) for n in ('L','K','M')]
  if any(t not in (1,2) for t in (l,c,r)):return False
  if c==2 and (l==2 or r==2):return False
  if l==r==2 and c==1:return False
 return old_check(labels,spec,use_orientability)
a.check=check

def renaming_coverage():
 counts=Counter();witnesses=[]
 for role,(free,ones,deficient) in ROLES.items():
  for omitted in combinations(deficient,3):
   contacts=set(deficient)-set(omitted);chosen=[n for n in free if n in contacts];other=[n for n in free if n not in contacts]
   permutation=dict(zip(chosen+other,free));renamed={permutation.get(n,n) for n in contacts}
   matches=[(tuple(rep),weight) for rep,weight in REPRESENTATIVES[role] if set(rep)==renamed]
   if len(matches)!=1 or set(permutation)!=set(free) or set(permutation.values())!=set(free):raise RuntimeError('Free renaming coverage failed')
   rep,weight=matches[0];counts[(role,rep)]+=1;witnesses.append({'role':role,'contacts':sorted(contacts),'free_bijection':permutation,'representative':rep})
 for role,rows in REPRESENTATIVES.items():
  for rep,weight in rows:
   if counts[(role,rep)]!=weight:raise RuntimeError('Free case weight differs')
 if len(witnesses)!=60 or len(counts)!=16:raise RuntimeError('Incomplete sixty-to-sixteen cover')
 return witnesses

def graph_data(faces):
 cells={a.face_key(tuple(f)) for f in faces};adj={v:set() for cell in cells for v in cell};t=Counter();corners=Counter()
 for cell in cells:
  for i,v in enumerate(cell):adj[v].update((cell[i-1],cell[(i+1)%len(cell)]));corners[v]+=1;t[v]+=len(cell)==3
 edges={tuple(sorted((v,w))) for v,ns in adj.items() for w in ns}
 return cells,adj,t,corners,edges

def distances(adj,start):
 distance={start:0};queue=deque([start])
 while queue:
  v=queue.popleft()
  for w in adj[v]:
   if w not in distance:distance[w]=distance[v]+1;queue.append(w)
 return distance

def signatures(cells,adj,t):
 five=[v for v in adj if len(adj[v])==5];three=[v for v in adj if len(adj[v])==3]
 if len(five)!=1 or len(three)!=1:raise RuntimeError('Wrong unique odd degrees')
 df,du=distances(adj,five[0]),distances(adj,three[0])
 return {v:(len(adj[v]),t[v],df[v],du[v],tuple(sorted((len(adj[w]),t[w]) for w in adj[v]))) for v in adj}

def isomorphism(source_faces,target_faces):
 left,la,lt,lc,le=graph_data(source_faces);right,ra,rt,rc,re=graph_data(target_faces);ls=signatures(left,la,lt);rs=signatures(right,ra,rt)
 candidates={v:tuple(w for w in ra if ls[v]==rs[w]) for v in la};mapping={};used=set();nodes=0
 def visit():
  nonlocal nodes
  nodes+=1
  if nodes>200000:raise RuntimeError('INCOMPLETE: fixed200000isomorphismnodes')
  if len(mapping)==len(la):
   if {a.face_key(tuple(mapping[v] for v in f)) for f in left}==right:return dict(mapping)
   return None
  v=min((x for x in la if x not in mapping),key=lambda x:(sum(w not in used for w in candidates[x]),-sum(y in mapping for y in la[x]),x))
  for w in candidates[v]:
   if w in used or any((u in la[v])!=(z in ra[w]) for u,z in mapping.items()):continue
   mapping[v]=w;used.add(w)
   if all(a.face_key(tuple(mapping[x] for x in cell)) in right for cell in left if all(x in mapping for x in cell)):
    answer=visit()
    if answer is not None:return answer
   used.remove(w);del mapping[v]
  return None
 answer=visit();return answer,nodes

def validate_map(mapdata):
 cells,adj,t,corners,edges=graph_data(mapdata['faces'])
 if set(adj)!=set(range(15)) or len(edges)!=30 or sorted(map(len,cells))!=[3]*8+[4]*9:raise RuntimeError('Wrong15point cell counts')
 if edges!=set(map(tuple,mapdata['edges'])) or len(distances(adj,0))!=15:raise RuntimeError('Wrong map edges or connectivity')
 if any(corners[v]!=len(adj[v]) for v in adj):raise RuntimeError('Incomplete mapped star')
 five=next(v for v in adj if len(adj[v])==5);u=next(v for v in adj if len(adj[v])==3);permutation={v:v for v in adj};permutation[0],permutation[five]=five,0
 # Canonical maps putF at0; renameU to1 for the generic separate predicate.
 if five!=0:raise RuntimeError('MapF notat0')
 permutation[1],permutation[u]=u,1;faces=tuple(tuple(permutation[v] for v in cell) for cell in cells)
 names=('F','U')+tuple('V'+str(i) for i in range(2,15));spec={'names':names,'faces':faces,'words':tuple(tuple(names[v] for v in cell) for cell in faces),'mode':'full','maxima':{},'exact':{permutation[v]:t[v] for v in adj},'distinct':(),'contact_edges':()}
 if not check(tuple(range(15)),spec):raise RuntimeError('Explicit map violates independent geometric necessities')
 wrong=dict(spec);wrong['exact']=dict(spec['exact']);wrong['exact'][0]=3
 if check(tuple(range(15)),wrong):raise RuntimeError('Independent wrong-F3 control accepted')
 if check(tuple(range(16)),spec):raise RuntimeError('Independent sixteen-point control accepted')
 if any(sorted(row)!=sorted(adj[v]) for v,row in enumerate(mapdata['rotations'])):raise RuntimeError('Map rotations wrong neighbor sets')
 oriented={}
 for face in mapdata['faces']:
  for i,v in enumerate(face):oriented.setdefault(v,{})[face[i-1]]=face[(i+1)%len(face)]
 for v,row in enumerate(mapdata['rotations']):
  if any(oriented[v][row[i]]!=row[(i+1)%len(row)] for i in range(len(row))):raise RuntimeError('Source cyclic rotation differs')
 # Directed cells/links, edge-two counts, orientation and Euler2 certify a sphere complex.
 boundary=Counter(tuple(sorted((cell[i],cell[(i+1)%len(cell)]))) for cell in cells for i in range(len(cell)))
 if any(m!=2 for m in boundary.values()) or 15-len(edges)+len(cells)!=2:raise RuntimeError('Not aclosedsphere complex')
 q=next(cell for cell in cells if five in cell and len(cell)==4);d=q[(q.index(five)+2)%4]
 return {'U':u,'D':d,'F_U_distance':distances(adj,five)[u],'U_D_contact':u in adj[d],'triangles_at_F':t[five],'one_T_fours':sum(t[v]==1 and len(adj[v])==4 for v in adj),'positive_closed_map_and_wrong_F3_and_16_point_controls':True}

def independently_propagate_corners(maps):
 """Derive M1 corners from ordinary stars, rather than reading its table.
 The vectors are formal symbols, so no trigonometric rounding is involved.
 """
 symbols=('pi','alpha','psi','z1','z2','z3','z4','x','rho_x')
 def expression(**kw):return tuple(kw.get(n,0) for n in symbols)
 def add(*rows):return tuple(sum(x) for x in zip(*rows))
 def subtract(left,right):return tuple(x-y for x,y in zip(left,right))
 alpha=expression(alpha=1);two_pi=expression(pi=2);A=expression(pi=2,alpha=-2);phi=expression(pi=2,alpha=-4)
 z=[expression(**{n:1}) for n in ('psi','z1','z2','z3','z4')];x=expression(x=1);rx=expression(rho_x=1)
 pairs=[(phi,z[0])]+[(subtract(A,z[j]),z[j+1]) for j in range(4)]+[(x,rx)]
 dual={}
 for left,right in pairs:dual[left]=right;dual[right]=left
 # Map identification uses its actual U neighborhood, not a canonical SHA.
 candidates=[m for m in maps.values() if graph_data(m['faces'])[1][6]=={1,11,12}]
 if len(candidates)!=1:raise RuntimeError('Independent M1 identification differs')
 m1=candidates[0];cells,adj,t,corner,edges=graph_data(m1['faces']);quads={f for f in cells if len(f)==4};corners={}
 def install(face,vertex,angle):
  other=dual.get(angle)
  if other is None:raise RuntimeError('Unknown formal rho pair')
  i=face.index(vertex)
  for j,u in enumerate(face):
   value=angle if (j-i)%2==0 else other
   key=(face,u)
   if key in corners and corners[key]!=value:raise RuntimeError('Independent corner conflict')
   corners[key]=value
 q=next(f for f in quads if 0 in f);install(q,0,phi)
 ordinary=(2,3,4,5,8,13,14)
 for vertex in ordinary:
  incident=[f for f in quads if vertex in f];known=[f for f in incident if (f,vertex) in corners];unknown=[f for f in incident if (f,vertex) not in corners]
  if t[vertex]!=2 or len(known)!=1 or len(unknown)!=1:raise RuntimeError('Independent ordinary corner transfer not unique')
  install(unknown[0],vertex,subtract(A,corners[(known[0],vertex)]))
 remaining=[f for f in quads if not any((f,u) in corners for u in f)]
 if len(remaining)!=1 or 6 not in remaining[0]:raise RuntimeError('Independent final Q differs')
 install(remaining[0],6,x)
 def residual(vertex):
  return subtract(add(expression(alpha=t[vertex]),*(corners[(f,vertex)] for f in quads if vertex in f)),two_pi)
 if any(residual(v)!=expression() for v in (0,)+ordinary):raise RuntimeError('Independent ordinary angle sum differs')
 if residual(6)!=expression(pi=2,alpha=-4,z3=-2,x=1):raise RuntimeError('Independent U angle equation differs')
 if residual(7)!=expression(alpha=-3,z2=1,x=1):raise RuntimeError('Independent D angle equation differs')
 if residual(1)!=expression(pi=-2,alpha=1,psi=1,z4=1,rho_x=1):raise RuntimeError('Independent X angle equation differs')
 m2=next(m for m in maps.values() if m is not m1);cells2,adj2,t2,corner2,edges2=graph_data(m2['faces']);u=next(v for v in adj2 if len(adj2[v])==3)
 dq=[f for f in cells2 if len(f)==4 and 7 in f]
 if t2[7]!=1 or len(dq)!=3 or sum(u in f for f in dq)!=2 or u not in adj2[7]:raise RuntimeError('Independent M2 D-U hinge differs')
 return {'ordinary_star_transfer_order':list(ordinary),'all_nine_M1_Qs_independently_propagated':True,'U_D_X_incidence_equations_verified':True,'M2_D_U_hinge_verified':True}

def independent_angle_arithmetic():
 from fractions import Fraction as Q
 def mul(x,y):
  answer=[Q(0)]*(len(x)+len(y)-1)
  for i,u in enumerate(x):
   for j,v in enumerate(y):answer[i+j]+=u*v
  return answer
 def at(poly,x):
  value=Q(0)
  for coefficient in poly[::-1]:value=value*x+coefficient
  return value
 P=mul([1,-6,1],[3,-4,1]);P[1]-=16;P[2]+=48
 if P!=[3,-38,76,-10,1]:raise RuntimeError('Independent quartertan polynomial expansion differs')
 x=Q(97,1000);margin=at(P,x);cq=at([1,-6,1],x)/(8*x);derivative_bound=4*Q(1,10)**3+152*Q(1,10)-38
 n14=[-1,0,3,-2,4];lower=at(n14,Q(14,25));upper=at(n14,Q(57,100))
 if not (margin>0 and Q(14,25)>cq and derivative_bound<0 and lower<0<upper):raise RuntimeError('Independent metric/N14 rational margin failed')
 c=Q(57,100);H=1+2*c;first=(H-c*c)/(2*c*c)
 M=((H,-H*c),(c*c,c*H));power=((Q(1),Q(0)),(Q(0),Q(1)));transfer=[]
 for j in range(4):
  denominator=power[1][0]*first+power[1][1]
  if denominator<=0:raise RuntimeError('Independent projective denominator failed')
  transfer.append((power[0][0]*first+power[0][1])/denominator)
  power=tuple(tuple(sum(power[i][k]*M[k][j] for k in range(2)) for j in range(2)) for i in range(2))
 if transfer!=[Q(18151,6498),Q(1969228,880479),Q(5953,3249),Q(87762898,58972599)] or any(v<=c for v in transfer):raise RuntimeError('Independent matrix corner transfer failed')
 v,w=transfer[2:4];branch=[v*v-H,3*H-v*v,w*w-H,3*H-w*w]
 E=H-w*w-2*v*w;Dmargin=v*(H-w*w)+2*w*H+E
 b=1/c;R=H-transfer[0]*b;Xmargin=c*(transfer[0]+b)+R
 if not (all(v>0 for v in branch) and E<0<Dmargin and R<0 and Xmargin<0):raise RuntimeError('Independent M1 tangent-branch certificates failed')
 return {'quartertan_polynomial_coefficients':list(map(int,P)),'P_at_97over1000':str(margin),'14over25_minus_c_at_97over1000':str(Q(14,25)-cq),'Pprime_upper':str(derivative_bound),'N14_lower_sign':str(lower),'N14_upper_sign':str(upper),
  'M1_matrix_power_transfer_a0_to_a3':list(map(str,transfer)),'M1_positive_tangent_branch_margins':list(map(str,branch)),
  'M1_E_negative':str(E),'M1_D_margin_positive':str(Dmargin),'M1_R_negative':str(R),'M1_X_margin_negative':str(Xmargin)}

def run(trace_path):
 data=trace_path.read_bytes();saved=json.loads((s/'EXPECTED.json').read_text());
 if hashlib.sha256(data).hexdigest()!=saved['trace_sha256']:raise RuntimeError('Regenerated production trace hash differs')
 trace=json.loads(data);maps=json.loads((s/'MAPS.json').read_text());facts={sha:validate_map(m) for sha,m in maps.items()};counts=Counter();witnesses=[];keys=set();renamings=renaming_coverage()
 if sorted(f['F_U_distance'] for f in facts.values())!=[2,3]:raise RuntimeError('Two map nonisomorphism invariant differs')
 toy=specification('D_one_X_one',('X','D','E'));prefix=toy['initial']+(12,8,13)
 if not old_check(prefix,toy) or check(prefix,toy):raise RuntimeError('Independent local212 positive/negative control differs')
 for role,rows in REPRESENTATIVES.items():
  for contacts,weight in rows:
   key=role+'_U'+''.join(contacts);keys.add(key);record=trace['cases'][key];spec=specification(role,contacts)
   if record['multiplicity']!=weight or list(spec['names'])!=record['names'] or not a.same_words(spec['words'],record['words']):raise RuntimeError('Independent role schema differs')
   if {spec['names'][i]:t for i,t in spec['exact'].items()}!=record['exact'] or set(spec['contact_edges'])!=set(map(tuple,record['contacts'])):raise RuntimeError('Exact original roles/contactedges differ')
   states,raw,bounds=a.cover(spec,record['base'],spec['initial']);counts['base_covers']+=1;counts['raw_tuples']+=raw;counts['compared_boundaries']+=bounds
   if len(states)!=len(record['ordinary_stars']):raise RuntimeError('Base survivor lists differ')
   for prefix,entry in zip(states,record['ordinary_stars']):
    if list(prefix)!=entry['prefix']:raise RuntimeError('Base actual partition differs')
    offenders=a.new_U_offenders(prefix,spec)
    if offenders:
     if entry.get('reason')!='one_T_U_new_neighbor':raise RuntimeError('EarlyU obstruction differs')
     counts['early_base_new_U_rejections']+=1;continue
    if 'reason' in entry:raise RuntimeError('Spurious early rejection')
    roles,full=a.ordinary_stars(prefix,spec)
    if roles!=entry['triangle_roles'] or list(full['names'])!=entry['names'] or not a.same_words(full['words'][len(spec['words']):],entry['forced_words']):raise RuntimeError('Independentordinary-star forcing differs')
    states,raw,bounds=a.cover(full,entry['cover'],prefix);counts['ordinary_star_covers']+=1;counts['raw_tuples']+=raw;counts['compared_boundaries']+=bounds
    if len(states)!=len(entry['closures']):raise RuntimeError('Ordinary-star survivors differ')
    for p,root in zip(states,entry['closures']):
     if list(p)!=root['prefix']:raise RuntimeError('Closureprefixdiffers')
     counts['closure_roots']+=1;queue=[(p,full,[])];steps=iter(root['steps'])
     while queue:
      labels,current,path=queue.pop();step=next(steps)
      if list(labels)!=step['prefix'] or json.loads(json.dumps(path))!=step['path']:raise RuntimeError('Closure currentpartition/path differs')
      bad=a.new_U_offenders(labels,current)
      if bad:
       if step.get('reason')!='one_T_U_new_neighbor' or step['vertex'] not in bad:raise RuntimeError('LateU obstruction differs')
       counts['new_U_rejections']+=1;continue
      forced=a.last_face(labels,current)
      if forced is None:
       actual_cells={a.face_key(tuple(labels[i] for i in word)) for word in current['faces']};cells,adj,t,corner,edges=graph_data(actual_cells)
       if set(adj)!=set(range(15)) or any(corner[v]!=len(adj[v]) for v in adj) or len(edges)!=30:raise RuntimeError('Open/non15terminalmapnotjustified')
       if step.get('reason')!='CLOSED_COMBINATORIAL_MAP':raise RuntimeError('Terminalstatusdiffers')
       matches=[]
       for sha,mapdata in maps.items():
        match,nodes=isomorphism(actual_cells,mapdata['faces']);counts['isomorphism_nodes']+=nodes
        if match is not None:matches.append((sha,match))
       if len(matches)!=1 or matches[0][0]!=step['map_sha256']:raise RuntimeError('Independent embedded-map classification differs')
       sha,match=matches[0];counts['closed_15_point_maps']+=1;counts['map_'+sha]+=1
       witnesses.append({'case':key,'prefix':labels,'map_sha256':sha,'independent_cell_isomorphism':match});continue
      name,t,words,nxt=forced
      if name!=step['vertex'] or t!=step['triangle_role'] or not a.same_words(words,step['words']) or list(nxt['names'])!=step['names']:raise RuntimeError('Independentmissingface differs')
      states,raw,bounds=a.cover(nxt,step['cover'],labels);counts['closing_face_covers']+=1;counts['raw_tuples']+=raw;counts['compared_boundaries']+=bounds
      for survivor in states:queue.append((survivor,nxt,path+step['words']))
     if next(steps,None) is not None:raise RuntimeError('Unconsumedsteps')
 if keys!=set(trace['cases']) or len(witnesses)!=16:raise RuntimeError('Incompletecase/mapaudit')
 for name in ('base_covers','ordinary_star_covers','closure_roots','closing_face_covers','early_base_new_U_rejections','closed_15_point_maps'):
  if counts[name]!=saved['stats'][name]:raise RuntimeError('Covercounts differ '+name)
 return {'agent':'six-tammes-1','role':'researcher','status':'SEPARATE_SAME_AUTHOR_RAW_LABEL_FREE_RENAMING_CELL_ISOMORPHISM_AUDIT',
   'counts':dict(counts),'map_facts':facts,'independent_corner_propagation':independently_propagate_corners(maps),
   'independent_exact_angle_arithmetic':independent_angle_arithmetic(),'local212_positive_then_forced_strip_negative':True,
   'sixty_labelled_cases_to_sixteen_representatives_verified':len(renamings),
   'every_stage_entrywise_agreement':True,'production_trace_sha256':saved['trace_sha256'],
   'scope':'Written geometric, role, renaming, strip, angle and N14 bridges are unformalized; same-author audit, not independent mathematical review. Both maps are excluded using written inequalities and exact certificates; unrestricted numerical bounds unchanged.'}

if __name__=='__main__':
 import argparse,subprocess,sys,tempfile
 parser=argparse.ArgumentParser();parser.add_argument('--production-partitions',type=Path);args=parser.parse_args()
 if args.production_partitions:summary=run(args.production_partitions)
 else:
  with tempfile.TemporaryDirectory(prefix='tammes15-six-zero-') as folder:
   trace=Path(folder)/'partitions.json';subprocess.run([sys.executable,'-B',str(s/'check.py'),'--export-partitions',str(trace)],check=True,capture_output=True,text=True,timeout=45);summary=run(trace)
 expected=json.loads((s/'AUDIT_EXPECTED.json').read_text())
 if summary!=expected:raise RuntimeError('Whole separate audit summary differs from AUDIT_EXPECTED.json')
 print(json.dumps(summary,sort_keys=True,separators=(',',':')))
