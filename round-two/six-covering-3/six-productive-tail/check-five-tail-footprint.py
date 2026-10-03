"""Independent physical2520 AP audit of EVERY original phase/coupled row."""
from pathlib import Path
from itertools import combinations
from math import gcd,lcm
from hashlib import sha256
import argparse,json,mmap,struct,time


def require(test,message):
    if not test:raise ValueError(message)


parser=argparse.ArgumentParser();parser.add_argument('--data',type=Path,required=True)
args=parser.parse_args();data=args.data
started=time.monotonic()
source=json.loads((data/'result.json').read_text())
D=sorted(3**i*5**j*7**k for i in range(3) for j in range(2) for k in range(2))
require(source['divisors']==D,'Original odd divisor inventory differs')
P=[(8,0),(9,0),(10,1),(14,1),(12,10)]
R={r:sum(1<<x for x in range(r,2520,8) if all(x%n!=a for n,a in P)) for r in range(1,8)}
rep={'O':1,'E2':2,'E4':4}
kind=lambda r:'O' if r%2 else ('E4' if r==4 else 'E2')
A={};M={};CRT_phase_checks=0
for r in range(1,8):
    A[r]={};M[r]={}
    oddholes=sum(1<<(x%315) for x in range(r,2520,8) if R[r]>>x&1)
    representative=rep[kind(r)]
    representativeholes=sum(1<<(x%315) for x in range(representative,2520,8) if R[representative]>>x&1)
    require(oddholes==representativeholes,'Physical P-complement type identification fails')
    for d in D:
        masks=[]
        for a in range(d):
            phase=r+8*((a-r)*pow(8,-1,d)%d) if d!=1 else r
            mask=sum(1<<x for x in range(phase,2520,8*d))
            require(sum(1<<(x%315) for x in range(phase,2520,8*d))==sum(1<<y for y in range(a,315,d)),
                    'Original projected phase CRT map differs')
            masks.append(mask);CRT_phase_checks+=1
        A[r][d]=masks
        M[r][d]=max((R[r]&mask).bit_count() for mask in masks)
        require(M[r][d]==source['single_projection_maxima'][kind(r)][str(d)],'Literal single projection marginal differs')
