"""Independent inverse13/rank/scalar coverage and every obstruction replay.

Credits six-sorting-1/8281 for the public independent core. Imports neither
the producer nor a SAT solver. New four-wire bounds use complete word lists.
"""
import itertools
import json
import resource
import signal
import time
from shared import HERE,arguments,choose,digest,inputs,program,read


def extended(record,full,rows,v):
    assert record['mode'] in ('min','max') and record['boundary_size']==4
    maximum=record['mode']=='max'
    control=record['original_control'];bits=[control>>i&1 for i in range(13)]
    marks=[i for i,b in enumerate(bits) if bool(b)==maximum];free=[i for i,b in enumerate(bits) if bool(b)!=maximum]
    assert len(marks)==6 and len(free)==record['free_inputs']==7
    assert v.scalar(bits,full)==tuple(sorted(bits))
    for mask in range(128):
        values=[None]*13
        for j,i in enumerate(marks):values[i]=2+j if maximum else -1-j
        for j,i in enumerate(free):values[i]=mask>>j&1
        out,charge=v.marked_simulate(values,full,maximum)
        assert {i for i,x in enumerate(out) if (x>1 if maximum else x<0)}==set(range(7,13) if maximum else range(6))
        assert charge==record['prefix_passages']
    assert record['imported_size_bound']==16
    assert record['touch_cap']==28-record['prefix_passages']
    cut=record['cut_row9'];assert cut in rows
    out=v.scalar([record['cut_original']>>i&1 for i in range(13)],full)
    assert sum(x<<i for i,x in enumerate(out[2:11]))==cut
    required=min(4,cut.bit_count())-(cut&480).bit_count() if maximum else min(4,9-cut.bit_count())-(4-(cut&15).bit_count())
    assert required==record['required_crossings']>0
    inner=sorted({r>>5 for r in rows if r&31==0}) if maximum else sorted({r&15 for r in rows if r&496==496})
    assert inner==record['internal_rows']
    lower=record['internal_lower_bound'];assert 1<=lower<=5
    gates=tuple(itertools.combinations(range(4),2));word_checks=0
    input_rows=[tuple(r>>i&1 for i in range(4)) for r in inner]
    for length in range(lower):
        for word in itertools.product(gates,repeat=length):
            assert any(v.scalar(row,word)!=tuple(sorted(row)) for row in input_rows),('Incorrect internal lower bound',word)
            word_checks+=1
    positive=record['internal_positive_word']
    assert len(positive)==lower and all(tuple(g) in gates for g in positive)
    assert all(v.scalar(row,positive)==tuple(sorted(row)) for row in input_rows)
    assert record['required_touches']==required+lower>record['touch_cap']
    return 128,word_checks


def extended_controls(v):
    gates=tuple(itertools.combinations(range(9),2));cuts=embeddings=0
    for maximum in (False,True):
        K=set(range(5,9) if maximum else range(4))
        control=[0]*5+[1]*4 if maximum else [0]*4+[1]*5
        for original in range(512):
            row=[original>>i&1 for i in range(9)]
            count=sum(row[i]==int(maximum) for i in K)
            for gate in gates:
                assert v.scalar(control,(gate,))==tuple(control)
                out=v.scalar(row,(gate,))
                crossing=(gate[0] in K)!=(gate[1] in K)
                assert 0<=sum(out[i]==int(maximum) for i in K)-count<=int(crossing)
                cuts+=1
        for original in range(16):
            local=[original>>i&1 for i in range(4)]
            row=[0]*5+local if maximum else local+[1]*5
            for gate in gates:
                out=v.scalar(row,(gate,))
                if not set(gate)<=K:assert out==tuple(row)
                else:
                    projected=(gate[0]-5,gate[1]-5) if maximum else gate
                    assert (out[5:] if maximum else out[:4])==v.scalar(local,(projected,))
                    assert (out[:5] if maximum else out[4:])==((0,)*5 if maximum else (1,)*5)
                embeddings+=1
    return cuts,embeddings


def summary(index,code,orders,t,basic,extra,tails):
    return dict(parent_index=index,class_code=code,effective_orders=orders,
                first_touch_orders={str(k):sum(r[3] for r in t['triples'] if r[1]==k) for k in (48,53)},
                phase_triples=len(t['triples']),normalized_prefixes=len(t['local_map_cases']),
                literal_images=len(t['images9']),image_budget_pairs=len(t['image_budget_pairs']),
                prefix_activity=t['prefix_activity_excluded_pairs'],basic_boundaries=len(basic),
                extended_boundaries=len(extra),solver_tails=len(tails),table_sha256=digest(t),
                basic_boundary_sha256=digest(basic),extended_boundary_sha256=digest(extra),tails_sha256=digest(tails))


