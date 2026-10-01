"""Independent inverse13 profiles, rank-permutation maps, and scalar replay.

six-sorting-1, researcher. Imports neither generate.py nor a solver.
All-real commutation/threshold arguments and published lower bounds are
written theorem imports, not proof-assistant formalizations.
"""
from collections import Counter,deque
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
GATES=tuple(itertools.combinations(range(11),2))
PAIRS=tuple(itertools.combinations(range(13),2))

def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':')).encode('ascii')).hexdigest()

def scalar(values,word):
    v=list(values)
    for a,b in word:
        if v[a]>v[b]:v[a],v[b]=v[b],v[a]
    return tuple(v)

def marked(pair,maximum):
    other=iter(range(11) if maximum else range(2,13))
    return tuple((11 if maximum else 0)+pair.index(i) if i in pair else next(other) for i in range(13))

def transport(values,word,maximum):
    values=list(values);hits=0
    for a,b in word:
        hits+=bool(values[a]>=11 or values[b]>=11) if maximum else bool(values[a]<2 or values[b]<2)
        if values[a]>values[b]:values[a],values[b]=values[b],values[a]
    ports=tuple(i for i,v in enumerate(values) if (v>=11 if maximum else v<2))
    assert len(ports)==2
    return ports,hits

def original_profile(prefix,maximum):
    out={}
    for p in PAIRS:
        destination,d=transport(marked(p,maximum),prefix,maximum)
        out[destination]=max(out.get(destination,-1),d)
    return tuple(sorted(out.items()))

def fibers(maximum):
    result={}
    for g in GATES:
        out={}
        for p in PAIRS:
            dest,d=transport(marked(p,maximum),((g[0]+1,g[1]+1),),maximum)
            out.setdefault(dest,[]).append((p,d))
        assert all(len(pre)<=2 for pre in out.values())
        assert all(d==1 for pre in out.values() if len(pre)==2 for p,d in pre)
        result[g]=out
    return result

def inverse(profile,fb):
    old=dict(profile);out={}
    for dest,pre in fb.items():
        values=[old[p]+d for p,d in pre if p in old]
        if values:out[dest]=max(values)
    return tuple(sorted(out.items()))

def canonical(s):
    vectors=[]
    for profile,held in ((s[0],0),(s[1],12)):
        vector=[0]*11
        for pair,d in profile:
            assert held in pair and d>=5
            port=next(i for i in pair if i!=held)-1;assert 0<=port<11
            vector[port]=1<<(d-5)
        vectors.append(tuple(vector))
    return *vectors,s[2]

def empty(s):
    c=canonical(s)
    return tuple(i for i,(a,b) in enumerate(zip(c[0],c[1])) if not a and not b)

def terminal(s):
    return s==((((0,1),9),),(((11,12),9),),True)

def full_graph(prefix):
    low,high=fibers(False),fibers(True)
    root=original_profile(prefix,False),original_profile(prefix,True),False
    assert sum(1<<d for p,d in root[0])==sum(1<<d for p,d in root[1])==480
    stack=[root];seen=set();outgoing={};edges=[]
    while stack:
        s=stack.pop()
        if s in seen:continue
        seen.add(s);outgoing[s]={}
        for g in GATES:
            if not s[2] and g[1]==10 and g[0] in (0,7,9):continue
            dl,dh=inverse(s[0],low[g]),inverse(s[1],high[g])
            if sum(1<<d for p,d in dl)>512 or sum(1<<d for p,d in dh)>512:continue
            child=dl,dh,s[2] or g[1]==10
            outgoing[s][g]=child;edges.append((canonical(s),g,canonical(child)))
            if child not in seen:stack.append(child)
    states=sorted(map(canonical,seen));before=Counter();unary=Counter();entries=set();loops=0
    for s in states:
        J={i for i,(a,b) in enumerate(zip(s[0],s[1])) if not a and not b}
        if not s[2]:
            assert sum(s[0])==sum(s[1])==15 and s[0][10]==s[1][10]==1
            assert [i for i,(a,b) in enumerate(zip(s[0],s[1])) if a and b]==[10]
            assert all(w==0 or w>=2 and w&(w-1)==0 for w in s[0][:10]+s[1][:10])
            assert len(J)<=4;before[len(J)]+=1
        else:assert sum(s[0])==sum(s[1])==16 and not any(a and b for a,b in zip(s[0],s[1]))
    for s,g,d in edges:
        J={i for i,(a,b) in enumerate(zip(s[0],s[1])) if not a and not b}
        K={i for i,(a,b) in enumerate(zip(d[0],d[1])) if not a and not b}
        if s==d:assert set(g)<=J;loops+=1;continue
        if not s[2] and d[2] and s[0][g[0]]==0:
            assert g[0] in J and K==J-{g[0]};entries.add((s,g,d));unary[len(J)]+=1
        else:
            assert J<=K and set(g).isdisjoint(J)
            if s[2] or not d[2]:assert len(K)==len(J)+1
    for s in seen:
        for g in itertools.combinations(empty(s),2):assert outgoing[s][g]==s
    audit={'states':len(seen),'edges':len(edges),'loops':loops,
           'state_sha256':digest(states),'edge_sha256':digest(sorted(edges)),
           'pre_empty_histogram':dict(sorted(before.items())),
           'unary_entry_histogram':dict(sorted(unary.items())),'unary_entries':len(entries)}
    assert len(seen)==2214 and len(edges)==22536
    return root,outgoing,entries,audit

