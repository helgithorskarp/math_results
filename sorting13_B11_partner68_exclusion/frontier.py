"""Exact complete partner(6,8) incidence and cumulative frontier; not a proof replay."""
import json
from shared import HERE,arguments,digest,inputs,read


def main():
    args=arguments();f,selected,fresh,old=inputs(args.repository)
    cert=read(HERE/'certificate.json')
    assert cert['selected_classes']==selected and cert['new_classes']==fresh
    assert len(cert['records'])==36 and sum(r['effective_orders'] for r in cert['records'])==421920
    assert {(r['parent_index'],r['class_code']) for r in cert['records']}=={(r[0],r[1]) for r in fresh}
    table=read(args.repository/'sorting_networks/thirteen_extreme_multiset_quotient/certificate.json')['class_table']
    ten=read(args.repository/'sorting13_B11_ten_event_branch_exclusion/certificate.json')
    assert ten['complete_branch_enrolled'] and len(ten['coverage'])==77
    prior23=read(args.repository/'sorting_networks/thirteen_repeated23_exclusion/certificate.json')
    prior13=read(args.repository/'sorting_networks/thirteen_repeated13_exclusion/certificate.json')
    first2=read(args.repository/'sorting13_B11_first2_exclusion/certificate.json')
    last_repeat=read(args.repository/'sorting_networks/thirteen_repeated_i4_exclusion/certificate.json')
    first3=read(args.repository/'sorting13_B11_first3_exclusion/certificate.json')
    assert first2['proof_status']=='ALL_PUBLIC_FINITE_REDUCTIONS_DATA_CLAUSES_NATIVE_DRAT_AND_PYTHON_RUP_ACTUALLY_CHECKED'
    assert prior23['all_six_repeated23_classes']==6 and prior13['all_six_repeated13_classes']==6
    prior=set()
    for index,(code,events,orders) in enumerate(table):
        counts=[(int(code)>>(2*k))&3 for k in range(55)]
        assert sum(counts)==events and max(counts)<=2
        if events==11 and counts[0]==2:prior.add(code)
    assert len(prior)==18
    prior.add(table[13][0])
    # Use actual lexicographic pair positions, without hardcoded shifts.
    import itertools
    pairs=list(itertools.combinations(range(11),2))
    repeated23={code for code,e,n in table if ((int(code)>>(2*pairs.index((2,3))))&3)==2}
    repeated13={code for code,e,n in table if ((int(code)>>(2*pairs.index((1,3))))&3)==2}
    assert len(repeated23)==len(repeated13)==6
    assert {table[i][0] for i in (34,40,149,155,237,243)}==repeated23
    assert {c for i,c in prior23['newly_excluded_classes']}<=repeated23
    assert {c for i,c in prior13['newly_excluded_classes']}==repeated13
    prior|=repeated23|repeated13|{r[1] for r in first2['new_classes']}
    assert len(prior)==66
    last={c for i,c in last_repeat['newly_excluded_classes']}
    assert len(last)==9 and last.isdisjoint(prior)
    assert all(table[i]==[c,11,5385] for i,c in last_repeat['newly_excluded_classes'])
    prior|=last
    assert len(first3['new_classes'])==36 and sum(r[3] for r in first3['new_classes'])==279810
    assert first3['proof_status']=='ALL_PUBLIC_FINITE_REDUCTIONS_DATA_CLAUSES_NATIVE_DRAT_COMPACT_NATIVE_AND_PYTHON_RUP_ACTUALLY_CHECKED'
    prior|={r[1] for r in first3['new_classes']}
    first4=read(args.repository/'sorting13_B11_first4_exclusion/certificate.json')
    assert len(first4['new_classes'])==45 and sum(r[3] for r in first4['new_classes'])==440190
    assert first4['proof_status']=='ALL_PUBLIC_FINITE_REDUCTIONS_PRIOR_IMAGE_DATA_CLAUSES_NATIVE_DRAT_COMPACT_NATIVE_AND_PYTHON_RUP_ACTUALLY_CHECKED'
    prior|={r[1] for r in first4['new_classes']}
    before={c for c,e,n in table if e==11 and c not in prior}
    assert len(before)==189 and sum(n for c,e,n in table if c in before)==1194030
    assert all(all(((int(c)>>(2*k))&3)<=1 for k in range(55)) for c in before)
    new={r[1] for r in fresh};assert new<=before
    assert old==[]
    assert {r[1] for r in selected}==new|{r[1] for r in old}
    current=before-new
    assert len(current)==153 and sum(n for c,e,n in table if c in current)==772110
    assert not any(((int(c)>>(2*pairs.index((4,10))))&3) or
                   ((int(c)>>(2*pairs.index((3,10))))&3) or
                   ((int(c)>>(2*pairs.index((2,10))))&3) for c in current)
    assert len([1 for c,e,n in table if e==10])==135
    groups={}
    for code,e,n in table:
        if code not in current:continue
        partners=tuple(i for i in (1,2,3,4,5,6,8) if (int(code)>>(2*pairs.index((i,10))))&3)
        assert partners in ((5,6),(5,8))
        groups.setdefault(partners,[]).append([code,e,n])
    assert {k:(len(v),sum(r[2] for r in v)) for k,v in groups.items()}=={(5,6):(18,210960),(5,8):(135,561150)}
    assert all((int(code)>>(2*pairs.index((5,10))))&3 for code in current)
    assert all(r['first_touch_orders']=={'48':r['effective_orders'],'53':0} for r in cert['records'])
    result=dict(agent='six-sorting-2',role='researcher',
        status='EXACT_PARTNER68_COMPLETE_COHORT_INCIDENCE_AND_FRONTIER_ARITHMETIC_VERIFIED',
        new_complete_classes=36,new_orders=421920,prior_classes=189,prior_effective_orders=1194030,
        remaining_ten=0,remaining_classes=153,remaining_distinct_eleven=153,remaining_repeated_eleven=0,
        remaining_effective_orders=772110,remaining_class_codes=sorted(current),
        remaining_codes_sha256=digest(sorted(current)),
        remaining_table_sha256=digest([r for r in table if r[0] in current]),
        remaining_allowed_partner_groups=[dict(partners=list(k),classes=len(v),orders=sum(r[2] for r in v)) for k,v in sorted(groups.items())],
        mandatory_effective_pair=[5,10],
        trust='Class incidence imports8321/8382/8395/8420/8452 and earlier complete-class theorems; not imported proof-suite replay, formalization or arbitrary-prefix S13 exclusion')
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'frontier-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='remaining_class_codes'},indent=2))


if __name__=='__main__':main()
