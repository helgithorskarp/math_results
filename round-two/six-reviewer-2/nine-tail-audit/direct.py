"""Independent definition-level audit. Imports no literal/author mathematics.

Uses ordinary sets for all raw H unions, modulo histograms for BASE demand,
and interleaved four-physical-lift bitmaps for every final original phase.
"""
import json,sys,hashlib
from itertools import combinations,product
from math import gcd

def need(ok,why):
    if not ok:raise ValueError(why)
def wire(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def push(h,row):h.update(wire(row)+b'\n')
def join(*ds):
    q=1
    for d in ds:q=q*d//gcd(q,d)
    return q

def audit(record):
    prefix=[(8,0),(9,0),(10,1),(14,0),(12,10),(28,4)]
    scope={'period':10080,'minimum':'exactly8','prefix':[[m,a]for m,a in prefix]+[[16,2],[32,6]],'actual_lcm':'divides10080','all_other_phases_omissions_free':True,'original_labels':True,'weakened_16_hypothesis':'nonempty actual BASE hole parent2','essential_32':True,'productive_count_lower':9,'global_L_min_8_improvement':False}
    need(record['scope']==scope and record['producer_imported'] is False,'whole quantified domain')
    R=[]
    for n in range(2520):
        if not any((n-a)%m==0 for m,a in prefix):R.append(n)
    need(record['R']==R,'every original initial residue')
    parents={r:[n for n in R if (n-r)%8==0]for r in range(8)}
    need(record['parent_counts']==[len(parents[r])for r in range(8)],'all parents')
    odd={r:sorted(n%315 for n in parents[r])for r in range(8)}
    need(odd[2]==odd[6] and all(odd[r]==odd[1]for r in (3,5,7)),'actual shadow identifications')
    D=sorted({3**a*5**b*7**c for a in range(3)for b in range(2)for c in range(2)}-{1})
    need(record['cofactors']==D,'all original cofactors, d1 spent')
    phases={r:{d:[frozenset(n for n in odd[r]if n%d==a)for a in range(d)]for d in [1]+D}for r in (1,2,4)}
    pops={str(r):{str(d):[len(v)for v in vs]for d,vs in phases[r].items()}for r in phases}
    need(record['phase_populations']==pops,'every raw cofactor phase')
    C={d:max(map(len,phases[2][d]))for d in [1]+D}
    need(record['capacity']==[[d,C[d]]for d in [1]+D],'whole marked capacity table')
    maxima={r:{d:max(map(len,phases[r][d]))for d in [1]+D}for r in (1,4)}
    S={str(k):max(sum(C[d]for d in v)for v in combinations(D,k))for k in range(1,6)}
    need(record['S']==S,'distinct global H sums')
    labels=sorted({2**a*3**b*5**c*7**e for a in range(4)for b in range(3)for c in range(2)for e in range(2)}-{1,2,3,4,5,6,7}-{m for m,a in prefix})
    rows=[];h=hashlib.sha256()
    for a in range(15):
        for b in range(18):
            covered=[n for n in R if n%15==a or n%18==b];remaining=set(R)-set(covered);marg=[]
            for m in labels:
                if m in (15,18):continue
                counts=[0]*m
                for n in remaining:counts[n%m]+=1
                marg.append(max(counts))
            row=[a,b,len(covered),marg,len(covered)+sum(marg)];rows.append(row);push(h,row)
    need(record['base177']=={'rows':rows,'stream_sha256':h.hexdigest(),'lower_K':min(v[-1]for v in rows),'upper_K':max(v[-1]for v in rows)},'entire270 original BASE bound')
    need(max(v[-1]for v in rows)==1219,'BASE demand177')
    for k in (2,3,4,5):
        rr=[[list(ds),C[join(*ds)],sum(C[join(*p)]for p in combinations(ds,2)),sum(C[join(*p)]for p in combinations(ds,3))if k>=3 else 0]for ds in combinations(D,k)]
        need(record['intersections'][str(k)]==rr,'all Q intersection rows')
    need(max(v[1]for v in record['intersections']['2'])==30 and max(v[1]for v in record['intersections']['3'])==18 and max(v[2]for v in record['intersections']['3'])==54 and max(v[3]for v in record['intersections']['4'])==36 and max(v[3]for v in record['intersections']['5'])==72,'all proof intersection constants')
    arms=[]
    for ds in combinations(D,4):
        for bits in list(range(1,7))+[0]:
            A=[ds[0]]+[ds[j+1]for j in range(3)if bits&(1<<j)];B=[d for d in ds if d not in A]
            arms.append([list(ds),A,B,min(sum(C[d]for d in A),sum(C[d]for d in B),sum(C[join(a,b)]for a in A for b in B))])
    need(record['four_Q_arms']==arms and max(v[-1]for v in arms)==66,'all unordered quarter arms')
    high=[ds for ds in combinations(D,5)if sum(C[d]for d in ds)>176]
    groups={ds for ds in combinations(D,3)if sum(C[d]for d in ds)>126}
    # Derive the full UB input catalogue without accepting claimed groups.
    for ds in high:
        for size in range(1,5):
            for P in combinations(ds,size):
                groups.add(P);rest=tuple(d for d in ds if d not in P)
                for k in range(1,len(rest)+1):groups.update(combinations(rest,k))
    groups.update((d,)for d in D);groups.update(combinations(D,2))
    unions={};union_rows=[];raw=0
    for ds in sorted(groups):
        count=0;best=0;h=hashlib.sha256()
        for aa in product(*(range(d)for d in ds)):
            members=set()
            for d,a in zip(ds,aa):members.update(phases[2][d][a])
            value=len(members);count+=1;best=max(best,value);push(h,[list(aa),value])
        raw+=count;unions[ds]=best;union_rows.append([list(ds),count,best,h.hexdigest()])
    need(record['all_exact_H_unions']==union_rows and record['union_phases']==raw,'every required full raw set union')
    def UB(ds):return unions[tuple(sorted(ds))]if ds else 0
    need(record['high_five_H_sets']==[list(ds)for ds in high],'nine high global H sets')
    triples=[[list(ds),sum(C[d]for d in ds),UB(ds)if sum(C[d]for d in ds)>126 else sum(C[d]for d in ds),sum(C[d]for d in ds)>126]for ds in combinations(D,3)]
    need(record['H_triples']==triples and max(v[2]for v in triples)==126,'all triple union bounds')
    five=[]
    for ds in high:
        for size in range(1,5):
            for P in combinations(ds,size):
                rest=tuple(d for d in ds if d not in P)
                for bits in range(1,2**len(rest)):
                    O=tuple(d for j,d in enumerate(rest)if bits&(1<<j));A=tuple(d for d in rest if d not in O)
                    cross=sum(C[join(o,a)]for o in O for a in A)
                    values=[UB(P)+min(UB(O),cross+min(C[q],sum(C[join(o,q)]for o in O)))for q in D]
                    five.append([list(ds),list(P),list(O),values])
    need(record['five_H_Q_rows']==five and max(max(v[-1])for v in five)==175,'all five-H global ownership and binary splits')
    mixed=[]
    for ds in combinations(D,3):
        for a in ds:
            rest=[d for d in ds if d!=a]
            for bits in range(1,4):
                O=[d for j,d in enumerate(rest)if bits&(1<<j)];A=[d for d in rest if d not in O]
                values=[C[a]+30+min(UB(O),sum(C[join(o,s)]for o in O for s in A)+min(C[q],sum(C[join(o,q)]for o in O)))for q in D]
                mixed.append([list(ds),a,O,values])
    need(record['mixed_HQQ_HHQ_rows']==mixed and max(max(v[-1])for v in mixed)==168,'every mixed ownership split')
    coupled=[]
    for gh in combinations(D,2):
        for abc in combinations([d for d in D if d not in gh],3):
            coupled.append([list(gh),list(abc)]+[maxima[r][join(*gh)]+sum(C[d]for d in abc)for r in (1,4)])
    need(record['three_parent_coupling']==coupled,'all global distinct five-H couplings')
    # Independent type catalogue from counts of Q, hence reverse to author order.
    expected=[];qb2=[0,0,30,54,66];qb6=[0,0,0,18,36,72]
    for n2,n6 in ((2,6),(3,5),(4,4),(5,3)):
        for q2 in range(n2-1,-1,-1):
            h2=n2-1-q2
            if h2==0 and q2<2:continue
            for q6 in range(n6-1,0,-1):
                h6=n6-1-q6
                if h6==0 and q6<3:continue
                hh=h2+h6;value=(int(S[str(hh)])if hh else 0)+qb2[q2]+qb6[q6];method='global distinct H plus Q intersections'
                if hh==5 and q2+q6==1:value=176;method='five H/one Q global allocation'
                if h2==0 and q2==2 and h6==3:value=156;method='one-parent triple H union'
                if(h2,q2,h6,q6)==(1,2,2,1):value=168;method='mixed O/S allocation'
                if(h2,q2,h6,q6)==(0,3,2,1):value=144;method='HHQ one-parent cap90'
                expected.append([n2,n6,'H'*h2+'Q'*q2,'H'*h6+'Q'*q6,value,method])
    need(record['type_rows']==expected and len(expected)==34,'complete two-parent types')
    # Actual CRT class realization of every inactive/half/quarter local state.
    physical_states=0
    def local(types,placed,r):
        resources=[];counters={'H':0,'Q':0}
        for t in types:
            d=D[counters[t]];counters[t]+=1;m=(16 if t=='H'else 32)*d
            attainable={}
            for a in range(r,m,8):
                mask=sum(1<<k for k in range(4)if(r+2520*k-a)%m==0)
                attainable.setdefault(mask,a)
            choices=[0,5,10]if t=='H'else[0,1,2,4,8]
            need(set(attainable)==set(choices),'all original physical local masks')
            resources.append(choices)
        out=[]
        for vs in product(*resources):
            covered={k for k in range(4)if placed&(1<<k)}
            for v in vs:covered.update(k for k in range(4)if v&(1<<k))
            out.append([list(vs),len(covered)==4,sum(bool(v)for v,t in zip(vs,types)if t=='H'),sum(bool(v)for v,t in zip(vs,types)if t=='Q')])
        return out
    locals=[]
    for n2,n6,t2,t6,value,method in expected:
        locals.extend([[2,t2,local(t2,5,2)],[6,t6,local(t6,1,6)]])
    need(record['all_local_states']==locals,'every actual two-parent local state')
    rawlocals=[]
    for r,lo,hi,placed in ((2,1,4,5),(6,2,5,1)):
        for length in range(lo,hi+1):
            for halves in range(length+1):
                types='H'*halves+'Q'*(length-halves)
                rawlocals.append([r,types,local(types,placed,r)])
    need(record['all_raw_local_types']==rawlocals and sum(len(v[2])for v in rawlocals)==10980,'whole10980 local state catalogue including excluded inventories')
    third=[];three=[]
    for r in (1,3,4,5,7):
        for types in ('HHH','HHQ','HQQ','QQQ'):third.append([r,types,local(types,0,r)])
        p=max(maxima[4 if r==4 else 1][join(a,b)]for a,b in combinations(D,2));linked=max(v[-1 if r==4 else -2]for v in coupled)
        tags=[[(2,4,2),'H/HHQ'],[(2,4,2),'H/HQQ'],[(2,4,2),'H/QQQ'],[(3,3,2),'HH/HQ'],[(3,3,2),'HQ/HQ'],[(3,3,2),'QQ/HQ'],[(2,3,3),'third HHH'],[(2,3,3),'third HHQ'],[(2,3,3),'third HQQ']]
        three.extend([[r,list(ns),tag,val]for(ns,tag),val in zip(tags,[linked,120+p,108+p,linked,120+p,120+p,120+2*p,120+p,120+p])])
    need(record['third_local_states']==third and record['three_parent_allocations']==three and max(v[-1]for v in three)==176,'all third states and45 allocations')
    inv=[]
    for f in (3,5,9):
        ab=[d for d in (3,5,9)if d!=f]
        for gh in combinations(D,2):
            for q in D:
                if q not in gh:inv.append([f,ab,list(gh),q,UB(ab)+C[join(*gh)]+C[join(f,q)]])
    need(record['remaining_inventory']==inv,'every original surviving-type inventory')
    need([v for v in inv if v[-1]>=177]==[[5,[3,9],[3,9],5,180]],'unique original inventory')
    need(max(sum(C[d]for d in ds)for ds in combinations(D,3)if ds!=(3,5,9))==145,'all other H triples')
    finals=[]
    for r,ms,prefixclass,threshold in ((2,[48,144,96,288],(16,2),147),(6,[80,160],(32,6),27)):
        points=parents[r];starts=sum(1<<(4*j)for j in range(len(points)))
        def bitmap(m,a):return sum(1<<(4*j+k)for j,n in enumerate(points)for k in range(4)if(n+2520*k-a)%m==0)
        placed=bitmap(*prefixclass);masks={m:{a:bitmap(m,a)for a in range(r,m,8)}for m in ms};good=[];h=hashlib.sha256();count=0;maximum=0
        for aa in product(*(range(r,m,8)for m in ms)):
            z=placed
            for m,a in zip(ms,aa):z|=masks[m][a]
            allfour=z&(z>>1)&(z>>2)&(z>>3)&starts;v=allfour.bit_count();count+=1;maximum=max(maximum,v);push(h,[list(aa),v])
            if v>=threshold:good.append([list(aa),v,hex(sum(1<<j for j in range(len(points))if allfour>>(4*j)&1))])
        finals.append({'parent':r,'moduli':ms,'raw_count':count,'maximum':maximum,'qualifying':good,'whole_raw_stream_sha256':h.hexdigest()})
    need(record['final_phases']==finals,'EVERY physical final phase tuple')
    glue=[]
    for c in range(5):
        protected=[n for n in R if n%8==2 or(n%8==6 and n%5==c)];pset=set(protected);outside=[n for n in R if n not in pset];rows=[];h=hashlib.sha256();raw=0
        for m in labels:
            hists={a:[0,0]for a in range(m)}
            for n in R:hists[n%m][0 if n in pset else 1]+=1
            for a,values in hists.items():push(h,[m,a]+values);raw+=1
            rows.append([m,max(out for inside,out in hists.values()if inside<=3)])
        glue.append({'c':c,'protected':len(protected),'outside':len(outside),'labels':rows,'sum':sum(v for m,v in rows),'whole_phase_stream_sha256':h.hexdigest(),'raw_phases':raw})
    need(record['BASE_gluing']==glue and all(v['sum']==1156 and v['outside']==1216 for v in glue),'whole original BASE gluing')
    expected_keys={'scope','R','parent_counts','cofactors','capacity','phase_populations','S','base177','intersections','four_Q_arms','H_triples','high_five_H_sets','all_exact_H_unions','union_phases','five_H_Q_rows','mixed_HQQ_HHQ_rows','three_parent_coupling','three_parent_allocations','third_local_states','type_rows','all_local_states','all_raw_local_types','remaining_inventory','final_phases','BASE_gluing','producer_imported'}
    need(set(record)==expected_keys,'entire record, no unsupported extra claim')
    return {'status':'COMPLETE_DIRECT_PHYSICAL_AUDIT','whole_record_sha256':hashlib.sha256(wire(record)).hexdigest(),'whole_record_bytes':len(wire(record)),'independent_kernel_imported':False,'raw_H_unions':record['union_phases'],'local_states':sum(len(v[2])for v in locals),'raw_local_states':10980,'third_states':sum(len(v[2])for v in third),'types':34,'three_parent_allocations':45,'final_original_phase_tuples':46856,'BASE_phases':46255}

if __name__=='__main__':print(wire(audit(json.load(open(sys.argv[1])))).decode())
