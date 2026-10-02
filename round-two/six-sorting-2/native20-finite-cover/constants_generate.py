"""Exact selected semantic (3,3) constant-bound screen of exact root cover."""
import hashlib,json,resource,sys,time
from collections import Counter
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
BASE=HERE.parent/'native24-kernel-cover'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def initial(lo,hi):
    free=[p for p in range(13) if not (lo|hi)>>p&1]
    n=len(free);allbits=(1<<(1<<n))-1
    columns=[0]*13
    for p in range(13):
        if hi>>p&1:columns[p]=allbits
    for i,p in enumerate(free):columns[p]=sum(1<<x for x in range(1<<n) if x>>i&1)
    return lo,hi,0,0,tuple(columns)
def advance(state,word):
    lo,hi,d,r,cols=state;cols=list(cols)
    for a,b in word:
        ba,bb=1<<a,1<<b;end=ba|bb
        if (lo|hi)&end:
            d+=1
            if (lo&end) in (ba,bb):lo=(lo&~end)|ba
            if (hi&end) in (ba,bb):hi=(hi&~end)|bb
        elif not cols[a]&~cols[b]:r+=1
        cols[a],cols[b]=cols[a]&cols[b],cols[a]|cols[b]
    return lo,hi,d,r,tuple(cols)
def main():
    start=time.monotonic();begin=int(sys.argv[1]);stop=int(sys.argv[2])
    data=json.loads((ROOT/'postjoint-cover.json').read_text());roots=data['roots'];stop=min(stop,len(roots))
    originals=set(map(tuple,json.loads((HERE/'fixture.json').read_text())['selected_original_clampings']))
    originals=sorted(originals)
    prefix=json.loads((ROOT/'p20-intake.json').read_text())['cases'][1]['gates']
    bases=[advance(initial(lo,hi),prefix) for lo,hi in originals]
    need(all(lo.bit_count()==hi.bit_count()==3 and not lo&hi for lo,hi in originals),'selected originals not (3,3)')
    controls=[];survivors=[];by_length=Counter()
    for index in range(begin,stop):
        root=roots[index];classes={}
        records=[]
        for oi,base in enumerate(bases):
            lo,hi,d,r,cols=advance(base,root['word'])
            tag=(lo,hi);label=d+r+16
            if label>classes.get(tag,(-1,None))[0]:classes[tag]=(label,oi)
        mass=sum(2**label for label,oi in classes.values())
        if mass>2**44:
            selected=[]
            for tag,(label,oi) in sorted(classes.items()):
                state=advance(bases[oi],root['word'])
                selected.append({'original':list(originals[oi]),'current':list(tag),'D':state[2],'R':state[3],'label':label})
            controls.append({'root':index,'prefix_length':root['prefix_length'],'mass':mass,'lower_bound':(mass-1).bit_length(),'selected':selected})
        else:survivors.append(index)
        by_length[root['prefix_length']]+=mass>2**44
    result={'agent':'six-sorting-2','role':'researcher','status':'COMPLETE_SELECTED_CONSTANT_SCREEN_FOR_DECLARED_ROOT_PARTITION','root_range':[begin,stop],'total_root_count':len(roots),'original_selected_domains':len(originals),'exclusions':len(controls),'not_excluded':len(survivors),'excluded_by_length':dict(by_length),'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'boundary':'Producer only: exact packed full128-cube semantic histories and selected class maxima with importedS7>=16/semantic8539. This is not a complete census of all clampings, and failed bounds are not feasibility.'}
    (ROOT/f'constant-screen-{begin}-{stop}.json').write_text(json.dumps({'summary':result,'sufficient_records':controls,'not_excluded_roots':survivors},separators=(',',':'))+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':main()
