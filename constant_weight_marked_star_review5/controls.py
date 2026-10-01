"""Small literal subset controls for the reviewer-owned whole-star kernel."""
from collections import Counter
from itertools import combinations
import random
from marked import model, solve, packing, require, Incomplete
from classify import maps, image

def brute(eligible, columns, quota, mandatory):
    output=[]
    for mask in range(1<<len(columns)):
        chosen=tuple(i for i in range(len(columns)) if mask>>i&1)
        blocks=tuple(columns[i] for i in chosen)
        counts=Counter(p for q in blocks for p in combinations(q,2))
        if any(n>1 for n in counts.values()):continue
        if tuple(sum(x in q for q in blocks) for x in range(15))!=tuple(quota):continue
        if set(mandatory)<=set(counts):output.append(chosen)
    return tuple(sorted(output))

def controls(reference):
    eligible=tuple(combinations(range(15),2));rng=random.Random(1908350)
    pool=tuple(combinations(range(9),4));positive=0;negative=0;cases=0
    for number in range(48):
        columns=tuple(sorted(rng.sample(pool,8)))
        chosen=[];used=set()
        for i in rng.sample(range(8),8):
            pairs=set(combinations(columns[i],2))
            if not used&pairs and rng.randrange(2):chosen.append(i);used|=pairs
        quota=tuple(sum(x in columns[i] for i in chosen) for x in range(15))
        mandatory=tuple(p for p in sorted(used) if number%3 and rng.randrange(2))
        if number%4==3:
            quota=quota[:-1]+(1,)
        expected=brute(eligible,columns,quota,mandatory)
        actual,_=solve(eligible,columns,quota,mandatory)
        require(actual==expected,'whole-star versus literal subset mismatch')
        positive+=bool(actual);negative+=not bool(actual);cases+=1
    data=model();columns=data['candidates'];last=columns[-1]
    quota=tuple(int(x in last) for x in range(15))
    actual,_=solve(data['eligible'],columns,quota,tuple(combinations(last,2)))
    require(actual==((224,),),'225-column/high-bit boundary failure')
    empty,_=solve(data['eligible'],columns,(0,)*15,())
    require(empty==((),),'empty optional-column case')
    rejected=[]
    def reject(name,call,error=ValueError):
        try:call()
        except error:rejected.append(name)
        else:raise ValueError('control accepted '+name)
    single=(last,);pairs=tuple(combinations(last,2))
    reject('short quota',lambda:solve(data['eligible'],single,(0,)*14,pairs))
    reject('negative quota',lambda:solve(data['eligible'],single,(-1,)+(0,)*14,pairs))
    reject('float quota',lambda:solve(data['eligible'],single,(0.0,)+(0,)*14,pairs))
    reject('duplicate column',lambda:solve(data['eligible'],single*2,quota,pairs))
    reject('repeated point',lambda:solve(eligible,((0,0,1,2),),quota,()))
    reject('outside point',lambda:solve(eligible,((0,1,2,15),),quota,()))
    reject('column outside eligible pairs',lambda:solve((),single,quota,()))
    reject('duplicate pair',lambda:solve(eligible+eligible[:1],single,quota,()))
    reject('bad pair',lambda:solve(((0,0),),(),(0,)*15,()))
    reject('unknown mandatory',lambda:solve((),(),(0,)*15,((0,1),)))
    reject('duplicate mandatory',lambda:solve(data['eligible'],single,quota,pairs+pairs[:1]))
    reject('negative guard',lambda:solve(data['eligible'],single,quota,pairs,limit=-1))
    reject('escalated guard',lambda:solve(data['eligible'],single,quota,pairs,limit=200001))
    reject('invalid seconds',lambda:solve(data['eligible'],single,quota,pairs,seconds=0))
    reject('escalated seconds',lambda:solve(data['eligible'],single,quota,pairs,seconds=11))
    reject('zero guard is INCOMPLETE',lambda:solve(data['eligible'],single,quota,pairs,limit=0),Incomplete)
    reject('bad packing duplicate',lambda:packing(reference[:-1]+reference[:1]))
    reject('wrong marked point',lambda:packing(reference,15))
    group,_=maps(reference,reference)
    false=tuple([1,0]+list(range(2,17)))
    require(image(reference,false)!=tuple(reference) and false not in group,'false point map accepted')
    require(positive and negative,'missing positive or negative literal control')
    return dict(status='COMPLETE',literal_subset_cases=cases,positive_cases=positive,
                negative_cases=negative,boundary_column_index=224,rejections=rejected,
                false_point_map_rejected=True,checks_use_assert=False)

if __name__=='__main__':
    import json
    from pathlib import Path
    here=Path(__file__).parent
    path=here/'expected.json' if (here/'expected.json').exists() else here/'classification.json'
    data=json.loads(path.read_text());record=data.get('classification',data)
    print(json.dumps(controls(tuple(tuple(q) for q in record['own_reference'])),indent=2))
