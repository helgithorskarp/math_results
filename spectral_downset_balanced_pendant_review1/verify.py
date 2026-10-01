#!/usr/bin/env python3
"""six-reviewer-1: independent balanced-pendant review and refinements.

Default mode imports no author code. Each required matching is constructed
from scratch with a frozen edge and recursive alternating paths, not producer
splices. Integer congruence kernel is adapted from this reviewer's review8428.
All-order Harris/Hall, double-star gap and zero-pendant bridges: REVIEW.md.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
from math import isqrt, lcm
from pathlib import Path
import argparse
import json

def need(ok, text):
    if not ok:
        raise ValueError(text)


def fingerprint(a):
    return sha256(json.dumps([[str(x) for x in row] for row in a],
                             separators=(',', ':')).encode()).hexdigest()


def determinant(a):
    result=0;N=len(a)
    for p in permutations(range(N)):
        sign=(-1)**sum(p[i]>p[j] for i in range(N) for j in range(i+1,N))
        term=sign
        for i in range(N):term*=a[i][p[i]]
        result+=term
    return result


def psd_rank(a):
    """Integer fraction-free symmetric elimination; every division exact.

    Positive pivots are congruences. A zero remaining diagonal forces its whole
    row zero for PSD; otherwise reject. Scaling by one positive grid is harmless.
    """
    N=len(a); need(N and all(len(row)==N for row in a), 'PSD shape')
    need(all(a[i][j]==a[j][i] for i in range(N) for j in range(N)), 'PSD symmetry')
    grid=lcm(*(F(x).denominator for row in a for x in row))
    z=[[int(grid*x) for x in row] for row in a]; prev=1; rank=0
    for k in range(N):
        need(all(z[i][i]>=0 for i in range(k,N)), 'negative PSD residual diagonal')
        p=next((i for i in range(k,N) if z[i][i]>0),None)
        if p is None:
            need(all(z[i][j]==0 for i in range(k,N) for j in range(k,N)), 'zero diagonal nonzero PSD row')
            break
        z[k],z[p]=z[p],z[k]
        for row in z:row[k],row[p]=row[p],row[k]
        pivot=z[k][k]
        for i in range(k+1,N):
            for j in range(i,N):
                numerator=pivot*z[i][j]-z[i][k]*z[k][j]
                need(numerator%prev==0,'nonexact symmetric elimination')
                z[i][j]=z[j][i]=numerator//prev
        for i in range(k+1,N):z[i][k]=z[k][i]=0
        prev=pivot;rank+=1
    return rank



def geometry(D,c):
    need(type(c)is int and c>=0 and type(D)is list and D==sorted(set(D))
         and D and D[0]==0 and all(type(a)is int and a>=0 for a in D),'family domain')
    members=set(D)
    need(all(a^(1<<i)in members for a in D for i in range(a.bit_length())if a&(1<<i)),'downset deletion')
    C=1<<c;E=[a for a in D if not a&C];s=len(E)
    need(s>=2 and set(D)==set(E)|{a|C for a in E},'balanced s>=2')
    return E,C


def matching(left,right,forced=None):
    """Exact complete alternating-path search, preserving a specified edge."""
    neighbors=[[j for j,b in enumerate(right)if not a&b]for a in left]
    owner={};locked_left=locked_right=None
    if forced is not None:
        locked_left,locked_right=forced
        need(locked_right in neighbors[locked_left],'forbidden forced edge')
        owner[locked_right]=locked_left
    calls=0
    def augment(a,seen):
        nonlocal calls
        calls+=1;need(calls<=10000,'bounded matching verification incomplete')
        for b in neighbors[a]:
            if b==locked_right or b in seen:continue
            seen.add(b)
            if b not in owner or augment(owner[b],seen):owner[b]=a;return True
        return False
    for a in sorted(range(len(left)),key=lambda x:(len(neighbors[x]),x)):
        if a==locked_left:continue
        need(augment(a,set()),'no complete matching for required input')
    result=[None]*len(left)
    for b,a in owner.items():result[a]=b
    need(len(owner)==len(left)==len(right)and set(result)==set(range(len(right))), 'matching bijection')
    need(all(not left[a]&right[b]for a,b in enumerate(result)),'matching support')
    if forced is not None:need(result[locked_left]==locked_right,'frozen edge lost')
    return result


def all_downsets():
    out=[]
    for mask in range(1<<16):
        if not mask&1:continue
        E=[a for a in range(16)if mask&(1<<a)]
        if len(E)<2:continue
        if any(not mask&(1<<(a^(1<<i)))for a in E for i in range(4)if a&(1<<i)):continue
        out.append(E)
    need(len(out)==166,'complete four-point E count')
    return out


def hall_census(E):
    s=len(E);nbr=[sum(1<<j for j,b in enumerate(E)if not a&b)for a in E]
    unions=[0]*(1<<s);tight=0
    for mask in range(1,1<<s):
        bit=mask&-mask;unions[mask]=unions[mask^bit]|nbr[bit.bit_length()-1]
        d=unions[mask].bit_count()-mask.bit_count();need(d>=0,'Hall inequality')
        if mask!=(1<<s)-1:tight+=d==0
    free=[i for i in range(max(E).bit_length())if 2*sum(bool(a&(1<<i))for a in E)==s]
    need(bool(tight)==bool(free),'strict Hall/free-coordinate criterion')
    return {'subfamilies':1<<s,'proper_nonempty_tight':tight,'free_coordinates':free}


def trade(D,E,p=None):
    pos={a:i for i,a in enumerate(D)};T=[[0]*len(D)for _ in D];choices=[]
    active=0
    for a in E:active|=a
    for y in E[1:]:
        if p is None:
            missing=active&~y;need(missing,'outside singleton for original trade')
            b=missing&-missing
        else:b=p
        need(b!=y and b in pos and not b&y,'trade support')
        i,j,k=pos[0],pos[y],pos[b]
        T[i][i]-=2
        for a,z,v in [(i,j,1),(i,k,1),(j,k,-1)]:T[a][z]+=v;T[z][a]+=v
        choices.append([y,b])
    need(all(sum(row)==0 for row in T),'row-zero trade')
    return T,choices


def base(D,c,augment):
    E,C=geometry(D,c);p=1<<max(D).bit_length()
    if augment:D=sorted(D+[p,p|C]);right=E+[p];left=sorted([a|C for a in E]+[p|C])
    else:right=E;left=sorted(a|C for a in E)
    pos={a:i for i,a in enumerate(D)};counts=[[0]*len(D)for _ in D];h=0
    for i,a in enumerate(left):
        for j,b in enumerate(right):
            if a&b:continue
            pair=matching(left,right,(i,j));h+=1
            for x,k in zip(left,pair):
                u,v=pos[x],pos[right[k]];counts[u][v]+=1;counts[v][u]+=1
    need(all(sum(row)==h for row in counts),'all matching row counts')
    need(all((counts[pos[a]][pos[b]]>0)==(not a&b)for a in left for b in right),'complete allowed-edge coverage')
    T,choices=trade(D,E,p if augment else None)
    return D,[[F(x,h)for x in row]for row in counts],T,h,choices


def matrix_check(D,c,M0,T,h,eps,gamma):
    N=len(D);s=N//2;q=[1 if a&(1<<c)else-1 for a in D]
    M=[[M0[i][j]+eps*T[i][j]for j in range(N)]for i in range(N)]
    need(all(sum(row)==1 for row in M),'normalized rows')
    need(all(M[i][j]==M[j][i]and(not a&b or M[i][j]==0)
             for i,a in enumerate(D)for j,b in enumerate(D)),'H support and symmetry')
    need(all(sum(M[i][j]*q[j]for j in range(N))==-q[i]for i in range(N)),'negative endpoint')
    need(min(M[0][1:])>=eps,'positive empty weights')
    for sign,kernel in [(1,q),(-1,[1]*N)]:
        slack=[[F(i==j)+sign*M[i][j]for j in range(N)]for i in range(N)]
        need(psd_rank(slack)==N-1,'full endpoint slack rank')
        buffered=[[slack[i][j]-gamma*(F(i==j)-F(kernel[i]*kernel[j],N))
                   for j in range(N)]for i in range(N)]
        need(psd_rank(buffered)==N-1,'complete endpoint-complement gap')
    return fingerprint(M)


def examine(E,c=4,augment=True):
    s=len(E);D=sorted(E+[a|(1<<c)for a in E]);D,M0,T,h,choices=base(D,c,augment)
    k=s-1
    if augment:
        square=2*k*(k+1);root=isqrt(square);theta=k+root+int(root*root<square)
        g=F(2,h*(s+3));eps=F(1,h*(s+3)*theta)
        oldg=F(2,h*(len(D)-1)**2);oldeps=F(1,4*h*k*(len(D)-1)**2)
        need(eps>oldeps,'strict repair improvement')
        oldhash=matrix_check(D,c,M0,T,h,oldeps,oldg/2)
    else:
        theta=3*k;g=F(2,h*(s+2));eps=F(1,3*h*k*(s+2));oldhash=None
    hsh=matrix_check(D,c,M0,T,h,eps,g/2)
    return {'E':E,'augment':augment,'N':len(D),'original_s':s,'h':h,'theta':theta,
            'gap':str(g),'epsilon':str(eps),'both_ranks':len(D)-1,
            'old_matrix_sha256':oldhash,'matrix_sha256':hsh,'trade_choices_sha256':sha256(json.dumps(choices).encode()).hexdigest()}


def analytic_controls():
    tested=0
    # Universal double-star Poincare bridge controls; the all-order proof is written.
    for s in range(2,18):
        N=2*s+2;H=[[0]*N for _ in range(N)]
        edges=[(0,1)]+[(0,i)for i in range(s+2,N)]+[(1,i)for i in range(2,s+2)]
        for a,b in edges:H[a][a]+=1;H[b][b]+=1;H[a][b]-=1;H[b][a]-=1
        gamma=F(2,s+3)
        need(psd_rank([[F(H[i][j])-gamma*(F(i==j)-F(1,N))for j in range(N)]for i in range(N)])==N-1,'double-star gap')
        tested+=1
    trades=0
    for k in range(1,16):
        D=[0]+[1<<i for i in range(k+1)];E=D[:-1];T,_=trade(D,E,D[-1]);square=2*k*(k+1);r=isqrt(square);theta=k+r+(r*r<square)
        need(theta<=3*k,'rational trade-norm improvement')
        for sign in (-1,1):psd_rank([[theta*int(i==j)+sign*T[i][j]for j in range(len(D))]for i in range(len(D))])
        # Exact three-coordinate action, with Gram diag(1,1,k).
        A=[[-2*k,k,k],[k,0,-k],[1,-1,0]]
        need(sum(A[i][i]for i in range(3))==-2*k and determinant(A)==0,'trade trace/kernel')
        need(sum(determinant([[A[i][j]for j in ix]for i in ix])for ix in combinations(range(3),2))==-k*k-2*k,'trade characteristic coefficient')
        trades+=1
    oracle=accepted=0
    for z in product((-1,0,1),repeat=6):
        A=[[z[0],z[1],z[2]],[z[1],z[3],z[4]],[z[2],z[4],z[5]]]
        expected=all(determinant([[A[i][j]for j in ix]for i in ix])>=0 for k in range(1,4)for ix in combinations(range(3),k))
        try:psd_rank(A);observed=True
        except ValueError:observed=False
        need(observed==expected,'independent principal-minor oracle');oracle+=1;accepted+=observed
    return {'double_stars':tested,'exact_trade_compressions':trades,'PSD_oracle_cases':oracle,'PSD_cases':accepted}


def controls():
    rejected=[]
    cases=[('non_downset',lambda:geometry([0,1,3],0)),
           ('unbalanced',lambda:geometry([0,1,2],0)),
           ('s1_input',lambda:geometry([0,1],0)),
           ('boolean_center',lambda:geometry([0,1,2,3],True)),
           ('duplicate_members',lambda:geometry([0,1,1,2,3],0)),
           ('inactive_center',lambda:geometry([0,1,2,3],6)),
           ('forbidden_forced_edge',lambda:matching([1,3],[0,2],(1,1))),
           ('nonextendible_old_cube_edge',lambda:matching([0,1],[0,1],(0,0))),
           ('zero_diagonal_indefinite',lambda:psd_rank([[0,1],[1,0]]))]
    D,M0,T,h,_=base([0,1,2,3],0,True)
    cases.append(('excessive_trade',lambda:psd_rank([[F(i==j)+M0[i][j]+T[i][j]for j in range(len(D))]for i in range(len(D))])))
    unit=[[-2,1,1],[1,0,-1],[1,-1,0]]
    cases.append(('false_norm_two',lambda:psd_rank([[2*int(i==j)+unit[i][j]for j in range(3)]for i in range(3)])))
    for name,run in cases:
        try:run()
        except ValueError:rejected.append(name)
        else:raise ValueError('damaged control accepted:'+name)
    # Uniform on a downset itself is not generally associated.
    need(F(0,3)-F(1,3)*F(1,3)==F(-1,9),'downset association counterexample')
    # On cube2 the two scaled centered stars are explicitly independent.
    v=[-2,2,-2,2];w=[-2,-2,2,2]
    gram=[[sum(a*b for a,b in zip(x,y))for y in [v,w]]for x in [v,w]]
    need(determinant(gram)==256,'one-pendant s1 rank obstruction')
    return {'damaged_inputs_rejected':rejected,'uniform_downset_association_counterexample':'-1/9',
            's1_one_pendant_star_Gram_determinant':256,'incomplete_search_is_nonexistence':False}


def author_bridge(path):
    import importlib.util
    producer=path/'balanced_pendant_completion.py'
    need(sha256(producer.read_bytes()).hexdigest()=='2a0c1efab02bd3dc09612363bb85a656aec48a5468219cfa671943efa526a884','pinned producer source')
    spec=importlib.util.spec_from_file_location('credited_producer',producer);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    expected_path=path/'balanced_pendant_expected.json'
    need(sha256(expected_path.read_bytes()).hexdigest()=='baa6f98b449b49076684dd864eb28cbea29378df5a7ece7d78c005b2436f5b3a','pinned expected source')
    expected=json.loads(expected_path.read_text());records=[]
    for q in range(2,6):
        D=list(range(1<<q));r=module.completion(D,0);N=r['N'];h=r['edge_count'];s=r['original_s'];M0=[[F(x,h)for x in row]for row in r['counts']]
        S=set(r['S'])
        need(all(type(x)is int and x>=0 for row in r['counts']for x in row),'nonnegative integer matching counts')
        need(all(sum(row)==h for row in r['counts']),'producer matching row count')
        need(all((r['counts'][i][j]>0)==((a in S)!=(b in S)and not a&b)
                 for i,a in enumerate(r['family'])for j,b in enumerate(r['family'])),'producer full cross-edge coverage')
        T,_=trade(r['family'],list(r['E']),r['fresh']);old=matrix_check(r['family'],0,M0,T,h,r['epsilon'],r['gap']/2)
        need(all(r['entry'](a,b)==M0[i][j]+r['epsilon']*T[i][j]for i,a in enumerate(r['family'])for j,b in enumerate(r['family'])),'literal producer entry bridge')
        pinned=next(x for x in expected['cohort']+expected['fixtures']if x['original_family']==D and x['center']==0)
        need(old==pinned['matrix_sha256'],'whole original fingerprint')
        k=s-1;square=2*k*(k+1);a=isqrt(square);theta=k+a+(a*a<square);eps=F(1,h*(s+3)*theta);g=F(2,h*(s+3));new=matrix_check(r['family'],0,M0,T,h,eps,g/2)
        records.append({'case':'cube'+str(q),'N':N,'h':h,'old_epsilon':str(r['epsilon']),'new_epsilon':str(eps),'new_gap':str(g),'both_ranks':N-1,'old_matrix_sha256':old,'new_matrix_sha256':new,'complete_entry_bridge':N*N})
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','method':'Optional untrusted pinned producer; independent literal trade/full slacks; standalone default imports no producer','records':records}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);p.add_argument('--author-root',type=Path);args=p.parse_args()
    if args.author_root:
        value=author_bridge(args.author_root)
    else:
        augmented_digest=sha256();original_digest=sha256();hall_digest=sha256();sizes={};unique=Hall=augmented_entries=original_entries=edges_aug=edges_old=0
        fixtures={}
        for E in all_downsets():
            H=hall_census(E);Hall+=H['subfamilies'];hall_digest.update(json.dumps([E,H],sort_keys=True).encode()+b'\n')
            sizes[str(len(E))]=sizes.get(str(len(E)),0)+1
            r=examine(E);augmented_entries+=r['N']**2;edges_aug+=r['h'];augmented_digest.update(json.dumps(r,sort_keys=True).encode()+b'\n')
            if E==list(range(len(E)))and len(E)in [2,4,8,16]:fixtures['cube'+str(len(E).bit_length())]=r
            if not H['free_coordinates']:
                unique+=1;r0=examine(E,augment=False);original_entries+=r0['N']**2;edges_old+=r0['h'];original_digest.update(json.dumps(r0,sort_keys=True).encode()+b'\n')
                if E in [[0,1,2],list(range(15))]:fixtures['zero_pendant_s'+str(len(E))]=r0
        value={'agent':'six-reviewer-1','role':'independent mathematical reviewer','target_height':8424,'target_ref':'bafkreihzrerxvgs25yihlw4oxcys3z3fgl2og752e6xqo2cfdtpohsfhcq','proof_status':'Exact finite evidence; separate all-order real bridges in REVIEW.md unformalized',
               'census':{'family_masks':65536,'nontrivial_labelled_four_point_E':166,'size_histogram':sizes,'one_pendant_cases':166,'zero_pendant_unique_center_cases':unique,'multiple_maximum_cases':166-unique,'complete_original_Hall_subfamilies':Hall,'augmented_entry_positions_per_parameter':augmented_entries,'original_entry_positions':original_entries,'augmented_conditioned_matchings':edges_aug,'original_conditioned_matchings':edges_old,'augmented_digest':augmented_digest.hexdigest(),'original_digest':original_digest.hexdigest(),'Hall_digest':hall_digest.hexdigest(),'scope':'Balanced D=E union(c+E) with marked extra coordinate4; not all arbitrary downsets'},
               'fixtures':fixtures,'analytic_controls':analytic_controls(),'controls':controls()}
    text=json.dumps(value,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')


if __name__=='__main__':main()
