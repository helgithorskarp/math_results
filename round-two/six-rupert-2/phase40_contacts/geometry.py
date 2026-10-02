"""Fresh exact receiving/contact data on the original closed phase40 cell.

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
POSES=[I,H,A,mm(A,H),B,mm(B,H)];NAMES=['I','H','A','AH','B','BH']
CYCLE=[16,0,36,28,10,11,47,55,27,7,43,31,13,12,48,40,20]
EDGES=list(zip(CYCLE,CYCLE[1:]+CYCLE[:1]))
PENT=[((5-S)/6,(5*S-7)/6),((1+3*S)/22,(21-3*S)/22),
      (Q(F(1,2)),Q(F(1,2))),((S-1)/2,Q(F(1,2))),((S-1)/2,(9*S-19)/2)]
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
    start=time.monotonic();original,caps,gyrated,built,axes=model.cupola_construction()
    require(len(V)==len(set(V))==60 and built==set(V),'original named two-cupola J74 identification')
    require({act(H,v) for v in V}==set(V) and {act(MX,v) for v in V}==set(V),'actual full-body H/Mx permutations')
    R2=(11+4*S)/4;require(all(a.dot(v,v)==R2 for v in V),'original common body radius')
    require(all(a.add(V[i],V[j])==Z for i,j in ((0,7),(1,6),(2,5))) and a.dot(V[0],a.cross(V[1],V[2]))!=0,'literal independent antipodal pairs imply original body origin interior')
    half=constraints();poly=polygon(half);require(poly==PENT,'entire closed five-corner phase40 polygon from every original support')
    heights=[];gaps=[];ratio=[];boundaryties=[];centroid=tuple(sum((p[k] for p in poly),Q())/5 for k in range(2))
    for pi,p in enumerate(poly):
        for i,j in EDGES:
            m,h=support(i,j,raw(p));require(h>0,'strict corner support height including entire closure');heights.append(h);ratio.append(R2*a.dot(m,m)/(h*h))
            require(ratio[-1]<Q(F(121,100)),'fresh whole-phase40 normalized corner bound for C21/20')
            for k,v in enumerate(V):
                gap=h-a.dot(m,v);require(gap>=0,'every literal original corner support');gaps.append(gap)
                if gap==0 and k not in (i,j):boundaryties.append([pi,i,j,k])
    for i,j in EDGES:
        m,h=support(i,j,raw(centroid))
        require(all(h-a.dot(m,V[k])>0 for k in range(60) if k not in (i,j)),'exact true17-corner phase interior')
    sides=[]
    for v,u in zip(poly,poly[1:]+poly[:1]):
        active=[w for w in half if value(w,v)==value(w,u)==0];require(active,'every polygon side has actual defining original support')
        sides.append({'line':vec(active[0]),'original_rows':half[active[0]]})
    images=[];preimages=[];parents=[]
    A_REGION=[PENT[0],PENT[1],((3-S)/2,(S-1)/2),((S-1)/2,(1+S)/6),PENT[4]]
    cut=(Q(-1),S/5,3*S/5)
    require(polygon([cut],PENT.copy())==A_REGION,'one exact extra halfspace gives the entire closed A/AH subpolygon')
    for name,g in zip(NAMES,POSES):
        proper(g);im=tuple(act(g,v) for v in V);images.append(im)
        pre=[next((k for k,v in enumerate(im) if v==V[i]),None) for i in CYCLE];preimages.append(pre)
        require(all(k is not None for k in pre),'literal original spatial preimages everywhere, including nonfitting parents')
        rawgaps=[h-a.dot(m,v) for p in poly for i,j in EDGES for m,h in [support(i,j,raw(p))] for v in im]
        parenthalf=constraints(im);allowed=polygon(parenthalf,poly.copy())
        require(allowed==(A_REGION if name in ('A','AH') else PENT),'complete finite-parent support-region classification')
        if name in ('A','AH'):
            k=24 if name=='A' else 26
            require(normalize(line(55,27,im[k]))==cut,'literal original transformed source witness for extra A/AH cut')
        parents.append({'name':name,'complete_corner_support_comparisons':len(rawgaps),'minimum_corner_gap':enc(min(rawgaps)),
            'fits_entire_cell':min(rawgaps)>=0,'constant_original_corner_preimages':pre,
            'unit_scale_T0_fit_region':list(map(vec,allowed)),'fit_region_double_area':enc(area(allowed)),
            'all_receiving_corners_have_spatial_preimages':all(x is not None for x in pre),
            'complete_corner_gap_stream_sha256':digest(list(map(enc,rawgaps)))})
    seam=[PENT[0],PENT[4]]
    tri=[((S-1)/2,3-S),PENT[0],PENT[4]]
    w=a.cross(a.sub(V[56],V[40]),a.sub(V[20],V[40]));wall=(w[1],w[0],-w[2]);wall=normalize(wall)
    require(wall is not None and all(value(wall,p)==0 for p in seam),'full genuine phase56/40 seam endpoints')
    p40=[value(wall,p) for p in PENT];p56=[value(wall,p) for p in tri]
    require((all(x>=0 for x in p40) and all(x<=0 for x in p56)) or (all(x<=0 for x in p40) and all(x>=0 for x in p56)),'actual opposite closed receiving cells')
    witness=(Q(F(1,2)),Q(F(1,2)));m,h=support(55,27,raw(witness))
    wa=h-a.dot(m,images[2][24]);wah=h-a.dot(m,images[3][26]);require(wa==wah==Q(F(-1,2),F(1,5)) and wa<0,'literal A/AH failure retained')
    return {'agent':'six-rupert-2','role':'researcher','scope':'entire closed original phase40 receiving geometry and FINITE six-parent unit-scale/T0 support regions only; no arbitrary-source/collar theorem',
       'whole_closed_pentagon':list(map(vec,PENT)),'original_cycle':CYCLE,'unique_actual_support_halfspaces':len(half),
       'original_corner_support_comparisons':len(gaps),'strict_support_heights':len(heights),'minimum_corner_height':enc(min(heights)),
       'maximum_corner_R2_normal_squared':enc(max(ratio)),'all85_fresh_C21_20_corner_bounds':True,'entire_polygon_double_area':enc(area(PENT)),
       'actual_side_rows':sides,'retained_offendpoint_boundary_ties':boundaryties,'literal_centroid_offendpoint_strict_checks':17*58,
       'complete_original_support_stream_sha256':digest(list(map(enc,gaps))),'parent_motions':parents,
       'full_original_phase56_seam':list(map(vec,seam)),'seam_line':vec(wall),'literal_A_AH_failure_gap':enc(wa),'exact_A_AH_extra_support_cut':vec(cut),
       'global_J74_Rupert_status':'OPEN','all_source_classification':False,'wall_seconds':time.monotonic()-start}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args();r=record()
    if args.output:Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
