# Independent six-reviewer-4 carrier; authored before any researcher executable read.
from pathlib import Path
from itertools import combinations, permutations, product
import json,hashlib,time,sys

def need(ok,message):
    if not ok:raise RuntimeError(message)

HERE=Path(__file__).resolve().parent

def fixture_data(override=None):
    p=HERE/'fixtures.json';b=p.read_bytes()
    if override is None:need(hashlib.sha256(b).hexdigest()=='c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7','fixture hash')
    data=json.loads(b) if override is None else override;out=[]
    need(len(data['stars'])==len(data['groups'])==23,'aligned input')
    for f,(rows,maps) in enumerate(zip(data['stars'],data['groups'])):
        q=tuple(sorted(tuple(sorted(r)) for r in rows));need(len(q)==len(set(q))==20,'20 distinct blocks')
        need(all(len(r)==len(set(r))==4 and all(type(v)is int and 0<=v<17 for v in r) for r in q),'block domain')
        rho=tuple(sum(v in r for r in q) for v in range(17));used={p for r in q for p in combinations(r,2)}
        need(len(used)==120 and max(rho)<=5 and sum(5-v for v in rho)==5,'pair uniqueness and deficits')
        high={v for v in range(17) if rho[v]<5};leave={p for p in combinations(range(17),2) if p not in used}
        need(len(leave)==16 and all(not(rho[a]==rho[b]==5) for a,b in leave),'reviewed no low-low leave on literal fixture')
        group={tuple(g) for g in maps} or {tuple(range(17))};need(tuple(range(17)) in group,'identity')
        for g in group:
            need(sorted(g)==list(range(17)),'bijection')
            need({tuple(sorted(g[v] for v in r)) for r in q}==set(q),'literal map preserves blocks')
        need(all(tuple(g[h[v]] for v in range(17)) in group for g in group for h in group),'subgroup closure')
        out.append({'q':q,'rho':rho,'high':high,'leave':leave,'group':group})
    need(len(out)==23,'23 credited fixtures')
    return out

def marking_domains(data):
    first=[];second=[];raw_first=[];raw_second=[]
    for f,d in enumerate(data):
        q,rho,high,leave,group=(d[k] for k in ['q','rho','high','leave','group'])
        marks=set()
        for u in high:
            if any(tuple(sorted((u,z))) in leave for z in high if z!=u):continue
            for y in high-{u}:
                if rho[y]!=4:continue
                for v in range(17):
                    if rho[v]==5 and tuple(sorted((v,y))) in leave:marks.add((u,v,y))
        raw_first.extend((f,m) for m in sorted(marks))
        reps={min(tuple(g[v] for v in m) for g in group) for m in marks}
        need(all(tuple(g[v] for v in m) in marks for m in marks for g in group),'first marking transport')
        first.extend((f,m) for m in sorted(reps))
        if min(rho)<4:continue
        marks=set()
        for x in high:
            for u in range(17):
                if u==x or tuple(sorted((u,x))) in leave:continue
                for v in range(17):
                    if v in (u,x):continue
                    if tuple(sorted((x,v))) in leave:marks.add((u,v,x))
        raw_second.extend((f,m) for m in sorted(marks))
        reps={min(tuple(g[v] for v in m) for g in group) for m in marks}
        need(all(tuple(g[v] for v in m) in marks for m in marks for g in group),'second marking transport')
        second.extend((f,m) for m in sorted(reps))
    counts={}
    for f,m in raw_second:
        key=str(data[f]['rho'][m[0]])+str(data[f]['rho'][m[1]])
        counts[key]=counts.get(key,0)+1
    norm={}
    for f,m in second:
        key=str(data[f]['rho'][m[0]])+str(data[f]['rho'][m[1]])
        norm[key]=norm.get(key,0)+1
    return first,second,{'raw_first':len(raw_first),'first':[[f,list(m)] for f,m in first],'raw_second_by_u_v':counts,'normalized_second_by_u_v':norm,'raw_second':len(raw_second),'normalized_second':len(second),'all_products':len(first)*len(second)}

def first_obstruction(d,y):
    # projected private second word = {global y} union a partial quadruple.
    # A repeated triple is either y plus a pair in a common tail, or a triple
    # in one of the sixteen private first quadruples. Precompute exact flags.
    pool=tuple(v for v in range(17) if v!=y);bad=bytearray(1<<17)
    anchors=[set(r)|{17} for r in d['q']]
    pbad={p for r in d['q'] if y in r for p in combinations(tuple(v for v in r if v!=y),2)}
    tbad={t for r in d['q'] if y not in r for t in combinations(r,3)}
    for forbidden in pbad|tbad:
        free=tuple(v for v in pool if v not in forbidden);base=sum(1<<v for v in forbidden)
        for extra_size in range(5-len(forbidden)):
            for extra in combinations(free,extra_size):bad[base+sum(1<<v for v in extra)]=1
    calibration=0
    for size in range(5):
        for points in combinations(pool,size):
            mask=sum(1<<v for v in points);literal=set(points)|{y}
            need(bool(bad[mask])==any(len(literal&r)>=3 for r in anchors),'all projected-subset literal calibration')
            calibration+=1
    return bad,calibration