def main():
    assert __debug__
    args=arguments();f,selected,fresh,old=inputs(args.repository)
    cert=read(HERE/'certificate.json')
    assert cert['schema']=='sorting13-partner68-reduction-v1'
    assert cert['selected_classes']==selected and cert['new_classes']==fresh and cert['imported_complete_classes']==old
    expected=fresh if args.class_index is None else choose(fresh,args.class_index)
    supplied={r['parent_index']:r for r in cert['records']}
    assert len(supplied)==len(cert['records'])
    assert all((i,code)==(supplied[i]['parent_index'],supplied[i]['class_code']) for i,code,e,n in expected)
    if args.class_index is None:assert len(cert['records'])==len(fresh)
    v=program(args.repository,'verify');began=time.monotonic()
    domains=v.reconstruct(f)
    root,outgoing,entries,graph=v.full_graph(f['prefix22'])
    assert v.canonical(root)==(tuple(f['initial_low']),tuple(f['initial_high']),False)
    monoids,_=v.rank_monoids();assert digest(monoids)==cert['local_monoids_sha256']
    results=[];extra_word_checks=0;extra_marked=0
    def stop(signum,frame):
        raise TimeoutError('45-second per-class verification limit: incomplete is not exclusion')
    signal.signal(signal.SIGALRM,stop)
    for index,code,events,orders in choose(fresh,args.class_index):
        signal.alarm(45)
        seed=dict(f,class_code=code,parent_effective_words=orders)
        triples=v.independent_triples(seed,root,outgoing)
        assert all(r[1] in (48,53) for r in triples)
        t,activity=v.completion_table(seed,root,outgoing,monoids,triples)
        saved=read(args.output/f'class{index:03d}.json')
        assert json.loads(json.dumps(t))==saved['table']
        basic=saved['basic_boundary'];extra=saved['extended_boundary'];tails=saved['tails']
        records=basic+extra+tails
        keys=[(r['image'],r['budget'],r['case']) for r in records]
        assert len(keys)==len(set(keys)) and set(keys)=={tuple(r) for r in t['remaining_completion_pairs']}
        actual_marked=originals=0
        for r in records:
            assert r['parent_index']==index
            word=v.prefix_word(seed,t,monoids,r['case'],root,outgoing)
            full=v.original_image(seed,word,t['images9'][r['image']])
            assert len(full)+r['budget']==44
            originals+=8192
            if r in basic:actual_marked+=v.check_boundary(r,full,t['images9'][r['image']])
            elif r in extra:
                markers,words=extended(r,full,t['images9'][r['image']],v)
                extra_marked+=markers;extra_word_checks+=words
            else:
                assert r['class_code']==code and r['rows9']==list(t['images9'][r['image']])
                assert r['prefix_B11']==[list(g) for g in word]
        actual=summary(index,code,orders,t,basic,extra,tails)
        assert actual==next(r for r in cert['records'] if r['parent_index']==index)
        result=dict(parent_index=index,status='COMPLETE_CLASS_FINITE_COVERAGE_AND_WITNESSES_VERIFIED',
                    normalized_prefixes=len(t['local_map_cases']),activity_assignments=activity,
                    original_inputs=originals,actual_basic_boundary_assignments=actual_marked,
                    solver_tails=len(tails))
        results.append(result);print(json.dumps(result),flush=True)
        signal.alarm(0)
    cuts,forced=v.local_cut_controls();extra_cuts,embeddings=extended_controls(v)
    result=dict(agent='six-sorting-2',role='researcher',
                status='COMPLETE_COHORT_FINITE_REDUCTION_VERIFIED_PENDING_RESIDUAL_TAIL_CHECKS' if args.class_index is None else 'SELECTED_CLASS_FINITE_REDUCTION_VERIFIED',
                classes=len(results),records=results,initial_actual_marked_assignments=domains,profile_audit=graph,
                total_actual_activity_assignments=sum(r['activity_assignments'] for r in results),
                total_original_prefix_inputs=sum(r['original_inputs'] for r in results),
                total_basic_boundary_marked_assignments=sum(r['actual_basic_boundary_assignments'] for r in results),
                extended_boundary_actual_marked_assignments=extra_marked,internal_short_words_exhausted=extra_word_checks,
                basic_cut_truth_controls=cuts,mandatory_internal_controls=forced,
                four_port_cut_truth_controls=extra_cuts,internal_projection_controls=embeddings,
                seconds=time.monotonic()-began,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                trust='Imported public profile/normal-form/size bounds and written unformalized bridges; independently implemented finite algorithms, no external reviewer verdict')
    (args.output/'verification-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:r for k,r in result.items() if k not in ('records','profile_audit')},indent=2),flush=True)


if __name__=='__main__':main()
