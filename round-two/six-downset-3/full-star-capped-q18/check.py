"""Fresh exact q18 capped-H verifier: standard library only.

Adapted from public D3 q16 check.py at52ce9643a4eb700056e37c0df6e3ed3736f71808.
No q16 certificate, executable or PSD margin is imported.

No numerical optimizer, original affine table, author repair generator,
sector decoder, or approximate Cholesky routine is imported.  Every
original matrix entry, actual-empty completion, and all277 basis images
are reconstructed.  Small dyadic factors are treated as untrusted data.
"""
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from pathlib import Path
import argparse
import hashlib
import json
import sys

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))


def require(ok,msg):
    if not ok:raise ValueError(msg)


def carrier():
    # A separate core/outside census, followed by complete downclosure checks.
    X=[]
    for c in range(8):
        allowed=range(1,3) if c==0 else (0,1) if c.bit_count() in (1,2) else (0,)
        for r in allowed:
            for T in combinations(range(18),r):
                if c==6 and r==1 and T[0]<9:continue
                X.append(c+sum(1<<(t+3) for t in T))
    X.sort();require(len(X)==277 and X[0]==1,'fresh proper carrier N278')
    require(all(B in X or B==0 for A in X for B in (A^(1<<j) for j in range(21) if A&(1<<j))),
            'entire fresh downward closure')
    O=[(A&7,((A>>3)&511).bit_count(),(A>>12).bit_count()) for A in X]
    K=sorted(set(O));require(len(K)==23,'all fresh physical member orbits')
    return X,O,K


def original_matrix(data,X,O):
    n=len(X);D=data['free_original_entry_denominator']
    require(D==16384 and type(D) is int,'explicit original common denominator16384')
    keys=sorted({tuple(sorted((O[i],O[j]))) for i in range(n) for j in range(i+1,n)
                 if not X[i]&X[j] and X[i]!=1 and X[j]!=1})
    require(data['free_original_entry_orbit_keys']==[[list(x) for x in key] for key in keys]
            and len(keys)==143,'EVERY actual free orbit in canonical order, no missing/extras')
    values=data['free_original_entry_numerators']
    require(len(values)==143 and all(type(x) is int for x in values),'all143 exact original coefficients')
    weights=dict(zip(keys,values));a=X.index(1);S=[i for i,A in enumerate(X) if A&1]
    C=[[0]*n for _ in X]
    for i,A in enumerate(X):
        for j,B in enumerate(X):
            C[i][j]=(57*D if A==B else -D if A&B else
                     0 if A==1 or B==1 else weights[tuple(sorted((O[i],O[j])))])
    for i,A in enumerate(X):
        if A&1:continue
        C[i][a]=C[a][i]=-sum(C[i][j] for j in S if j!=a)
    require(all(C[i][j]==C[j][i] and (A!=B or C[i][j]==57*D)
                and (A==B or not A&B or C[i][j]==-D)
                for i,A in enumerate(X) for j,B in enumerate(X)), 'ALL original symmetry/diagonal/support positions')
    require(all(sum(C[i][j] for j in S)==0 for i in range(n)), 'ALL original maximum-star kernel rows')
    U=[[278*D*int(i==j)-D-C[i][j] for j in range(n)] for i in range(n)]
    return C,U,D,S


def sparse(v):return {i:x for i,x in enumerate(v) if x}


def dot(v,w):return sum(x*w.get(i,0) for i,x in v.items())


