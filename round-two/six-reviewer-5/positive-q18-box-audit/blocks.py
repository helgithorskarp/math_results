"""Independent original-coordinate basis, full actions, and exact PSD residual reader."""
from fractions import Fraction as F
from itertools import combinations
from geometry import need,integer,typ,canon
import hashlib


def dot(x,y):return sum(v*y.get(i,0) for i,v in x.items())


def action(M,x):return [sum(row[i]*v for i,v in x.items()) for row in M]


def sparse(v):return {i:x for i,x in enumerate(v) if x}


def frame(D):
    proper=D[1:];lookup={A:i for i,A in enumerate(proper)};types=sorted({typ(A) for A in proper});groups={t:[i for i,A in enumerate(proper) if typ(A)==t] for t in types};n=277
    B=[];labels=[];blocks={}
    def save(v,label):need(v and all(type(i) is int and type(x) is int for i,x in v.items()),'exact basis vector');B.append(v);labels.append(label)
    tt=[{i:1 for i in groups[t]} for t in types];blocks['TT']=tt
    for i,v in enumerate(tt):save(v,('TT',i,0))
    for sector,offset,component in (('Z',3,1),('W',12,2)):
        selected=[t for t in types if t[component]];need(len(selected)==(8 if sector=='Z' else 9),'all standard types');prototypes=[]
        for t in selected:
            v={i:int(bool(proper[i]>>offset&1))-int(bool(proper[i]>>(offset+1)&1)) for i in groups[t]};v={i:x for i,x in v.items() if x};prototypes.append(v)
        blocks[sector]=prototypes
        for copy in range(1,9):
            for i,t in enumerate(selected):
                v={r:int(bool(proper[r]>>offset&1))-int(bool(proper[r]>>(offset+copy)&1)) for r in groups[t]};save({r:x for r,x in v.items() if x},(sector,i,copy))
    def pair_vector(offset,edges):
        out={}
        for (i,j),x in edges.items():
            if x:out[lookup[(1<<(offset+i))|(1<<(offset+j))]]=x
        return out
    for sector,offset in (('ZZ',3),('WW',12)):
        proto=pair_vector(offset,{(0,2):1,(0,3):-1,(1,2):-1,(1,3):1});need(dot(proto,proto)==4,'own scalar prototype norm');blocks[sector]=[proto]
        free=[(i,j) for i,j in combinations(range(1,9),2) if (i,j)!=(1,2)];need(len(free)==27,'all pair free pivots')
        for index,(i,j) in enumerate(free):
            edges={(i,j):2,(1,2):-2}
            for t in range(1,9):edges[0,t]=-2*int(t in (i,j))+2*int(t in (1,2))
            v=pair_vector(offset,edges)
            need(all(sum(x for (i,j),x in edges.items() if t in (i,j))==0 for t in range(9)),'every pair incidence')
            need(all(v.get(lookup[(1<<(offset+k))|(1<<(offset+l))],0)==(2 if (k,l)==(i,j) else 0) for k,l in free),'complete independent pair decoder')
            save(v,(sector,index,0))
    def rectangle(i,j):return {lookup[(1<<(3+z))|(1<<(12+w))]:s for z,w,s in ((0,0,1),(0,j,-1),(i,0,-1),(i,j,1))}
    blocks['ZW']=[rectangle(1,1)];need(dot(blocks['ZW'][0],blocks['ZW'][0])==4,'mixed prototype norm')
    for i in range(1,9):
        for j in range(1,9):
            v=rectangle(i,j)
            need(all(v.get(lookup[(1<<(3+k))|(1<<(12+l))],0)==int((k,l)==(i,j)) for k in range(1,9) for l in range(1,9)),'all rectangle independence pivots')
            save(v,('ZW',(i,j),0))
    need(len(B)==277,'all original proper directions')
    # All Gram positions: cross-sector orthogonality and actual standard-copy metric.
    for i,x in enumerate(B):
        si,ti,ci=labels[i]
        for j,y in enumerate(B):
            sj,tj,cj=labels[j];g=dot(x,y)
            if si!=sj:need(g==0,'whole cross-sector orthogonality')
            elif si=='TT':need(g==(len(groups[types[ti]]) if i==j else 0),'whole orbit physical norm')
            elif si in ('Z','W'):
                norm=dot(blocks[si][ti],blocks[si][ti]);need(norm>0 and norm%2==0,'standard norm multiplier')
                need(g==(norm if ci==cj else norm//2) if ti==tj else g==0,'all standard copies physical Gram')
    return B,labels,blocks,types,groups


def factor_check(G,masses,data,label,damage):
    n=len(G);Q=integer(data['factor_denominator'],'factor denominator');need(Q==2**32,'dyadic factor denominator')
    V=data['factor_lower_triangle_numerators'];need(type(V) is list and len(V)==n and all(type(r) is list and len(r)==i+1 for i,r in enumerate(V)),'complete triangular factor')
    V=[[integer(x,'factor integer') for x in r] for r in V]
    if damage=='factor' and label=='TT_lower':V[0][0]+=2**40
    scale=Q*Q//1048576;need(scale*1048576==Q*Q,'exact residual clearing')
    R=[[G[i][j]*scale-sum(V[i][k]*V[j][k] for k in range(min(i,j)+1)) for j in range(n)] for i in range(n)]
    need(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'every residual symmetric entry')
    margins=[R[i][i]-sum(abs(R[i][j]) for j in range(n) if j!=i) for i in range(n)]
    for i,m in enumerate(margins):need(m>0 and 32*m>=masses[i]*Q*Q,'each exact original physical floor')
    need(integer(data['whole_residual_denominator'],'residual denominator')==Q*Q,'whole residual denominator')
    claimed=data['whole_residual_row_margin_numerators'];need(type(claimed) is list and [integer(x,'residual margin integer') for x in claimed]==margins,'whole supplied residual margins after independent computation')
    return dict(gram_numerators=G,gram_denominator=1048576,physical_norms=masses,residual_denominator=Q*Q,whole_residual_margins=margins,minimum_physical_floor=str(min(F(v,masses[i]*Q*Q) for i,v in enumerate(margins))),whole_residual_sha256=hashlib.sha256(canon(R)).hexdigest())


def inspect(D,C,U,cert,damage='none'):
    B,labels,proto,types,groups=frame(D);pc=cert['positive_sector_certificates'];need(type(pc) is dict and set(pc)=={s+'_'+e for s in ('TT','Z','W','ZZ','WW','ZW') for e in ('lower','upper')},'all twelve certificate blocks')
    models={};grams={};out={};a_type=types.index((1,0,0))
    for endpoint,M in (('lower',C),('upper',U)):
        for sector,vs in proto.items():
            imgs=[action(M,x) for x in vs];G=[[sum(v*imgs[j][i] for i,v in x.items()) for j in range(len(vs))] for x in vs]
            need(all(G[i][j]==G[j][i] for i in range(len(vs)) for j in range(len(vs))),'entire prototype energy symmetry')
            norms=[dot(x,x) for x in vs]
            if sector in ('TT','Z','W'):
                coeff=[]
                for img in imgs:
                    col=[]
                    for v in vs:
                        i=next(i for i,x in v.items() if x>0);need(v[i]==1,'prototype positive unit decoder');col.append(img[i])
                    expected=[sum(col[k]*v.get(i,0) for k,v in enumerate(vs)) for i in range(277)]
                    need(img==expected,'every original prototype image')
                    coeff.append(col)
                models[endpoint,sector]=coeff
            else:
                norm=dot(vs[0],vs[0]);need(norm==4,'scalar prototype norm')
                need(all(norm*imgs[0][i]==G[0][0]*vs[0].get(i,0) for i in range(277)),'all original scalar prototype image')
                models[endpoint,sector]=F(G[0][0],norm)
            label=sector+'_'+endpoint;data=pc[label]
            if sector in ('ZZ','WW','ZW'):
                need(integer(data['scalar_gram_denominator'],'scalar denominator')==1048576 and integer(data['scalar_gram_numerator'],'scalar numerator')==G[0][0],'fresh entire scalar Gram')
                need(G[0][0]>0 and 32*G[0][0]>=4*1048576,'each original scalar floor');out[label]=dict(gram_numerators=G,gram_denominator=1048576,physical_norms=norms,minimum_physical_floor=str(F(G[0][0],4*1048576)))
            else:
                if label=='TT_lower':
                    keep=[i for i in range(23) if i!=a_type];G=[[G[i][j] for j in keep] for i in keep];norms=[norms[i] for i in keep]
                out[label]=factor_check(G,norms,data,label,damage)
        # Every original coordinate of all277 basis directions, not just prototypes.
        for v,(sector,t,copy) in zip(B,labels):
            image=action(M,v)
            if sector in ('TT','Z','W'):
                col=models[endpoint,sector][t]
                if sector=='TT':basis=proto[sector]
                else:
                    selected=[b for b,l in zip(B,labels) if l[0]==sector and l[2]==copy];need(len(selected)==len(col),'whole standard copy census');basis=selected
                expected=[sum(col[k]*b.get(i,0) for k,b in enumerate(basis)) for i in range(277)]
                if damage=='action' and endpoint=='lower' and sector=='ZW':expected[0]+=1
                need(image==expected,'every original full basis action')
            else:
                scalar=models[endpoint,sector]
                expected=[scalar*v.get(i,0) for i in range(277)]
                if damage=='action' and endpoint=='lower' and sector=='ZW':expected[0]+=1
                need(image==expected,'every original scalar full basis action')
    return dict(blocks=out,orbit_types=[list(t) for t in types],orbit_masses=[len(groups[t]) for t in types],all277_original_basis_directions=True,all153458_original_endpoint_action_positions=True,all76729_original_frame_Gram_positions=True,sector_dimensions=dict(TT=23,Z=64,W=72,ZZ=27,WW=27,ZW=64),deleted_lower_TT_anchor_type=list(types[a_type]))
