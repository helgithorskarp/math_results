"""Exact original-domain validation; not finite inference of uniform coverage."""
from pathlib import Path
import argparse,json,signal,time,resource
from fractions import Fraction as F
from closure import *

def alarm(signum,frame):raise TimeoutError('one-point closure fixture60s guard')
signal.signal(signal.SIGALRM,alarm)

def largest_cliques(family,s):
    """Exhaustive actual-set intersection census, with a fixed small order."""
    vertices=family[1:];N=len(vertices)
    require(N<=23,'census guard')
    adj=[sum(1<<j for j,B in enumerate(vertices) if i!=j and A&B) for i,A in enumerate(vertices)]
    counts=[];nodes=0
    def visit(R,P):
        nonlocal nodes
        nodes+=1;require(nodes<=100000,'census node guard')
        if len(R)==s:
            counts.append(sorted(vertices[i] for i in R));return
        if len(R)+P.bit_count()<s:return
        while P:
            bit=P&-P;P-=bit;i=bit.bit_length()-1
            visit(R+[i],P&adj[i])
    visit([], (1<<N)-1)
    return sorted(counts),nodes

def damage_controls(family,C,M,s):
    labels=[]
    def reject(label,fn):
        try:fn()
        except ValueError:labels.append(label);return
        raise ValueError('damage accepted: '+label)
    bad=cube(2);bad['core'][0][1]=bad['core'][1][0]=F(100)
    reject('private indefinite disjoint entry',lambda:construct(3,[(0,bad)]))
    bad=cube(2);bad['core'][0][2]=bad['core'][2][0]=F(-2)
    reject('private intersection entry',lambda:construct(3,[(0,bad)]))
    bad=cube(2);bad['family']=[0,1,3]
    reject('private missing subset',lambda:construct(3,[(0,bad)]))
    bad=cube(2);bad['s']=1
    reject('private incorrect star',lambda:construct(3,[(0,bad)]))
    reject('private star above q',lambda:construct(2,[(0,cube(3))]))
    reject('old mark out of range',lambda:construct(3,[(3,cube(1))]))
    reject('trivial old cube guard',lambda:construct(1,[(0,cube(1))]))
    reject('no attachment guard',lambda:construct(3,[]))
    bad=[row[:] for row in M];bad[0][0]+=1
    reject('actual empty loop',lambda:check_h(family,bad,s))
    bad=[row[:] for row in M];i=next(j for j,A in enumerate(family) if A)
    bad[i][i]=F(1)
    reject('whole original intersection',lambda:check_h(family,bad,s))
    reject('singular PSD range',lambda:psd_rank([[0,1],[1,1]]))
    return labels

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path)
    args=parser.parse_args();start=time.monotonic()
    fixtures=[
        ('rank-two baseline',2,[(0,cube(1)),(1,cube(1))]),
        ('private size exceeds q, star strict',2,[(0,singletons(7)),(1,cube(1))]),
        ('mixed triangle and other-mark pendant',3,[(0,cube(2)),(1,cube(1))]),
        ('two distinct triangle facets',3,[(0,cube(2)),(1,cube(2))]),
        ('same-mark repeated facets and other mark',3,[(0,cube(2)),(0,cube(2)),(2,cube(1))]),
        ('private uniform rank-two input',3,[(0,uniform_rank_two(3)),(1,cube(2)),(2,cube(1))]),
        ('two maximum-load marks with private edges',3,[(0,cube(2)),(1,cube(2)),(2,cube(1))]),
        ('large private star below q',4,[(0,uniform_rank_two(4)),(3,cube(3))]),
        ('four marks and repeated maximum',4,[(0,cube(2)),(1,cube(2)),(2,cube(1)),(3,cube(1))]),
        ('five marks mixed private families',5,[(0,cube(2)),(1,cube(1)),(2,cube(1)),(3,cube(1)),(4,cube(1))]),
        ('literal n6 boundary',6,[(0,cube(2)),(5,cube(1))]),
        ('weak equality one facet',3,[(0,cube(3))]),
        ('weak equality plus other mark',3,[(0,cube(3)),(1,cube(1))]),
        ('weak equality repeated heavy mark',3,[(0,cube(3)),(1,cube(3))]),
        ('weak equality rank-two input',2,[(0,cube(2)),(1,cube(1))]),
    ]
    rows=[];census=[];damages=[]
    for label,n,attachments in fixtures:
        signal.alarm(60);t0=time.monotonic();family,C,M,out=construct(n,attachments)
        out['label']=label
        if out['strict'] and len(family)<=24:
            actual,nodes=largest_cliques(family,out['s'])
            heavy=[i for i,d in enumerate(out['loads']) if d==max(out['loads'])]
            expected=sorted(sorted(A for A in family if A&(1<<i)) for i in heavy)
            require(actual==expected,'complete maximum-family census')
            census.append({'label':label,'N':len(family),'all_maximum_families':len(actual),'nodes':nodes})
        if label=='mixed triangle and other-mark pendant':
            require(M[0][0]==F(7,3),'explicit ordinary output exceeds cap')
            damages=damage_controls(family,C,M,out['s'])
            # Old-mark rotation and the private u/v swap are actual coordinate permutations.
            permutation={0:2,1:0,2:1,3:4,4:3,5:5}
            relabel=lambda A:sum(1<<permutation[i] for i in range(6) if A&(1<<i))
            other_family,other_C,other_M,other=construct(3,[(2,cube(2)),(0,cube(1))])
            lookup={A:i for i,A in enumerate(other_family)}
            require(all(M[i][j]==other_M[lookup[relabel(A)]][lookup[relabel(B)]] for i,A in enumerate(family) for j,B in enumerate(family)),'every transported original matrix entry')
            out['relabeling_positions']=len(family)**2
        out['elapsed_seconds']=time.monotonic()-t0;rows.append(out);signal.alarm(0)
        print(json.dumps({'label':label,'N':out['N'],'s':out['s'],'rank':out['lower_rank'],'seconds':out['elapsed_seconds']}),flush=True)
    result={'agent':'six-downset-1','role':'researcher','status':'finite exact validation of ordinary closure; uniformity rests on the written proof',
            'fixtures':rows,'maximum_family_censuses':census,'corruption_rejections':damages,
            'per_fixture_guard_seconds':60,'literal_n_guard':6,'literal_N_guard':80,
            'native_threads':1,'elapsed_seconds':time.monotonic()-start,
            'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:
        expected=json.loads(args.expected.read_text())
        require(stable(result)==stable(expected),'complete expected record')
    if args.write:args.write.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'fixtures':len(rows),'all_core_positions':sum(r['ordered_core_positions'] for r in rows),
                      'damages':len(damages),'censuses':len(census),'seconds':result['elapsed_seconds']}),flush=True)

def stable(value):
    if isinstance(value,dict):return {k:stable(v) for k,v in value.items() if k not in ('elapsed_seconds','peak_RSS_KiB')}
    if isinstance(value,list):return [stable(v) for v in value]
    return value

if __name__=='__main__':main()
