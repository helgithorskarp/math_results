"""Standard-library integer certificate checker; six-code-1, researcher.

No solver, census-enumeration verdict or imported twenty-star lemma is inferred
from a timeout. The ordinary bridges are stated in PROOF.md, not formalized.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import produce

HERE=Path(__file__).resolve().parent
BASELINE_SHA='cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d'


def check(ok,message):
    if not ok:raise ValueError(message)


def encode(x):
    return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()


def independent_carriers():
    raw=(HERE/'NINETEEN_STARS.json').read_bytes()
    check(hashlib.sha256(raw).hexdigest()==produce.MANIFEST_SHA,'manifest integrity')
    data=json.loads(raw);out=[];representatives=0
    for mi,m in enumerate(data['models']):
        forbidden_columns={};offset=0
        for n in m['cycle_half_lengths']:
            for row in range(offset,offset+n):
                forbidden_columns[row]={row,offset+(row-offset+1)%n}
            offset+=n
        occupied=[(r,c) for r in range(5) for c in range(5)
                  if c not in forbidden_columns[r]]
        labels={rc:i for i,rc in enumerate(occupied)}
        anchor_masks=[]
        for r in range(5):
            anchor_masks.append((1<<15)+sum(1<<labels[r,c] for c in range(5) if (r,c) in labels))
        for c in range(5):
            anchor_masks.append((1<<16)+sum(1<<labels[r,c] for r in range(5) if (r,c) in labels))
        injections=set()
        for rows in combinations(range(5),4):
            for cols in permutations(range(5),4):
                if all((r,c) in labels for r,c in zip(rows,cols)):
                    injections.add(tuple(sorted(labels[r,c] for r,c in zip(rows,cols))))
        candidates=[sum(1<<i for i in w) for w in sorted(injections)]
        for ci,entry in enumerate(m['marked_classes']):
            representatives+=1
            words=sorted(anchor_masks+[candidates[i] for i in entry['clique']])
            check(len(words)==len(set(words))==19,'nineteen distinct masks')
            rho=[0]*17;owner=[[-1]*17 for _ in range(17)]
            for wi,w in enumerate(words):
                check(type(w) is int and w>0 and w>>17==0 and w.bit_count()==4,'quadruple mask')
                for x in range(17):
                    if not w>>x&1:continue
                    rho[x]+=1
                    for y in range(x+1,17):
                        if w>>y&1:
                            check(owner[x][y]==-1,'repeated pair')
                            owner[x][y]=wi
            check(sum(rho)==76 and max(rho)<=5,'replication condition')
            low=[x for x in range(17) if rho[x]==5]
            high=[x for x in range(17) if rho[x]<5]
            leave=[(a,b) for a in range(17) for b in range(a+1,17) if owner[a][b]==-1]
            ll=[list(p) for p in leave if p[0] in low and p[1] in low]
            check(len(leave)==22 and len(ll) in (1,2),'eligible nineteen-star leave')
            check(len({x for p in ll for x in p})==2*len(ll),'LL matching')
            for u in range(17):
                if rho[u]!=4:continue
                cm=0
                for w in words:
                    if w>>u&1:cm|=w
                cm &= ~(1<<u)
                C=[x for x in range(17) if cm>>x&1];W=[x for x in high if x!=u]
                check(len(C)==12,'marked covered neighborhood')
                q=[];friends=[]
                for y in W:
                    xs=[x for x in C if x in low and owner[min(x,y)][max(x,y)]==-1]
                    if xs:q.append([y,len(xs)]);friends.append([y,xs])
                row={'model':mi,'class':ci,'u':u,'blocks':words,'rho':rho,
                     'C':C,'W':W,'low':low,'W_C':[x for x in W if x in C],
                     'q':q,'friends':friends,'heavy_v':[x for x in W if rho[x]==3],
                     'low_low_pairs':ll,'mu':len(ll),'p':len(W),'k':sum(x in C for x in W),
                     'LL_C_endpoints':sum(x in C for p in ll for x in p)}
                check(row['LL_C_endpoints']==2*row['mu'],'LL endpoints not all covered')
                out.append(row)
    check(representatives==46 and len(out)==388,'carrier coverage')
    return out


def independent_screen(rows):
    tested=0;coarse=[];final=[]
    for r in rows:
        q=dict(r['q']);wc=r['W_C']
        for tc_bits in range(1<<len(wc)):
            tc=[y for i,y in enumerate(wc) if tc_bits>>i&1];c=len(tc)
            for X in range(3):
                for z in range(5):
                    if 2*X+z+c>4:continue
                    tested+=1
                    R=4-z+c-2*X
                    Q=sum(max(q.get(y,0),2 if y in tc else 0) for y in r['W'])
                    if Q>R:continue
                    if X==0 and R-Q<max(0,r['mu']-z):continue
                    row=[r['model'],r['class'],r['u'],X,tc,z,Q,R]
                    coarse.append(row)
                    if any(q.get(y,0)>=2 and y not in r['heavy_v'] for y in tc):continue
                    final.append(row)
    coarse.sort(key=encode);final.sort(key=encode)
    check(len(coarse)==62 and len(final)==40,'inventory coverage changed')
    check(all(s[3]==0 and s[5] in (0,1) and s[7]-s[6]==1-s[5]
              for s in coarse),'one-exception exhaustion')
    ids=sorted({tuple(s[:3]) for s in final})
    check(ids==[(0,17,14),(0,19,1),(1,11,7)],'residual carrier list')
    lookup={tuple(r[x] for x in ('model','class','u')):r for r in rows}
    for s in final:
        r=lookup[tuple(s[:3])];q=dict(r['q'])
        check(r['p']==8 and r['k']==7 and r['mu']==1 and not r['heavy_v'],
              'residual profile')
        check(sorted(q.values())==[1,1,1] and all(q.get(y,0)==1 for y in s[4]),
              'covered T carriers')
    return {'tested_inventories':tested,'coarse':coarse,'after_shared_hub':final}


def candidates_independent(r):
    # Direct intersections, rather than the producer's forbidden-triple filter.
    values=[]
    for points in combinations(range(17),5):
        w=sum(1<<i for i in points)
        if all((w&s).bit_count()<=2 for s in r['blocks']):values.append(w)
    check(len(values)==1219,'compatible-word coverage')
    return values


def row_semantics(label,r,e):
    """Return exact b and signed subset indicators for the row A x <= b."""
    check(type(label) is list and label and type(label[0]) is str,'row descriptor')
    tag=label[0];u=r['u'];good=set(r['low'])-{e};q=dict(r['q'])
    good_b=set(r['W_C'])-set(q)
    arity={'point':1,'triple':3,'pair':3,'good-coverage':2,
           'forced-leave-upper':2,'u-good-upper':2,'u-good-lower':2,
           'u-good-b-lower':2,'u-exception-lower':2,'u-covered-t-lower':2,
           'u-outside-t-lower':2}
    check(tag in arity and len(label)==arity[tag]+1,'unknown row type or arity')
    coords=label[1:3] if tag=='pair' else label[1:]
    check(all(type(x) is int and 0<=x<17 for x in coords),'point range')
    check(coords==sorted(set(coords)),'unordered or repeated row points')
    m=sum(1<<x for x in coords)
    inc=sum(w&m==m for w in r['blocks'])
    if tag=='point':return (16 if coords[0]==u else 20)-r['rho'][coords[0]],[(m,1)]
    if tag=='triple':
        check(inc==0,'triple already in the fixed star')
        return 1,[(m,1)]
    if tag.startswith('u-'):
        check(u in coords,'unmarked hub in row')
        x=next(x for x in coords if x!=u)
        if tag in ('u-good-upper','u-good-lower'):
            check(x in good,'point is not good A')
            return (4-inc,[(m,1)]) if tag.endswith('upper') else (inc-3,[(m,-1)])
        if tag=='u-good-b-lower':
            check(x in good_b,'point is not forced good B');lower=5
        elif tag=='u-exception-lower':
            check(x==e,'point is not the matching exception');lower=2
        elif tag=='u-covered-t-lower':
            check(x in set(r['W_C'])-good_b,'point is not a possible covered T');lower=3
        else:
            check(x in set(r['W'])-set(r['C']),'point is not the outside W point')
            lower=2 if q.get(x,0) else 4
        return inc-lower,[(m,-1)]
    check(u not in coords,'S-S row contains u')
    if tag=='pair':
        lower=5 if set(coords)<=good or set(coords)<=good_b else 4
        check(type(label[3]) is int and label[3]==lower,'pair lower bound')
        return inc-lower,[(m,-1)]
    if tag=='forced-leave-upper':
        check(inc==0 and set(coords)&set(r['low']),'unforced leave deficit')
        return 4,[(m,1)]
    check(set(coords)&good,'coverage row has no good A endpoint')
    t=m|(1<<u);it=sum(w&t==t for w in r['blocks'])
    return inc+it-5,[(m,-1),(t,-1)]


def check_certificate(data,rows):
    check(type(data) is dict and set(data)=={'format','cases'} and
          data['format']=='M4_INTEGER_DUAL_V1','certificate format')
    check(type(data['cases']) is list,'case list')
    _,final=produce.screen(rows)
    ids=sorted({tuple(s[:3]) for s in final})
    expected={(a,b,u,e) for a,b,u in ids for e in next(
        r for r in rows if (r['model'],r['class'],r['u'])==(a,b,u))['low_low_pairs'][0]}
    seen=set();results=[]
    for c in data['cases']:
        check(type(c) is dict and set(c)=={'model','class','u','exception','scale','weights'},'case fields')
        key=tuple(c[k] for k in ('model','class','u','exception'))
        check(all(type(x) is int for x in key) and key in expected and key not in seen,'case coverage')
        seen.add(key)
        r=next(r for r in rows if (r['model'],r['class'],r['u'])==key[:3])
        D=c['scale'];check(type(D) is int and D>0,'positive integer scale')
        check(type(c['weights']) is list and c['weights'],'nonempty weights')
        words=candidates_independent(r);coverage=[0]*len(words);numerator=0;labels=set()
        for item in c['weights']:
            check(type(item) is list and len(item)==2,'weighted row')
            label,weight=item
            check(type(weight) is int and weight>0,'positive integer weight')
            code=encode(label);check(code not in labels,'duplicate row');labels.add(code)
            b,terms=row_semantics(label,r,key[3]);numerator+=weight*b
            for j,w in enumerate(words):
                coverage[j]+=weight*sum(v for m,v in terms if w&m==m)
        check(min(coverage)>=D,'a candidate column is not covered')
        check(numerator<52*D,'bound is not strict below52')
        results.append({'case':list(key),'candidate_count':len(words),'weighted_rows':len(labels),
                        'min_column':min(coverage),'integer_bound':numerator,'scale':D})
    check(seen==expected and len(seen)==6,'missing residual case')
    return sorted(results,key=lambda r:r['case'])


def no_excess_bridge():
    arithmetic=[]
    for p in range(9):
        for k in range(p+1):
            if 6+k>p*(p-1)//2 or 5*p+k>21+p*(p-1)//2:continue
            for X in (1,2):
                for c in range(5):
                    for z in range(5):
                        if 2*X+z+c>4:continue
                        R=4-z+c-2*X
                        if max(12-k,2*c)<=R:arithmetic.append([p,k,X,c,z])
    check(arithmetic==[[8,8,1,2,0]],'mu0 excess inventory')
    # Abstract names: two T_C centers0,1 and their four distinct low friends2..5.
    outcomes=Counter()
    for edge in combinations(range(16),2):
        if edge==(0,1):
            # Hubs16/17 lie outside the sixteen abstract saturated labels.
            # The partner is additional to the two actual low friends.
            for t in (0,1):
                friends=(2,3) if t==0 else (4,5)
                neighbors=(16,17,1-t,*friends)
                deficits=(1,1,2,1,1)
                check(len(neighbors)==len(set(neighbors))==5,
                      'heavy partner and actual friends must be distinct')
                check(sum(deficits)==6>5,'heavy-partner row-sum contradiction')
            outcomes['row_sum_contradiction']+=1
            continue
        usable=[t for t in (0,1) if t not in edge and
                any(a not in edge for a in ((2,3) if t==0 else (4,5)))]
        check(usable,'no unaffected shared-isolated-hub pair')
        outcomes['unaffected_shared_hub']+=1
    check(outcomes=={'row_sum_contradiction':1,'unaffected_shared_hub':119},'heavy-edge coverage')
    return {'arithmetic_survivor':arithmetic,'heavy_edge_positions':dict(outcomes),
            'heavy_partner_distinct_deficient_neighbors':5,'heavy_partner_minimum_deficit':6}


def baseline():
    raw=(HERE/'acl69.txt').read_bytes();check(hashlib.sha256(raw).hexdigest()==BASELINE_SHA,'baseline bytes')
    strings=raw.decode().split();check(len(strings)==len(set(strings))==69,'baseline size')
    check(all(len(s)==18 and set(s)<=set('01') and s.count('1')==5 for s in strings),'baseline word')
    ws=[int(s,2) for s in strings];distances=Counter((a^b).bit_count() for a,b in combinations(ws,2))
    check(distances=={6:1264,8:637,10:445},'baseline distances')
    return {'words':69,'distances':{str(d):n for d,n in sorted(distances.items())}}


def controls(data,rows):
    variants=[]
    def variant(name,mutation):
        d=copy.deepcopy(data);mutation(d);variants.append((name,d))
    variant('negative weight',lambda d:d['cases'][0]['weights'][0].__setitem__(1,-1))
    variant('zero scale',lambda d:d['cases'][0].__setitem__('scale',0))
    variant('unknown row',lambda d:d['cases'][0]['weights'][0][0].__setitem__(0,'UNKNOWN'))
    variant('unknown exception',lambda d:d['cases'][0].__setitem__('exception',0))
    variant('missing case',lambda d:d['cases'].pop())
    variant('duplicate case',lambda d:d['cases'].append(copy.deepcopy(d['cases'][0])))
    variant('empty weights',lambda d:d['cases'][0].__setitem__('weights',[]))
    variant('uncovered columns',lambda d:d['cases'][0].__setitem__('weights',[[['point',0],1]]))
    variant('non-strict bound',lambda d:[item.__setitem__(1,item[1]*2) for item in d['cases'][0]['weights']])
    variant('noninteger weight',lambda d:d['cases'][0]['weights'][0].__setitem__(1,0.5))
    variant('point outside domain',lambda d:d['cases'][0]['weights'].__setitem__(0,[['point',17],1]))
    variant('wrong pair lower',lambda d:d['cases'][0]['weights'].__setitem__(0,[['pair',0,1,6],1]))
    rejected=[]
    for name,d in variants:
        try:check_certificate(d,rows)
        except (ValueError,KeyError,TypeError,StopIteration):rejected.append(name)
        else:raise ValueError('accepted malformed control: '+name)
    return rejected


def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'INTEGER_DUALS.json')
    p.add_argument('--write-expected',type=Path);p.add_argument('--skip-controls',action='store_true')
    args=p.parse_args();rows=independent_carriers();primary=produce.literal_carriers()
    check(rows==primary,'the complete primary and independent readouts differ')
    inventory=independent_screen(rows);coarse,final=produce.screen(primary)
    check(sorted(coarse,key=encode)==inventory['coarse'] and sorted(final,key=encode)==inventory['after_shared_hub'],
          'the complete cohort streams differ')
    data=json.loads(args.certificate.read_bytes())
    exact=check_certificate(data,rows)
    buckets=Counter((r['mu'],r['p'],r['k'],sum(q for _,q in r['q']),r['LL_C_endpoints']) for r in rows)
    report={'actual_agent':'six-code-1','role':'researcher','status':'COMPLETE exact arithmetic and integer duals',
            'carrier_sha256':hashlib.sha256(encode(rows)).hexdigest(),
            'marked_representatives':46,'replication_four_marks':388,
            'buckets':[[list(k),v] for k,v in sorted(buckets.items())],
            'inventory':inventory,'duals':exact,'no_excess_bridge':no_excess_bridge(),
            'baseline':baseline(),'malformed_controls':[] if args.skip_controls else controls(data,rows)}
    if args.write_expected:args.write_expected.write_bytes(encode(report))
    elif args.certificate==HERE/'INTEGER_DUALS.json':
        check(report==json.loads((HERE/'expected.json').read_bytes()),'expected replay record differs')
    print(json.dumps({'status':report['status'],'carrier_marks':388,'duals':exact,
                      'controls':len(report['malformed_controls']),
                      'manifest_sha256':hashlib.sha256(encode(report)).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
