"""Literal complete actions and four-family projector floor on original sets.

Completeness for every integerq is the ordinary elementary layer argument
in PROOF.md/8757. This finite validation is separate from coefficient signs.
"""
import bootstrap
from fractions import Fraction as F
from weights import formula,model,inverse,FLOOR,KAPPA
from matrices import literal_base
from exact import require,schur_psd,polynomial_psd,digest

def harmonic(mask,degree):
    if degree==0:return 1
    if degree==1:return int(bool(mask&1))-int(bool(mask&2))
    return (int(bool(mask&1))-int(bool(mask&2)))*(int(bool(mask&4))-int(bool(mask&8)))

def copies(q,degree):
    j,ell=degree
    return (1 if not j else 2)*(1 if not ell else q-1 if ell==1 else q*(q-3)//2)

def run(q=4):
    X,C,families=literal_base(q);Y=X[1:];size=len(C);s=3*q+4
    gram=[[sum((v[i]*w[i] for i in range(size)),F(0)) for w in families] for v in families]
    inv=[[x.at(0) for x in row] for row in inverse(gram)]
    P=[[F(i==j)-sum((families[a][i]*inv[a][b]*families[b][j] for a in range(4) for b in range(4)),F(0)) for j in range(size)] for i in range(size)]
    require(all(sum((P[i][j]*v[j] for j in range(size)),F(0))==0 for i in range(size) for v in families),'original projector kernels')
    require(all(sum((P[i][h]*P[h][j] for h in range(size)),F(0))==P[i][j] for i in range(size) for j in range(size)),'original projector idempotence')
    require(sum(P[i][i] for i in range(size))==size-4,'four independent literal family columns')
    rank=schur_psd([[C[i][j]-FLOOR*P[i][j] for j in range(size)] for i in range(size)])
    require(rank==size-4,'original full base projector floor rank')
    require(all(sum(row)==KAPPA*sum(P[i]) for i,row in enumerate(C)),'original C1=kappaP1 identity')
    typ=lambda A:((A&7).bit_count(),(A>>3).bit_count());count=0;dimensions=[];secondary=[];records=[]
    for item in model(F(q),formula(F(q))):
        degree=item['degree'];levels=item['levels'];norms=[x.at(0) for x in item['norms']];g=[[x.at(0) for x in row] for row in item['lower']];ks=item['kernel'];n=len(levels)
        columns=[]
        for kind,norm in zip(levels,norms):
            col=[harmonic(A&7,degree[0])*harmonic(A>>3,degree[1]) if typ(A)==kind else 0 for A in Y]
            require(sum(v*v for v in col)==norm*2**sum(degree),'original harmonic norm')
            columns.append(col)
        H=[[g[i][j]/norms[i] for j in range(n)] for i in range(n)]
        for j,col in enumerate(columns):
            actual=[sum((row[h]*col[h] for h in range(size)),F(0)) for row in C]
            predicted=[sum((columns[a][i]*H[a][j] for a in range(n)),F(0)) for i in range(size)]
            require(actual==predicted,'original base complete action');count+=1
        pg=[[F(norms[i]*int(i==j)) for j in range(n)] for i in range(n)]
        if ks:
            kg=[[sum((norms[h]*v[h]*w[h] for h in range(n)),F(0)) for w in ks] for v in ks];ki=[[x.at(0) for x in row] for row in inverse(kg)]
            for i in range(n):
                for j in range(n):pg[i][j]-=norms[i]*norms[j]*sum(ks[a][i]*ki[a][b]*ks[b][j] for a in range(len(ks)) for b in range(len(ks)))
        floor=[[g[i][j]-FLOOR*pg[i][j] for j in range(n)] for i in range(n)]
        anchors=[(1,0),(2,0)] if degree==(0,0) else [(1,0)] if degree==(1,0) else []
        keep=[i for i,t in enumerate(levels) if t not in anchors]
        quotient=[[floor[i][j] for j in keep] for i in keep]
        direct=schur_psd(quotient);alternate=polynomial_psd(quotient)
        require(direct==alternate[0]==len(keep),'secondary quotient characteristic criterion')
        upper=[[F(2*s*norms[i]*int(i==j))-g[i][j] for j in range(n)] for i in range(n)]
        ur=schur_psd(upper);uc=polynomial_psd(upper);require(ur==uc[0],'secondary upper characteristic criterion')
        secondary.append({'degree':degree,'floor_rank':direct,'floor_characteristic_sha256':alternate[1],'upper_rank':ur,'upper_characteristic_sha256':uc[1]})
        dim=copies(q,degree)*n;dimensions.append(dim);records.append({'degree':degree,'levels':levels,'copies':copies(q,degree),'dimension':dim})
    require(count==18 and sum(dimensions)==size,'complete original sector coverage')
    return {'q':q,'N0':len(X),'full_projector_floor_rank':rank,'original_action_columns':count,'sector_dimensions':dimensions,'sectors':records,'secondary_characteristic_forms':2*len(secondary),'secondary_records':secondary,'core_sha256':digest([[str(x) for x in row] for row in C])}
