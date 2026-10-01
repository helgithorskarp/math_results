"""Exact single-preparation normal form and class13 completion table.

six-sorting-1, researcher. Python3.11+, standard library, exact integers.
Profile core adapts this author's published coupled-profile/quota sources.
Local maps use Boolean bit planes; this file imports no solver.
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

def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':')).encode('ascii')).hexdigest()

def move(weights,gate,maximum):
    a,b=gate;out=list(weights);w=2*max(weights[a],weights[b])
    out[a],out[b]=(0,w) if maximum else (w,0)
    return tuple(out)

def successor(s,g):
    lo,hi,flag=s
    if not flag and g[1]==10 and g[0] in (0,7,9):return None
    dl,dh=move(lo,g,False),move(hi,g,True)
    if sum(dl)>16 or sum(dh)>16:return None
    return dl,dh,flag or g[1]==10

def empty(s):
    return tuple(i for i,(a,b) in enumerate(zip(s[0],s[1])) if not a and not b)

def terminal(s):
    return s==((16,)+(0,)*10,(0,)*10+(16,),True)

def planes(rows,n):
    return tuple(sum((r>>w&1)<<i for i,r in enumerate(rows)) for w in range(n))

def apply(p,word):
    p=list(p)
    for a,b in word:p[a],p[b]=p[a]&p[b],p[a]|p[b]
    return tuple(p)

def local_monoids():
    records=[];lookups={}
    for n in range(1,5):
        gates=tuple(itertools.combinations(range(n),2));root=planes(range(1<<n),n)
        states=[root];ids={root:0};words=[()];queue=deque([0]);edges=[]
        while queue:
            i=queue.popleft()
            for k,g in enumerate(gates):
                d=apply(states[i],(g,))
                if d not in ids:
                    ids[d]=len(states);states.append(d);words.append(words[i]+(k,));queue.append(ids[d])
                edges.append([i,k,ids[d]])
        records.append({'wires':n,'maps':len(states),'edges':len(edges),
                        'loops':sum(i==j for i,k,j in edges),
                        'diameter':max(map(len,words)),
                        'length_histogram':dict(sorted(Counter(map(len,words)).items())),
                        'edge_sha256':digest(edges),'representative_words':words})
        lookups[n]={s:words[i] for i,s in enumerate(states)}
    return records,lookups

def profile_graph(f):
    root=(tuple(f['initial_low']),tuple(f['initial_high']),False)
    words={root:()};queue=deque([root]);edges=[];outgoing={}
    while queue:
        s=queue.popleft();outgoing[s]=[]
        for g in GATES:
            d=successor(s,g)
            if d is None:continue
            outgoing[s].append((g,d));edges.append((s,g,d))
            if d not in words:words[d]=words[s]+(g,);queue.append(d)
    before=Counter();unary=Counter();entries=[];loops=0
    for s in words:
        if not s[2]:
            assert sum(s[0])==sum(s[1])==15 and s[0][10]==s[1][10]==1
            assert [i for i,(a,b) in enumerate(zip(s[0],s[1])) if a and b]==[10]
            assert all(w==0 or w>=2 and w&(w-1)==0 for w in s[0][:10]+s[1][:10])
            assert len(empty(s))<=4;before[len(empty(s))]+=1
        else:assert sum(s[0])==sum(s[1])==16 and not any(a and b for a,b in zip(s[0],s[1]))
    for s,g,d in edges:
        J,K=set(empty(s)),set(empty(d))
        if s==d:
            assert set(g)<=J;loops+=1;continue
        if not s[2] and d[2] and s[0][g[0]]==0:
            assert g[0] in J and K==J-{g[0]}
            entries.append((s,g,d));unary[len(J)]+=1
        else:
            assert J<=K and set(g).isdisjoint(J)
            if s[2] or not d[2]:assert len(K)==len(J)+1
        # Every allowed comparison on two jointly empty ports is a loop.
    for s in words:
        for g in itertools.combinations(empty(s),2):assert successor(s,g)==s
    audit={'states':len(words),'edges':len(edges),'loops':loops,
           'state_sha256':digest(sorted(words)),'edge_sha256':digest(sorted(edges)),
           'pre_empty_histogram':dict(sorted(before.items())),
           'unary_entry_histogram':dict(sorted(unary.items())),'unary_entries':len(entries)}
    assert audit['states']==2214 and audit['edges']==22536
    return root,words,outgoing,sorted(entries),audit

def normalize(word,root,lookups):
    s=root;before=[];after=[];A=[];B=[];first=None;J=None
    for g in word:
        d=successor(s,g);assert d is not None
        if d==s:(B if first is not None else A).append(g)
        elif not s[2] and d[2]:
            assert first is None and s[0][g[0]]==0
            first=g;J=empty(s)
        elif first is None:before.append(g)
        else:after.append(g)
        s=d
    assert terminal(s) and first is not None and len(before)==len(J)
    assert len(before)+1+len(after)==11 and all(set(g)<=set(J) for g in A)
    assert all(1<=a<b<=9 for a,b in B)
    local=tuple(itertools.combinations(range(len(J)),2));index={p:i for i,p in enumerate(J)}
    small=tuple((index[a],index[b]) for a,b in A)
    lp=planes(range(1<<len(J)),len(J));labels=lookups[len(J)][apply(lp,small)]
    prep=tuple((J[local[k][0]],J[local[k][1]]) for k in labels)
    commuted=tuple(before+A+[first]+after+B)
    compressed=tuple(before)+prep+(first,)+tuple(after+B)
    return commuted,compressed,len(A),len(prep)

def equivalence_controls(root,paths,outgoing,entries,lookups):
    @lru_cache(None)
    def finish(s):
        if terminal(s):return ()
        for g,d in sorted(outgoing[s]):
            if d!=s:
                tail=finish(d)
                if tail is not None:return (g,)+tail
        return None
    controls=[];commuted=[];compressed=[];counts=Counter();truth=planes(range(2048),11)
    for case,(source,f,dest) in enumerate(entries):
        before=paths[source];assert len(before)==len(empty(source))
        events=before+(f,)+finish(dest);assert len(events)==11
        s=root;word=[];loops=0;target=9+case%3
        for pos,g in enumerate(events):
            choices=tuple(itertools.combinations(empty(s),2))
            copies=(target-loops) if pos==len(before) and choices else int(bool(choices) and loops<11)
            for j in range(copies):word.append(choices[(case+pos+j)%len(choices)]);loops+=1
            word.append(g);s=successor(s,g)
        choices=tuple(itertools.combinations(empty(s),2))
        while loops<11:word.append(choices[(case+loops)%len(choices)]);loops+=1
        assert len(word)==22
        c,z,a,h=normalize(word,root,lookups)
        assert apply(truth,word)==apply(truth,c)==apply(truth,z)
        controls.append([GATES.index(g) for g in word]);commuted.append([GATES.index(g) for g in c])
        compressed.append([GATES.index(g) for g in z]);counts[a,h]+=1
    return controls,{'cases':len(controls),'inputs_per_case':2048,
                     'function_equalities':len(controls)*2048,
                     'preparation_length_pairs':[[a,h,n] for (a,h),n in sorted(counts.items())],
                     'commuted_words_sha256':digest(commuted),'compressed_words_sha256':digest(compressed)}

def trace(word):
    remaining=set(range(len(word)));answer=[]
    while remaining:
        allowed=[i for i in remaining if not any(j<i and not set(word[j]).isdisjoint(word[i]) for j in remaining)]
        i=min(allowed,key=lambda j:(word[j],j));answer.append(word[i]);remaining.remove(i)
    return tuple(answer)

def class_triples(f,root):
    code=int(f['class_code']);start=root,0;target=((16,)+(0,)*10,(0,)*10+(16,),True),code
    nodes={start};outgoing={};queue=deque([start])
    while queue:
        q=queue.popleft();s,used=q;choices=[]
        for k,g in enumerate(GATES):
            d=successor(s,g)
            if d is None or d==s or (used>>(2*k)&3)>=(code>>(2*k)&3):continue
            child=d,used+(1<<(2*k));choices.append((g,child))
            if child not in nodes:nodes.add(child);queue.append(child)
        outgoing[q]=choices
    @lru_cache(None)
    def live(q):return q==target or any(live(d) for g,d in outgoing[q])
    triples=Counter()
    def walk(q,before,first,after):
        if q==target:
            assert first is not None and len(before)+1+len(after)==11
            triples[trace(before),first,trace(after)]+=1;return
        for g,d in outgoing[q]:
            if not live(d):continue
            if first is None and d[0][2]:walk(d,before,g,())
            elif first is None:walk(d,before+(g,),None,after)
            else:walk(d,before,first,after+(g,))
    walk(start,(),None,())
    table=[[list(map(GATES.index,b)),GATES.index(g),list(map(GATES.index,a)),n]
           for (b,g,a),n in sorted(triples.items())]
    assert sum(triples.values())==5385 and len(table)==6
    return table

def completion_table(f,root,monoids,triples):
    rows=f['B11_states'];truth=planes(rows,11);rowindex={r:i for i,r in enumerate(rows)}
    families=f['families'];domains=tuple(tuple(sum(1<<rowindex[r] for r in d) for d in fam['domains']) for fam in families)
    images=[];ids={};cases=[];representatives={};extreme_lo=sum((r==2047)<<i for i,r in enumerate(rows));extreme_hi=sum((r!=0)<<i for i,r in enumerate(rows))
    for ti,(bl,fl,al,count) in enumerate(triples):
        before=tuple(GATES[k] for k in bl);first=GATES[fl];after=tuple(GATES[k] for k in al);s=root
        for g in before:s=successor(s,g)
        J=empty(s);assert len(J)==len(before) and first[0] in J
        local=tuple(itertools.combinations(range(len(J)),2))
        for mi,labels in enumerate(monoids[len(J)-1]['representative_words']):
            prep=tuple((J[local[k][0]],J[local[k][1]]) for k in labels);word=before+prep+(first,)+after
            out=apply(truth,word);assert out[0]==extreme_lo and out[10]==extreme_hi
            image=tuple(sorted(set(sum((out[w]>>i&1)<<(w-1) for w in range(1,10)) for i in range(len(rows)))))
            if image not in ids:ids[image]=len(images);images.append(image)
            imageid=ids[image];budget=11-len(prep);ci=len(cases)
            cases.append([ti,mi,imageid,budget])
            representatives.setdefault((imageid,budget),(ci,word))
    pairs=[];survivors=[];blocked=0
    for (ii,budget),(ci,word) in sorted(representatives.items()):
        wires=list(truth);routes=[fam['partner'] for fam in families];hits=[fam['prefix_D'] for fam in families];obstacle=None
        for event,(a,b) in enumerate(word):
            swaps=wires[a]&~wires[b]
            for j,(r,ds) in enumerate(zip(routes,domains)):
                if r in (a,b):continue
                for k,d in enumerate(ds):
                    if not swaps&d and obstacle is None:obstacle=[event,j,k]
            wires[a],wires[b]=wires[a]&wires[b],wires[a]|wires[b]
            for j,fam in enumerate(families):
                if routes[j] in (a,b):hits[j]+=1;routes[j]=b if fam['mode']=='max' else a
        assert hits==[9]*len(families) and all(r==(10 if fam['mode']=='max' else 0) for r,fam in zip(routes,families))
        pairs.append([ii,budget,ci,obstacle])
        if obstacle is None:survivors.append([ii,budget,ci])
        else:blocked+=1
    assert len(cases)==288 and len(images)==108 and len(pairs)==139 and blocked==134 and len(survivors)==5
    return {'effective_words':sum(t[3] for t in triples),'triples':triples,'local_map_cases':cases,
            'images9':images,'image_budget_pairs':pairs,'remaining_completion_pairs':survivors,
            'prefix_activity_excluded_pairs':blocked,
            'remaining_row_budget_pairs':sorted([[len(images[i]),b] for i,b,c in survivors]),
            'scope':'Existence reduction, not checked exclusion of any of the five residual tails.'}

def main():
    assert sys.flags.optimize==0,'Run without -O'
    f=json.loads((HERE/'fixture.json').read_text());monoids,lookups=local_monoids()
    root,paths,outgoing,entries,audit=profile_graph(f)
    controls,summary=equivalence_controls(root,paths,outgoing,entries,lookups)
    triples=class_triples(f,root);table=completion_table(f,root,monoids,triples)
    cert={'schema':'sorting13-single-preparation-v1','agent':'six-sorting-1','role':'researcher',
          'fixture_sha256':digest(f),'profile_audit':audit,'local_monoids':monoids,
          'equivalence_controls':controls,'equivalence_control_summary':summary,'class13':table,
          'scope':'All eleven-event B11 C22 words admit one preparation block on at most four ports; class13 reduces to five explicit ordinary nine-wire tails.'}
    cert=json.loads(json.dumps(cert));path=HERE/'certificate.json'
    if path.exists():assert json.loads(path.read_text())==cert,'Certificate mismatch'
    else:path.write_text(json.dumps(cert,separators=(',',':'))+'\n')
    print(json.dumps({'status':'SINGLE_PREPARATION_AND_FIVE_TAILS_GENERATED',
                      'profile_states':audit['states'],'unary_entries':audit['unary_entries'],
                      'local_map_counts':[m['maps'] for m in monoids],
                      'class13_completion_pairs':len(table['remaining_completion_pairs']),
                      'certificate_sha256':digest(cert)}))

if __name__=='__main__':main()
