"""six-sorting-2 researcher: complete36-class allowed-partner(6,8) reduction producer.

Profile/bit-plane/basic-boundary core credited to six-sorting-1/8281.
Large deterministic finite tables stay in the ignored generated directory.
"""
from collections import deque
import itertools
import json
import resource
import signal
import time
from shared import arguments,choose,digest,inputs,program


def internal(rows,g):
    root=tuple(rows);queue=deque([(root,())]);seen={root}
    gates=tuple(itertools.combinations(range(4),2))
    while queue:
        state,word=queue.popleft()
        if all(r==((1<<r.bit_count())-1)<<(4-r.bit_count()) for r in state):return len(word),word
        if len(word)==5:continue
        for gate in gates:
            child=tuple(sorted({g.replay(r,(gate,))[0] for r in state}))
            if child not in seen:seen.add(child);queue.append((child,word+(gate,)))
    raise AssertionError('A known five-gate full four-wire sorter sorts every subset')


def extended(f,t,word,index,image,budget,case,g):
    full=f['prefix22']+[[a+1,b+1] for a,b in word]
    rows=t['images9'][image];controls=[None,None];preimages={}
    for original in range(8192):
        out,_=g.replay(original,full)
        preimages.setdefault((out>>2)&511,original)
        for maximum,ones,target in ((False,7,8128),(True,6,8064)):
            if original.bit_count()!=ones or out!=target:continue
            _,spent=g.replay(original,full,maximum)
            control=controls[int(maximum)]
            if control is None or spent>control[1]:controls[int(maximum)]=original,spent
    assert sorted(preimages)==list(rows)
    for maximum,control in enumerate(controls):
        if control is None:continue
        x,spent=control
        if maximum:
            local=sorted({r>>5 for r in rows if r&31==0})
            required,cut=max((min(4,r.bit_count())-(r&480).bit_count(),r) for r in rows)
        else:
            local=sorted({r&15 for r in rows if r&496==496})
            required,cut=max((min(4,9-r.bit_count())-(4-(r&15).bit_count()),r) for r in rows)
        bound,witness=internal(local,g)
        cap=44-16-spent
        if required+bound<=cap:continue
        return dict(parent_index=index,image=image,budget=budget,case=case,mode='max' if maximum else 'min',boundary_size=4,
                    original_control=x,prefix_passages=spent,free_inputs=7,imported_size_bound=16,touch_cap=cap,
                    cut_row9=cut,cut_original=preimages[cut],required_crossings=required,
                    internal_rows=local,internal_lower_bound=bound,internal_positive_word=[list(p) for p in witness],
                    required_touches=required+bound)
    return None


def main():
    assert __debug__
    args=arguments();f,selected,fresh,old=inputs(args.repository)
    g=program(args.repository,'generate');args.output.mkdir(parents=True,exist_ok=True)
    monoids,_=g.local_monoids();root=tuple(f['initial_low']),tuple(f['initial_high']),False
    records=[];began=time.monotonic()
    def stop(signum,frame):
        raise TimeoutError('45-second per-class finite reduction bound: incomplete computation gives no exclusion')
    signal.signal(signal.SIGALRM,stop)
    for index,code,events,orders in choose(fresh,args.class_index):
        signal.alarm(45)
        seed=dict(f,class_code=code,parent_effective_words=orders)
        triples=g.class_triples(seed,root)
        assert all(r[1] in (48,53) for r in triples)
        t=g.completion_table(seed,root,monoids,triples)
        basic=[];extra=[];tails=[]
        for image,budget,case in t['remaining_completion_pairs']:
            word=g.prefix_word(seed,t,monoids,case)
            b=g.boundary_obstruction(seed,t,word,index,image,budget,case)
            if b is not None:basic.append(b);continue
            b=extended(seed,t,word,index,image,budget,case,g)
            if b is not None:extra.append(b);continue
            tails.append(dict(parent_index=index,class_code=code,image=image,budget=budget,case=case,
                              rows9=t['images9'][image],prefix_B11=[list(p) for p in word]))
        value=dict(table=t,basic_boundary=basic,extended_boundary=extra,tails=tails)
        (args.output/f'class{index:03d}.json').write_text(json.dumps(value,separators=(',',':'))+'\n')
        summary=dict(parent_index=index,class_code=code,effective_orders=orders,
                     first_touch_orders={str(k):sum(r[3] for r in triples if r[1]==k) for k in (48,53)},
                     phase_triples=len(triples),normalized_prefixes=len(t['local_map_cases']),
                     literal_images=len(t['images9']),image_budget_pairs=len(t['image_budget_pairs']),
                     prefix_activity=t['prefix_activity_excluded_pairs'],basic_boundaries=len(basic),
                     extended_boundaries=len(extra),solver_tails=len(tails),
                     table_sha256=digest(t),basic_boundary_sha256=digest(basic),
                     extended_boundary_sha256=digest(extra),tails_sha256=digest(tails))
        records.append(summary);print(json.dumps(summary),flush=True)
        signal.alarm(0)
    result=dict(agent='six-sorting-2',role='researcher',selected_classes=selected,new_classes=fresh,
                imported_complete_classes=old,local_monoids_sha256=digest(monoids),records=records,
                seconds=time.monotonic()-began,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (args.output/'reduction-summary.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
