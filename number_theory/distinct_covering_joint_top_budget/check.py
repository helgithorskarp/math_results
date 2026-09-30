"""Solver-free controls for the written joint/known-footprint reduction."""
import argparse,hashlib,json
from pathlib import Path
from math import gcd,lcm
from joint import (joint_budget,literal_maximum,actual_score,known_bound,
                   periodic_known_footprint,require,divisors)


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def cover_check(N,classes,minimum=2):
    require(len({n for n,a in classes})==len(classes), 'Repeated covering modulus')
    require(all(n>=minimum and N%n==0 and 0<=a<n for n,a in classes), 'Covering domain')
    require(all(any(x%n==a for n,a in classes) for x in range(N)), 'False positive cover')


def summary(J):
    return {key:J[key] for key in ['joint_budget','periodic_budget','separate_top_budget',
            'ordinary_top_capacity','winning_partition','actual_witness_phases']}


def run():
    identity=[]
    fixtures=[
     (5,6,1,'nonperiodic',[(x*x+3)%7 for x in range(30)],[(2*z+1)%5 for z in range(6)]),
     (4,15,2,'point_plus_odd',[int(x==1) for x in range(60)],[int(x%2) for x in range(30)]),
     (4,15,2,'unrestricted_only',[(x*x+5*x+1)%9 for x in range(60)],[0]*30),
     (4,15,2,'periodic_only',[0]*60,[(x*x+7*x+3)%8 for x in range(30)]),
     (3,8,1,'prime_cube',[(x*x+3*x)%7 for x in range(24)],[(3*z+1)%5 for z in range(8)]),
     (3,4,1,'prime_square',[(x*x+2)%6 for x in range(12)],[(z*z+1)%4 for z in range(4)])]
    W=[[2,0,0],[0,3,0],[2,0,0],[0,0,0]]
    fixtures.append((9,4,3,'attributed_coarsest_comparison',[0]*36,[W[x%4][x%3] for x in range(12)]))
    for B,C,b,name,u,v in fixtures:
        J=joint_budget(B,C,b,u,v);literal=literal_maximum(B,C,b,u,v)
        require(J['joint_budget']==literal['maximum'], 'Actual phase maximum differs')
        require(actual_score(B,C,b,u,v,literal['attaining_phases'])==literal['maximum'], 'Literal witness fails')
        identity.append({'B':B,'C':C,'b':b,'name':name,'u_sha256':digest(u),'v_sha256':digest(v),
                         'joint':summary(J),'literal':literal})
    H={d:[max(sum(W[z][t] for z in range(r,4,d)) for r in range(d)) for t in range(3)] for d in [2,4]}
    M={d:max(vals) for d,vals in H.items()}
    G=max(sum(max(M[d],2*H[d][t]) for d in H) for t in range(3))
    require(identity[-1]['joint']['joint_budget']==10 and G==12 and 2*sum(M.values())==14,
            'Attributed six-covering-3 comparison')

    cover=[(2,0),(3,0),(4,1),(6,1),(12,11)];supported=[];affine=[]
    for N,B,C,b in [(60,4,15,2),(216,8,27,4)]:
        cover_check(N,cover)
        for shift in range(3):
            shifted=[(n,(a+shift)%n) for n,a in cover];cover_check(N,shifted)
            A=shifted[:2]
            for k in range(3):
                u=[0 if any(x%n==a for n,a in A) else (x*x+3*x+5*k+shift)%7 for x in range(N)]
                v=[0 if any(x%n==a for n,a in A) else (x*x+7*x+k+2)%11 for x in range(b*C)]
                e=known_bound(B,C,b,A,u,v,minimum=2)
                require(e['capacity']>=e['demand'] and all(w==0 for n,w in e['known_footprints']), 'Supported cover false cut')
                supported.append({'N':N,'shift':shift,'case':k,'demand':e['demand'],'capacity':e['capacity']})
    for N,B,C,b,A in [(60,4,15,2,[(2,0)]),(60,4,15,2,[(3,0)]),
                     (60,4,15,2,[(2,0),(3,0),(6,1)]),(24,3,8,1,[(2,0),(4,1)])]:
        cover_check(N,cover);Q=b*C;S={B*d for d in divisors(C)}
        for seed in range(6):
            u=[0 if any(x%n==a for n,a in A) else (x*x+seed*x+2*seed)%7 for x in range(N)]
            v=[1+(x*x+2*seed*x+seed)%11 for x in range(Q)]
            e=known_bound(B,C,b,A,u,v,minimum=2)
            literal_known=[[m,sum(v[x%Q] for x in range(a,N,m))] for m,a in A]
            require(e['known_footprints']==literal_known, 'Literal known footprint differs')
            require(e['demand']==sum(u)+sum(v)*(N//Q)-sum(w for m,w in literal_known), 'Affine demand multiplicity')
            actual_outside=sum(sum(u[a::m])+sum(v[x%Q] for x in range(a,N,m))
                               for m,a in cover if m not in dict(A) and m not in S)
            require(e['demand']<=actual_outside+e['joint']['joint_budget'], 'Actual genuine completion false cut')
            require(e['demand']<=e['capacity'], 'Affine cover false cut')
            affine.append({'N':N,'known':A,'seed':seed,'demand':e['demand'],
                           'actual_outside_plus_joint':actual_outside+e['joint']['joint_budget'],
                           'known_periodic_mass':sum(w for m,w in literal_known)})

    roots=[]
    for N,B,b in [(10080,288,48),(15120,432,72)]:
        e=known_bound(B,35,b,[(8,0)],[int(x==1) for x in range(N)],
                      [int(x%8!=0) for x in range(b*35)])
        require(e['joint']['joint_budget']==28 and e['ordinary_capacity']-e['capacity']==24 and
                e['capacity']>e['demand'], 'Root strengthening is not an exclusion')
        roots.append({'N':N,'demand':e['demand'],'ordinary_capacity':e['ordinary_capacity'],
                      'previous_mixed_capacity':e['separate_mixed_capacity'],'capacity':e['capacity'],
                      'joint':summary(e['joint'])})
    v=[1+(x*x+3*x)%19 for x in range(216)]
    known=periodic_known_footprint(15120,v,35,17);D=70*sum(v)
    require(35*known==D and known==sum(v[x%216] for x in range(17,15120,35)), 'Coprime35 identity')

    fixture_path=Path(__file__).with_name('positive_cover.json');raw=fixture_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()=='f3b7ab8112f2fdba3ab32ea992f2380c43c404e8b54c8abdd71c839a9f5424e3', 'Attributed cover bytes changed')
    fixture=json.loads(raw);N=fixture['lcm'];classes=[(n,a) for a,n in fixture['congruences']]
    cover_check(N,classes,minimum=8)
    require(N==lcm(*(n for n,a in classes))==20160 and min(n for n,a in classes)==8, 'Attributed actual LCM/minimum')
    # A coprime known35 class is present. The old zero-support periodic model
    # would have only the zero vector at Q144; the affine model retains it.
    B,C,b,Q=2240,9,16,144;A=classes[:15];external=[]
    require(any(n==35 for n,a in A) and gcd(Q,35)==1, 'External coprime35 fixture')
    for k in range(3):
        u=[0 if any(x%n==a for n,a in A) else (x*x+5*k*x+3)%7 for x in range(N)]
        v=[1+(x*x+7*k*x+2)%11 for x in range(Q)]
        e=known_bound(B,C,b,A,u,v)
        require(e['demand']<=e['capacity'], 'Published20160 cover false cut')
        require(all(w>0 for n,w in e['known_footprints']), 'Periodic weight accidentally forced to zero')
        require(dict(e['known_footprints'])[35]*35==sum(v)*(N//Q), 'External coprime cost')
        external.append({'case':k,'demand':e['demand'],'capacity':e['capacity'],
                         'periodic_demand':sum(v)*(N//Q),'known35_footprint':dict(e['known_footprints'])[35]})

    bad=0
    for args in [(4,15,4,[0]*60,[0]*60),(4,15,2,[-1]*60,[0]*30),(4,15,2,[True]*60,[0]*30),
                 (4,15,2,[0]*59,[0]*30),(6,15,1,[0]*90,[0]*15),(4,12,2,[0]*48,[0]*24)]:
        try:joint_budget(*args)
        except ValueError:bad+=1
        else:raise ValueError('Malformed top input accepted')
    for A in [[(4,1)],[(2,0),(2,1)],[(2,2)]]:
        try:known_bound(4,15,2,A,[0]*60,[1]*30,minimum=2)
        except ValueError:bad+=1
        else:raise ValueError('Malformed known input accepted')
    try:known_bound(4,15,2,[(2,0)],[1]*60,[1]*30,minimum=2)
    except ValueError:bad+=1
    else:raise ValueError('Unsupported unrestricted input accepted')
    return {'agent':'six-covering-2','role':'researcher','all_passed':True,'identities':identity,
            'actual_phase_tuples_checked':sum(e['literal']['actual_phase_tuples'] for e in identity),
            'supported_cover_cases':supported,'affine_cover_cases':affine,'roots':roots,
            'coarsest_comparison':{'F':10,'G':G,'doubled_sum':14,'author':'six-covering-3','graph_height':7516},
            'coprime35':{'N':15120,'Q':216,'demand':D,'known_footprint':known},
            'external_20160':{'file_sha256':hashlib.sha256(raw).hexdigest(),'classes':len(classes),
                               'known_classes':classes[:15],'B':B,'C':C,'b':b,'Q':Q,'cases':external},
            'malformed_inputs_rejected':bad,
            'scope':'Written joint and affine reduction; no new global numerical bound'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write-expected',action='store_true');a=parser.parse_args()
    result=json.loads(json.dumps(run()));path=Path(__file__).with_name('expected.json')
    if a.write_expected:path.write_text(json.dumps(result,indent=2)+'\n')
    else:require(result==json.loads(path.read_text()), 'Expected evidence differs')
    print(json.dumps({'all_passed':True,'actual_phase_tuples_checked':result['actual_phase_tuples_checked'],
                      'genuine_cover_cases':len(result['supported_cover_cases'])+len(result['affine_cover_cases'])+
                                             len(result['external_20160']['cases']),
                      'malformed_inputs_rejected':result['malformed_inputs_rejected'],'scope':result['scope']}))
