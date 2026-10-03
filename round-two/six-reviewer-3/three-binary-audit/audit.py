"""Complete instance proof. Input comes from a published untrusted certificate.
Fresh engine/cover generic source was frozen before that certificate access.
"""
import sys,json,itertools
from collections import Counter
from engine import *
from cover import local,forest,semigroup
from input_adapter import check

def run(cover,cert,start=0,stop=None):
    require(cert['literal_prefix']==[list(g) for g in Q] and cert['dead_ports']==list(DEAD) and cert['size_budget']==44,'literal scope')
    require(cert['imported_live_head_lemma']=='10034/0','live premise')
    early=cert['early_negative_first_gates'];require(sorted(tuple(e['gate']) for e in early)==sorted(EARLY),'early gates incomplete');early_records=[]
    for e in early:early_records.append({'gate':e['gate'],'result':check(Q+(tuple(e['gate']),),e['witness'])})
    # Complete independent cover has a shortest representative for every ordered
    # whole-Q function. All actual witness prefixes must be these literal words.
    representatives={gates(r['word']):r for r in cover['representatives']};table=cert['function_bindings'];words=[gates(r[0]) for r in table]
    require(len(words)==len(set(words)) and set(words)==set(representatives),'missing/duplicate/wrong minimum functions')
    total_functions=len(table);table=table[start:stop]
    results=[];live=0;covered=0;counts=Counter();witnessuses=Counter();domains=set();physical_hashes={};firsts={}
    def checked(word,index):
        require(type(index)is int and 0<=index<len(cert['witnesses']),'bad witness index')
        w=cert['witnesses'][index];r=check(word,w)
        witnessuses[index]+=1;firsts.setdefault(index,(word,w))
        for rec in r.get('records',[r.get('record')]):
            if rec is None:continue
            domains.add(tuple(rec[:2]));_,x,free=replay(word,rec[0],rec[1]);key=(word,rec[0],rec[1])
            physical_hashes[key]=digest(list(rows(x,len(free))))
        counts[r['kind']]+=1;return r
    for word,heads in table:
        word=gates(word);require(len(heads)==len(DEAD),'head domain');rep=representatives[word];e,_=forest(word[:3])
        for q,bind in zip(DEAD,heads):
            H=tuple(sorted((8,q)));front=Q+word+(H,)
            if bind=='L':require(q in e,'freed partner falsely imported live');live+=1;continue
            require(q not in e,'live branch not explicitly imported')
            if type(bind)is int:
                result=checked(front,bind);results.append({'word':word,'head':q,'tail':None,'index':bind,'result':result});covered+=3
            else:
                require(type(bind)is list and len(bind)==3,'tails missing');Ts=tails(q);require(len(Ts)==3,'own balanced tails')
                # Decode all possible slot permutations without importing native
                # tail ordering. A matching must be a bijection, not cherry-picked
                # isolated tail coverage; every submitted slot is checked.
                chosen=None
                for perm in itertools.permutations(range(3)):
                    try:
                        for t,j in zip(Ts,perm):check(front+t,cert['witnesses'][bind[j]])
                    except (ValueError,IndexError,KeyError):continue
                    chosen=perm;break
                require(chosen is not None,'not all three actual tails excluded')
                for t,j in zip(Ts,chosen):
                    result=checked(front+t,bind[j]);results.append({'word':word,'head':q,'tail':t,'index':bind[j],'slot':j,'result':result});covered+=1
    require(live==3*len(table) and covered==9*len(table),'complete live/freed coverage')
    if start==0 and stop is None:require(set(witnessuses)==set(range(len(cert['witnesses']))),'unused instance witness')
    first=[]
    for i,(word,w) in sorted(firsts.items()):first.append({'index':i,'word':word,'witness':w})
    cubes=[{'word':word,'low':lo,'high':hi,'whole_rows_sha256':v} for (word,lo,hi),v in sorted(physical_hashes.items())]
    return {'slice':[start,start+len(table)],'total_functions':total_functions,'scope':'10084/0, relative10034 live-head theorem and primary S(k)','early':early_records,'census':cover['census'],'live_heads':live,'freed_tail_alternatives':covered,'binding_kinds':dict(counts),'numerical_bindings':len(results),'original_domains':sorted(domains),'witness_uses':sorted(witnessuses.items()),'actual_bindings':results,'physical_cubes':cubes,'scalar_first_witnesses':first,'full_case_cover_sha256':digest(cover)}
if __name__=='__main__':
    c=json.load(open(sys.argv[1]));instance=json.load(open(sys.argv[2]));out=run(c,instance,int(sys.argv[4]) if len(sys.argv)>4 else 0,int(sys.argv[5]) if len(sys.argv)>5 else None);open(sys.argv[3],'w').write(json.dumps(out,separators=(',',':'),sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k in ('live_heads','freed_tail_alternatives','binding_kinds','numerical_bindings','census')}));print('whole_record_sha256',digest(out))