def rank_monoids():
    records=[];lookups={}
    for n in range(1,5):
        gates=tuple(itertools.combinations(range(n),2));inputs=tuple(itertools.permutations(range(n)))
        states=[inputs];indices={inputs:0};words=[()];edges=[];queue=deque([0])
        while queue:
            i=queue.popleft()
            for k,g in enumerate(gates):
                child=tuple(scalar(row,(g,)) for row in states[i])
                if child not in indices:
                    indices[child]=len(states);states.append(child);words.append(words[i]+(k,));queue.append(indices[child])
                edges.append([i,k,indices[child]])
        records.append({'wires':n,'maps':len(states),'edges':len(edges),
                        'loops':sum(i==j for i,k,j in edges),'diameter':max(map(len,words)),
                        'length_histogram':dict(sorted(Counter(map(len,words)).items())),
                        'edge_sha256':digest(edges),'representative_words':words})
        lookups[n]={s:words[i] for i,s in enumerate(states)}
    return records,lookups

def check_controls(cert,root,outgoing,entries,lookups):
    recovered=set();commuted=[];compressed=[];counts=Counter()
    for labels in cert['equivalence_controls']:
        assert len(labels)==22 and all(0<=k<55 for k in labels)
        original=tuple(GATES[k] for k in labels);s=root;A=[];B=[];before=[];after=[];first=None;J=None
        classified=[]
        for g in original:
            child=outgoing[s][g]
            if child==s:
                classified.append((g,False,s[2]));(B if first is not None else A).append(g)
            elif not s[2] and child[2]:
                assert first is None and canonical(s)[0][g[0]]==0
                recovered.add((canonical(s),g,canonical(child)));first=g;J=empty(s)
                classified.append((g,True,True))
            elif first is None:before.append(g);classified.append((g,True,False))
            else:after.append(g);classified.append((g,True,True))
            s=child
        assert terminal(s) and first is not None and len(before)==len(J)
        assert len(before)+1+len(after)==11 and all(set(g)<=set(J) for g in A)
        assert all(1<=a<b<=9 for a,b in B)
        for i,(g,event,phase) in enumerate(classified):
            if event:continue
            assert all(set(g).isdisjoint(h) for h,e,p in classified[i+1:] if e and p==phase)
        local=tuple(itertools.combinations(range(len(J)),2));index={p:i for i,p in enumerate(J)}
        small=tuple((index[a],index[b]) for a,b in A)
        maps=tuple(scalar(row,small) for row in itertools.permutations(range(len(J))))
        prep=tuple((J[local[k][0]],J[local[k][1]]) for k in lookups[len(J)][maps])
        c=tuple(before+A+[first]+after+B);z=tuple(before)+prep+(first,)+tuple(after+B)
        assert len(c)==22 and len(z)<=22 and len(prep)<=5
        for x in range(2048):
            bits=tuple(x>>i&1 for i in range(11))
            assert scalar(bits,original)==scalar(bits,c)==scalar(bits,z)
        commuted.append([GATES.index(g) for g in c]);compressed.append([GATES.index(g) for g in z])
        counts[len(A),len(prep)]+=1
    assert len(cert['equivalence_controls'])==len(entries) and recovered==entries
    return {'cases':len(commuted),'inputs_per_case':2048,'function_equalities':len(commuted)*2048,
            'preparation_length_pairs':[[a,h,n] for (a,h),n in sorted(counts.items())],
            'commuted_words_sha256':digest(commuted),'compressed_words_sha256':digest(compressed)}

