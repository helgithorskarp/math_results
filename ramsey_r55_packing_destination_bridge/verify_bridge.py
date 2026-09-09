"""Standalone literal verifier; imports no transport, normalizer, or encoder."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import re
from check_census import graph_lines, parse_line, require

PAIRS = list(combinations(range(43),2))

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def decode(g):
    require(type(g) is dict and type(g.get('n')) is int and g['n'] == 43, 'graph order')
    h=g.get('red_hex')
    require(type(h) is str and re.fullmatch('[0-9a-f]{226}',h) is not None,'graph format')
    w=int(h,16); require(w<2**903,'graph padding')
    return {e for k,e in enumerate(PAIRS) if w>>k&1}

def color(edges,u,v): return int(tuple(sorted((u,v))) in edges)
def mono(edges,s,c): return all(color(edges,u,v)==c for u,v in combinations(s,2))

@lru_cache(None)
def core_lines(cache,n): return graph_lines(cache,n)

def parameters(task):
    require(type(task) is str and re.fullmatch('bo1-q(8|9|10)-r([5-9]|10)-c[0-9]{6}',task) is not None,'task syntax')
    _,q,r,c=task.split('-');q=int(q[1:]);r=int(r[1:]);c=int(c[1:])
    require(5<=r<=q and 0<=c<{8:546356,9:362,10:4}[q],'task range')
    return q,r,c

@lru_cache(None)
def forbidden_pair(left,right):
    result=set()
    for s in combinations(range(8),5):
        for c in (0,1):
            fixed=[]; mask=0
            for u,v in combinations(s,2):
                if v<4: fixed.append(left)
                elif u>=4: fixed.append(right)
                else: mask |= 1 << (4*u+v-4)
            if all(x==c for x in fixed): result.add((mask,mask if c else 0))
    return tuple(sorted(result))

def check_carrier(task,g,cache):
    q,r,c=parameters(task); edges=decode(g); core=parse_line(core_lines(str(cache),43-4*q)[c],43-4*q)
    for i in range(q): require(mono(edges,range(4*i,4*i+4),int(i<r)),'block color')
    for u,v in combinations(range(43-4*q),2):
        require(color(edges,4*q+u,4*q+v)==int((u,v) in core),'task core')
    words=[]
    for i,j in combinations(range(q),2):
        w=sum(color(edges,4*i+u,4*j+v)<<(4*u+v) for u in range(4) for v in range(4))
        require(all(w&mask!=bad for mask,bad in forbidden_pair(int(i<r),int(j<r))),'two-block Ramsey domain')
        if i==0:
            signatures=[sum(color(edges,u,4*j+v)<<u for u in range(4)) for v in range(4)]
            require(signatures==sorted(signatures,reverse=True),'root columns')
            words.append(w)
    require(words[:r-1]==sorted(words[:r-1],reverse=True),'red block order')
    require(words[r-1:]==sorted(words[r-1:],reverse=True),'blue block order')
    for i in range(q):
        for v in range(4*q,43):
            require(not all(color(edges,u,v)==int(i<r) for u in range(4*i,4*i+4)),'block-core star')
    require(all(not mono(edges,s,1) for s in combinations(range(4*r,43),4)),'red maximality')
    return q,r,edges

def physical(source,target,permutation):
    require(type(permutation) is list and all(type(x) is int for x in permutation) and sorted(permutation)==list(range(43)),'physical permutation')
    before,after=decode(source),decode(target)
    for u,v in PAIRS:
        require(color(before,permutation[u],permutation[v])==color(after,u,v),'903-edge transport')
    return 903

def check_normalization(source,result,cache):
    require(result['status']=='ORDERED_CARRIER_NO_RAMSEY_VERDICT','normalization status')
    q,r,_=check_carrier(result['task'],result['graph'],cache)
    require(q in (9,10),'normalization destination order')
    require((q,r)==(len(source['blocks']),source['r']),'normalization class')
    p=result['new_to_old']; checks=physical(source,result['graph'],p)
    require(sorted(p[4*q:])==sorted(source['core']),'normalization core partition')
    source_red={frozenset(x) for x in source['blocks'][:r]}
    source_blue={frozenset(x) for x in source['blocks'][r:]}
    require({frozenset(p[4*i:4*i+4]) for i in range(r)}==source_red,'red block partition')
    require({frozenset(p[4*i:4*i+4]) for i in range(r,q)}==source_blue,'blue block partition')
    return checks

def selected(edges,core,size):
    used=set(); answer=[]
    for e in combinations(sorted(core),2):
        if color(edges,*e) and not used.intersection(e): answer.append(e);used.update(e)
    require(len(answer)>=size,'matching too short')
    return answer[:size]

def violation(edges,q,r):
    if q==10:return False
    matches=selected(edges,range(4*q,43),4 if q==8 else 2)
    return any(all(color(edges,u,v) for part,edge in ((s,e),(tuple(x for x in b if x not in s),f)) for u in part for v in edge)
               for i in range(r) for b in [list(range(4*i,4*i+4))]
               for e,f in combinations(matches,2) for s in combinations(b,2))

def check_reduce(source,result,cache):
    require(result['source_sha256']==digest(source),'source binding')
    if result['status']=='MONOCHROMATIC_FIVE':
        s=result['vertices'];c=result['color']
        require(type(s) is list and len(s)==5 and len(set(s))==5 and all(type(x) is int and 0<=x<43 for x in s),'five-set')
        require(type(c) is int and c in (0,1) and mono(decode(source),s,c),'monochromatic-five certificate')
        return {'status':'VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE','edge_identities':10}
    require(result['status']=='REDUCED_FAMILY_CARRIER_NO_RAMSEY_VERDICT','reduction status')
    require(result['source_task']==source['task'],'source task')
    q,r,_=check_carrier(source['task'],source,cache)
    require(q in (8,9),'source class')
    name=source['task'];current={'n':43,'red_hex':source['red_hex']};permutation=list(range(43));checks=0
    require(type(result['steps']) is list and len(result['steps'])<=10-q,'step limit')
    for step in result['steps']:
        ex=step['exchange'];norm=step['normalization']
        obj=dict(current,blocks=[list(range(4*i,4*i+4)) for i in range(q)],core=list(range(4*q,43)),r=r)
        require(ex['status']=='PACKING_TRANSPORT_NEEDS_CATALOG_AND_ROOT_ORDER' and ex['source_sha256']==digest(obj),'exchange binding')
        i=ex['replaced_block'];require(type(i) is int and 0<=i<r,'replacement block')
        first,second=ex['new_blocks_old_labels'];b=obj['blocks'][i];edges=decode(current)
        require(len(first)==len(second)==4 and len(set(first+second))==8,'exchange blocks')
        require(set(first+second).intersection(b)==set(b) and len(set(first).intersection(b))==2 and len(set(second).intersection(b))==2,'exchange split')
        e=tuple(sorted(set(first)-set(b)));f=tuple(sorted(set(second)-set(b)))
        m=selected(edges,obj['core'],4 if q==8 else 2)
        require(e in m and f in m and e!=f,'selected exchange edges')
        require(mono(edges,first,1) and mono(edges,second,1),'exchange red cliques')
        blocks=[x for j,x in enumerate(obj['blocks'][:r]) if j!=i]+[first,second]+obj['blocks'][r:]
        core=[v for v in obj['core'] if v not in e+f]
        require(ex['new_to_old']==sum(blocks,[])+core,'exchange permutation convention')
        mid=ex['output'];require(mid['r']==r+1 and mid['blocks']==[list(range(4*j,4*j+4)) for j in range(q+1)] and mid['core']==list(range(4*(q+1),43)),'exchange output partition')
        checks+=physical(current,mid,ex['new_to_old'])
        checks+=check_normalization(mid,norm,cache)
        permutation=[permutation[ex['new_to_old'][x]] for x in norm['new_to_old']]
        current=norm['graph'];name=norm['task'];q+=1;r+=1
    require(result['destination_task']==name and result['graph']==current and result['new_to_old']==permutation,'final destination binding')
    checks+=physical(source,result['graph'],permutation)
    q,r,edges=check_carrier(name,result['graph'],cache)
    require(not violation(edges,q,r),'terminal reduced-family clause')
    return {'status':'VERIFIED_REDUCED_FAMILY_CARRIER_NO_RAMSEY_VERDICT','edge_identities':checks,'steps':len(result['steps'])}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('source');p.add_argument('certificate');p.add_argument('--normalization',action='store_true');args=p.parse_args()
    source=json.loads(Path(args.source).read_text());cert=json.loads(Path(args.certificate).read_text())
    result=({'status':'VERIFIED_NORMALIZATION_NO_RAMSEY_VERDICT','edge_identities':check_normalization(source,cert,args.cache)} if args.normalization and cert['status']!='MONOCHROMATIC_FIVE' else check_reduce(source,cert,args.cache))
    print(json.dumps(result,sort_keys=True))
