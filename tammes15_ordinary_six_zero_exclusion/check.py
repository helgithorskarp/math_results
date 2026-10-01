"""Exact original-face cover and metric certificates for profile (0,6,0).
Uses only a hash-guarded PRIOR PUBLIC checker in the sibling8180 directory.
Written geometric and metric bridges are in PROOF.md; all traces regenerate.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import hashlib,importlib.util,json,math
s=Path(__file__).resolve().parent;source=s.parent/'tammes15_ordinary_five_four_one_exclusion/check.py'
if hashlib.sha256(source.read_bytes()).hexdigest()!='2d543e31857e3a64d31e9306617ac7fb3e20cd3f7605941f1d96c5306d579c86':raise RuntimeError('Published8180 kernel changed')
loader=importlib.util.spec_from_file_location('published_original_face_kernel',source);k=importlib.util.module_from_spec(loader);loader.loader.exec_module(k)
TABLE={
 'D_one_X_one':(('E','G','B','C'),('D','X','E','G','B','C')),
 'D_one_Z_one':(('E','G','B','C'),('D','Z','E','G','B','C')),
 'D_one_both_one':(('E','G','B'),('D','X','Z','E','G','B')),
}

def schema(role,choice):
 extra,ones=TABLE[role];originals=k.ANCHORS+extra;deficient=tuple(n for n in originals if n in ones);contacts=tuple(deficient[i] for i in choice)
 names=originals+('L','K','M','P','Q');words=k.CORE
 if 'X' in ones:names+=('AX',);words+=(('X','D','AX','P'),)
 else:words+=(('X','D','P'),)
 if 'Z' in ones:names+=('AZ',);words+=(('Z','Q','AZ','D'),)
 else:words+=(('Z','Q','D'),)
 number={n:i for i,n in enumerate(names)}
 if len(deficient)!=6 or len(names)!=18:raise RuntimeError('Wrong six-one original cover')
 return {'case':role+'_U'+''.join(contacts),'names':names,'words':words,'number':number,
   'faces':tuple(tuple(number[n] for n in w) for w in words),'mode':'full','maxima':{},'exact':{'F':4,'U':0,**{n:1 for n in ones}},
   'distinct':(),'initial':tuple(range(len(originals))),'contact_edges':tuple((1,number[n]) for n in contacts)}

original_necessary=k.necessary
ALLOWED_STRIPS={(1,1,1),(1,1,2),(1,2,1),(2,1,1)}
def reduced_necessary(labels,spec):
    if max(labels)+1>15:return 'more_than_fifteen_actual_points'
    if sum(t==1 for t in spec['exact'].values())==6 and all(n in spec['number'] for n in ('L','K','M')):
        slots=[spec['number'][n] for n in ('L','K','M')]
        if max(slots)<len(labels):
            roles=tuple(k.triangle_role(labels,spec,n) for n in ('L','K','M'))
            if roles not in ALLOWED_STRIPS:return 'classified_forbidden_strip_roles'
    return original_necessary(labels,spec)
k.necessary=reduced_necessary

def representatives(role):
    extra,ones=TABLE[role];initial=k.ANCHORS+extra;deficient=tuple(n for n in initial if n in ones)
    fixed=tuple(n for n in deficient if n in k.ANCHORS);free=extra
    for m in range(len(fixed)+1):
        q=3-m
        if not 0<=q<=len(free):continue
        for chosen in combinations(fixed,m):
            contacts=chosen+free[:q];choice=tuple(sorted(deficient.index(n) for n in contacts))
            yield choice,math.comb(len(free),q)

def closed_map(labels,spec):
    faces,corners,neighbors,actual_neighbors,outgoing=k.actual_state(labels,spec);count=max(labels)+1
    for v in range(count):
        degree=5 if v==0 else 3 if v==1 else 4
        if len(corners[v])!=degree or len(actual_neighbors[v])!=degree:return None
    if count!=15:return {'status':'CLOSED_COMPONENT_TOO_SMALL','points':count}
    return {'status':'CLOSED_COMBINATORIAL_MAP_NOT_METRIC','points':count,'faces':tuple(sorted(faces)),
        'edges':tuple(sorted({tuple(sorted((v,w))) for v,row in actual_neighbors.items() for w in row})),
        'degrees':{v:len(row) for v,row in actual_neighbors.items()},'outgoing':{v:dict(row) for v,row in outgoing.items()}}

def canonical_map(mapping):
    faces=mapping['faces'];five=next(v for v,d in mapping['degrees'].items() if d==5)
    sole=[f for f in faces if five in f and len(f)==4]
    if len(sole)!=1:raise RuntimeError('Ordinary-five Q is not unique')
    candidates=[]
    for sign in (1,-1):
        oriented=[f if sign==1 else f[::-1] for f in faces];row={}
        for f in oriented:
            for i,v in enumerate(f):row.setdefault(v,{})[f[i-1]]=f[(i+1)%len(f)]
        q=sole[0] if sign==1 else sole[0][::-1];start=q[q.index(five)-1]
        labels={five:0};queue=[five];rotations=[]
        for v in queue:
            first=start if v==five else min((w for w in row[v] if w in labels),key=labels.get)
            ordered=[];w=first
            while w not in ordered:
                ordered.append(w)
                if w not in labels:labels[w]=len(labels);queue.append(w)
                w=row[v][w]
            if w!=first or len(ordered)!=mapping['degrees'][v]:raise RuntimeError('Bad actual cyclic link')
            rotations.append([labels[w] for w in ordered])
        if len(labels)!=15:raise RuntimeError('Closed map graph is disconnected')
        normalized_faces=sorted(k.cyclic(tuple(labels[v] for v in f)) for f in oriented)
        result={'faces':normalized_faces,'rotations':rotations,
            'edges':sorted(tuple(sorted((labels[a],labels[b]))) for a,b in mapping['edges'])}
        encoded=json.dumps(result,sort_keys=True,separators=(',',':'))
        candidates.append((encoded,result,{str(v):n for v,n in labels.items()},sign))
    encoded,result,renaming,sign=min(candidates,key=lambda x:x[0])
    return hashlib.sha256(encoded.encode()).hexdigest(),result,renaming,sign


def serialized(value):return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

MAP1='9e75c890402048caf6dc42f456efc364be64daa9a33c646809f8f29d55b9fdfa'
MAP2='cde759765dedf9a482dc6bc05de9f8219240108e73a636e78043d44264691df5'

def corner_incidence_controls(maps):
 """Verify the written M1 corner table as formal linear expressions.
 Trigonometric identities, concavity and monotonicity remain written bridges.
 """
 basis=('pi','alpha','psi','z1','z2','z3','z4','x','rho_x')
 def v(**terms):return tuple(terms.get(n,0) for n in basis)
 def add(*rows):return tuple(sum(column) for column in zip(*rows))
 def neg(row):return tuple(-x for x in row)
 pi=v(pi=1);alpha=v(alpha=1);A=v(pi=2,alpha=-2);phi=v(pi=2,alpha=-4)
 z=[v(**{name:1}) for name in ('psi','z1','z2','z3','z4')];x=v(x=1);rx=v(rho_x=1)
 table=[((0,2,7,1),(phi,z[0],phi,z[0])),
  ((2,3,9,8),(add(A,neg(z[0])),z[1],add(A,neg(z[0])),z[1])),
  ((3,4,10,9),(add(A,neg(z[1])),z[2],add(A,neg(z[1])),z[2])),
  ((4,5,11,10),(add(A,neg(z[2])),z[3],add(A,neg(z[2])),z[3])),
  ((1,6,11,5),(z[4],add(A,neg(z[3])),z[4],add(A,neg(z[3])))),
  ((7,8,13,12),(z[2],add(A,neg(z[1])),z[2],add(A,neg(z[1])))),
  ((9,10,14,13),(z[3],add(A,neg(z[2])),z[3],add(A,neg(z[2])))),
  ((6,12,14,11),(add(A,neg(z[3])),z[4],add(A,neg(z[3])),z[4])),
  ((1,7,12,6),(rx,x,rx,x))]
 cells=maps[MAP1]['faces'];quads={k.cyclic(tuple(f)) for f in cells if len(f)==4}
 if {k.cyclic(f) for f,row in table}!=quads:raise RuntimeError('M1 corner table differs from actual Qs')
 totals={u:v(alpha=sum(len(f)==3 and u in f for f in cells)) for u in range(15)}
 for face,row in table:
  if row[0]!=row[2] or row[1]!=row[3]:raise RuntimeError('Opposite corner table differs')
  for u,angle in zip(face,row):totals[u]=add(totals[u],angle)
 ordinary=(2,3,4,5,8,13,14)
 if any(totals[u]!=v(pi=2) for u in (0,)+ordinary):raise RuntimeError('Ordinary vertex propagation differs')
 if add(totals[6],v(pi=-2))!=v(pi=2,alpha=-4,z3=-2,x=1):raise RuntimeError('U equation differs')
 if add(totals[7],v(pi=-2))!=v(alpha=-3,z2=1,x=1):raise RuntimeError('D equation differs')
 if add(totals[1],v(pi=-2))!=v(pi=-2,alpha=1,psi=1,z4=1,rho_x=1):raise RuntimeError('X equation differs')
 # In M2, the two D-U edge faces are exactly the other D quadrilaterals.
 cells2=maps[MAP2]['faces'];dq=[f for f in cells2 if len(f)==4 and 7 in f]
 if len(dq)!=3 or sum(13 in f for f in dq)!=2 or sum(len(f)==3 and 7 in f for f in cells2)!=1:raise RuntimeError('M2 D-U hinge differs')
 return {'M1_ordinary_vertices':list(ordinary),'M1_all_nine_Q_corner_words_verified':True,
  'M1_U_D_X_formal_incidence_equations_verified':True,'M2_one_T_D_two_U_adjacent_Qs_verified':True}

def map1_endpoint_certificate():
 from fractions import Fraction as Q
 c=Q(57,100);H=1+2*c;a=[(H-c*c)/(2*c*c)]
 for j in range(3):a.append(H*(a[-1]-c)/(c*(H+c*a[-1])))
 if a!=[Q(18151,6498),Q(1969228,880479),Q(5953,3249),Q(87762898,58972599)]:raise RuntimeError('M1 rational transfer differs')
 if any(t<=c or H+c*t<=0 for t in a):raise RuntimeError('M1 endpoint recurrence branch failed')
 branch={'a2_squared_minus_H':a[2]**2-H,'3H_minus_a2_squared':3*H-a[2]**2,
  'a3_squared_minus_H':a[3]**2-H,'3H_minus_a3_squared':3*H-a[3]**2}
 E=H-a[3]**2-2*a[2]*a[3];N=a[2]*(H-a[3]**2)+2*a[3]*H
 b=1/c;R=H-a[0]*b;Xmargin=c*(a[0]+b)+R
 if not (all(t>0 for t in branch.values()) and E<0 and N+E>0 and R<0 and Xmargin<0):raise RuntimeError('M1 exact angle endpoint signs failed')
 return {'c0':str(c),'H':str(H),'a0_to_a3':list(map(str,a)),
  'positive_branch_margins':{n:str(t) for n,t in branch.items()},'E_negative':str(E),
  'N_plus_E_positive':str(N+E),'R_negative':str(R),'X_margin_negative':str(Xmargin)}

def controls():
 from fractions import Fraction as Q
 maps=json.loads((s/'MAPS.json').read_text());map_controls={}
 for sha,data in maps.items():
  adj={v:set() for v in range(15)};t=Counter()
  for f in data['faces']:
   for i,v in enumerate(f):adj[v].update((f[i-1],f[(i+1)%len(f)]));t[v]+=len(f)==3
  u=next(v for v in adj if len(adj[v])==3);rename={v:v for v in adj};rename[1],rename[u]=u,1
  names=('F','U')+tuple('V'+str(i) for i in range(2,15));faces=tuple(tuple(rename[v] for v in f) for f in data['faces'])
  toy={'names':names,'number':{n:i for i,n in enumerate(names)},'faces':faces,'words':tuple(tuple(names[v] for v in f) for f in faces),
    'mode':'full','maxima':{},'exact':{names[rename[v]]:t[v] for v in adj},'distinct':(),'contact_edges':()}
  labels=tuple(range(15))
  if k.necessary(labels,toy) is not None:raise RuntimeError('Positive fullmap rejected')
  wrong=dict(toy);wrong['exact']=dict(toy['exact']);wrong['exact']['F']=3
  if k.necessary(labels,wrong) is None:raise RuntimeError('WrongF3 fullmap accepted')
  large=dict(toy);large['names']=names+('V15',);large['number']={n:i for i,n in enumerate(large['names'])}
  if k.necessary(tuple(range(16)),large)!='more_than_fifteen_actual_points':raise RuntimeError('Cardinality16 control differs')
  q=next(f for f in data['faces'] if 0 in f and len(f)==4);d=q[(q.index(0)+2)%4]
  map_controls[sha]={'positive_full_15_map':True,'wrongF3_negative':True,'16points_negative':True,'U':u,'D':d,'U_D_contact':u in adj[d]}
 spec=schema('D_one_X_one',(0,1,2));prefix=spec['initial']+(12,8,13)
 if original_necessary(prefix,spec) is not None or k.necessary(prefix,spec)!='classified_forbidden_strip_roles':raise RuntimeError('Positive local212 prefix/negative forced-strip control differs')
 x=Q(97,1000);P=x**4-10*x**3+76*x*x-38*x+3;f=lambda c:4*c**4-2*c**3+3*c*c-1
 values={'P(97/1000)':str(P),'c(97/1000)':str((1-6*x+x*x)/(8*x)),
   '14/25-c(97/1000)':str(Q(14,25)-(1-6*x+x*x)/(8*x)),
   'Pprime_upper_0_to_1over10':str(4*Q(1,10)**3+152*Q(1,10)-38),
   'N14_f(14/25)':str(f(Q(14,25))),'N14_f(57/100)':str(f(Q(57,100)))}
 if P<=0 or Q(14,25)-(1-6*x+x*x)/(8*x)<=0 or f(Q(14,25))>=0 or f(Q(57,100))<=0:raise RuntimeError('Exact angle/N14 arithmetic failed')
 return {'full_map_controls':map_controls,'local212_positive_then_forced_role_negative':True,
  'corner_incidence':corner_incidence_controls(maps),'map1_exact_endpoint':map1_endpoint_certificate(),'map2_and_N14_exact_values':values}

def run():
    stats=Counter();cases={};maps={};source_controls=controls()
    for role in TABLE:
        for choice,multiplicity in representatives(role):
            spec=schema(role,choice);base=k.cover(spec);extensions=[]
            stats['base_covers']+=1;stats['labelled_cases_covered']+=multiplicity;stats['base_nodes']+=base['nodes'];stats['base_survivors']+=len(base['survivors'])
            for prefix in base['survivors']:
                if k.one_T_U_obstruction(prefix,spec):
                    stats['early_base_new_U_rejections']+=1
                    extensions.append({'prefix':prefix,'reason':'one_T_U_new_neighbor'});continue
                roles,full=k.complete_ordinary_stars(prefix,spec);first=k.cover(full,prefix);roots=[]
                stats['ordinary_star_covers']+=1;stats['ordinary_star_nodes']+=first['nodes'];stats['ordinary_star_survivors']+=len(first['survivors'])
                for patch in first['survivors']:
                    stats['closure_roots']+=1;root={'prefix':patch,'names':full['names'],'steps':[]};queue=[(patch,full,[])]
                    while queue:
                        labels,chart,path=queue.pop();bad=k.one_T_U_obstruction(labels,chart)
                        if bad:
                            stats['new_U_rejections']+=1;root['steps'].append({'prefix':labels,'path':path,'reason':'one_T_U_new_neighbor','vertex':bad});continue
                        forced=k.force_last_face(labels,chart)
                        if forced is None:
                            completed=closed_map(labels,chart)
                            if completed is None:
                                stats['open_terminal_patches']+=1;root['steps'].append({'prefix':labels,'path':path,'reason':'OPEN_TERMINAL','names':chart['names'],'words':chart['words']});continue
                            if completed['status']=='CLOSED_COMPONENT_TOO_SMALL':
                                stats['closed_small_component_rejections']+=1;root['steps'].append({'prefix':labels,'path':path,'reason':'closed_small_component','points':completed['points']});continue
                            sha,mapping,renaming,sign=canonical_map(completed);stats['closed_15_point_maps']+=1
                            maps.setdefault(sha,{'canonical_map':mapping,'labelled_occurrences':0,'example':{'case':spec['case'],'prefix':labels,'names':chart['names'],'words':chart['words'],'exact':chart['exact'],'contact_edges':chart['contact_edges'],'canonical_renaming':renaming,'canonical_orientation':sign}})['labelled_occurrences']+=1
                            root['steps'].append({'prefix':labels,'path':path,'reason':'CLOSED_COMBINATORIAL_MAP','map_sha256':sha,'canonical_renaming':renaming,'canonical_orientation':sign});continue
                        if len(path)>=12:raise RuntimeError('INCOMPLETE: unchanged12faceforcingdepth')
                        name,t,words,nxt=forced;res=k.cover(nxt,labels);stats['closing_face_covers']+=1;stats['closing_face_nodes']+=res['nodes'];stats['maximum_positions']=max(stats['maximum_positions'],len(nxt['names']))
                        root['steps'].append({'prefix':labels,'path':path,'vertex':name,'triangle_role':t,'words':words,'names':nxt['names'],'cover':res})
                        for survivor in res['survivors']:queue.append((survivor,nxt,path+list(words)))
                    roots.append(root)
                extensions.append({'prefix':prefix,'triangle_roles':roles,'names':full['names'],'forced_words':full['words'][len(spec['words']):],'cover':first,'closures':roots})
            record={'case':spec['case'],'role':role,'choice':choice,'multiplicity':multiplicity,'names':spec['names'],'words':spec['words'],'exact':spec['exact'],'contacts':spec['contact_edges'],'initial':spec['initial'],'base':base,'ordinary_stars':extensions}
            cases[spec['case']]=record
    if stats['base_covers']!=16 or stats['labelled_cases_covered']!=60:raise RuntimeError('Incomplete renaming cover')
    stats['open_terminal_patches']=stats.get('open_terminal_patches',0);stats['closed_15_point_maps']=stats.get('closed_15_point_maps',0);stats['canonical_maps']=len(maps)
    canonical={sha:record['canonical_map'] for sha,record in maps.items()}
    fixture=json.loads((s/'MAPS.json').read_text())
    if json.loads(serialized(canonical))!=fixture:raise RuntimeError('Recomputed maps differ from MAPS.json')
    if stats['open_terminal_patches'] or stats['closed_15_point_maps']!=16:raise RuntimeError('Incomplete closed-map cover')
    trace={'cases':cases,'maps':maps,'controls':source_controls}
    encoded=serialized(trace)
    summary={'agent':'six-tammes-1','role':'researcher','status':'AUTHOR_CHECKED_FULL_CONDITIONAL_ROW_EXCLUSION',
      'profile':[0,6,0],'stats':dict(stats),'two_combinatorial_map_hashes':sorted(maps),
      'metric_excluded_map_hashes':sorted(maps),'remaining_single_three_profiles':[[1,5,0]],
      'beta_count_profiles_by_r':[1,12,11],
      'trace_sha256':hashlib.sha256(encoded).hexdigest(),'trace_bytes':len(encoded),'controls':source_controls,
      'scope':'Written geometric, role, renaming, strip, angle and N14 bridges are unformalized; separate same-author algorithmic audit; independent mathematical review pending. Full row exclusion under stated hypotheses; unrestricted Tammes-15 numerical bounds unchanged.'}
    return summary,trace

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--export-partitions',type=Path);args=parser.parse_args()
 summary,trace=run();expected=json.loads((s/'EXPECTED.json').read_text())
 if summary!=expected:raise RuntimeError('Whole recomputed summary differs from EXPECTED.json')
 if args.export_partitions:args.export_partitions.write_bytes(serialized(trace))
 print(serialized(summary).decode(),end='')
