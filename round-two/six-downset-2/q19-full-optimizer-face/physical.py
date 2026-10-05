"""Separate original-set and complete-basis checker for the private count pilot.

Original sets are built directly from named core pairs, not the producer's
membership predicate. Block actions are compared with every original row of
every physical basis vector. No numerical eigenvalue or old factor is input.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from pathlib import Path
import json
import resource
import time
from model import canonical, coefficient_input, comparison, digest, exact_ldl, parameters, q19_candidate, require, sector_forms


def original(table,k,m):
    ground=k+m+3
    collection={()}
    collection.update((i,) for i in range(ground))
    collection.update(combinations(range(ground),2))
    collection.add((0,1,2))
    for z in range(3,ground):
        collection.add((0,1,z));collection.add((0,2,z))
        if z>=k+3:
            collection.add((1,2,z))
    members=sorted(collection,key=lambda a:sum(1<<i for i in a))
    masks=[sum(1<<i for i in a) for a in members]
    N=len(members);s=sum(bool(v&1) for v in masks);h=N-s
    require((N,s,h)==parameters(k,m) and members[:2]==[(),(0,)],'independent count/actual anchor')
    require(all(tuple(a for a in v if a!=i) in collection for v in members for i in v),
            'each downward deletion in original construction')
    xmask=((1<<(k+3))-1)^7
    ymask=((1<<ground)-1)^((1<<(k+3))-1)
    types=[(v&7,(v&xmask).bit_count(),(v&ymask).bit_count()) for v in masks]
    den=lcm(*(a.denominator for a in table.values()))
    C=[]
    for i,v in enumerate(masks[1:]):
        row=[]
        for j,w in enumerate(masks[1:]):
            if i==j: a=(s-1)*den
            elif v&w: a=-den
            elif i==0 or j==0:a=0
            else:
                f=table[tuple(sorted((types[i+1],types[j+1])))]*den
                require(f.denominator==1,'exact whole original clearing')
                a=f.numerator
            row.append(a)
        C.append(row)
    stars=[i for i,v in enumerate(masks[1:]) if v&1]
    for i,v in enumerate(masks[1:]):
        if not v&1:
            C[i][0]=C[0][i]=-sum(C[i][j] for j in stars if j!=0)
    rows=list(map(sum,C))
    L=[[den+sum(rows)]+[den-a for a in rows]]+[[den-rows[i]]+[den+a for a in row] for i,row in enumerate(C)]
    Qtypes=types[2:];n=N-2
    r=[int(bool(v&1)) for v in masks[2:]];b=[1-a for a in r]
    T=[row[1:] for row in C[1:]]
    G=[[int(i==j)+r[i]*r[j]+b[i]*b[j] for j in range(n)] for i in range(n)]
    GI=[[s*h*int(i==j)-h*r[i]*r[j]-s*b[i]*b[j] for j in range(n)] for i in range(n)]
    cap=[[N*den*GI[i][j]-s*h*T[i][j] for j in range(n)] for i in range(n)]
    z=[N*int(bool(v&1))-s for v in masks]
    require(all(sum(C[i][j] for j in stars)==0 for i in range(N-1)),'each actual proper star row')
    require(all(sum(row)==N*den and sum(a*v for a,v in zip(row,z))==0 for row in L),
            'every actual stochastic and centered-star row')
    require(all(L[i][j]==L[j][i] and (not(masks[i]&masks[j]) or L[i][j]==s*den*int(i==j))
                for i in range(N) for j in range(N)),'all original support/symmetry positions')
    rs=[sum(GI[a][j] for a in range(n) if r[a]) for j in range(n)]
    bs=[sum(GI[a][j] for a in range(n) if b[a]) for j in range(n)]
    require(all(GI[i][j]+r[i]*rs[j]+b[i]*bs[j]==s*h*int(i==j) and
                GI[i][j]+r[j]*rs[i]+b[j]*bs[i]==s*h*int(i==j)
                for i in range(n) for j in range(n)), 'both ENTIRE original inverse-metric products')
    def lift(A):
        out=[[0]*N for _ in range(N)]
        for i,row in enumerate(A):
            pi=1 if r[i] else 0
            for j,a in enumerate(row):
                pj=1 if r[j] else 0
                out[i+2][j+2]+=a;out[pi][pj]+=a
                out[pi][j+2]-=a;out[i+2][pj]-=a
        return out
    low=lift(T);up=lift(cap)
    require(all(L[i][j]==den+low[i][j] and
                s*h*(N*den*int(i==j)-L[i][j])==up[i][j]+den*z[i]*z[j]
                for i in range(N) for j in range(N)), 'BOTH ENTIRE original endpoint lifts')
    return dict(k=k,m=m,N=N,s=s,h=h,members=members,masks=masks,types=Qtypes,
                T=T,cap=cap,G=G,den=den,clear=s*h,L=L)


def complete_basis(point):
    k,m=point['k'],point['m'];Q=point['members'][2:];types=sorted(set(point['types']))
    basis=[]
    def put(tag,sub,values):
        require(any(values),'nonzero original basis vector')
        basis.append(dict(tag=tag,sub=sub,values=values,sparse={i:a for i,a in enumerate(values) if a}))
    for t in types:
        put('trivial',(t,),[int(u==t) for u in point['types']])
    for pool,size,start in [('X',k,3),('Y',m,k+3)]:
        position=1 if pool=='X' else 2
        for a in range(1,size):
            for t in types:
                if t[position]:
                    vals=[(int(start in v)-int(start+a in v))*int(u==t) for v,u in zip(Q,point['types'])]
                    put(pool+'_standard',(t,a),vals)
        for i,j in combinations(range(1,size),2):
            if (i,j)==(1,2):continue
            edges={tuple(sorted((start+i,start+j))):2, (start+1,start+2):-2}
            for a in range(1,size):
                value=-2*int(a in (i,j))+2*int(a in (1,2))
                if value:edges[(start,start+a)]=value
            require(all(sum(v for edge,v in edges.items() if start+a in edge)==0 for a in range(size)),
                    'every pair-harmonic incidence equation')
            t=(0,2,0) if pool=='X' else (0,0,2)
            put(pool+pool+'_harmonic',(t,i,j),[edges.get(v,0) for v in Q])
    for a in range(1,k):
        for b in range(1,m):
            put('XY_mixed',((0,1,1),a,b),[
                (int(3 in v)-int(3+a in v))*(int(k+3 in v)-int(k+3+b in v))*int(u==(0,1,1))
                for v,u in zip(Q,point['types'])])
    require(len(basis)==len(Q),'complete physical basis count')
    pair_index={v:i for i,v in enumerate(Q)}
    for v in basis:
        if v['tag'] in ('XX_harmonic','YY_harmonic'):
            size,start=(k,3) if v['tag']=='XX_harmonic' else (m,k+3)
            _,i,j=v['sub']
            require(all(v['values'][pair_index[(start+a,start+b)]]==
                        2*int((a,b)==(i,j))-2*int((a,b)==(1,2))
                        for a,b in combinations(range(1,size),2)),
                    'ENTIRE independent free pair-coordinate witness')
        elif v['tag']=='XY_mixed':
            _,i,j=v['sub']
            require(all(v['values'][pair_index[(3+a,k+3+b)]]==int((a,b)==(i,j))
                        for a in range(1,k) for b in range(1,m)),
                    'ENTIRE independent free rectangle-coordinate witness')
    # Entire cross-sector orthogonality and all asserted standard/trivial metrics.
    gram=[];expected_positions=0;cross_positions=0
    for v in basis:
        row=[]
        for w in basis:
            val=sum(a*w['sparse'].get(i,0) for i,a in v['sparse'].items())
            row.append(val)
            if v['tag']!=w['tag']:
                require(val==0,'every physical cross-sector Gram entry');cross_positions+=1
            elif v['tag']=='trivial':
                t=v['sub'][0]
                expected=sum(u==t for u in point['types']) if v['sub']==w['sub'] else 0
                require(val==expected,'every trivial orbit metric');expected_positions+=1
            elif v['tag'] in ('X_standard','Y_standard'):
                t,a=v['sub'];u,b=w['sub']
                norms=((k-2 if t[1]==2 else 1)*m**t[2] if v['tag']=='X_standard' else
                       (m-2 if t[2]==2 else 1)*k**t[1])
                expected=norms*(1+int(a==b)) if t==u else 0
                require(val==expected,'every physical standard metric');expected_positions+=1
            elif v['tag']=='XY_mixed':
                _,a,b=v['sub'];_,c,d=w['sub']
                require(val==(1+int(a==c))*(1+int(b==d)),'every physical mixed metric');expected_positions+=1
        gram.append(row)
    return basis,dict(whole_physical_Gram_positions=len(Q)**2,
                      cross_sector_orthogonality_positions=cross_positions,
                      declared_metric_positions=expected_positions,
                      whole_basis_Gram_sha256=digest(gram),
                      basis_counts={tag:sum(v['tag']==tag for v in basis) for tag in sorted({v['tag'] for v in basis})})


def literal_actions(point,table,basis):
    require(len(basis)==point['N']-2 and
            len({(v['tag'],v['sub']) for v in basis})==point['N']-2,
            'all distinct physical directions, no missing or duplicated copy')
    forms=sector_forms(table,point['k'],point['m'])
    for side,actual in [('lower',point['T']),('upper',point['cap'])]:
        scale=point['den']*(1 if side=='lower' else point['clear'])
        for v in basis:
            block=forms[v['tag']+'_'+side]
            t=v['sub'][0];j=block['types'].index(t)
            # Lower/upper actions differ from quadratic matrices by the orbit metric.
            action=[block['matrix'][i][j]/block['metric'][i] for i in range(len(block['types']))]
            scalar=action[0] if len(action)==1 else None
            for i,(member,u) in enumerate(zip(point['members'][2:],point['types'])):
                observed=sum(actual[i][a]*b for a,b in v['sparse'].items())
                if v['tag']=='trivial':
                    expected=scale*action[block['types'].index(u)]
                elif v['tag'] in ('X_standard','Y_standard'):
                    start=3 if v['tag']=='X_standard' else point['k']+3
                    a=v['sub'][1]
                    value=int(start in member)-int(start+a in member)
                    expected=scale*action[block['types'].index(u)]*value if u in block['types'] else F(0)
                else:
                    expected=scale*scalar*v['values'][i]
                require(expected.denominator==1 and observed==expected.numerator,
                        'EVERY original '+side+' row/basis image, '+v['tag'])
    return dict(entire_original_action_positions=2*(point['N']-2)**2,
                both_endpoints_every_original_row_every_basis_checked=True)


def run(path,tau):
    start=time.monotonic();raw=coefficient_input(path)
    table,recipe=q19_candidate(raw,tau)
    point=original(table,9,10)
    basis,metrics=complete_basis(point)
    actions=literal_actions(point,table,basis)
    tests={tag:exact_ldl(block['matrix'],block['metric'],F(1,1024))
           for tag,block in sector_forms(table,9,10).items()}
    require(all(v['positive_definite'] for v in tests.values()),'all12 fresh physical endpoint comparisons')
    return dict(agent='six-downset-2',role='researcher',tau=str(tau),k=9,m=10,N=303,s=61,h=242,
                whole_original_positions_each=303**2,full_metric_positions=301**2,
                original_denominator=point['den'],cap_clear=point['clear'],
                original_T_num_sha256=digest(point['T']),original_L_num_sha256=digest(point['L']),
                original_cap_num_sha256=digest(point['cap']),metrics=metrics,actions=actions,
                original_L_rational_sha256=digest([[str(F(a,point['den'])) for a in row] for row in point['L']]),
                original_T_rational_sha256=digest([[str(F(a,point['den'])) for a in row] for row in point['T']]),
                fresh_block_certificates=tests,
                generic_completeness_proof_ordinary_unformalized='STRUCTURAL.md',
                no_old_factor_floor_or_peer_executable_used=True,
                observed_seconds=time.monotonic()-start,
                peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--coefficients',required=True);p.add_argument('--tau',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();result=run(args.coefficients,F(args.tau))
    raw=canonical(result)+b'\n';Path(args.out).write_bytes(raw)
    import hashlib
    print(json.dumps(dict(tau=args.tau,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                          observed_seconds=result['observed_seconds'],peak_RSS_KiB=result['peak_RSS_KiB'],
                          complete_action_positions=result['actions']['entire_original_action_positions'])))
