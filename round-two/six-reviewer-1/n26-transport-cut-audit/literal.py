"""Fresh literal bit-set controls; arbitrary signed matrices, NOT PSD witnesses."""
import json,hashlib
from math import lcm
from fractions import Fraction as Q
from pathlib import Path
from affine import C,dimensions
from check import require


def control(n):
    N,s,h=dimensions(n);B=[[Q(0)for b in range(n-1)]for a in range(n-1)]
    for a in range(2,n-1):
        for b in range(a,n-1):
            if a+b<=n:B[a][b]=B[b][a]=Q((a+2*b)%7-3,11*(a+b))
    for a in range(2,n-1):B[a][1]=B[1][a]=s-sum(C(n-a-1,b-1)*B[a][b]for b in range(2,n-1))
    B[1][1]=s-sum(C(n-2,b-1)*B[1][b]for b in range(2,n-1))
    e=[Q(0)]+[h-sum(C(n-a,b)*B[a][b]for b in range(1,n-1))for a in range(1,n-1)]
    ell=N-sum(C(n,a)*e[a]for a in range(1,n-1))
    denom=lcm(*[x.denominator for row in B for x in row],*[x.denominator for x in e],ell.denominator)
    scaled=lambda q:int(q*denom)
    BB=[[scaled(x)for x in row]for row in B];ee=list(map(scaled,e));ll=scaled(ell)
    masks=[a for a in range(1<<n)if a.bit_count()<=n-2];sizes=[a.bit_count()for a in masks];index={a:j for j,a in enumerate(masks)}
    require(len(masks)==N and masks[0]==0,'complete original vertex census including empty')
    direct=[[ll if a==b==0 else ee[sizes[j]] if a==0 else ee[sizes[i]] if b==0 else s*denom if a==b else 0 if a&b else BB[sizes[i]][sizes[j]] for j,b in enumerate(masks)]for i,a in enumerate(masks)]
    adjacent=[[0]*N for _ in masks];adjacent[0][0]=ll;full=(1<<n)-1
    for j in range(1,N):adjacent[0][j]=adjacent[j][0]=ee[sizes[j]]
    for i,a in enumerate(masks[1:],1):
        adjacent[i][i]=s*denom;comp=full^a;sub=comp
        while sub:
            j=index.get(sub)
            if j is not None:adjacent[i][j]=BB[sizes[i]][sizes[j]]
            sub=(sub-1)&comp
    require(direct==adjacent,'EVERY literal entry in two independent full constructors')
    for i,a in enumerate(masks):
        require(sum(direct[i])==N*denom,'EVERY literal row')
        for p in range(n):require(sum(x for j,x in enumerate(direct[i])if masks[j]&(1<<p))==s*denom,'EVERY original point-star action including empty')
        for j,b in enumerate(masks):
            require(direct[i][j]==direct[j][i],'EVERY literal symmetric entry')
            if a&b and a!=b:require(direct[i][j]==0,'EVERY intersecting off-diagonal zero')
    profiles=[[((a*3)%7)-3 for a in range(1,n-1)],[(-1)**a*(a%4+1)for a in range(1,n-1)]]
    energies=[];norms=[]
    for z in profiles:
        v=[0 if not a else z[a.bit_count()-1]*(int(bool(a&1))-int(bool(a&2)))for a in masks]
        exact=Q(sum(v[i]*sum(x*v[j]for j,x in enumerate(row))for i,row in enumerate(direct)),denom)
        formula=2*s*sum(C(n-2,a-1)*z[a-1]**2 for a in range(1,n-1))-2*sum(B[a][b]*C(n-2,a-1)*C(n-a-1,b-1)*z[a-1]*z[b-1]for a in range(1,n-1)for b in range(1,n-1))
        require(exact==formula,'whole original literal quadratic form versus counted formula')
        norm=sum(x*x for x in v);require(norm==2*sum(C(n-2,a-1)*z[a-1]**2 for a in range(1,n-1)),'literal original norm')
        energies.append(str(exact));norms.append(norm)
    complement=[]
    for a in range(2,n-1):
        A=(1<<a)-1;T=full^A;i=index[A];j=index[T]
        energy=Q(direct[i][i]+direct[j][j]-direct[i][j]-direct[j][i],denom)
        require(energy==2*(s-B[a][n-a]),'ALL original complement differences')
        complement.append(str(energy))
    require(Q(direct[0][0],denom)==ell,'retained original empty loop')
    # Hash records only follow, and never replace, the complete comparisons above.
    digest=hashlib.sha256(json.dumps(direct,separators=(',',':')).encode()).hexdigest()
    return {'n':n,'N':N,'s':s,'h':h,'original_vertices':masks,'common_denominator':denom,'B':[[str(q)for q in row]for row in B],'empty_entries':list(map(str,e)),'empty_loop':str(ell),'profiles':profiles,'quadratic_forms':energies,'squared_norms':norms,'complement_difference_energies':complement,'all_original_entries_compared':N*N,'all_original_point_star_actions_compared':N*n,'entire_scaled_matrix_sha256_after_full_comparison':digest,'scope':'Arbitrary signed affine controls, NOT PSD or H witnesses; no finite-to-n26 extrapolation.'}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','controls':[control(n)for n in [7,9]]}
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps([{k:r[k]for k in ['n','N','all_original_entries_compared','all_original_point_star_actions_compared']}for r in result['controls']]))