def relative_maps(first,second,mark1,mark2,bad):
    u1,v1,y1=mark1;u2,v2,x2=mark2
    target_tails=[tuple(v for v in r if v!=y1) for r in first['q'] if y1 in r]
    source_tails=[tuple(v for v in r if v!=x2) for r in second['q'] if x2 in r]
    need(len(target_tails)==len(source_tails)==4,'four common tails')
    target_u=next(t for t in target_tails if u1 in t);source_u=next(t for t in source_tails if u2 in t)
    ta=sorted(t for t in target_tails if t!=target_u);sa=sorted(t for t in source_tails if t!=source_u)
    su=tuple(v for v in source_u if v!=u2);tu=tuple(v for v in target_u if v!=u1)
    source_assigned={x2,v2}|{v for t in source_tails for v in t}
    target_assigned={17,v1}|{v for t in target_tails for v in t}
    need(len(source_assigned)==len(target_assigned)==14 and y1 not in target_assigned,'14-point partial domain')
    source_free=tuple(v for v in range(17) if v not in source_assigned)
    target_free=tuple(v for v in range(18) if v!=y1 and v not in target_assigned)
    private=[r for r in second['q'] if x2 not in r]
    private.sort(key=lambda r:-sum(v in source_assigned for v in r))
    original_words=tuple(sorted(sum(1<<v for v in (*r,17)) for r in first['q']))
    partials=[];positives=[];expanded=0;survived=0
    for paired in permutations(ta):
        for target_u_other in permutations(tu):
            for tail_images in product(*(tuple(permutations(t)) for t in paired)):
                mapping=[-1]*17;mapping[x2]=17;mapping[v2]=v1;mapping[u2]=u1
                for v,w in zip(su,target_u_other):mapping[v]=w
                for a,b in zip(sa,tail_images):
                    for v,w in zip(a,b):mapping[v]=w
                key=tuple(mapping);partials.append(key)
                bit_image=[0 if v<0 else 1<<v for v in mapping]
                if any(bad[sum(bit_image[v] for v in r)] for r in private):continue
                survived+=1
                for images in permutations(target_free):
                    full=mapping[:]
                    for v,w in zip(source_free,images):full[v]=w
                    bits=[1<<v for v in full];expanded+=1
                    if any(bad[sum(bits[v] for v in r)] for r in private):continue
                    words=tuple(sorted(set(original_words)|{(1<<y1)+sum(bits[v] for v in r) for r in second['q']}))
                    need(len(words)==36 and all((a&b).bit_count()<=2 for a,b in combinations(words,2)),'literal36-word positive')
                    need(sorted(full)==[v for v in range(18) if v!=y1],'full actual bijection')
                    positives.append({'map':full,'words':list(words)})
    need(len(partials)==len(set(partials))==2592,'complete distinct partial maps')
    digest=hashlib.sha256(json.dumps(sorted(partials),separators=(',',':')).encode()).hexdigest()
    positives.sort(key=lambda z:z['map'])
    return {'partial_maps':len(partials),'represented_full_maps':len(partials)*6,'expanded_full_maps':expanded,'surviving_partials':survived,'partial_universe_sha256':digest,'positives':positives}

if __name__=='__main__':
    start=time.monotonic();data=fixture_data();first,second,domain=marking_domains(data)
    work=Path(sys.argv[3]);work.mkdir(parents=True,exist_ok=True)
    (work/'domain.json').write_text(json.dumps(domain,indent=2)+'\n')
    print('DOMAIN',domain,flush=True)
    lo=int(sys.argv[1]) if len(sys.argv)>1 else 0;hi=int(sys.argv[2]) if len(sys.argv)>2 else lo+3
    all_products=list(product(first,second));bounds={};records=[]
    for index in range(lo,min(hi,len(all_products))):
        (fi,m1),(se,m2)=all_products[index];key=(fi,m1[2])
        if key not in bounds:bounds[key]=first_obstruction(data[fi],m1[2])
        result=relative_maps(data[fi],data[se],m1,m2,bounds[key][0])
        records.append({'product':index,'first_fixture':fi,'first_mark':m1,'second_fixture':se,'second_mark':m2,'u_replication':data[se]['rho'][m2[0]],'v_replication':data[se]['rho'][m2[1]],**result})
    path=work/f'census-{lo}-{hi}.json';path.write_text(json.dumps(records,separators=(',',':'))+'\n')
    print('DONE',lo,hi,'seconds',time.monotonic()-start,'positives',sum(len(z['positives']) for z in records),'subsets_calibrated',sum(v[1] for v in bounds.values()),flush=True)
