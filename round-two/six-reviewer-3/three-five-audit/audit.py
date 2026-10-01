"""Independent exact incidence audit of the complete three-five T/Q branch.

No researcher module or certificate is a mathematical runtime input.
Nine-edge subsets generate the complete labeled bipartite neighborhood domain;
path components complete links, and triangle sets check original fan quotas.
Continuous spherical coverage and the closed eta interval are in REVIEW.md.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations, permutations, product
import json
from math import comb
from pathlib import Path


def need(ok,message):
    if not ok:raise ValueError(message)


def digest(rows):
    return hashlib.sha256(json.dumps(sorted(rows),separators=(',',':')).encode()).hexdigest()


def edge(a,b):
    need(a!=b and type(a) is int and type(b) is int,'distinct actual edge endpoints')
    return frozenset((a,b))


def face(word):
    need(len(word) in (3,4) and len(set(word))==len(word)
         and all(type(x) is int for x in word),'simple actual face')
    return frozenset(word)


def link(known,degree,required):
    """A disjoint collection of paths can extend; a smaller cycle cannot."""
    known=set(known);required=set(required)
    if len(known)>degree or degree<3:return False
    graph={v:set() for v in known}
    for e in required:
        if len(e)!=2 or not e<=known:return False
        a,b=e;graph[a].add(b);graph[b].add(a)
    if any(len(x)>2 for x in graph.values()):return False
    unseen=set(known)
    while unseen:
        start=min(unseen);stack=[start];component=set()
        while stack:
            v=stack.pop()
            if v in component:continue
            component.add(v);unseen.discard(v);stack.extend(graph[v]-component)
        if len(component)>1 and all(len(graph[v])==2 for v in component):
            if len(component)!=degree:return False
    return True


def cycles(vertices):
    """Undirected complete cycles from edge sets, not vertex permutations."""
    vertices=set(vertices);n=len(vertices);out=[]
    for es in combinations([edge(a,b) for a,b in combinations(sorted(vertices),2)],n):
        degrees=Counter(v for e in es for v in e)
        if set(degrees)!=vertices or any(d!=2 for d in degrees.values()):continue
        if link(vertices,n,es):out.append(frozenset(es))
    return out


def triangles(words):
    return {face(w) for w in words}


def quota(ts,ceiling):
    counts=Counter(v for t in ts for v in t)
    return all(counts[v]<=ceiling[v] for v in counts)


def profiles():
    rows=[(k,f1,f2,a,b) for k,f1,f2,a,b in product(range(3),range(4),range(4),range(7),range(4))
          if k+f1+f2==3 and a+2*b+f1+2*f2==6 and a+b<=9]
    return sorted(rows,key=lambda x:(x[0],x[2],x[4]))


def classification(rows,k,f1,f2,a,b):
    ns=[set(x) for x in rows];m=a+b+f1+f2
    if any(len(ns[i]&ns[j])>2 for i,j in combinations(range(3),2)):
        return 'COMMON_CONTACT'
    sets=[{u for u in range(3) if s in ns[u]} for s in range(m)]
    caps=[2]*a+[3]*b+[1]*f1+[2]*f2
    if any(len(s)>c for s,c in zip(sets,caps)):return 'QQ_SUPPLY'
    required=[set() for _ in sets]
    for supplier,us in enumerate(sets):
        forced=supplier<a or supplier>=a+b+f1
        if not forced or len(us)!=2:continue
        u,v=sorted(us);other=(ns[u]&ns[v])-{supplier}
        if len(other)!=1:return 'NO_SHARED_Q_OPPOSITE'
        opposite=next(iter(other));corner=edge(u,v)
        required[supplier].add(corner);required[opposite].add(corner)
    if any(not link(s,4 if j<a+b else 5,r) for j,(s,r) in enumerate(zip(sets,required))):
        return 'SEALED_LINK'
    need((k,f1,f2,a,b) in ((2,1,0,3,1),(1,2,0,2,1)),'complete residual census')
    return 'TWO_ORDINARY_NORMAL_FORM' if k==2 else 'ONE_ORDINARY_NORMAL_FORM'


def canonical_rows(rows,k,a,b,f1,f2):
    groups=[range(a),range(a,a+b),range(a+b,a+b+f1),range(a+b+f1,a+b+f1+f2)]
    variants=[]
    for us in permutations(range(3)):
        for words in product(*(list(permutations(g)) for g in groups)):
            image={v:w for group,word in zip(groups,words) for v,w in zip(group,word)}
            variants.append(tuple(tuple(sorted(image[s] for s in rows[u])) for u in us))
    return min(variants)


def neighborhoods():
    out=[];raw_total=0;edge_subsets=0
    for k,f1,f2,a,b in profiles():
        m=a+b+f1+f2;full=[];admitted=[];terminal=[];orbits=set();counts=Counter()
        for selected in combinations(range(3*m),9):
            edge_subsets+=1
            ns=[[],[],[]]
            for e in selected:ns[e%3].append(e//3)
            if any(len(x)!=3 for x in ns):continue
            rows=tuple(tuple(sorted(x)) for x in ns);tag=classification(rows,k,f1,f2,a,b)
            full.append((rows,tag));counts[tag]+=1
            if tag not in ('COMMON_CONTACT','QQ_SUPPLY'):admitted.append((rows,tag))
            if tag in ('TWO_ORDINARY_NORMAL_FORM','ONE_ORDINARY_NORMAL_FORM'):
                terminal.append(rows);orbits.add(canonical_rows(rows,k,a,b,f1,f2))
        raw=comb(m,3)**3 if m>=3 else 0
        need(len(full)==raw and len(full)==len({r[0] for r in full}),'complete nine-edge to row-domain bijection')
        raw_total+=raw
        out.append({'ordinary_fives':k,'f1':f1,'f2':f2,'a':a,'b':b,'ordinary_fours':9-a-b,
                    'raw_ordered_three_neighbor_triples':raw,'classifications':dict(sorted(counts.items())),
                    'full_row_records_sha256':digest(full),'admitted_records_sha256':digest(admitted),
                    'terminal_rows_sha256':digest(terminal),'role_orbits':sorted(orbits)})
    need(len(out)==19 and raw_total==30451,'complete census and original labeled raw domain')
    need(sum(x['classifications'].get('TWO_ORDINARY_NORMAL_FORM',0) for x in out)==36,'all two-ordinary entries')
    need(sum(x['classifications'].get('ONE_ORDINARY_NORMAL_FORM',0) for x in out)==12,'all one-ordinary entries')
    need(sum(len(x['role_orbits']) for x in out)==2,'exactly the two residual role patterns')
    return out,edge_subsets


def p_quota_two(x):
    ceiling=[0,0,0,1,1,1,0,3,4,4]+[2]*5;records=[];allowed=set()
    for p,m,k in permutations(set(range(15))-{x,0,7},3):
        if p in (5,6):continue
        ts=triangles([(7,x,p),(7,p,m),(7,m,k),(5,x,p)])
        need(sum(p in t for t in ts)==3,'three distinct Ts at P')
        valid=quota(ts,ceiling);records.append((p,m,k,valid))
        if valid:allowed.add(p)
    need(allowed=={8,9},'complete H-fan forces original ordinary P')
    return allowed,{'x':x,'proper_original_H_fan_assignments':len(records),
                    'entrywise_sha256':digest(records),'allowed_P_originals':sorted(allowed)}


def p_quota_one(x):
    ceiling=[0,0,0,1,1,0,3,3,4]+[2]*6;records=[];allowed=set()
    for p in set(range(15))-{x,0,2,5,6,7}:
        for m1 in set(range(15))-{x,p,0,6}:
            for m2 in set(range(15))-{x,p,2,7}:
                ts=triangles([(6,x,p),(6,p,m1),(7,x,p),(7,p,m2)])
                need(sum(p in t for t in ts)>=3,'two fans share at most one actual T')
                valid=quota(ts,ceiling);records.append((p,m1,m2,valid))
                if valid:allowed.add(p)
    need(allowed=={8},'both original H fans force sole ordinary five')
    return allowed,{'x':x,'proper_original_partial_fan_assignments':len(records),
                    'entrywise_sha256':digest(records),'allowed_P_originals':sorted(allowed)}


def x_reason(x,b,left,right,fives,diagonals):
    if x in {0,1,2,b}:return 'X_SELF_OR_OLD_B_NEIGHBOR'
    if edge(b,x) in diagonals:return 'X_CONTACT_Q_DIAGONAL'
    if len(set((b,0,left,x)))<4 or len(set((b,2,right,x)))<4:return 'X_REPEATED_Q_VERTEX'
    if x in fives:return 'X_FIVE_OPPOSITE_THREE'
    return 'X_ORDINARY_FOUR'


def two_terminal():
    ceilings=[0,0,0,1,1,1,0,3,4,4]+[2]*5;D={3,4,5,6}
    counts=Counter();records=[];prefixes=[];quotas=[];forced_link_records=[]
    for x in range(15):
        tag=x_reason(x,6,7,5,{8,9},{edge(6,3),edge(6,4)})
        counts[tag]+=1;records.append(('X',x,-1,-1,-1,tag))
        if tag!='X_ORDINARY_FOUR':continue
        allowed,qr=p_quota_two(x);quotas.append(qr)
        for r in range(15):
            if len(set((2,4,r,5)))<4:tag='R_REPEATED_Q_VERTEX'
            elif r==x:tag='R_REPEATED_ONE_T_LINK_CORNER'
            elif r in (0,1):tag='R_EXTRA_C_THREE_CONTACT'
            elif r in (7,8,9):tag='R_FIVE_OPPOSITE_THREE'
            elif r in D:
                es={edge(6,x),edge(5,r)};need(sum(len(e&D) for e in es)>2,'deficient R exceeds all non-three QQ ends')
                tag='R_DEFICIENT_QQ_DEBT'
            else:tag='R_ORDINARY_FOUR'
            counts[tag]+=1;records.append(('R',x,r,-1,-1,tag))
            if tag!='R_ORDINARY_FOUR':continue
            for p in range(15):
                if p in {x,5,6,7}:tag='P_SELF_OR_OLD_X_NEIGHBOR'
                elif p not in allowed:tag='P_THREE_TRIANGLES_AT_NONFIVE'
                else:
                    req={edge(2,x),edge(2,r),edge(x,p)};cs=[c for c in cycles((2,x,r,p)) if req<=c]
                    need(cs and all(edge(r,p) in c for c in cs),'actual degree-four C link forces last P-R sector')
                    forced_link_records.append((x,r,p,len(cs)));tag='P_ORDINARY_FIVE'
                counts[tag]+=1;records.append(('P',x,r,p,-1,tag))
                if tag!='P_ORDINARY_FIVE':continue
                prefixes.append((x,r,p))
                for y in range(15):
                    if len(set((5,p,y,r)))<4:tag='Y_REPEATED_Q_VERTEX'
                    elif edge(5,y) in {edge(5,2),edge(5,x)}:tag='Y_CONTACT_Q_DIAGONAL'
                    else:
                        need(ceilings[p]==4 and ceilings[r]==2,'opposite ordinary five/four mismatch')
                        tag='OPPOSITE_ORDINARY_FOUR_FIVE_CORNER'
                    counts[tag]+=1;records.append(('Y',x,r,p,y,tag))
    need(len(prefixes)==40 and counts['OPPOSITE_ORDINARY_FOUR_FIVE_CORNER']==400,'full two-ordinary alias cover')
    return {'canonical_classifications':dict(sorted(counts.items())),'entrywise_sha256':digest(records),
            'prefixes':prefixes,'full_original_H_fan_quota_audits':quotas,
            'forced_C_link_records_sha256':digest(forced_link_records)}


def alignment():
    names=('K','H1','X','H2','L');result=[]
    edges=[frozenset(e) for e in combinations(names,2)];required={frozenset(('H1','X')),frozenset(('H2','X'))}
    for es in combinations(edges,4):
        if not required<=set(es):continue
        ds=Counter(v for e in es for v in e)
        if ds!={'K':1,'L':1,'H1':2,'H2':2,'X':2}:continue
        graph={n:set() for n in names}
        for e in es:a,b=e;graph[a].add(b);graph[b].add(a)
        reached=set();stack=['K']
        while stack:
            v=stack.pop()
            if v in reached:continue
            reached.add(v);stack.extend(graph[v]-reached)
        if reached!=set(names):continue
        word=['K'];previous=None
        while len(word)<5:
            legal=graph[word[-1]]-({previous} if previous else set())
            need(len(legal)==1,'connected actual triangle path')
            previous=word[-1];word.append(next(iter(legal)))
        need(len(set(word))==5,'simple F fan path');result.extend((tuple(word),tuple(reversed(word))))
    need(len(result)==len(set(result))==4,'all four fan alignments')
    return sorted(result)


def one_terminal():
    ceiling=[0,0,0,1,1,0,3,3,4]+[2]*6
    counts=Counter();records=[];prefixes=[];quotas=[];sealed=[];forced=[]
    for x in range(15):
        tag=x_reason(x,5,6,7,{8},{edge(5,3),edge(5,4)})
        counts[tag]+=1;records.append(('X',x,-1,-1,-1,tag))
        if tag!='X_ORDINARY_FOUR':continue
        possible,qr=p_quota_one(x);quotas.append(qr)
        for p in range(15):
            if p in {x,5,6,7}:tag='P_SELF_OR_OLD_X_NEIGHBOR'
            elif p not in possible:tag='P_AT_LEAST_THREE_T_AT_NONFIVE'
            else:tag='P_UNIQUE_ORDINARY_FIVE'
            counts[tag]+=1;records.append(('P',x,p,-1,-1,tag))
        for k in range(15):
            tag='K_NOT_DISTINCT_ORDINARY_INTERNAL' if k==x or ceiling[k]!=2 else 'K_ORDINARY_FOUR'
            counts[tag]+=1;records.append(('K',x,k,-1,-1,tag))
            if tag!='K_ORDINARY_FOUR':continue
            for z in range(15):
                tag='Z_DEFICIENT_FOUR' if z in {3,4,5} else 'Z_NOT_DEFICIENT_FOUR_OPPOSITE'
                counts[tag]+=1;records.append(('Z',x,k,z,-1,tag))
                if tag!='Z_DEFICIENT_FOUR':continue
                for r in range(15):
                    if r in {0,6,8,x,k}:tag='R_REPEATED_H1_FAN_OR_CENTER'
                    elif ceiling[r]==0:tag='R_ZERO_T_FAN_ENDPOINT'
                    elif r==7:tag='R_FIVE_FIVE_Q_EDGE'
                    elif r==z:
                        req={edge(8,6),edge(6,r),edge(8,z)}
                        for fourth in set(range(15))-{8,6,r,k}:
                            need(not link({8,6,r,fourth},4,req),'sealed K link cannot take another actual neighbor')
                            sealed.append((x,k,z,r,fourth))
                        tag='SEALED_K_DEGREE_FOUR_LINK'
                    else:
                        req={edge(8,6),edge(6,r),edge(8,z)};cs=[c for c in cycles((8,6,r,z)) if req<=c]
                        need(cs and all(edge(r,z) in c for c in cs),'K remaining sector is Q')
                        es={edge(5,x),edge(k,z)};ends=sum(len(e&{3,4,5}) for e in es)
                        need(len(es)==2 and ends==2 and ends>1,'two actual QQ ends exceed residual budget one')
                        forced.append((x,k,z,r,len(cs)));prefixes.append((x,k,z,r));tag='TWO_DISTINCT_QQ_ENDS_EXCEED_ONE'
                    counts[tag]+=1;records.append(('R',x,k,z,r,tag))
    need(len(prefixes)==480,'all original one-ordinary QQ terminal aliases')
    return {'canonical_classifications':dict(sorted(counts.items())),'entrywise_sha256':digest(records),
            'final_QQ_prefixes_sha256':digest(prefixes),'two_original_fan_quota_audits':quotas,
            'full_F_fan_alignment_words':alignment(),'sealed_fourth_neighbor_checks':len(sealed),
            'sealed_fourth_neighbor_sha256':digest(sealed),'forced_K_link_sha256':digest(forced)}


def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c


def analytic():
    D=[F(1),F(2),F(-1)];square=mul(D,D)
    lhs=square[:];lhs[3]-=4;lhs[4]-=8
    P=[F(-1),F(-3),F(1),F(7)];rhs=[-x for x in mul([F(1),F(1)],P)]
    need(lhs==rhs,'cot(phi/2)^2-c exact numerator identity')
    need(mul([F(1),F(1)],[F(1),F(1),F(-4)])==[F(1),F(2),F(-3),F(-4)],'y-(pi-alpha) comparison identity')
    value=lambda c:7*c**3+c**2-3*c-1
    upper=F(13,20);need(value(upper)<0 and 21*F(1,2)**2+2*F(1,2)-3>0,'positive adjacent-five obstruction on whole interval')
    g=lambda c:4*c*c-c-1
    lo,hi=F(1,2),upper;need(g(lo)<0<g(hi),'eta unique positive root bracket')
    for _ in range(48):
        mid=(lo+hi)/2
        if g(mid)<0:lo=mid
        else:hi=mid
    scale=10**12
    low=(lo*scale).numerator//(lo*scale).denominator
    high=(hi*scale).numerator//(hi*scale).denominator+1
    need(g(F(low,scale))<0<g(F(high,scale)),'outward rational eta enclosure')
    return {'eta_polynomial_coefficients':[-1,-1,4],'eta_formula':'(1+sqrt(17))/8',
            'eta_decimal_bracket_numerators':[low,high],'eta_decimal_bracket_denominator':scale,
            'adjacent_five_numerator_coefficients':[int(x) for x in lhs],
            'P_at_13_over_20':str(value(upper)),'rho_phi_boundary_included':'deficient-five corners are strictly below phi, so reciprocal corners strictly exceed y even when y=pi-alpha',
            'left_boundary_included':'u+rho(u)<=A; a three pair is strictly greater than A, leaving the neighbor strictly below A'}


def degree_bound():
    counts=[];r4=[]
    for r in range(8):
        for f1,f2,a,b in product(range(r+1),range(r+1),range(7),range(4)):
            if f1+f2>r or a+2*b+f1+2*f2!=6 or a+b>15-2*r:continue
            capacity=2*a+4*b+f1+2*f2
            if 3*r>capacity:counts.append((r,f1,f2,a,b,'CAPACITY'));continue
            if r==4:
                need(f1==f2==0 and a+2*b==6,'complete equality case')
                if b>=2:reason='TWO_ZERO_T_FOURS_HAVE_FOUR_COMMON_THREES'
                elif b==0:reason='ONLY_ONE_ORDINARY_FOUR_CANNOT_SUPPLY_A_Q'
                else:reason='TWO_ORDINARY_FOURS_HAVE_FOUR_COMMON_FIVES'
                r4.append((a,b,1+b,reason));counts.append((r,f1,f2,a,b,reason))
            else:need(r<=3,'all r>=4 are excluded');counts.append((r,f1,f2,a,b,'NOT_EXCLUDED_BY_UPPER3'))
    need(len(r4)==4,'all four saturated r4 count cases')
    return {'complete_count_rows':len(counts),'all_row_classification_sha256':digest(counts),'r4_equality_cases':r4,
            'scope':'self-contained upper3 on closed eta interval; no lower bound on r or full old7817 catalogue verdict'}


def controls():
    rejected=0
    for action in (lambda:edge(2,2),lambda:edge(0,True),lambda:face((0,1,1,3)),lambda:face((0,1,2,True))):
        try:action()
        except ValueError:rejected+=1
        else:raise ValueError('bad original identity accepted')
    need(not link({0,1,2,3},4,{edge(0,1),edge(1,2),edge(2,0)}),'sealed triangle negative control');rejected+=1
    need(not link({0,1,2,3},4,{edge(0,1),edge(0,2),edge(0,3)}),'branching link negative control');rejected+=1
    need(not link({0,1,2,3,4},4,set()),'degree-excess negative control');rejected+=1
    need(not link({0,1,2},4,{edge(0,4)}),'nonneighbor corner negative control');rejected+=1
    need(not quota(triangles([(0,1,2),(0,2,3),(0,3,4)]),[2]*5),'three Ts at ordinary four negative control');rejected+=1
    need(sum(len(e&{3,4,5}) for e in {edge(5,9),edge(10,5)})==2,'two incidences at same deficient point remain two');rejected+=1
    need(link({0,1,2,3},4,{edge(0,1),edge(1,2),edge(2,3)}),'positive extendable link')
    need(quota(triangles([(0,1,2),(0,2,3)]),[2]*4),'positive saturated two-T quota')
    need(rejected==10,'ten damaged or false mathematical controls')
    return rejected


def main():
    neighborhoods_result,batches=neighborhoods()
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','status':'VERIFIED',
            'method':'global nine-edge subsets; path-component links; triangle-set incidence; complete actual alias schemas',
            'censuses':neighborhoods_result,'raw_nine_edge_subsets':batches,
            'two_ordinary_original_aliases':two_terminal(),'one_ordinary_original_aliases':one_terminal(),
            'analytic_closed_interval':analytic(),'self_contained_degree_bound':degree_bound(),'damaged_controls':controls(),
            'trust':'ordinary spherical completeness and global-to-local coverage unformalized; exact standard-library Python; older k3 theorem imported through scoped prior8953 review'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);args=p.parse_args();record=main()
    if args.output:args.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':record['status'],'complete_evidence_sha256':hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'raw_triples':sum(x['raw_ordered_three_neighbor_triples'] for x in record['censuses']),'damaged_controls':record['damaged_controls']},sort_keys=True))
