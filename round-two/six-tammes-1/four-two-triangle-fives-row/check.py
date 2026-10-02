"""Exact full F4T/D2T row cover, with all actual-original aliases."""
from collections import Counter,defaultdict
from itertools import combinations,permutations,product
from pathlib import Path
import json,hashlib
from patch import *

FAMILIES=[((A,B,C),(A,B,D)),((A,B,D),(A,C,D))]
def need(test,message):
    if not test:raise RuntimeError(message)
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def supplier_cover():
    maps=[];orbits=Counter();rows=[]
    for u,v in product(combinations(range(5),3),repeat=2):
        if len(set(u)&set(v))!=2 or 4 not in set(u)|set(v):continue
        rows.append((u,v));images=[]
        for p in permutations(range(4)):
            ren=(*p,4);a,b=tuple(sorted(ren[x]for x in u)),tuple(sorted(ren[x]for x in v))
            images.extend(((a,b),(b,a)))
        rep=min(images);orbits[rep]+=1;maps.append([u,v,rep])
    need(dict(orbits)=={((0,1,2),(0,1,4)):24,((0,1,4),(0,2,4)):24},'complete supplier role maps')
    return {'input_rows':100,'admitted_rows':len(rows),
            'orbits':[[list(u),list(v),n]for (u,v),n in sorted(orbits.items())],
            'original_role_map_sha256':digest(maps)}
def contact_fan_cover():
    rows=[]
    for position in (1,2,3):
        fan=[4,8,9,10,7];fan[position]=D
        a,b=fan[position-1],fan[position+1]
        ts={tuple(sorted((F,fan[i],fan[i+1])))for i in range(4)}
        need(sum(D in f for f in ts)==2,'D Ts consumed at FD')
        for threes in ((U,V),(V,U)):
            rows.append([position,fan,[a,F,b,*threes],sorted(ts)])
    return {'F_D_positions':3,'three_orders':2,'rows':6,'entry_sha256':digest(rows)}
def slots(k,start):
    words=[]
    for types in product(sorted(ONET)+[None],repeat=k):
        names=[x for x in types if x is not None]
        if len(names)!=len(set(names)):continue
        nxt=start;word=[]
        for x in types:
            if x is None:word.append(nxt);nxt+=1
            else:word.append(x)
        words.append(tuple(word))
    return sorted(words)
def evaluate(q):
    try:return q.evaluate()
    except Bad:return None