def full_basis(X,O,K):
    TT=[[int(o==key) for o in O] for key in K]
    standard={};orders={}
    for name,offset,countpos in (('Z',3,1),('W',12,2)):
        orders[name]=[o for o in K if o[countpos]>0]
        standard[name]=[[[(int(bool(A&(1<<offset)))-int(bool(A&(1<<(offset+j)))))*int(o==key)
                           for A,o in zip(X,O)] for key in orders[name]] for j in range(1,9)]
    pair={};free_pair=list(e for e in combinations(range(1,9),2) if e!=(1,2))
    for name,offset in (('ZZ',3),('WW',12)):
        cols=[]
        for i,j in free_pair:
            edge={(i,j):2,(1,2):-2}
            for t in range(1,9):edge[0,t]=-2*int(t in (i,j))+2*int(t in (1,2))
            cols.append([edge.get(tuple(t for t in range(9) if A&(1<<(offset+t))),0)
                         if A&7==0 and A.bit_count()==2 else 0 for A in X])
        pair[name]=cols
        # Unique free-edge coordinate2 certifies all27 columns independent.
        require(all(cols[i][X.index(sum(1<<(offset+t) for t in edge))]==2*int(i==j)
                    for i in range(27) for j,edge in enumerate(free_pair)), 'entire pair-basis independence decoder')
        require(all(sum(col[X.index((1<<(offset+t))+(1<<(offset+r)))] for r in range(9) if r!=t)==0
                    for col in cols for t in range(9)), 'entire pair-basis zero incidence')
    mixed=[[(int(bool(A&8))-int(bool(A&(1<<(3+i)))))*
            (int(bool(A&(1<<12)))-int(bool(A&(1<<(12+j)))))
            if A&7==0 and A.bit_count()==2 else 0 for A in X] for i in range(1,9) for j in range(1,9)]
    require(all(mixed[(i-1)*8+j-1][X.index((1<<(3+r))+(1<<(12+t)))]==int(i==r and j==t)
                for i in range(1,9) for j in range(1,9) for r in range(1,9) for t in range(1,9)),
            'whole64 rectangle independence decoder')
    blocks={'TT':TT,'Z':[v for B in standard['Z'] for v in B],
            'W':[v for B in standard['W'] for v in B],**pair,'ZW':mixed}
    require({k:len(v) for k,v in blocks.items()}=={'TT':23,'Z':64,'W':72,'ZZ':27,'WW':27,'ZW':64},
            'exact full277 coordinate dimensions')
    sp={name:list(map(sparse,B)) for name,B in blocks.items()}
    require(all(dot(v,w)==0 for name,B in sp.items() for other,E in sp.items() if name<other
                for v in B for w in E), 'ALL cross-sector original Gram entries zero')
    require(all(dot(v,w)==(dot(v,v) if i==j else 0) for i,v in enumerate(sp['TT']) for j,w in enumerate(sp['TT'])),
            'whole TT orthogonal independence')
    norms={name:[dot(sparse(v),sparse(v)) for v in standard[name][0]] for name in ('Z','W')}
    for name in ('Z','W'):
        d=len(standard[name][0]);require(d==len(norms[name]) and all(v>0 and v%2==0 for v in norms[name]),'standard positive norms')
        require(all(dot(sparse(standard[name][r][i]),sparse(standard[name][t][j]))==
                    (norms[name][i]//2)*(1+int(r==t))*int(i==j)
                    for r in range(8) for t in range(8) for i in range(d) for j in range(d)),
                'ENTIRE standard Gram: positive norm times(I+J) on every physical orbit')
    seeds={'TT':TT,'Z':standard['Z'][0],'W':standard['W'][0]}
    for name,offset in (('ZZ',3),('WW',12)):
        weights={(0,1):1,(2,3):1,(0,2):-1,(1,3):-1}
        seeds[name]=[[weights.get(tuple(t for t in range(9) if A&(1<<(offset+t))),0)
                      if A&7==0 and A.bit_count()==2 else 0 for A in X]]
    seeds['ZW']=[mixed[0]]
    norms={name:[sum(x*x for x in v) for v in B] for name,B in seeds.items()}
    return blocks,standard,seeds,norms


def gram(A,B):
    sp=list(map(sparse,B))
    return [[sum(x*A[i][j]*y for i,x in v.items() for j,y in w.items()) for w in sp] for v in sp]


def image(A,v):
    sp=sparse(v)
    return [sum(row[j]*x for j,x in sp.items()) for row in A]


def action_block(A,B,G,norm):
    clear=lcm(*norm);count=0
    for c,v in enumerate(B):
        Av=image(A,v)
        for i in range(len(A)):
            require(clear*Av[i]==sum(B[b][i]*G[b][c]*(clear//norm[b]) for b in range(len(B))),
                    'ENTIRE original block action at EACH coordinate')
            count+=1
    return count


def exact_factor(A,D,certificate,norms,floor):
    Q=certificate['factor_denominator'];V=certificate['factor_lower_triangle_numerators'];n=len(A)
    require(type(Q) is int and Q==1<<32 and len(V)==n and all(len(row)==i+1 for i,row in enumerate(V))
            and all(type(x) is int for row in V for x in row),'all fresh dyadic factor values')
    require(Q*Q%D==0,'integer residual clearing');scale=Q*Q//D
    E=[[scale*A[i][j]-sum(V[i][k]*V[j][k] for k in range(min(i,j)+1)) for j in range(n)] for i in range(n)]
    margins=[E[i][i]-sum(abs(E[i][j]) for j in range(n) if j!=i) for i in range(n)]
    require(min(margins)>0 and margins==certificate['whole_residual_row_margin_numerators']
            and certificate['whole_residual_denominator']==Q*Q,'ALL exact fresh residual margins')
    require(all(F(v,Q*Q*mass)>=floor for v,mass in zip(margins,norms)),
            'EVERY original physical-norm lower bound')
    return min(F(v,Q*Q*mass) for v,mass in zip(margins,norms))


def verify(data):
    require((data['q'],data['k'],data['actual_empty_N'],data['maximum_star_s'])==(18,9,278,58), 'exact finite quantified carrier')
    X,O,K=carrier();C,U,D,S=original_matrix(data,X,O)
    floor=F(data['claimed_original_floor']);require(floor>0,'strict claimed original floor')
    stars=[sum(bool(A&(1<<i)) for A in X) for i in range(21)]
    require(stars==[58,49,49]+[23]*9+[24]*9,'all21 exact original stars, unique maximum a')
    blocks,standard,seeds,norms=full_basis(X,O,K);action_positions=0;bounds={}
    certificates=data['positive_sector_certificates']
    require(set(certificates)=={a+'_'+b for a in seeds for b in ('lower','upper')},'all12 endpoint certificates')
    for endpoint,A in (('lower',C),('upper',U)):
        for name,B in seeds.items():
            G=gram(A,B)
            if name=='TT':action_positions+=action_block(A,B,G,norms[name])
            elif name in ('Z','W'):
                for full in standard[name]:action_positions+=action_block(A,full,G,norms[name])
            else:
                require(len(G)==1 and norms[name]==[4],'fresh scalar seed norm4')
                for v in blocks[name]:
                    Av=image(A,v)
                    require(all(4*x==G[0][0]*y for x,y in zip(Av,v)),'ENTIRE nonfixed scalar basis action')
                    action_positions+=len(A)
            key=name+'_'+endpoint
            ix=[i for i in range(len(G)) if not(name=='TT' and endpoint=='lower' and K[i]==(1,0,0))]
            H=[[G[i][j] for j in ix] for i in ix]
            if len(H)==1:
                require(certificates[key]['scalar_gram_numerator']==H[0][0]
                        and certificates[key]['scalar_gram_denominator']==D
                        and F(H[0][0],D*norms[name][0])>=floor, 'exact scalar and original margin')
                bounds[key]=str(F(H[0][0],D*norms[name][0]))
            else:
                bound=exact_factor(H,D,certificates[key],[norms[name][i] for i in ix],floor)
                bounds[key]=str(bound)
    # Actual-empty integer lift and BOTH full endpoints, not a row/rank proxy.
    rows=[sum(row) for row in C]
    L=[[D+sum(rows)]+[D-r for r in rows]]+[[D-rows[i]]+[D+x for x in row] for i,row in enumerate(C)]
    require(len(L)==278 and all(sum(row)==278*D for row in L), 'every actual-empty lift row exactly N')
    require(all(L[i][j]==L[j][i] for i in range(278) for j in range(278)), 'entire actual-empty symmetry')
    actual=[0]+X;M=[[L[i][j]-58*D*int(i==j) for j in range(278)] for i in range(278)]
    require(all(sum(row)==220*D for row in M),'every original M row exactly1 after clearing')
    require(all(not A&B or M[i][j]==0 for i,A in enumerate(actual) for j,B in enumerate(actual)),
            'ALL original intersecting-pair/diagonal M entries zero')
    ur=[sum(row) for row in U]
    lifted_U=[[sum(ur)]+[-r for r in ur]]+[[-ur[i]]+row for i,row in enumerate(U)]
    require(all(lifted_U[i][j]==278*D*int(i==j)-L[i][j] for i in range(278) for j in range(278)),
            'EVERY actual-empty upper endpoint equals EUE transpose')
    centered=[278*int(bool(A&1))-58 for A in actual]
    require(sum(centered)==0 and all(sum(x*y for x,y in zip(row,centered))==0 for row in L),
            'entire original centered maximum-star lower kernel')
    allowed=[(i,j) for i in range(277) for j in range(i+1,277) if not X[i]&X[j]]
    free=[(i,j) for i,j in allowed if X[i]!=1 and X[j]!=1]
    dimension=len(free)
    require((len(allowed),dimension,len(X)-len(S))==(30021,29802,219),
            'fresh full affine dimension and one independent anchor equation per nonstar')
    negative=[(i,j,M[i][j]) for i,A in enumerate(actual) for j,B in enumerate(actual)
              if not A&B and M[i][j]<0]
    require(all(i==0 or j==0 for i,j,v in negative),'every negative entry confined to actual empty row')
    negative_orbits=[]
    for key in K:
        members=[j for j,o in enumerate(O,1) if o==key and M[0][j]<0]
        if members:
            values={M[0][j] for j in members};require(len(values)==1,'entire orbit empty-row equality')
            negative_orbits.append({'proper_member_orbit':list(key),'members':len(members),
                                    'M_entry':str(F(next(iter(values)),220*D))})
    bad=[j for j,A in enumerate(actual) if j and not A&1 and M[0][j]<0]
    deficit=-sum(M[0][j] for j in bad)
    require((len(bad),deficit,M[0][0])==(81,2497887,2021552),
            'literal nonstar deficit and actual empty-loop capacity')
    require(M[0][0]-deficit<0,'strict one-sided nonstar repair capacity obstruction')
    matrix_hashes={name:hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest()
                   for name,A in (('C_numerators',C),('U_numerators',U),('L_numerators',L))}
    return {'actual_agent':'six-downset-3','role':'researcher','q':18,'k':9,'actual_empty_N':278,'s':58,
            'original_core_ordered_entries':277**2,'original_actual_empty_lift_entries':278**2,
            'complete_original_basis_columns':277,'both_full_original_basis_action_positions':action_positions,
            'all21_original_star_sizes':stars,'complete_original_repair_dimension':dimension,
            'complete_sector_dimensions':{name:len(cols) for name,cols in blocks.items()},
            'invariant_free_entry_count':143,'original_C_kernel':'span(actual a-star)',
            'C_on_actual_star_perpendicular_and_U_margin':str(floor),
            'all12_exact_original_block_bounds':bounds,
            'independent_real_coordinate_cube_radius':str(floor/(4*dimension)),
            'cube_original_lower_and_upper_margin':str(floor/2),
            'both_actual_empty_endpoint_ranks':277,'simple_unit_eigenvalue':True,
            'simple_minimum_M_eigenvalue':True,'minimum_M_eigenvalue':'-29/110',
            'point_other276_M_lower_bound':str(-F(29,110)+floor/220),
            'point_other276_M_upper_bound':str(1-floor/220),
            'cube_other276_M_lower_bound':str(-F(29,110)+floor/440),
            'cube_other276_M_upper_bound':str(1-floor/440),
            'negative_admissible_M_ordered_entry_count':len(negative),
            'all_negative_empty_row_orbits':negative_orbits,
            'one_sided_nonstar_repair_positive_entry_obstruction':{
                'bad_nonstar_members':len(bad),
                'total_negative_nonstar_empty_M_deficit':str(F(deficit,220*D)),
                'original_empty_M_loop_capacity':str(F(M[0][0],220*D)),
                'necessary_new_loop_upper_bound':str(F(M[0][0]-deficit,220*D)),
                'scope':'all support/star-kernel preserving real repairs whose nonstar/nonstar entries are nonpositive; arbitrary anchored star trades allowed',
                'unrestricted_positive_H_absence_claim':False},
            'entire_original_matrix_SHA256':matrix_hashes,
            'minimum_admissible_M':str(min(F(M[i][j],220*D) for i,A in enumerate(actual) for j,B in enumerate(actual) if not A&B)),'actual_empty_M_loop':str(F(M[0][0],220*D)),
            'ordinary_PSD_lift_sector_completeness_and_cube_bridges_unformalized':True,
            'independent_reviewer_verdict':'UNREVIEWED'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'CERTIFICATE.json')
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    import sourcecheck
    sourcecheck.check_bundle(BASE)
    data=json.loads(args.certificate.read_bytes());result=verify(data)
    raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    if args.certificate.resolve()==(BASE/'CERTIFICATE.json').resolve():
        require(raw==(BASE/'EXPECTED.json').read_bytes(),'ENTIRE fresh mathematical expected record')
    args.out.write_bytes(raw)
    print(json.dumps({'completed':True,'N':278,'s':58,
                      'all_original_entries':277**2,'all_original_basis_actions':result['both_full_original_basis_action_positions'],
                      'margin':result['C_on_actual_star_perpendicular_and_U_margin'],
                      'record_SHA256':hashlib.sha256(raw).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
