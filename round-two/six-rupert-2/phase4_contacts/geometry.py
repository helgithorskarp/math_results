"""Fresh exact receiving/contact data on the original closed phase4 triangle.
Small ordered-field/matrix/clipping routines adapted with attribution from phase40_contacts.

No arbitrary-source classification follows from this geometric layer.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json,sys,time
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
PINS={'model.py':'cc0ce4358eea0139da13962b6abdf25a9710fb934e8e41ee3e6f3cbe3acb8cd7',
      'q5.py':'cef1fe01c185fc5c63d729d8e27588b4efe56d8487c87a73f22a68297b18ed3c'}
for name,pin in PINS.items():
    if hashlib.sha256((BASE/name).read_bytes()).hexdigest()!=pin:raise ValueError('before-import original source pin: '+name)
sys.path.insert(0,str(BASE));import q5 as a
Q=a.Q
spec=importlib.util.spec_from_file_location('original_J74_phase40_model',BASE/'model.py');model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
V=model.VERTICES;Z=(Q(),)*3;I=tuple(tuple(Q(int(i==j)) for j in range(3)) for i in range(3))
def require(ok,msg):
    if not ok:raise ValueError(msg)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def enc(x):return [str(x.a),str(x.b)]
def vec(v):return [enc(x) for x in v]
def act(A,v):return tuple(a.dot(row,v) for row in A)
def transpose(A):return tuple(zip(*A))
def mm(A,B):return tuple(tuple(a.dot(row,col) for col in zip(*B)) for row in A)
def proper(A):require(mm(A,transpose(A))==I and a.dot(A[0],a.cross(A[1],A[2]))==1,'actual proper source motion')
S=Q(0,1);aa=(S-1)/4;bb=(S+1)/4;cc=Q(F(1,2))
H=((Q(-1),Q(),Q()),(Q(),Q(-1),Q()),(Q(),Q(),Q(1)))
MX=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
A=((bb,aa,cc),(-aa,-cc,bb),(cc,-bb,-aa));B=((-aa,-cc,-bb),(cc,-bb,aa),(-bb,-aa,cc))
G=((aa,-cc,-bb),(-cc,-bb,aa),(-bb,aa,-cc))
POSES=[I,H,A,mm(A,H),B,mm(B,H),G,mm(G,H),mm(H,B),mm(mm(H,B),H)];NAMES=['I','H','A','AH','B','BH','G','GH','HB','HBH']
CYCLE=[4,0,36,28,10,11,47,55,27,7,43,31,13,12,48,40,20]
EDGES=list(zip(CYCLE,CYCLE[1:]+CYCLE[:1]))
PENT=[(Q(F(1,2)),Q(F(1,2))),((S-1)/2,(3-S)/2),((S-1)/2,Q(F(1,2)))]
def raw(p):return (p[0],Q(1),-p[1])
def line(i,j,v):
    w=a.cross(a.sub(V[i],v),a.sub(V[j],V[i]));return (w[1],w[0],-w[2])
def value(w,p):return w[0]+w[1]*p[0]+w[2]*p[1]
def normalize(w):
    t=next((x for x in w if x!=0),None)
    if t is None:return None
    return tuple(x/(t if t>0 else -t) for x in w)
def clip(poly,w):
    out=[]
    for v,u in zip(poly,poly[1:]+poly[:1]):
        fv,fu=value(w,v),value(w,u)
        if fv>=0:out.append(v)
        if fv<0<fu or fu<0<fv:
            t=fv/(fv-fu);out.append(tuple(x+t*(y-x) for x,y in zip(v,u)))
    result=[]
    for v in out:
        if not result or v!=result[-1]:result.append(v)
    if len(result)>1 and result[0]==result[-1]:result.pop()
    return result
def support(i,j,r):
    m=a.cross(a.sub(V[j],V[i]),r);return m,a.dot(m,V[i])
def constraints(images=V):
    out={}
    for i,j in EDGES:
        for k,v in enumerate(images):
            w=normalize(line(i,j,v))
            if w is not None:out.setdefault(w,[]).append([i,j,k])
    return out
def polygon(halfspaces,start=None):
    poly=start if start is not None else [(Q(-1),Q(-1)),(Q(1),Q(-1)),(Q(1),Q(1)),(Q(-1),Q(1))]
    for w in halfspaces:poly=clip(poly,w)
    return poly
def area(poly):
    d=sum((v[0]*u[1]-v[1]*u[0] for v,u in zip(poly,poly[1:]+poly[:1])),Q())
    return d if d>=0 else -d

def record():
    start=time.monotonic()
    original,caps,gyrated,built,axes=model.cupola_construction()
    require(len(V)==len(set(V))==60 and built==set(V),'original named two-nonopposite-cupola J74 identification')
    require({act(H,v) for v in V}==set(V) and {act(MX,v) for v in V}==set(V),'actual full-body H/Mx permutations')
    R2=(11+4*S)/4
    require(all(a.dot(v,v)==R2 for v in V),'original common body radius')
    require(all(a.add(V[i],V[j])==Z for i,j in ((0,7),(1,6),(2,5))) and a.dot(V[0],a.cross(V[1],V[2]))!=0,'original origin interior without body centrality')
    half=constraints();poly=polygon(half)
    require(PENT[0] in poly,'literal first whole-triangle corner')
    first=poly.index(PENT[0]);poly=poly[first:]+poly[:first]
    require(poly==PENT,'entire closed three-corner phase4 from every original support')
    require(area(poly)==Q(F(9,4),-1)>0,'literal nondegenerate triangle double area')
    gaps=[];heights=[];ratios=[];ties=[]
    for pi,point in enumerate(poly):
        for i,j in EDGES:
            m,h=support(i,j,raw(point));require(h>0,'every closed original support height')
            heights.append(h);ratios.append(R2*a.dot(m,m)/(h*h))
            require(ratios[-1]<Q(F(121,100)),'fresh C21/20 nonlinear normal bound')
            for k,v in enumerate(V):
                gap=h-a.dot(m,v);require(gap>=0,'every original closed-corner support gap');gaps.append(gap)
                if gap==0 and k not in (i,j):ties.append([pi,i,j,k])
    center=tuple(sum((v[k] for v in poly),Q())/3 for k in range(2))
    for i,j in EDGES:
        m,h=support(i,j,raw(center))
        require(all(h-a.dot(m,V[k])>0 for k in range(60) if k not in (i,j)),'actual strict seventeen-corner interior')
    sides=[]
    for v,u in zip(poly,poly[1:]+poly[:1]):
        active=[w for w in half if value(w,v)==value(w,u)==0]
        require(active,'no artificial clipping-square side enters whole triangle')
        sides.append({'ends':list(map(vec,[v,u])),'line':vec(active[0]),'original_rows':half[active[0]]})
    parents=[]
    for name,g in zip(NAMES,POSES):
        proper(g);im=tuple(act(g,v) for v in V)
        pre=[next((k for k,v in enumerate(im) if v==V[i]),None) for i in CYCLE]
        missing=[CYCLE[i] for i,k in enumerate(pre) if k is None]
        require(missing==([20] if name in ('G','GH','HB','HBH') else []),'literal spatial preimages, including the new genuine missing20')
        require(all(pre[CYCLE.index(i)] is not None or pre[CYCLE.index(j)] is not None for i,j in EDGES),'at least one persistent original spatial preimage on EVERY support edge')
        rawgaps=[h-a.dot(m,v) for point in poly for i,j in EDGES for m,h in [support(i,j,raw(point))] for v in im]
        allowed=polygon(constraints(im),poly.copy())
        expected=[] if name in ('A','AH') else [PENT[1]] if name in ('G','GH','HB','HBH') else PENT
        require(allowed==expected,'complete ten finite-parent fit regions on whole closure')
        witness=None
        if name in ('A','AH'):
            k=24 if name=='A' else 26
            require(normalize(line(55,27,im[k]))==(Q(-1),S/5,3*S/5),'actual physical parent exclusion row')
            w=[h-a.dot(m,im[k]) for point in poly for m,h in [support(55,27,raw(point))]]
            require(max(w)<0,'single affine A/AH row strictly excludes entire closed triangle')
            witness={'edge':[55,27],'original_source':k,'closed_corner_gaps':list(map(enc,w)),'maximum_gap':enc(max(w))}
        elif name in ('G','GH','HB','HBH'):
            k={'G':15,'GH':9,'HB':12,'HBH':10}[name]
            w=[h-a.dot(m,im[k]) for point in poly for m,h in [support(4,0,raw(point))]]
            require(w[1]==0 and w[0]==w[2]==Q(F(-3,8),F(1,8))<0,'literal single support excludes the entire triangle except the true corner')
            witness={'edge':[4,0],'original_source':k,'closed_corner_gaps':list(map(enc,w)),'only_feasible_corner':1}
        parents.append({'name':name,'complete_corner_support_comparisons':len(rawgaps),'minimum_corner_gap':enc(min(rawgaps)),'fits_entire_cell':min(rawgaps)>=0,'constant_original_corner_preimages':pre,'unit_scale_T0_fit_region':list(map(vec,allowed)),'strict_exclusion_witness':witness,'full_corner_gap_stream_sha256':digest(list(map(enc,rawgaps)))})
    upper_side=[PENT[2],PENT[0]]
    require(all(p[1]==Q(F(1,2)) for p in upper_side),'entire original phase4/40 seam')
    require(all(p[1]<=Q(F(1,2)) for p in poly),'new closed cell on opposite lower side')
    return {'agent':'six-rupert-2','role':'researcher','scope':'entire closed original phase4 receiving geometry and TEN finite parent unit-scale/T0 fits ONLY','whole_closed_triangle':list(map(vec,PENT)),'original_cycle':CYCLE,'unique_actual_support_halfspaces':len(half),'entire_triangle_double_area':enc(area(poly)),'actual_side_rows':sides,'original_corner_support_comparisons':len(gaps),'minimum_corner_height':enc(min(heights)),'maximum_corner_R2_normal_squared':enc(max(ratios)),'fresh_C21_20_corner_bounds':len(ratios),'retained_offendpoint_boundary_ties':ties,'literal_centroid_offendpoint_strict_checks':17*58,'full_original_support_stream_sha256':digest(list(map(enc,gaps))),'parent_motions':parents,'full_phase4_40_seam':list(map(vec,upper_side)),'all_source_classification':False,'global_J74_status':'OPEN','wall_seconds':time.monotonic()-start}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    r=record();Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('parent_motions','retained_offendpoint_boundary_ties','actual_side_rows')},indent=2))
