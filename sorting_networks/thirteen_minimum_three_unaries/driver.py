"""Housekeeping, compact certificate checks and private caching only.
Author: six-sorting-1, researcher. Comparator mathematics is in the two
independent scripts. Run the generator to completion before the verifier.
"""
import argparse
from collections import OrderedDict
import hashlib
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
FIELDS = ('kernel','status','phase_counts','states','edges','maximum_cuts','weight_cuts','prefix_state_hashes')
NODE_FIELDS = ('prefix','seed_sha256','count','processed','nongate_edges','maximum_cuts','weight_cuts','state_sha256')
MEMO = OrderedDict()
MEMO_STATES = 0


def digest(value, keys=False):
    return hashlib.sha256(json.dumps(value,sort_keys=keys,separators=(',',':')).encode()).hexdigest()


def source_hash():
    return ''.join(hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                   for name in ('generate.py','verify.py','driver.py','fixture.json','certificate.json'))


def read_node(path):
    """Decode and validate immutable local data; no comparator mathematics."""
    global MEMO_STATES
    if path in MEMO:
        MEMO.move_to_end(path)
        return MEMO[path]
    record=json.loads(path.read_text())
    states=frozenset((bool(flag),tuple(map(tuple,profile))) for flag,profile in record.pop('states'))
    assert len(states)==record['count'] and digest(sorted(states))==record['state_sha256']
    while MEMO and MEMO_STATES+len(states)>50000:
        old_record,old_states=MEMO.popitem(last=False)[1]
        MEMO_STATES-=len(old_states)
    if len(states)<=50000:
        MEMO[path]=(record,states)
        MEMO_STATES+=len(states)
    return record,states


def finalize(cases, certificate, cache):
    canonical = [{key:case[key] for key in FIELDS} for case in cases]
    nodes = [json.loads(path.read_text()) for path in cache.glob('*.json')]
    nodes.sort(key=lambda node:node['prefix'])
    summary = {
      'all_kernel_words':1138,'forbidden9_words':288,'permitted_cases':850,
      'case_sha256':digest(canonical,True),
      'state_appearances':sum(c['states'] for c in cases),
      'transitions':sum(c['edges'] for c in cases),
      'maximum_cuts':sum(c['maximum_cuts'] for c in cases),
      'weight_cuts':sum(c['weight_cuts'] for c in cases),
      'largest_class_states':max(c['states'] for c in cases),
      'phase_state_appearances':[sum(c['phase_counts'][i] for c in cases) for i in range(5)],
      'prefix_nodes':len(nodes),
      'prefix_node_sha256':digest([{k:n[k] for k in NODE_FIELDS} for n in nodes],True),
      'unique_node_states':sum(n['count'] for n in nodes),
      'unique_nongate_edges':sum(n['nongate_edges'] for n in nodes)}
    assert all(c['status']=='complete_empty_selected_kernel_closure' for c in cases)
    for key,value in summary.items():assert value==certificate['expected'][key],(key,value)
    word=certificate['selected_control']['kernel']
    case=next(c for c in cases if c['kernel']==word)
    for key in ('states','edges','phase_counts'):
        assert case[key]==certificate['selected_control'][key]
    state_hash=hashlib.sha256()
    for phase in range(4):
        node=json.loads((cache/(digest(word[:phase])+'.json')).read_text())
        for flag,profile in node['states']:
            state_hash.update(json.dumps((phase,flag,profile),separators=(',',':')).encode())
    assert state_hash.hexdigest()==certificate['selected_control']['state_sha256']
    return summary


def run(method,words,all_words,execute,controls,cache):
    if not __debug__:raise RuntimeError('Run with assertions enabled, without -O.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--resume',action='store_true')
    args=parser.parse_args()
    start=time.monotonic()
    certificate=json.loads((HERE/'certificate.json').read_text())
    assert len(all_words)==len(set(all_words))==1138
    assert digest(all_words)==certificate['catalogue_sha256']
    assert len(words)==850 and digest(words)==certificate['permitted_order_sha256']
    cache.mkdir(parents=True,exist_ok=True)
    progress_path=cache.parent/'progress.json'
    source=source_hash()
    if args.resume and progress_path.exists():
        saved=json.loads(progress_path.read_text())
        assert saved['source_sha256']==source and saved['method']==method
        cases=saved['cases']
        assert [c['kernel'] for c in cases]==[list(map(list,w)) for w in words[:len(cases)]]
    else:cases=[]
    before=len(cases)
    deferred=None
    for word in words[before:]:
        if time.monotonic()-start>=35:break
        case=execute(word,source,start+45)
        if case['status']!='complete_empty_selected_kernel_closure':
            deferred=case
            break
        assert case['states']<=50000 and len(case['phase_counts'])==5 and case['phase_counts'][-1]==0
        cases.append(json.loads(json.dumps({key:case[key] for key in FIELDS})))
        progress_path.write_text(json.dumps({'agent':'six-sorting-1','role':'researcher','method':method,
                                  'source_sha256':source,'cases':cases},separators=(',',':'))+'\n')
    result={'agent':'six-sorting-1','role':'researcher','method':method,
            'status':'all_cases_complete' if len(cases)==850 else 'batch_incomplete',
            'completed_cases':len(cases),'new_cases':len(cases)-before,
            'total_cases':850,'deferred':deferred,'controls':controls}
    if len(cases)==850:
        result['checked_certificate']=finalize(cases,certificate,cache)
    result['seconds']=time.monotonic()-start
    result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(json.dumps(result))
