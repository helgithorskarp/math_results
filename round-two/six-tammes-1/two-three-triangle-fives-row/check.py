"""Complete exact covers for two degree fives, each with three T corners."""
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json
from patch import *

PARTS = ('noncontact', 'contact-separated', 'contact-adjacent')
FAMILIES = [((A,B,C),(A,B,E)), ((A,B,C),(A,B,D)),
            ((A,B,F),(A,B,D)), ((A,B,C),(E,F,D)), ((A,B,F),(C,E,D))]

def need(test, message):
    if not test: raise RuntimeError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def supplier_cover():
    rows=[];maps=[];orbits=Counter()
    for u,v in product(combinations(range(6),3),repeat=2):
        common=set(u)&set(v)
        if common&{4,5} or len(common)>2 or common and len(common)!=2:continue
        rows.append((u,v));images=[]
        for p in permutations(range(4)):
            for ds in ((4,5),(5,4)):
                ren=dict(enumerate(p))|dict(zip((4,5),ds))
                a,b=tuple(sorted(ren[x]for x in u)),tuple(sorted(ren[x]for x in v))
                images.extend(((a,b),(b,a)))
        rep=min(images);orbits[rep]+=1;maps.append([u,v,rep])
    expected={((0,1,2),(0,1,3)):12,((0,1,2),(0,1,4)):48,
              ((0,1,4),(0,1,5)):12,((0,1,2),(3,4,5)):8,((0,1,4),(2,3,5)):12}
    need(dict(orbits)==expected,'all supplier original-role maps')
    return {'input_rows':400,'admitted_rows':len(rows),
            'orbits':[[list(u),list(v),n]for (u,v),n in sorted(orbits.items())],
            'original_role_map_sha256':digest(maps)}

def paired_fans():
    rows=[];admitted=[]
    for j,k in product((2,3,4),repeat=2):
        fc=(2,1,3,4,5);dc=(2,0,3,6,7)
        ts={tuple(sorted(t))for t in [(0,1,2),(0,1,3),
             (0,fc[j],fc[(j+1)%5]),(1,dc[k],dc[(k+1)%5])]}
        counts=Counter(v for t in ts for v in t)
        good=all(counts[v]<=2 for v in range(2,8))
        rows.append([j,k,sorted(ts),good])
        if good:admitted.append([j,k])
    need(admitted==[[2,3],[2,4],[3,2],[3,3],[3,4],[4,2],[4,3]],'nine contact fan cases')
    return {'rows':9,'admitted':admitted,'entry_sha256':digest(rows)}

def slots(k,start):
    out=[]
    for word in product(sorted(ONET)+[None],repeat=k):
        names=[x for x in word if x is not None]
        if len(names)!=len(set(names)):continue
        nxt=start;outword=[]
        for x in word:
            if x is None:outword.append(nxt);nxt+=1
            else:outword.append(x)
        out.append(tuple(outword))
    return sorted(out)

def evaluate(q):
    try:return q.evaluate()
    except Bad:return None