def canonical_trace(word):
    word=list(word);result=[]
    while word:
        available=[i for i,g in enumerate(word) if all(set(g).isdisjoint(h) for h in word[:i])]
        i=min(available,key=lambda j:(word[j],j));result.append(word.pop(i))
    return tuple(result)

def independent_triples(f,root,outgoing):
    code=int(f['class_code']);start=root,0;target=((((0,1),9),),(((11,12),9),),True),code
    graph={};stack=[start];seen=set()
    while stack:
        q=stack.pop()
        if q in seen:continue
        seen.add(q);s,used=q;graph[q]=[]
        for g,d in outgoing[s].items():
            k=GATES.index(g)
            if d==s or (used>>(2*k)&3)>=(code>>(2*k)&3):continue
            child=d,used+(1<<(2*k));graph[q].append((g,child))
            if child not in seen:stack.append(child)
    visiting=set()
    @lru_cache(None)
    def ways(q):
        assert q not in visiting,'Non-loop cycle'
        visiting.add(q)
        n=1 if q==target else sum(ways(d) for g,d in graph[q])
        visiting.remove(q);return n
    assert ways(start)==5385
    triples=Counter()
    def enumerate_words(q,word):
        if q==target:
            split=next(i for i,g in enumerate(word) if g[1]==10)
            b,g,a=canonical_trace(word[:split]),word[split],canonical_trace(word[split+1:])
            triples[b,g,a]+=1;return
        for g,d in graph[q]:
            if ways(d):enumerate_words(d,word+(g,))
    enumerate_words(start,())
    return [[list(map(GATES.index,b)),GATES.index(g),list(map(GATES.index,a)),n]
            for (b,g,a),n in sorted(triples.items())]

def reconstruct(f):
    prefix=f['prefix22'];assert len(prefix)==22
    assert prefix==f['prefix20'][:-1]+[[10,12]]+f['minimum_word'] and f['minimum_word']==[[0,5],[0,1]]
    rows=set()
    control=prefix+[[a+1,b+1] for a,b in f['B11_known23_control']];assert len(control)==45
    for x in range(8192):
        bits=tuple(x>>i&1 for i in range(13));out=scalar(bits,prefix)
        assert out[0]==min(bits) and out[12]==max(bits)
        rows.add(sum(v<<i for i,v in enumerate(out[1:12])))
        assert scalar(bits,control)==tuple(sorted(bits))
    assert sorted(rows)==f['B11_states'] and len(rows)==158
    for fam in f['families']:
        maximum=fam['mode']=='max'
        assert len(fam['domains'])==len(fam['original_representatives'])
        for pair,domain in zip(fam['original_representatives'],fam['domains']):
            pair=tuple(pair);dest,d=transport(marked(pair,maximum),prefix,maximum)
            assert d==fam['prefix_D'] and dest==tuple(sorted((12 if maximum else 0,fam['partner']+1)))
            free=[i for i in range(13) if i not in pair];actual=set()
            for x in range(2048):
                values=[0]*13
                values[pair[0]],values[pair[1]]=(2,3) if maximum else (-2,-1)
                for j,i in enumerate(free):values[i]=x>>j&1
                out=scalar(values,prefix)
                actual.add(sum(int(v>0)<<i for i,v in enumerate(out[1:12])))
            assert sorted(actual)==domain
    return 13*2048

