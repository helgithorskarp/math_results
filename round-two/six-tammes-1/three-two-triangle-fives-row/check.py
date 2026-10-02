"""Exact full F3T/D2T row cover, with all actual-original aliases."""
from collections import Counter,defaultdict
from itertools import combinations,permutations,product
from pathlib import Path
import json,hashlib
from patch import *

FAMILIES=[((A,B,C),(A,B,D)),((A,B,F),(A,B,D)),((A,B,D),(A,C,D)),((A,B,D),(A,F,D))]
def need(test,message):
    if not test:raise RuntimeError(message)
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def supplier_cover():
    maps=[];orbits=Counter();rows=[]
    for u,v in product(combinations(range(5),3),repeat=2):
        common=set(u)&set(v)
        if len(common)!=2 or 3 in common or 4 not in set(u)|set(v):continue
        rows.append((u,v));images=[]
        for p in permutations(range(3)):
            ren=(*p,3,4);a,b=tuple(sorted(ren[x]for x in u)),tuple(sorted(ren[x]for x in v))
            images.extend(((a,b),(b,a)))
        rep=min(images);orbits[rep]+=1;maps.append([u,v,rep])
    need(dict(orbits)=={((0,1,2),(0,1,4)):6,((0,1,3),(0,1,4)):6,
                       ((0,1,4),(0,2,4)):6,((0,1,4),(0,3,4)):12},'complete supplier role maps')
    return {'input_rows':100,'admitted_rows':len(rows),
            'orbits':[[list(u),list(v),n]for (u,v),n in sorted(orbits.items())],
            'original_role_map_sha256':digest(maps)}
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
def closed_obstruction(st):
    n=st['contacts'];fs=sorted(st['faces']);cells=defaultdict(list)
    need(len(fs)==17 and sum(len(f)==3 for f in fs)==8 and sum(len(f)==4 for f in fs)==9,'closed face profile')
    need(all(len(n[v])==DEG[v]for v in range(15)),'closed degree profile')
    t=Counter(v for f in fs if len(f)==3 for v in f)
    q=Counter(v for f in fs if len(f)==4 for v in f)
    need(all(t[v]==QUOTA[v]and q[v]==DEG[v]-QUOTA[v]for v in range(15)),'closed corner profile')
    reached={F};todo=[F]
    while todo:
        v=todo.pop()
        for w in n[v]-reached:reached.add(w);todo.append(w)
    need(len(reached)==15,'closed connected graph')
    for f in fs:
        for a,b in zip(f,f[1:]+f[:1]):cells[edge(a,b)].append(f)
    need(len(cells)==30 and all(len(v)==2 for v in cells.values()),'closed two-sided edges')
    witnesses=sorted(e for e,v in cells.items()if set(e)<=ORD and all(len(f)==4 for f in v))
    need(bool(witnesses),'unexpected geometrically unexcluded terminal')
    return list(witnesses[0]),digest(fs)