def cover(part):
    need(part in PARTS,'unknown partition')
    tested=Counter();admitted=Counter();events=Counter();allhash=hashlib.sha256();keep=hashlib.sha256()
    def record(tag,key,value):
        line=json.dumps([tag,list(key),value],separators=(',',':')).encode()+b'\n'
        allhash.update(line)
        if value is True or tag.endswith('-selected'):keep.update(line)
    def accept(tag,key,q):
        tested[tag]+=1;st=evaluate(q);admitted[tag]+=st is not None
        record(tag,key,st is not None);return st
    def finish_faces(tag,key,q,st):
        events[tag+' nodes']+=1;ec=defaultdict(list);n=st['contacts']
        for f in sorted(st['faces']):
            for i,v in enumerate(f):ec[edge(v,f[(i+1)%len(f)])].append(f)
        def other(v,w,f):
            k=f.index(v);old=f[k-1]if f[(k+1)%len(f)]==w else f[(k+1)%len(f)]
            if v in st['cycles']:
                out=set()
                for cyc in st['cycles'][v]:
                    j=cyc.index(w);ends={cyc[j-1],cyc[(j+1)%len(cyc)]}
                    need(old in ends,'known corner in full link')
                    out.update(ends-{old})
                return out
            return {x for x in range(15)if x not in {v,w,old} and
                    (x in n[v]or(len(n[v])<DEG[v]and len(n[x])<DEG[x]))}
        opts=[]
        for (u,v),fs in sorted(ec.items()):
            if len(fs)!=1:continue
            us,vs=other(u,v,fs[0]),other(v,u,fs[0])
            candidates={face((u,v,x))for x in us&vs}
            candidates|={face((u,v,x,w))for w,x in product(us,vs)if w!=x}
            candidates-=st['faces']
            opts.append((len(candidates),u,v,sorted(candidates)))
        need(bool(opts),'unexpected completed map or closed component')
        count,u,v,candidates=min(opts)
        record(tag+'-selected',(*key,u,v),count);passed=0
        for f in candidates:
            ky=(*key,u,v,*f);child=q.plus(f);ss=accept(tag+'-face',ky,child)
            if ss is not None:passed+=1;finish_faces(tag,ky,child,ss)
        if not passed:events[tag+' dead edges']+=1
    def complete_D(key,q,st):
        three=st['contacts'][D]&THREE
        if not three:
            events['D separated parents']+=1
            ts=Counter(v for f in st['faces']if len(f)==3 for v in f)
            possible=[v for v in range(15)if v not in {D,F,U,V} and
                (D in st['contacts'][v]or(len(st['contacts'][v])<DEG[v]and ts[v]<QUOTA[v]))]
            record('D-supply-selected',key,possible)
            need(len(possible)<5,'uncovered separated D completion')
            events['D neighbor-T-supply reject']+=1;return
        need(len(three)==1,'unique D three')
        t3=min(three);dfs=[f for f in st['faces']if D in f and len(f)==4]
        need(len(dfs)==2 and all(t3 in f for f in dfs),'both D Qs determined')
        endpoints=sorted(st['contacts'][D]-{t3})
        need(len(endpoints)==2,'D T-path endpoints')
        a,d=endpoints;events['D adjacent parents']+=1
        for i,j in permutations(sorted(ORD),2):
            ky=(*key,D,a,i,j,d);child=q.plus((D,a,i),(D,i,j),(D,j,d))
            ss=accept('D-completion',ky,child)
            if ss is not None:finish_faces('non-close',ky,child,ss)
    def threes(tag,key,q,st):
        events[tag+' nodes']+=1;opts=[]
        for v in (U,V):
            need(len(st['contacts'][v])==3,'complete three contacts')
            known={edge(f[f.index(v)-1],f[(f.index(v)+1)%len(f)])for f in st['faces']if v in f}
            for a,b in combinations(sorted(st['contacts'][v]),2):
                if edge(a,b)in known:continue
                choices=[]
                for x in range(15):
                    ky=(*key,v,a,b,x);child=q.plus((v,a,x,b));ss=accept(tag+'-Q',ky,child)
                    if ss is not None:choices.append((ky,child,ss))
                opts.append((len(choices),v,a,b,choices))
        if not opts:
            events[tag+' full stars']+=1;record(tag+'-full-selected',key,0)
            if tag=='non':complete_D(key,q,st)
            else:finish_faces('contact-close',key,q,st)
            return
        count,v,a,b,choices=min(opts,key=lambda x:x[:4])
        record(tag+'-selected',(*key,v,a,b),count)
        if not choices:events[tag+' dead corners']+=1
        for ky,child,ss in choices:threes(tag,ky,child,ss)
    if part=='noncontact':
        for fi,(un,vn)in enumerate(FAMILIES):
            extra=[(U,x)for x in un]+[(V,x)for x in vn]
            shared=sorted(set(un)&set(vn));sq=[(shared[0],U,shared[1],V)]if shared else[]
            three=U if F in un else V if F in vn else None
            if three is None:
                for a,b,c,d in slots(4,9):
                    fs=[(F,a,I),(F,I,b),(F,c,d)]+sq
                    for h,k in product(sorted(ONET)+[D],repeat=2):
                        ky=(fi,a,b,c,d,h,k);q=Patch(fs+[(F,b,h,c),(F,d,k,a)],extra)
                        ss=accept('non-separated',ky,q)
                        if ss is not None:threes('non',ky,q,ss)
            else:
                for a,d in slots(2,10):
                    fs=[(F,a,I),(F,I,R),(F,R,d)]+sq
                    for h,k in product(sorted(ONET)+[D],repeat=2):
                        ky=(fi,a,d,h,k);q=Patch(fs+[(F,d,h,three),(F,three,k,a)],extra)
                        ss=accept('non-adjacent',ky,q)
                        if ss is not None:threes('non',ky,q,ss)
    else:
        for fi,(un,vn)in enumerate(FAMILIES):
            if fi==3:continue # Same three would be a third F,D common contact.
            if (part=='contact-separated')!=(fi==0):continue
            extra=[(U,x)for x in un]+[(V,x)for x in vn]
            shared=sorted(set(un)&set(vn));sq=[(shared[0],U,shared[1],V)]if shared else[]
            ft=U if F in un else V if F in vn else None
            dt=U if D in un else V if D in vn else None
            cases=[(3,3)]if ft is None and dt is None else [(3,2),(3,4)]if ft is None else [(2,4),(4,2)]
            for j,k in cases:
                if (j,k)==(3,3):words=slots(6,8)
                elif (j,k)==(3,2):words=[(a,8,c,d,e,dt)for a,c,d,e in slots(4,9)]
                elif (j,k)==(3,4):words=[(8,b,c,d,dt,f)for b,c,d,f in slots(4,9)]
                elif (j,k)==(2,4):words=[(8,9,c,ft,dt,f)for c,f in slots(2,10)]
                elif (j,k)==(4,2):words=[(8,9,ft,d,e,dt)for d,e in slots(2,10)]
                else:raise RuntimeError('contact case cover')
                for a,b,c,d,e,f in words:
                    fc=(a,D,b,c,d);dc=(a,F,b,e,f)
                    fs=[(F,D,a),(F,D,b),(F,fc[j],fc[(j+1)%5]),(D,dc[k],dc[(k+1)%5])]+sq
                    sectors=[(v,cyc[s],cyc[(s+1)%5])for v,cyc,third in [(F,fc,j),(D,dc,k)]for s in range(2,5)if s!=third]
                    for opp in product(sorted(ONET),repeat=4):
                        ky=(fi,j,k,a,b,c,d,e,f,*opp)
                        q=Patch(fs+[(v,x,o,y)for (v,x,y),o in zip(sectors,opp)],extra,fd_contact=True)
                        ss=accept('paired-fans',ky,q)
                        if ss is not None:threes('contact',ky,q,ss)
    return {'part':part,'tested':dict(sorted(tested.items())),
            'admitted':dict(sorted(admitted.items())),'events':dict(sorted(events.items())),
            'all_tested_and_selected_sha256':allhash.hexdigest(),
            'admitted_and_selected_sha256':keep.hexdigest(),'completed_maps':0}

def build_report(part):
    return {'claim':'r2_a4_b0_f0_0_f1_2_f2_0_O7_excluded',
            'supplier_cover':supplier_cover(),'paired_fans':paired_fans(),
            'canonical_slot_counts':{'two':len(slots(2,10)),'four':len(slots(4,9)),'six':len(slots(6,8))},
            'local_cover':cover(part)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--part',required=True,choices=PARTS)
    part=parser.parse_args().part;report=build_report(part)
    expected=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
    need(report==expected[part],'complete partition output mismatch')
    print(json.dumps(report,sort_keys=True,indent=2))

if __name__=='__main__':main()
