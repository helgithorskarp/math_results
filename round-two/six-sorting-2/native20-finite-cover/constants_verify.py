"""Independent numeric-image-set checker of selected semantic certificates.
Distinct original ranks and full cubes establish each initial image. Cached
transitions use scalar min/max on every current numeric category-image row.
"""
import hashlib,json,resource,time
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
PREV=ROOT
COUNTS=defaultdict(int)
def need(ok,msg):
    if not ok:raise ValueError(msg)
def initial_numeric(lo,hi,word):
    lows=[p for p in range(13) if lo>>p&1]
    highs=[p for p in range(13) if hi>>p&1]
    free=[p for p in range(13) if not (lo|hi)>>p&1]
    need(len(lows)==len(highs)==3 and len(free)==7 and not lo&hi,'original not full (3,3) clamping')
    touches=None;active=0;images=set();tag=None
    for x in range(128):
        values=[0]*13
        for rank,p in enumerate(lows):values[p]=rank-3
        for rank,p in enumerate(highs):values[p]=rank+2
        for j,p in enumerate(free):values[p]=x>>j&1
        hitmask=0
        for gi,(a,b) in enumerate(word):
            hit=values[a]<0 or values[b]<0 or values[a]>1 or values[b]>1
            if hit:hitmask|=1<<gi
            elif values[a]>values[b]:active|=1<<gi
            values[a],values[b]=min(values[a],values[b]),max(values[a],values[b])
        current=(sum(1<<p for p,v in enumerate(values) if v<0),sum(1<<p for p,v in enumerate(values) if v>1))
        if touches is None:touches=hitmask;tag=current
        need(touches==hitmask and tag==current,'free-dependent numeric marker route')
        images.add(sum(1<<p for p,v in enumerate(values) if v==1))
        COUNTS['original_full_cube_assignments']+=1
        COUNTS['original_numeric_gate_controls']+=len(word)
    redundant=((1<<len(word))-1)&~(touches|active)
    return tag[0],tag[1],tuple(sorted(images)),touches.bit_count(),redundant.bit_count()
@lru_cache(None)
def numeric_transition(lo,hi,image,gate):
    a,b=gate;end=(1<<a)|(1<<b);touched=bool((lo|hi)&end)
    active=False;out=set();tag=None
    for x in image:
        va=-1 if lo>>a&1 else 2 if hi>>a&1 else x>>a&1
        vb=-1 if lo>>b&1 else 2 if hi>>b&1 else x>>b&1
        mn,mx=min(va,vb),max(va,vb)
        current=(lo&~end | ((1<<a) if mn<0 else 0) | ((1<<b) if mx<0 else 0),hi&~end | ((1<<a) if mn>1 else 0) | ((1<<b) if mx>1 else 0))
        if tag is None:tag=current
        need(tag==current,'category route depends on free row')
        out.add(x&~end | ((1<<a) if mn==1 else 0) | ((1<<b) if mx==1 else 0))
        active|=not touched and va>vb
        COUNTS['numeric_conditional_row_controls']+=1
    need(out,'empty conditional full-cube image')
    return tag[0],tag[1],tuple(sorted(out)),int(touched),int(not touched and not active)
def main():
    start=time.monotonic()
    roots=json.loads((ROOT/'postjoint-cover.json').read_text())['roots']
    pieces=[]
    for begin,stop in [(0,135),(135,4231),(4231,23006)]:
        piece=json.loads((ROOT/f'constant-screen-{begin}-{stop}.json').read_text())
        need(piece['summary']['root_range']==[begin,stop],'screen partition differs')
        pieces.append(piece)
    need(pieces[-1]['summary']['root_range'][1]==len(roots),'screen partitions do not cover entire root family')
    sufficient=[];not_excluded=[]
    for p in pieces:sufficient.extend(p['sufficient_records']);not_excluded.extend(p['not_excluded_roots'])
    ids=[x['root'] for x in sufficient]+not_excluded
    need(sorted(ids)==list(range(len(roots))),'root classification missing or duplicated')
    grouped=defaultdict(list)
    for record in sufficient:
        rid=record['root'];r=roots[rid]
        need(record['prefix_length']==r['prefix_length'],'certificate root length differs')
        tags=[tuple(w['current']) for w in record['selected']]
        need(len(tags)==len(set(tags)),'selected current classes repeat')
        for witness in record['selected']:grouped[tuple(witness['original'])].append((rid,witness))
    prefix=json.loads((PREV/'p20-intake.json').read_text())['cases'][1]['gates']
    verified=0
    for original,occurrences in sorted(grouped.items()):
        base=initial_numeric(*original,prefix)
        @lru_cache(None)
        def state(word):
            if not word:return base
            lo,hi,image,d,r=state(word[:-1])
            nl,nh,newimage,dd,dr=numeric_transition(lo,hi,image,word[-1])
            return nl,nh,newimage,d+dd,r+dr
        for rid,witness in occurrences:
            word=tuple(map(tuple,roots[rid]['word']))
            lo,hi,image,d,r=state(word)
            need([lo,hi]==witness['current'] and d==witness['D'] and r==witness['R'],'numeric semantic record differs')
            need(witness['label']==d+r+16,'selected constant label differs')
            verified+=1
        COUNTS['shared_literal_prefix_states']+=state.cache_info().currsize
        state.cache_clear()
    for record in sufficient:
        mass=sum(2**w['label'] for w in record['selected'])
        need(mass==record['mass'] and mass>2**44,'selected mass does not exclude')
        need((mass-1).bit_length()==record['lower_bound'],'selected lower bound differs')
    result={'agent':'six-sorting-2','role':'researcher','status':'ALL_SELECTED_CONSTANT_ROOT_CERTIFICATES_NUMERIC_IMAGE_SET_VERIFIED','total_roots':len(roots),'verified_exclusions':len(sufficient),'not_excluded_roots':len(not_excluded),'selected_domain_occurrences':verified,'distinct_original_clampings':len(grouped),'numeric_transition_states':numeric_transition.cache_info().currsize,'metrics':dict(COUNTS),'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'boundary':'Selected immutable original full seven-free-input domains are retained. Numeric full-cube base rows and scalar min/max over exact conditional image sets differ from producer packed columns. Category collapse of only marked ranks preserves free Boolean values/marker masks/D/R and is an unformalized bridge. ImportedS7>=16 and semantic transport8539 are explicit. Failed bounds are not feasibility;765 targets require the separately checked nested stage.'}
    (ROOT/'verify-constants.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'constant-remaining-roots.json').write_text(json.dumps(sorted(not_excluded),separators=(',',':'))+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':main()
