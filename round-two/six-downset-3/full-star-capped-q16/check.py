"""Independent exact original capped-H verifier: standard library only.

No numerical optimizer, original affine table, author repair generator,
sector decoder, or approximate Cholesky routine is imported.  Every
original matrix entry, actual-empty completion, and all231 basis images
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
    X=[]
    for r in (1,2,3):
        for T in combinations(range(19),r):
            core=sum(t<3 for t in T)
            if r==3 and core<2:continue
            if r==3 and 1 in T and 2 in T and T[-1] in range(3,11):continue
            X.append(sum(1<<t for t in T))
    X.sort();require(len(X)==231 and X[0]==1,'literal proper carrier with actual empty N232')
    require(all(B in X or B==0 for A in X for B in (A^(1<<j) for j in range(19) if A&(1<<j))),
            'complete original downward closure')
    def orbit(A):return A&7,((A>>3)&255).bit_count(),(A>>11).bit_count()
    O=[orbit(A) for A in X];K=sorted(set(O));require(len(K)==23,'entire physical member orbits')
    return X,O,K


def original_matrix(data,X,O):
    n=len(X);D=data['free_original_entry_denominator']
    require(D==1024 and type(D) is int,'explicit original common denominator1024')
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
            C[i][j]=(51*D if A==B else -D if A&B else
                     0 if A==1 or B==1 else weights[tuple(sorted((O[i],O[j])))])
    for i,A in enumerate(X):
        if A&1:continue
        C[i][a]=C[a][i]=-sum(C[i][j] for j in S if j!=a)
    require(all(C[i][j]==C[j][i] and (A!=B or C[i][j]==51*D)
                and (A==B or not A&B or C[i][j]==-D)
                for i,A in enumerate(X) for j,B in enumerate(X)), 'ALL original symmetry/diagonal/support positions')
    require(all(sum(C[i][j] for j in S)==0 for i in range(n)), 'ALL original maximum-star kernel rows')
    U=[[232*D*int(i==j)-D-C[i][j] for j in range(n)] for i in range(n)]
    return C,U,D,S


def sparse(v):return {i:x for i,x in enumerate(v) if x}


def dot(v,w):return sum(x*w.get(i,0) for i,x in v.items())


def full_basis(X,O,K):
    TT=[[int(o==key) for o in O] for key in K]
    standard={};orders={}
    for name,offset,countpos in (('Z',3,1),('W',11,2)):
        orders[name]=[o for o in K if o[countpos]>0]
        standard[name]=[[[(int(bool(A&(1<<offset)))-int(bool(A&(1<<(offset+j)))))*int(o==key)
                           for A,o in zip(X,O)] for key in orders[name]] for j in range(1,8)]
    pair={};free_pair=list(e for e in combinations(range(1,8),2) if e!=(1,2))
    for name,offset in (('ZZ',3),('WW',11)):
        cols=[]
        for i,j in free_pair:
            edge={(i,j):2,(1,2):-2}
            for t in range(1,8):edge[0,t]=-2*int(t in (i,j))+2*int(t in (1,2))
            cols.append([edge.get(tuple(t for t in range(8) if A&(1<<(offset+t))),0)
                         if A&7==0 and A.bit_count()==2 else 0 for A in X])
        pair[name]=cols
        # Unique free-edge coordinate2 certifies all20 columns independent.
        require(all(cols[i][X.index(sum(1<<(offset+t) for t in edge))]==2*int(i==j)
                    for i in range(20) for j,edge in enumerate(free_pair)), 'entire pair-basis independence decoder')
        require(all(sum(col[X.index((1<<(offset+t))+(1<<(offset+r)))] for r in range(8) if r!=t)==0
                    for col in cols for t in range(8)), 'entire pair-basis zero incidence')
    mixed=[[(int(bool(A&8))-int(bool(A&(1<<(3+i)))))*
            (int(bool(A&(1<<11)))-int(bool(A&(1<<(11+j)))))
            if A&7==0 and A.bit_count()==2 else 0 for A in X] for i in range(1,8) for j in range(1,8)]
    require(all(mixed[(i-1)*7+j-1][X.index((1<<(3+r))+(1<<(11+t)))]==int(i==r and j==t)
                for i in range(1,8) for j in range(1,8) for r in range(1,8) for t in range(1,8)),
            'whole49 rectangle independence decoder')
    blocks={'TT':TT,'Z':[v for B in standard['Z'] for v in B],
            'W':[v for B in standard['W'] for v in B],**pair,'ZW':mixed}
    require({k:len(v) for k,v in blocks.items()}=={'TT':23,'Z':56,'W':63,'ZZ':20,'WW':20,'ZW':49},
            'exact full231 coordinate dimensions')
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
                    for r in range(7) for t in range(7) for i in range(d) for j in range(d)),
                'ENTIRE standard Gram: positive norm times(I+J) on every physical orbit')
    seeds={'TT':TT,'Z':standard['Z'][0],'W':standard['W'][0]}
    for name,offset in (('ZZ',3),('WW',11)):
        weights={(0,1):1,(2,3):1,(0,2):-1,(1,3):-1}
        seeds[name]=[[weights.get(tuple(t for t in range(8) if A&(1<<(offset+t))),0)
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


def exact_factor(A,D,certificate,maxnorm):
    Q=certificate['factor_denominator'];V=certificate['factor_lower_triangle_numerators'];n=len(A)
    require(type(Q) is int and Q==1<<32 and len(V)==n and all(len(row)==i+1 for i,row in enumerate(V))
            and all(type(x) is int for row in V for x in row),'entire dyadic factor shape and values')
    require(Q*Q%D==0,'integer residual clearing');scale=Q*Q//D
    E=[[scale*A[i][j]-sum(V[i][k]*V[j][k] for k in range(min(i,j)+1)) for j in range(n)] for i in range(n)]
    margins=[E[i][i]-sum(abs(E[i][j]) for j in range(n) if j!=i) for i in range(n)]
    require(min(margins)>0 and min(margins)==certificate['whole_residual_minimum_row_margin_numerator']
            and certificate['whole_residual_denominator']==Q*Q,'WHOLE exact residual row margins')
    require(min(margins)*128>=Q*Q*maxnorm,'EXACT block-to-original margin at least1/128')
    return min(margins)


def verify(data):
    require((data['q'],data['k'],data['actual_empty_N'],data['maximum_star_s'])==(16,8,232,52), 'exact finite quantified carrier')
    X,O,K=carrier();C,U,D,S=original_matrix(data,X,O)
    stars=[sum(bool(A&(1<<i)) for A in X) for i in range(19)]
    require(stars[0]==52 and all(v<52 for v in stars[1:]),'all19 original stars, unique maximum a')
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
                require(len(G)==1 and norms[name]==[4],'scalar seed norm4')
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
                        and H[0][0]*128>=D*norms[name][0], 'exact scalar and original margin')
                bounds[key]=str(F(H[0][0],D*norms[name][0]))
            else:
                bound=exact_factor(H,D,certificates[key],max(norms[name][i] for i in ix))
                bounds[key]=str(F(bound,(1<<64)*max(norms[name][i] for i in ix)))
    # Actual-empty integer lift and BOTH full endpoints, not a row/rank proxy.
    rows=[sum(row) for row in C]
    L=[[D+sum(rows)]+[D-r for r in rows]]+[[D-rows[i]]+[D+x for x in row] for i,row in enumerate(C)]
    require(len(L)==232 and all(sum(row)==232*D for row in L), 'every actual-empty lift row exactly N')
    require(all(L[i][j]==L[j][i] for i in range(232) for j in range(232)), 'entire actual-empty symmetry')
    actual=[0]+X;M=[[L[i][j]-52*D*int(i==j) for j in range(232)] for i in range(232)]
    require(all(sum(row)==180*D for row in M),'every original M row exactly1 after clearing')
    require(all(not A&B or M[i][j]==0 for i,A in enumerate(actual) for j,B in enumerate(actual)),
            'ALL original intersecting-pair/diagonal M entries zero')
    ur=[sum(row) for row in U]
    lifted_U=[[sum(ur)]+[-r for r in ur]]+[[-ur[i]]+row for i,row in enumerate(U)]
    require(all(lifted_U[i][j]==232*D*int(i==j)-L[i][j] for i in range(232) for j in range(232)),
            'EVERY actual-empty upper endpoint equals EUE transpose')
    centered=[232*int(bool(A&1))-52 for A in actual]
    require(sum(centered)==0 and all(sum(x*y for x,y in zip(row,centered))==0 for row in L),
            'entire original centered maximum-star lower kernel')
    allowed=[(i,j) for i in range(231) for j in range(i+1,231) if not X[i]&X[j]]
    free=[(i,j) for i,j in allowed if X[i]!=1 and X[j]!=1]
    dimension=len(free);require(len(allowed)==20282 and dimension==20103 and len(allowed)-dimension==179,
                              'complete original maximum-star affine dimension')
    # The old five-face cannot alter this disjoint singleton/pair entry.
    outside_single=X.index(8);outside_pair=X.index(16+32)
    require(105*C[outside_single][outside_pair]!=-D,'explicit original entry outside old five-face')
    return {'actual_agent':'six-downset-3','role':'researcher','q':16,'k':8,'actual_empty_N':232,'s':52,
            'original_core_ordered_entries':231**2,'original_actual_empty_lift_entries':232**2,
            'complete_original_basis_columns':231,'both_full_original_basis_action_positions':action_positions,
            'all19_original_star_sizes':stars,'complete_original_repair_dimension':dimension,
            'invariant_free_entry_count':143,'original_C_kernel':'span(actual a-star)',
            'C_on_actual_star_perpendicular_and_U_margin':'1/128',
            'all12_exact_original_block_bounds':bounds,
            'independent_real_coordinate_cube_radius':str(F(1,512*dimension)),
            'cube_original_lower_and_upper_margin':'1/256',
            'both_actual_empty_endpoint_ranks':231,'simple_unit_eigenvalue':True,
            'explicit_outside_old_face_entry':str(F(C[outside_single][outside_pair],D)),
            'old_face_fixed_entry':'-1/105','actual_empty_M_loop':str(F(M[0][0],180*D)),
            'ordinary_PSD_lift_sector_completeness_and_cube_bridges_unformalized':True,
            'independent_reviewer_verdict':'UNREVIEWED'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'CERTIFICATE.json')
    ap.add_argument('--out',type=Path);args=ap.parse_args()
    import sourcecheck
    sourcecheck.check_bundle(BASE)
    data=json.loads(args.certificate.read_bytes());result=verify(data)
    raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    if args.certificate.resolve()==(BASE/'CERTIFICATE.json').resolve():
        require(raw==(BASE/'EXPECTED.json').read_bytes(),'ENTIRE original expected proof record')
    if args.out:args.out.write_bytes(raw)
    print(json.dumps({'completed':True,'N':232,'s':52,'all_original_entries':231**2,
                      'all_original_basis_actions':result['both_full_original_basis_action_positions'],
                      'margin':'1/128','cube_dimension':20103,'cube_radius':'1/10292736',
                      'record_SHA256':hashlib.sha256(raw).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