def all_covers():
    tested=Counter();admitted=Counter();events=Counter();whole=hashlib.sha256();kept=hashlib.sha256()
    full_by_family=[0,0]
    def record(tag,key,value):
        line=json.dumps([tag,list(key),value],separators=(',',':')).encode()+b'\n';whole.update(line)
        if value is True or tag.endswith('-selected'):kept.update(line)
    def accept(tag,key,q):
        tested[tag]+=1;st=evaluate(q);admitted[tag]+=st is not None;record(tag,key,st is not None);return st
    def finish(tag,key,q,st):
        events[tag+' nodes']+=1;n=st['contacts'];edges=defaultdict(list)
        for f in sorted(st['faces']):
            for i,v in enumerate(f):edges[edge(v,f[(i+1)%len(f)])].append(f)
        def other(v,w,f):
            i=f.index(v);old=f[i-1]if f[(i+1)%len(f)]==w else f[(i+1)%len(f)]
            if v in st['cycles']:
                out=set()
                for cyc in st['cycles'][v]:
                    j=cyc.index(w);ends={cyc[j-1],cyc[(j+1)%len(cyc)]}
                    need(old in ends,'full link contains known corner');out.update(ends-{old})
                return out
            return {x for x in range(15)if x not in {v,w,old}and
                    (x in n[v]or(len(n[v])<DEG[v]and len(n[x])<DEG[x]))}
        options=[]
        for (u,v),fs in sorted(edges.items()):
            if len(fs)!=1:continue
            left,right=other(u,v,fs[0]),other(v,u,fs[0])
            candidates={face((u,v,w))for w in left&right}
            candidates|={face((u,v,x,w))for w,x in product(left,right)if w!=x}
            candidates-=st['faces'];options.append((len(candidates),u,v,sorted(candidates)))
        need(bool(options),'unexpected completed map or closed component')
        count,u,v,candidates=min(options);record(tag+'-selected',(*key,u,v),count);passed=0
        for f in candidates:
            ky=(*key,u,v,*f);child=q.plus(f);ss=accept(tag+'-face',ky,child)
            if ss is not None:passed+=1;finish(tag,ky,child,ss)
        if not passed:events[tag+' dead edges']+=1
    def complete_D(key,q,st):
        # Every surviving full three-star patch is family1; family0 is already
        # eliminated by the exhaustive three-star completion. Fail if changed.
        need(key[0]==1 and st['contacts'][D]&THREE==THREE,'both D three contacts')
        qs=[f for f in st['faces']if D in f and len(f)==4]
        endpoints=sorted(st['contacts'][D]-THREE)
        need(len(qs)==3 and len(endpoints)==2,'D Q cover and T endpoints')
        a,b=endpoints;events['D adjacent-T parents']+=1
        for i in sorted(ORD):
            ky=(*key,D,a,i,b);child=q.plus((D,a,i),(D,i,b));ss=accept('D-adjacent',ky,child)
            if ss is not None:finish('non-close',ky,child,ss)
    def threes(tag,key,q,st):
        events[tag+' nodes']+=1;options=[]
        for v in (U,V):
            need(len(st['contacts'][v])==3,'three full neighbor set')
            known={edge(f[f.index(v)-1],f[(f.index(v)+1)%len(f)])for f in st['faces']if v in f}
            for a,b in combinations(sorted(st['contacts'][v]),2):
                if edge(a,b)in known:continue
                choices=[]
                for x in range(15):
                    ky=(*key,v,a,b,x);child=q.plus((v,a,x,b));ss=accept(tag+'-Q',ky,child)
                    if ss is not None:choices.append((ky,child,ss))
                options.append((len(choices),v,a,b,choices))
        if not options:
            events[tag+' full three stars']+=1;record(tag+'-full-selected',key,0)
            if tag=='non':full_by_family[key[0]]+=1;complete_D(key,q,st)
            else:finish('contact-close',key,q,st)
            return
        count,v,a,b,choices=min(options,key=lambda x:x[:4]);record(tag+'-selected',(*key,v,a,b),count)
        if not choices:events[tag+' dead corners']+=1
        for ky,child,ss in choices:threes(tag,ky,child,ss)
    for fi,(un,vn)in enumerate(FAMILIES):
        extra=[(U,x)for x in un]+[(V,x)for x in vn]
        common=sorted(set(un)&set(vn));sq=[(common[0],U,common[1],V)]
        for e,p in slots(2,11):
            fan=(e,I,R,S,p);ts=[(F,fan[i],fan[i+1])for i in range(4)]
            for h in sorted(ONET):
                ky=(fi,e,p,h);q=Patch(ts+[(F,e,h,p)]+sq,extra);ss=accept('non-initial',ky,q)
                if ss is not None:threes('non',ky,q,ss)
    un,vn=FAMILIES[1];extra=[(U,x)for x in un]+[(V,x)for x in vn]
    for position in (1,2,3):
        for e,p in slots(2,10):
            fan=(e,D,I,R,p)if position==1 else(e,I,D,R,p)if position==2 else(e,I,R,D,p)
            a,b=fan[position-1],fan[position+1]
            for t,w in ((U,V),(V,U)):
                for h,k,l in product(sorted(ONET),repeat=3):
                    ky=(position,e,p,t,w,h,k,l)
                    fs=[(F,fan[i],fan[i+1])for i in range(4)]
                    fs+=[(F,e,h,p),(D,b,k,t),(D,t,A,w),(D,w,l,a)]
                    q=Patch(fs,extra,fd_contact=True);ss=accept('contact-initial',ky,q)
                    if ss is not None:threes('contact',ky,q,ss)
    return {'tested':dict(sorted(tested.items())),'admitted':dict(sorted(admitted.items())),
            'events':dict(sorted(events.items())),'noncontact_full_three_stars_by_family':full_by_family,
            'all_tested_and_selected_sha256':whole.hexdigest(),'admitted_and_selected_sha256':kept.hexdigest(),
            'completed_maps':0}
def build_report():
    return {'claim':'r2_a4_b0_f0_1_f1_0_f2_1_O7_excluded','supplier_cover':supplier_cover(),
            'contact_fan_cover':contact_fan_cover(),'endpoint_words':len(slots(2,11)),
            'local_covers':all_covers()}
def main():
    report=build_report();expected=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
    need(report==expected,'complete output mismatch');print(json.dumps(report,sort_keys=True,indent=2))
if __name__=='__main__':main()
