"""Exact exact pre6 function folding and complete first6 image cover.
No cutoff in finite input sets. No suffix exclusion is claimed here.
"""
import hashlib,json,resource,time
from collections import Counter
from itertools import combinations
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
PREV=ROOT
PORTS=(1,2,3,5,7,8,9,10,11)
INDEX={p:i for i,p in enumerate(PORTS)}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def fun(word):
    cols=[sum(1<<x for x in range(512) if x>>p&1) for p in range(9)]
    for a,b in word:
        i,j=INDEX[a],INDEX[b]
        cols[i],cols[j]=cols[i]&cols[j],cols[i]|cols[j]
    return tuple(cols)
def advance(cols,word):
    cols=list(cols)
    for a,b in word:
        i,j=INDEX[a],INDEX[b]
        cols[i],cols[j]=cols[i]&cols[j],cols[i]|cols[j]
    return tuple(cols)
def evaluate(x,word):
    for a,b in word:
        if x>>a&1 and not x>>b&1:x^=(1<<a)|(1<<b)
    return x
def encode(values):
    return b''.join(int(x).to_bytes(2,'little') for x in values)
def profilekey(case):
    return tuple(map(tuple,case['low'])),tuple(map(tuple,case['high']))
def main():
    start=time.monotonic()
    cover=json.loads((PREV/'pre6-cover.json').read_text())
    intake=json.loads((PREV/'p20-intake.json').read_text())
    prepared=json.loads((PREV/'preparation-functions.json').read_text())
    states=cover['states']
    candidates=cover['first6_cases']
    function_words={0:[[]]}
    for data in prepared:
        paths=[]
        for row in data['functions']:
            if row['parent'] is None:word=[]
            else:word=paths[row['parent']]+[row['gate']]
            need(len(word)==row['length'],'preparation parent/length mismatch')
            paths.append(word)
        function_words[data['n']]=paths
    tmap={}
    for wi,item in enumerate(cover['all_event_words']):
        sid=item['state_id'];word=item['event_word'];columns=fun(word)
        key=(sid,columns)
        previous=tmap.get(key)
        if previous is None or len(word)<len(previous['word']):
            tmap[key]={'state_id':sid,'word':word,'original_event_index':wi,'columns':columns}
    ts=list(tmap.values())
    print(json.dumps({'stage':'T','original_event_words':len(cover['all_event_words']),'distinct_full_function_profile_pairs':len(ts),'by_dead_ports':dict(Counter(len(states[x['state_id']]['preparation_ports']) for x in ts))}),flush=True)
    tfmap={};preparation_compositions=0
    for ti,t in enumerate(ts):
        dead=states[t['state_id']]['preparation_ports']
        for fi,local in enumerate(function_words[len(dead)]):
            mapped=[[dead[a],dead[b]] for a,b in local]
            columns=advance(t['columns'],mapped)
            preparation_compositions+=1
            key=(t['state_id'],columns)
            entry={'state_id':t['state_id'],'t_index':ti,'preparation_index':fi,'preparation_word':mapped,'word':t['word']+mapped,'columns':columns}
            old=tfmap.get(key)
            if old is None or len(entry['word'])<len(old['word']):tfmap[key]=entry
    tfs=list(tfmap.values())
    print(json.dumps({'stage':'TF','all_preparation_compositions':preparation_compositions,'distinct_full_function_profile_pairs':len(tfs),'by_word_length':dict(Counter(len(x['word']) for x in tfs))}),flush=True)
    prefix=intake['cases'][1]['gates']
    image=sorted({evaluate(x,prefix) for x in range(8192)})
    need(len(image)==209,'H22 full image differs')
    joint={};all_joint_cases=0
    for ti,tf in enumerate(tfs):
        sid=tf['state_id']
        outputs=[evaluate(x,tf['word']) for x in image]
        for case in candidates[sid]['cases']:
            r=case['partner']
            if r==4:continue
            gate=sorted((6,r));after=sorted({evaluate(x,[gate]) for x in outputs})
            key=(profilekey(case),encode(after))
            record={'state_id':sid,'tf_index':ti,'partner':r,'low':case['low'],'high':case['high'],'word':tf['word']+[gate],'prefix_length':22+len(tf['word'])+1,'full_image':after}
            old=joint.get(key)
            if old is None or record['prefix_length']<old['prefix_length']:joint[key]=record
            all_joint_cases+=1
    records=list(joint.values())
    records.sort(key=lambda x:(x['prefix_length'],x['state_id'],x['partner'],x['word']))
    # Image-only folding is sufficient for sorting. Keep it separate from the
    # conservative profile-aware cover and always select a shortest prefix.
    best={}
    for i,record in enumerate(records):
        key=encode(record['full_image'])
        old=best.get(key)
        if old is None or record['prefix_length']<records[old]['prefix_length']:best[key]=i
    result={'agent':'six-sorting-2','role':'researcher','status':'COMPLETE_EXACT_PRE6_FUNCTION_AND_FIRST6_IMAGE_COVER_NO_SUFFIX_EXCLUSION','original_event_words':len(cover['all_event_words']),'distinct_T_function_profile_pairs':len(ts),'all_preparation_compositions':preparation_compositions,'distinct_TF_function_profile_pairs':len(tfs),'all_joint_cases':all_joint_cases,'joint_profile_image_pairs':len(records),'joint_distinct_images':len(best),'T_by_dead_ports':dict(Counter(len(states[x['state_id']]['preparation_ports']) for x in ts)),'joint_by_prefix_length':dict(Counter(x['prefix_length'] for x in records)),'joint_by_partner':dict(Counter(x['partner'] for x in records)),'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'seconds':time.monotonic()-start,'boundary':'The all-event pre6 cover and complete preparation closures are imported generated exact premises. Full-function folding keeps compatible profiles; joint image folding selects shortest prefixes. Postjoint event cover, semantic certificates and suffix exclusion are not inferred.'}
    (ROOT/'joint-cover.json').write_text(json.dumps({'summary':result,'joint_roots':records,'image_only_selected_roots':sorted(best.values())},separators=(',',':'))+'\n')
    # Full functions are operational evidence, not publication artifacts.
    (ROOT/'tf-cover.json').write_text(json.dumps({'T':ts,'TF':tfs},separators=(',',':'))+'\n')
    (ROOT/'joint-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':main()