def all_covers():
    tested=Counter();admitted=Counter();events=Counter();whole=hashlib.sha256();kept=hashlib.sha256();terminals=[]
    def record(tag,key,value):
        line=json.dumps([tag,list(key),value],separators=(',',':')).encode()+b'\n';whole.update(line)
        if value is True or tag.endswith('-selected'):kept.update(line)
    def accept(tag,key,q):
        tested[tag]+=1;st=evaluate(q);admitted[tag]+=st is not None;record(tag,key,st is not None);return st
    def finish(tag,key,q,st):
        events[tag+' close nodes']+=1;n=st['contacts'];edges=defaultdict(list)
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
        if not options:
            witness,sha=closed_obstruction(st);events[tag+' metric-excluded terminals']+=1
            record(tag+'-closed-selected',key,[witness,sha])
            terminals.append({'tag':tag,'family':key[0],'ordinary_QQ_edge':witness,'full_faces_sha256':sha})
            return
        count,u,v,candidates=min(options);record(tag+'-close-selected',(*key,u,v),count);passed=0
        for f in candidates:
            ky=(*key,u,v,*f);child=q.plus(f);ss=accept(tag+'-face',ky,child)
            if ss is not None:passed+=1;finish(tag,ky,child,ss)
        if not passed:events[tag+' dead edges']+=1
    def threes(tag,key,q,st):
        events[tag+' three nodes']+=1;options=[]
        for v in (U,V):
            need(len(st['contacts'][v])==3,'three full supplier set')
            known={edge(f[f.index(v)-1],f[(f.index(v)+1)%len(f)])for f in st['faces']if v in f}
            for a,b in combinations(sorted(st['contacts'][v]),2):
                if edge(a,b)in known:continue
                choices=[]
                for x in range(15):
                    ky=(*key,v,a,b,x);child=q.plus((v,a,x,b));ss=accept(tag+'-Q',ky,child)
                    if ss is not None:choices.append((ky,child,ss))
                options.append((len(choices),v,a,b,choices))
        if not options:
            events[tag+' full three stars']+=1;record(tag+'-full-selected',key,0);finish(tag,key,q,st);return
        count,v,a,b,choices=min(options,key=lambda x:x[:4]);record(tag+'-selected',(*key,v,a,b),count)
        if not choices:events[tag+' dead corners']+=1
        for ky,child,ss in choices:threes(tag,ky,child,ss)
    for fi,(un,vn)in enumerate(FAMILIES):
        extra=[(v,x)for v,nbr in ((U,un),(V,vn))for x in nbr]
        common=sorted(set(un)&set(vn));forced=[(common[0],U,common[1],V)]
        if F not in set(un)|set(vn):
            for a,b,c,d in slots(4,8):
                for h,k in product(sorted(ONET|{D}),repeat=2):
                    ky=(fi,a,b,c,d,h,k);fs=[(F,a,I),(F,I,b),(F,b,h,c),(F,c,d),(F,d,k,a)]
                    q=Patch(fs+forced,extra);ss=accept('non-separated-initial',ky,q)
                    if ss is not None:threes('non-separated',ky,q,ss)
        else:
            t=U if F in un else V
            for e,p in slots(2,9):
                for h,k in product(sorted(ONET|{D}),repeat=2):
                    ky=(fi,e,p,t,h,k);fs=[(F,e,I),(F,I,R),(F,R,p),(F,p,h,t),(F,t,k,e)]
                    q=Patch(fs+forced,extra);ss=accept('non-adjacent-initial',ky,q)
                    if ss is not None:threes('non-adjacent',ky,q,ss)
    un,vn=FAMILIES[2];extra=[(v,x)for v,nbr in ((U,un),(V,vn))for x in nbr]
    for a,b,c,d in slots(4,7):
        for t,w in ((U,V),(V,U)):
            for h,k,l,m in product(sorted(ONET),repeat=4):
                ky=(2,a,b,c,d,t,w,h,k,l,m)
                fs=[(F,a,D),(F,D,b),(F,b,h,c),(F,c,d),(F,d,k,a),
                    (D,b,l,t),(D,t,A,w),(D,w,m,a)]
                q=Patch(fs,extra,fd_contact=True);ss=accept('contact-initial',ky,q)
                if ss is not None:threes('contact',ky,q,ss)
    need(tested['non-separated-initial']==2336 and tested['non-adjacent-initial']==416
         and tested['contact-initial']==11826,'complete initial counts')
    return {'tested':dict(sorted(tested.items())),'admitted':dict(sorted(admitted.items())),
            'events':dict(sorted(events.items())),'all_tested_and_selected_sha256':whole.hexdigest(),
            'admitted_and_selected_sha256':kept.hexdigest(),'metric_excluded_closed_terminals':terminals,
            'geometrically_unexcluded_terminals':0}

def build_report():
    return {'claim':'r2_a3_b0_f0_0_f1_1_f2_1_O8_excluded','supplier_cover':supplier_cover(),
            'endpoint_words':{'four_slots':len(slots(4,8)),'two_slots':len(slots(2,9))},
            'local_covers':all_covers()}
def main():
    report=build_report();expected=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
    need(report==expected,'complete output mismatch');print(json.dumps(report,sort_keys=True,indent=2))
if __name__=='__main__':main()
