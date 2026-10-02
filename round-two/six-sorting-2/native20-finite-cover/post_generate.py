"""Exact complete saturated equality-event cover after first6.
All preparations commute past the live events. The residual suffix is arbitrary.
"""
import hashlib,json,resource,time
from collections import Counter
from itertools import combinations
from functools import lru_cache
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
def need(ok,msg):
    if not ok:raise ValueError(msg)
def evaluate(x,word):
    for a,b in word:
        if x>>a&1 and not x>>b&1:x^=(1<<a)|(1<<b)
    return x
def encode(values):
    return b''.join(int(x).to_bytes(2,'little') for x in values)
def endpoints(rows,kind):
    result=[]
    for low,high,d in rows:
        mask=low if kind=='low' else high
        frozen=0 if kind=='low' else 12
        mask&=~(1<<frozen)
        need(mask and not mask&(mask-1),'not a secondary singleton')
        result.append((mask.bit_length()-1,d))
    return tuple(sorted(result))
@lru_cache(None)
def family_cover(initial,kind):
    ports=[p for p,d in initial]
    k=len(ports);index={p:i for i,p in enumerate(ports)}
    identity=tuple(sum(1<<x for x in range(1<<k) if x>>i&1) for i in range(k))
    functions={};all_event_words=state_controls=0
    states=set()
    def descend(state,word,cols):
        nonlocal all_event_words,state_controls
        states.add(state)
        need(sum(2**d for p,d in state)==512,'saturated mass changed')
        if len(state)==1:
            need(state[0]==(1 if kind=='low' else 11,9),'wrong terminal route')
            functions.setdefault(cols,word)
            all_event_words+=1
            return
        has_successor=False
        for i,j in combinations(range(len(state)),2):
            state_controls+=1
            a,da=state[i];b,db=state[j]
            if da!=db:continue
            has_successor=True;gate=tuple(sorted((a,b)))
            newport=min(a,b) if kind=='low' else max(a,b)
            nxt=tuple(sorted([x for z,x in enumerate(state) if z not in (i,j)]+[(newport,da+1)]))
            newcols=list(cols);ia,ib=index[gate[0]],index[gate[1]]
            newcols[ia],newcols[ib]=newcols[ia]&newcols[ib],newcols[ia]|newcols[ib]
            descend(nxt,word+[list(gate)],tuple(newcols))
        need(has_successor,'nonterminal saturated state has no equal-cost merge')
    descend(initial,[],identity)
    result={'initial':list(map(list,initial)),'kind':kind,'canonical_full_functions':len(functions),'all_event_words':all_event_words,'reachable_states':len(states),'pair_controls_with_word_multiplicity':state_controls,'word_length':k-1,'words':list(functions.values())}
    return result
def main():
    start=time.monotonic()
    joint=json.loads((ROOT/'joint-cover.json').read_text())
    need(len(joint['joint_roots'])==joint['summary']['joint_profile_image_pairs'],'joint packet truncated')
    records=joint['joint_roots']
    post={};all_compositions=0;by_pref=Counter()
    for ji,record in enumerate(records):
        low=family_cover(endpoints(record['low'],'low'),'low')
        high=family_cover(endpoints(record['high'],'high'),'high')
        for li,lw in enumerate(low['words']):
            for hi,hw in enumerate(high['words']):
                events=lw+hw
                n=record['prefix_length']+len(events)
                whole=[evaluate(x,events) for x in record['full_image']]
                for x in whole:
                    weight=x.bit_count()
                    sorted_x=((1<<weight)-1)<<(13-weight)
                    need(x&6147==sorted_x&6147,'four outer ports are not correct')
                middle=sorted({(x>>2)&511 for x in whole})
                key=encode(middle)
                candidate={'joint_root':ji,'low_function_index':li,'high_function_index':hi,'prefix_length':n,'suffix_budget':44-n,'word':record['word']+events,'middle_image':middle}
                old=post.get(key)
                if old is None or n<old['prefix_length']:post[key]=candidate
                by_pref[n]+=1;all_compositions+=1
    roots=list(post.values())
    roots.sort(key=lambda x:(x['prefix_length'],x['middle_image']))
    summary={'agent':'six-sorting-2','role':'researcher','status':'COMPLETE_EXACT_NATIVE20_NORMALIZED_NINE_CORE_ROOT_COVER_NOT_EXCLUDED','joint_roots':len(records),'all_postjoint_compositions':all_compositions,'distinct_nine_core_images':len(roots),'all_compositions_by_prefix_length':dict(by_pref),'canonical_roots_by_prefix_length':dict(Counter(r['prefix_length'] for r in roots)),'image_size_range':[min(len(r['middle_image']) for r in roots),max(len(r['middle_image']) for r in roots)],'suffix_budget_range':[min(r['suffix_budget'] for r in roots),max(r['suffix_budget'] for r in roots)],'family_profiles':family_cover.cache_info().currsize,'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'boundary':'Complete joint cover is imported. Equal-cost live-event coverage and disjoint preparation commutation are author proofs. Full function equality folds event words; nine-image equality keeps shortest prefixes. Residual suffixes remain arbitrary and no certificate/exclusion is inferred.'}
    (ROOT/'postjoint-cover.json').write_text(json.dumps({'summary':summary,'roots':roots},separators=(',',':'))+'\n')
    profiles=[]
    seen=set()
    for record in records:
        for kind in ['low','high']:
            initial=endpoints(record[kind],kind)
            if (initial,kind) not in seen:seen.add((initial,kind));profiles.append(family_cover(initial,kind))
    (ROOT/'postjoint-family-covers.json').write_text(json.dumps(profiles,separators=(',',':'))+'\n')
    (ROOT/'postjoint-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    digest=hashlib.sha256()
    for r in roots:
        digest.update(bytes([r['suffix_budget']])+encode(r['middle_image'])+b'\xff\xff')
    summary['root_image_budget_sha256']=digest.hexdigest()
    (ROOT/'postjoint-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True),flush=True)
if __name__=='__main__':main()