def completion_table(f,root,outgoing,monoids,triples):
    rows=f['B11_states'];images=[];ids={};cases=[];representatives={};families=f['families']
    words=[]
    for ti,(bl,fl,al,count) in enumerate(triples):
        before=tuple(GATES[k] for k in bl);first=GATES[fl];after=tuple(GATES[k] for k in al);s=root
        for g in before:s=outgoing[s][g]
        J=empty(s);assert len(J)==len(before) and first[0] in J
        local=tuple(itertools.combinations(range(len(J)),2))
        for mi,labels in enumerate(monoids[len(J)-1]['representative_words']):
            prep=tuple((J[local[k][0]],J[local[k][1]]) for k in labels);word=before+prep+(first,)+after
            middle=set()
            for r in rows:
                out=scalar(tuple(r>>w&1 for w in range(11)),word)
                assert out[0]==int(r==2047) and out[10]==int(r!=0)
                middle.add(sum(v<<w for w,v in enumerate(out[1:10])))
            image=tuple(sorted(middle))
            if image not in ids:ids[image]=len(images);images.append(image)
            imageid=ids[image];budget=11-len(prep);ci=len(cases)
            cases.append([ti,mi,imageid,budget]);words.append(word)
            representatives.setdefault((imageid,budget),(ci,word))
            # Independently check all thirteen actual marked-pair saturations
            # on every prefix, including equivalent-image representatives.
            full=f['prefix22']+[(a+1,b+1) for a,b in word]
            for fam in families:
                for p in fam['original_representatives']:
                    maximum=fam['mode']=='max';dest,d=transport(marked(tuple(p),maximum),full,maximum)
                    assert d==9 and dest==((11,12) if maximum else (0,1))
    pairs=[];survivors=[];blocked=0;actual_obstruction_checks=0
    for (ii,budget),(ci,word) in sorted(representatives.items()):
        domains=[[[list(r>>w&1 for w in range(11)) for r in d] for d in fam['domains']] for fam in families]
        routes=[fam['partner'] for fam in families];hits=[fam['prefix_D'] for fam in families];obstacle=None
        for event,(a,b) in enumerate(word):
            for j,(route,ds) in enumerate(zip(routes,domains)):
                if route in (a,b):continue
                for k,domain in enumerate(ds):
                    if not any(row[a]>row[b] for row in domain) and obstacle is None:obstacle=[event,j,k]
            for ds in domains:
                for domain in ds:
                    for row in domain:
                        if row[a]>row[b]:row[a],row[b]=row[b],row[a]
            for j,fam in enumerate(families):
                if routes[j] in (a,b):hits[j]+=1;routes[j]=b if fam['mode']=='max' else a
        assert hits==[9]*len(families) and all(r==(10 if fam['mode']=='max' else 0) for r,fam in zip(routes,families))
        pairs.append([ii,budget,ci,obstacle])
        if obstacle is None:survivors.append([ii,budget,ci]);continue
        blocked+=1;event,j,k=obstacle;fam=families[j];pair=tuple(fam['original_representatives'][k]);maximum=fam['mode']=='max'
        free=[i for i in range(13) if i not in pair]
        pre=f['prefix22']+[(a+1,b+1) for a,b in word[:event]];a,b=word[event];a+=1;b+=1
        for x in range(2048):
            v=[0]*13;v[pair[0]],v[pair[1]]=(2,3) if maximum else (-2,-1)
            for k,i in enumerate(free):v[i]=x>>k&1
            out=scalar(v,pre)
            assert out[a] in (0,1) and out[b] in (0,1) and out[a]<=out[b]
            actual_obstruction_checks+=1
    table={'effective_words':sum(t[3] for t in triples),'triples':triples,'local_map_cases':cases,
           'images9':images,'image_budget_pairs':pairs,'remaining_completion_pairs':survivors,
           'prefix_activity_excluded_pairs':blocked,
           'remaining_row_budget_pairs':sorted([[len(images[i]),b] for i,b,c in survivors]),
           'scope':'Existence reduction, not checked exclusion of any of the five residual tails.'}
    return table,actual_obstruction_checks

def main():
    assert sys.flags.optimize==0,'Run without -O'
    f=json.loads((HERE/'fixture.json').read_text())
    path=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'certificate.json'
    cert=json.loads(path.read_text());assert cert['fixture_sha256']==digest(f)
    assert cert['schema']=='sorting13-single-preparation-v1' and cert['agent']=='six-sorting-1' and cert['role']=='researcher'
    domain_assignments=reconstruct(f)
    root,outgoing,entries,audit=full_graph(f['prefix22'])
    assert canonical(root)==(tuple(f['initial_low']),tuple(f['initial_high']),False)
    assert json.loads(json.dumps(audit))==cert['profile_audit']
    monoids,lookups=rank_monoids();assert json.loads(json.dumps(monoids))==cert['local_monoids']
    triples=independent_triples(f,root,outgoing)
    table,actual=completion_table(f,root,outgoing,monoids,triples)
    assert json.loads(json.dumps(table))==cert['class13']
    assert len(table['remaining_completion_pairs'])==5
    summary=check_controls(cert,root,outgoing,entries,lookups)
    assert summary==cert['equivalence_control_summary']
    print(json.dumps({'status':'INDEPENDENT_SINGLE_PREPARATION_AND_FIVE_TAILS_VERIFIED',
                      'profile_states':audit['states'],'profile_edges':audit['edges'],
                      'rank_monoid_counts':[m['maps'] for m in monoids],
                      'full11_control_function_equalities':summary['function_equalities'],
                      'B11_original_inputs':8192,'domain_assignments':domain_assignments,
                      'actual_marked_obstruction_checks':actual,'class13_effective_words':5385,
                      'normalized_prefixes':len(table['local_map_cases']),
                      'remaining_row_budget_pairs':table['remaining_row_budget_pairs']}))

if __name__=='__main__':main()