require(CRT_phase_checks==4368,'Incomplete physical parent/phase CRT audit')
require(sum(R[r].bit_count() for r in R)==1398,'Literal total P-complement differs')
S={};star_audits=[]
for item in source['stars']:
    t=item['parent_type'];r=rep[t]
    tuples=[(u,v,w) for u in D for v,w in combinations([d for d in D if d!=u],2)]
    require(len(tuples)==660 and item['triples']==660,'Original star triple inventory differs')
    expected_phases=sum(u*(v//gcd(u,v))*(w//gcd(u,w)) for u,v,w in tuples)
    path=data/('star-'+t+'.bin')
    require(path.stat().st_size==14*expected_phases and expected_phases==644512,'Phase stream incomplete/extra')
    table={};rows=[];offset=0
    with path.open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as raw:
        for u,v,w in tuples:
            guv,guw=gcd(u,v),gcd(u,w)
            nv,nw=v//guv,w//guw
            best=-1;witness=None
            for au in range(u-1,-1,-1):
                singleton=R[r]&A[r][u][au]
                for iv in range(nv-1,-1,-1):
                    av=au%guv+guv*iv
                    for iw in range(nw-1,-1,-1):
                        aw=au%guw+guw*iw
                        hit=(singleton&(A[r][v][av]|A[r][w][aw])).bit_count()
                        index=offset+au*nv*nw+iv*nw+iw
                        expected=(u,v,w,au,av,aw,hit)
                        require(struct.unpack_from('<7H',raw,14*index)==expected,'Original phase field differs at '+t+':'+str(index))
                        phase=[au,av,aw]
                        if hit>best or (hit==best and (witness is None or phase<witness)):
                            best,witness=hit,phase
            offset+=u*nv*nw;table[(u,v,w)]=best
            rows.append([u,v,w,best,*witness])
        digest=sha256(raw).hexdigest()
    require(offset==expected_phases and item['phase_records']==offset and item['all_phase_records_sha256']==digest
            and rows==item['maxima_rows'],'Complete star maxima/phase trace differs')
    S[t]=table
    star_audits.append({'parent_type':t,'complete_original_triples':660,'complete_phase_records':offset,
                        'all_phase_records_sha256':digest,'all_fields_equal':True,'maximum_star':max(table.values())})
require(set(S)==set(rep) and len(source['stars'])==3,'Missing/duplicated star parent type')
types=['O','E2','E4']
states=[(r,t) for r in types for t in types if (r,t)!=('E4','E4')]
actual_states={(kind(r),kind(t)) for r in range(1,8) for t in range(1,8) if r!=t}
require(set(states)==actual_states and [list(x) for x in states]==source['ordered_parent_types'],'Ordered actual-parent state domain differs')
coupled=[]
for item in source['coupled_label_cases']:
    family=item['kind'];require(family in ('mixed','all16'),'Unsupported three-class family')
    rows=0;maximum=[-1]*8;witnesses=[None]*8
    path=data/(family+'.bin')
    with path.open('rb') as stream:
        for p,q in combinations(D,2):
            for u in [d for d in D if d not in (p,q)]:
                available=D if family=='mixed' else [d for d in D if d not in (p,q,u)]
                for v,w in combinations(available,2):
                    originals=[16*p,16*q,16*u,*([32*v,32*w] if family=='mixed' else [16*v,16*w])]
                    require(len(set(originals))==5,'Repeated original modulus in coupled case')
                    caps=[M[rep[r]][lcm(p,q)]+(M[rep[t]][lcm(u,v,w)] if family=='mixed' else S[t][(u,v,w)]) for r,t in states]
                    raw=stream.read(26)
                    require(len(raw)==26 and struct.unpack('<13H',raw)==tuple([p,q,u,v,w,*caps]),'Coupled original-label field differs at '+family+':'+str(rows))
                    for i,value in enumerate(caps):
                        if value>maximum[i]:maximum[i],witnesses[i]=value,[p,q,u,v,w]
                    rows+=1
        require(stream.read(1)==b'','Extra coupled original-label record')
    expected=43560 if family=='mixed' else 23760
    digest=sha256(path.read_bytes()).hexdigest()
    require(rows==expected and item['complete_original_label_records']==rows
            and item['all_records_sha256']==digest and item['ordered_parent_type_maxima']==maximum
            and item['original_cofactor_witnesses']==witnesses,'Complete coupled summary differs')
    coupled.append({'kind':family,'complete_original_label_records':rows,'all_records_sha256':digest,
                    'ordered_parent_type_maxima':maximum,'all_fields_equal':True})
require(len(coupled)==2 and {x['kind'] for x in coupled}=={'mixed','all16'},'Missing coupled family')
maximum=max(max(x['ordered_parent_type_maxima']) for x in coupled)
require(maximum==source['maximum_five_class_footprint_candidate'],'Combined capacity differs')
# A concrete abstract P-uncovered demand, not a completed BASE-hole witness.
H2=set(range(2,2520,24));H4={x for x in range(4,2520,40) if x%9!=0};H=H2|H4
classes=[(16,2),(48,26),(80,4),(32,12),(160,124)]
require(len(H2)==105 and len(H4)==56 and len(H)==161,'Abstract demand count differs')
require(all(all(x%n!=a for n,a in P) for x in H),'Abstract demand intersects P')
require(len({n for n,a in classes})==5 and all(0<=a<n for n,a in classes),'Original labels/phase domains malformed')
lifts={x+2520*j for x in H for j in range(4)}
covered={x for n,a in classes for x in range(a,10080,n)}
require(lifts<=covered and all(any(x%n==a for x in lifts) for n,a in classes),'Abstract five-class repair is incomplete/unproductive')
bad=[(n,44 if n==160 else a) for n,a in classes]
badcovered={x for n,a in bad for x in range(a,10080,n)}
require(len(lifts-badcovered)==56,'Same-half32 damage was not detected by actual lifts')
repeated=[(16,2),(16,10),(80,4),(32,12),(160,124)]
require(len({n for n,a in repeated})<5,'Repeated original-label damage was not detected')
Pcovered={x for n,a in P for x in range(a,10080,n)}
remaining=len(set(range(10080))-Pcovered-covered)
require(remaining>0,'Abstract demand was accidentally a full cover')
result={'agent':'six-covering-3','role':'researcher','status':'PRIVATE_AUTHOR_CHECKED_LITERAL_AP_COMPLETE',
        'literal_P_parent_points':{str(r):R[r].bit_count() for r in R},
        'complete_original_phase_CRT_checks':CRT_phase_checks,'actual_ordered_parent_pairs':42,
        'projected_parent_type_states':[list(x) for x in states],'star_audits':star_audits,
        'complete_star_phase_records':sum(x['complete_phase_records'] for x in star_audits),
        'coupled_audits':coupled,'five_productive_footprint_upper':maximum,
        'abstract_P_uncovered_demand_holes':161,'abstract_demand_lifts':len(lifts),
        'abstract_five_original_classes':classes,'same_half32_damage_uncovered_lifts':56,
        'abstract_P_plus_TAIL_uncovered_physical_points':remaining,
        'actual_completed_BASE_H_witness_claimed':False,'uniform_six_TAIL_claimed':False,
        'external_review':False,'ordinary_case_completeness_bridges_unformalized':True,
        'seconds':time.monotonic()-started}
print(json.dumps(result,indent=2))
