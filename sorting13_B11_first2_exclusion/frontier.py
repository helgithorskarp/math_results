"""Exact class incidence and cumulative arithmetic; not an UNSAT checker."""
import json
from shared import HERE,arguments,digest,inputs,read


def main():
    args=arguments();f,selected,fresh,old=inputs(args.repository)
    cert=read(HERE/'certificate.json')
    assert cert['selected_classes']==selected and cert['new_classes']==fresh
    assert len(cert['records'])==35 and sum(r['effective_orders'] for r in cert['records'])==191490
    assert {(r['parent_index'],r['class_code']) for r in cert['records']}=={(r[0],r[1]) for r in fresh}
    q=read(args.repository/'sorting_networks/thirteen_extreme_multiset_quotient/certificate.json')
    table={r[0]:(r[1],r[2]) for r in q['class_table']}
    ten=read(args.repository/'sorting13_B11_ten_event_loop_postponement/certificate.json')
    complete_ten=read(args.repository/'sorting13_B11_ten_event_branch_exclusion/certificate.json')
    assert complete_ten['complete_branch_enrolled'] and len(complete_ten['coverage'])==77
    boundary=read(args.repository/'sorting_networks/thirteen_class13_boundary_obstruction/certificate.json')
    peer=read(args.repository/'sorting_networks/thirteen_repeated23_reduction/certificate.json')
    earlier=set(ten['peer_repeated_exclusion_codes'])|{boundary['class_code']}
    earlier|={r['class_code'] for r in peer['classes'] if r['parent_index'] in peer['excluded_parent_indices']}
    assert len(earlier)==22
    new={r[1] for r in fresh};assert new.isdisjoint(earlier)
    all_eleven={code for code,(e,n) in table.items() if e==11}
    prior=all_eleven-earlier;assert len(prior)==323 and sum(table[c][1] for c in prior)==2202450
    current=prior-new
    peer23=read(args.repository/'sorting_networks/thirteen_repeated23_exclusion/certificate.json')
    peer13=read(args.repository/'sorting_networks/thirteen_repeated13_exclusion/certificate.json')
    concurrent_rows=peer23['newly_excluded_classes']+peer13['newly_excluded_classes']
    assert [r[0] for r in concurrent_rows]==[40,155,243,36,42,151,157,239,245]
    quotient=read(args.repository/'sorting_networks/thirteen_extreme_multiset_quotient/certificate.json')['class_table']
    concurrent={code for index,code in concurrent_rows}
    assert len(concurrent)==9 and concurrent.isdisjoint(new) and concurrent<=current
    assert all(quotient[index]==[code,11,5385] for index,code in concurrent_rows)
    assert sum(table[c][1] for c in concurrent)==48465
    def repeated(code):
        return any((int(code)>>(2*k))&3==2 for k in range(55))
    assert sum(repeated(code) for code in new)==8
    assert len(current)==288 and sum(repeated(code) for code in current)==18
    assert sum(table[c][1] for c in current)==2010960
    current-=concurrent
    assert len(current)==279 and sum(repeated(code) for code in current)==9
    assert sum(table[c][1] for c in current)==1962495
    assert len([c for c,(e,n) in table.items() if e==10])==135
    result=dict(agent='six-sorting-2',role='researcher',status='EXACT_FIRST2_COMPLETE_COHORT_INCIDENCE_AND_FRONTIER_ARITHMETIC_VERIFIED',
                first2_eleven_classes=36,first2_eleven_orders=196875,imported_class13_orders=5385,
                new_complete_classes=35,new_distinct=27,new_repeated=8,new_orders=191490,
                own_new_exclusion_frontier=288,own_new_exclusion_orders=2010960,
                concurrent_new_complete_classes=9,concurrent_new_orders=48465,
                remaining_ten=0,remaining_classes=279,remaining_distinct_eleven=270,
                remaining_repeated_eleven=9,remaining_effective_orders=1962495,
                remaining_class_codes=sorted(current),remaining_codes_sha256=digest(sorted(current)),
                trust='Class arithmetic assumes the independently checked new finite/certificate proofs and imported8198/8321/8281/8340/8372 and earlier parent theorems; imported peer proof suites not replayed; no arbitrary-prefix S13 exclusion')
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'frontier-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='remaining_class_codes'},indent=2))


if __name__=='__main__':main()
