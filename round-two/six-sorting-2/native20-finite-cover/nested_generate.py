"""Exact bounded nested B7 upgrade of the765 remaining exact roots.
The generic nested operator is imported from published lemma9007.
"""
import hashlib,importlib.util,json,resource,sys,time
from collections import Counter
from functools import lru_cache
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
BASE=HERE.parent/'native24-kernel-cover'
spec=importlib.util.spec_from_file_location('native20_nested_published_producer',BASE/'nested_generate.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
def need(ok,msg):
    if not ok:raise ValueError(msg)
@lru_cache(None)
def inner(word):
    data=q.s.analyze(7,word);anchors=q.m.base.anchors.both(7,data)
    b=max(16,*(a['lower_bound'] for a in anchors.values()))
    return {'inner_records_sha256':{name:q.m.base.digest(a['records']) for name,a in data.items()},'inner_anchor_leaves':{side:[[r['port'],r['label']] for r in a['rows']] for side,a in anchors.items()},'inner_anchor_bounds':{side:a['lower_bound'] for side,a in anchors.items()},'inner_bound':b}
def upgrade(gates,record):
    pruned=q.m.prune(gates,record)
    result=inner(tuple(map(tuple,pruned['retained_prefix'])))
    return {'pruning':pruned,**result,'prefix_cost':record[4]+record[5],'nested_label':record[4]+record[5]+result['inner_bound']}
def main():
    start=time.monotonic();begin=int(sys.argv[1]);stop=int(sys.argv[2])
    roots=json.loads((ROOT/'postjoint-cover.json').read_text())['roots']
    remaining=json.loads((ROOT/'constant-remaining-roots.json').read_text())
    stop=min(stop,len(remaining));prefix=json.loads((ROOT/'p20-intake.json').read_text())['cases'][1]['gates']
    originals=set(map(tuple,json.loads((HERE/'fixture.json').read_text())['selected_original_clampings']))
    originals=sorted(originals)
    excluded=[];open_roots=[];upgrade_count=0;bounds=Counter()
    for position in range(begin,stop):
        rid=remaining[position];root=roots[rid];gates=prefix+root['word']
        records=[q.record_for(gates,lo,hi) for lo,hi in originals]
        classes={}
        for i,row in enumerate(records):
            label=row[4]+row[5]+16;tag=tuple(row[2:4])
            if label>classes.get(tag,(-1,None,None))[0]:classes[tag]=(label,i,None)
        initial_mass=sum(2**r[0] for r in classes.values())
        need(initial_mass<=2**44,'constant remaining root already excluded')
        bestfirst=sorted({v[1] for v in classes.values()},key=lambda i:(-(records[i][4]+records[i][5]),records[i][:2]))
        others=sorted(set(range(len(records)))-set(bestfirst),key=lambda i:(-(records[i][4]+records[i][5]),records[i][:2]))
        mass=initial_mass;attempts=0
        for i in bestfirst+others:
            row=records[i];w=upgrade(gates,row);upgrade_count+=1;attempts+=1;bounds[w['inner_bound']]+=1
            tag=tuple(row[2:4])
            if w['nested_label']>classes[tag][0]:
                old=classes[tag][0];classes[tag]=(w['nested_label'],i,w);mass+=2**w['nested_label']-2**old
            if mass>2**44:break
        if mass>2**44:
            selected=[]
            for tag,(label,i,w) in sorted(classes.items()):
                if w is None:selected.append({'original':records[i][:2],'current':list(tag),'outer_record':records[i],'inner_bound':16,'nested_label':label,'constant_only':True})
                else:selected.append({'original':records[i][:2],'current':list(tag),'constant_only':False,**w})
            excluded.append({'root':rid,'remaining_position':position,'prefix_length':root['prefix_length'],'initial_constant_mass':initial_mass,'selected_mass':mass,'total_lower_bound':(mass-1).bit_length(),'attempted_upgrades':attempts,'selected_domains':selected})
        else:open_roots.append({'root':rid,'remaining_position':position,'best_selected_mass':mass,'constant_mass':initial_mass,'attempted_upgrades':attempts})
        if (position-begin+1)%10==0:print(json.dumps({'processed':position-begin+1,'excluded':len(excluded),'open':len(open_roots),'inner_prefixes':inner.cache_info().currsize,'elapsed':time.monotonic()-start}),flush=True)
    summary={'agent':'six-sorting-2','role':'researcher','status':'COMPLETE_SELECTED_NESTED_SCREEN_FOR_DECLARED_REMAINING_ROOT_PARTITION','remaining_position_range':[begin,stop],'remaining_input_count':len(remaining),'original_selected_domains':len(originals),'exclusions':len(excluded),'not_excluded':len(open_roots),'upgrade_calls':upgrade_count,'distinct_inner_prefixes':inner.cache_info().currsize,'inner_bound_counts':dict(bounds),'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'boundary':'Published nested9007 and producer machinery imported; exact selected full cubes and original histories. Early stopping is sound when selected class mass is already >2^44. Failed selected bounds are not feasibility. New nested certificates still need independent numeric checks.'}
    (ROOT/f'nested-screen-{begin}-{stop}.json').write_text(json.dumps({'summary':summary,'sufficient_records':excluded,'not_excluded_roots':open_roots},separators=(',',':'))+'\n')
    print(json.dumps(summary,sort_keys=True),flush=True)
if __name__=='__main__':main()
