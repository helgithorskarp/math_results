"""Late DATA-only whole mathematical correspondence, after pre-native seal.
Native transition counts are replay-checked, not claimed equal to our kernel.
Run only after both complete source-only replays; no producer import.
"""
import argparse,collections,functools,hashlib,itertools as it,json,pathlib,time

def need(ok,message):
    if not ok:raise ValueError(message)
def freeze(x):
    if isinstance(x,list):return tuple(map(freeze,x))
    return x
def sparse(v):return tuple((i,n) for i,n in enumerate(v) if n)
PAIRS=list(it.combinations(range(4),2))

def compare(primary,native,original):
    start=time.monotonic();S=native/'round-two/six-code-3/scratch'
    validation=json.loads((native/'VALIDATION.json').read_text())
    need(validation['status']=='COMPLETE_PUBLIC_SOURCE_T0_REPLAY_PASS','complete native replay required')
    m=json.loads((original/'SOURCE_MANIFEST.json').read_text())['files']
    need(all(hashlib.sha256((original/n).read_bytes()).hexdigest()==d for n,d in m.items()),'original source/input manifest changed')
    own=json.loads((primary/'census22.json').read_text());phys=json.loads((primary/'physical22.json').read_text())
    author=json.loads((S/'pass23-T0-producer.json').read_text())['inventory']
    fields=('e','k','q','eligible','h','g1_S','ss_excess','psi','margin')
    need([list(r[f] for f in fields) for r in author['types']]==own['types'],'whole60 type fields')
    need([r['ss_hist'] for r in author['types']]==own['histograms'],'whole60 SAT color histograms')
    native_pops=[];branches={};original_fail={'too_few_weighted_partners':'distinct_partners','hub_complete_radius_two':'relaxed_radius13','odd_weight_layer':'color_parity'}
    own_branches={(b['branch']['Q'],b['branch']['X'],b['branch']['tau']):b for b in own['branches']};flag_differences=0
    for b in author['branches']:
        key=(b['Q'],b['X'],b['tau']);ours=own_branches[key]
        need([b[k] for k in ('E','K','margin_budget')]==[ours['branch'][k] for k in ('E','K','budget')],'whole branch charges')
        od={sparse(r['counts']):set(r['all_failures']) for r in ours['complete_vectors']}
        nd={freeze(r['population']):{original_fail[f] for f in r['failures']} for r in b['templates']}
        need(od.keys()==nd.keys(),'every whole scalar vector')
        need({v for v,f in od.items() if not f}=={v for v,f in nd.items() if not f},'entire preliminary survivor domain')
        flag_differences+=sum(od[v]!=nd[v] for v in od)
        for t in b['templates']:
            if not t['failures']:native_pops.append((key,freeze(t['population'])))
    need(len(own_branches)==len(author['branches'])==84 and len(native_pops)==11077,'full scalar domain coverage')
    catalogue=json.loads((S/'pass23-T0-hub-friend-catalogue.json').read_text())['records']
    renamed=[]
    for r in phys['physical_rows']:
        i,d,hh,hhh,wc,iso,L=r['signature'];si,role=r['witness']
        renamed.append(dict(type_id=i,hub_deficits=d,HH_leave_mask=hh,HHH_covered_mask=hhh,
                            word_hub_counts=wc,eligible_hub_mask=iso,low_sat_friend_degrees=L,
                            frequency=r['frequency'],witness=dict(fixture=si,hub_roles=role)))
    # The primary selects min(fixture,ordered roles). The target explicitly
    # selects its original traversal order: fixture,sorted H,heavy index,
    # light order. These are different valid witness conventions.
    without_witness=lambda rs:[{k:v for k,v in r.items() if k!='witness'} for r in rs]
    need(without_witness(renamed)==without_witness(catalogue),'ALL7729 complete physical signatures/frequencies')
    witness_policy_differences=sum(a['witness']!=b['witness'] for a,b in zip(renamed,catalogue))
    import sys
    sys.path.insert(0,str(primary));from controls22 import verify_row
    stars=json.loads((primary/'fixtures.json').read_text())['stars']
    for row in catalogue:
        sig=[row['type_id'],row['hub_deficits'],row['HH_leave_mask'],row['HHH_covered_mask'],
             row['word_hub_counts'],row['eligible_hub_mask'],row['low_sat_friend_degrees']]
        verify_row(dict(signature=sig,witness=[row['witness']['fixture'],row['witness']['hub_roles']]),stars,list(map(tuple,own['types'])))
    canonical=json.loads((S/'pass23-T0-canonical-carriers.json').read_text())
    first=json.loads(next((primary/'column-phases').glob('*.json')).read_text())
    need([(r['lambda6'],r['D4'],r['HH_leave_totals']) for r in canonical]==[tuple(r) for r in first['canonical_carriers']],'all6 ordered canonical carrier fields')
    by_pop={};choices={}
    for f in sorted((primary/'column-phases').glob('*.json')):
        for r in json.loads(f.read_text())['records']:
            key=(r['branch']['Q'],r['branch']['X'],r['branch']['tau']),sparse(r['counts']);by_pop[key]=r
            for c in r['carriers']:
                for v in c['complete_choices']:choices[key,c['carrier'],tuple(v['N'])]=v
    coordinate_records=0;native_choices=set()
    files=[S/('pass23-T0-N-%04d-%04d.json'%(a,min(a+64,11077))) for a in range(0,11077,64)]
    for f in files:
        for r in json.loads(f.read_text())['records']:
            key=native_pops[r['survivor_ordinal']];ours=by_pop[key]
            need(tuple(r['branch'][i] for i in (0,2,3))==key[0] and freeze(r['population'])==key[1],'whole column/population identity')
            for c in r['carrier_results']:
                other=ours['carriers'][c['carrier_index']]
                need(c['coordinate_N_sets']==other['coordinate_support_sets'],'ALL66462 full coordinate N sets')
                need(sorted(map(tuple,c['coupled_N4']))==sorted(tuple(v['N']) for v in other['complete_choices']),'ALL66462 whole coupled support sets')
                coordinate_records+=1
                for N in c['coupled_N4']:native_choices.add((key,c['carrier_index'],tuple(N)))
    need(coordinate_records==66462 and native_choices==choices.keys() and len(choices)==969,'no dropped full column record or coupled case')
    # Check each compact certificate entry directly against the independent
    # domains, not against the target's own certificate checker.
    certificates=json.loads((original/'CERTIFICATE.json').read_text());certkeys=[];witnesses=[]
    for pop,ci,N,why in certificates['cases']:
        key=(native_pops[pop],ci,tuple(N));need(key in choices,'original certificate unknown necessary case');certkeys.append(key)
        counts=dict(key[0][1]);D=canonical[ci]['D4'];Z=[d-n for d,n in zip(D,N)]
        if why[0]=='capacity':
            capacity=sum(min(n,z) for n,z in zip(N,Z) if n>=5)
            need(why==['capacity',counts.get(18,0),capacity] and counts.get(18,0)>capacity,'whole actual weighted capacity inequality')
            continue
        domain={i:[(j,r) for j,r in enumerate(catalogue) if r['type_id']==i and r['HHH_covered_mask']==0
                  and all(not d or r['low_sat_friend_degrees'][a]<N[a] for a,d in enumerate(r['hub_deficits']))] for i in counts}
        if why[0]=='empty_row_domain':need(why[1] in counts and not domain[why[1]],'actual complete empty type domain')
        else:
            family,mask,target,lo,hi=why[1:]
            need(all(domain[i] for i in counts),'row-sum certificate on empty domain')
            targets={'deficit':D,'positive_support':N,'deficit_excess':Z,'HH_leave':canonical[ci]['HH_leave_totals']}
            need(target==sum(x for a,x in enumerate(targets[family]) if mask>>a&1),'exact original row total')
            def values(r):
                d=r['hub_deficits']
                return {'deficit':d,'positive_support':[int(x>0) for x in d],
                        'deficit_excess':[max(0,x-1) for x in d],
                        'HH_leave':[r['HH_leave_mask']>>a&1 for a in range(6)]}[family]
            scores={i:[sum(x for a,x in enumerate(values(r)) if mask>>a&1) for j,r in domain[i]] for i in counts}
            lower=sum(counts[i]*min(scores[i]) for i in counts);upper=sum(counts[i]*max(scores[i]) for i in counts)
            need((lo,hi)==(lower,upper) and (target<lower or target>upper),'entire exact compact row inequality')
    need(len(certkeys)==len(set(certkeys))==969 and set(certkeys)==choices.keys(),'ALL compact certificate cases exactly once')
    # All stored common domains and every complete native bound prefix/cell.
    rows=json.loads((S/'pass23-T0-row-base-independent.json').read_text())['records'];bound_count=cell_count=domain_count=0
    @functools.cache
    def admissible(i,N):
        return [(j,r) for j,r in enumerate(catalogue) if r['type_id']==i and r['HHH_covered_mask']==0
                and all((not d and r['low_sat_friend_degrees'][a]==0) or (d and r['low_sat_friend_degrees'][a]<N[a]) for a,d in enumerate(r['hub_deficits']))]
    for case in rows:
        N=tuple(case['N4']);D=case['carrier']['D4'];Z=[d-n for d,n in zip(D,N)];L=case['carrier']['HH_leave_totals']
        for entry in case['admissible_original_rows']:
            need([j for j,r in admissible(entry['type_id'],N)]==entry['actual_catalogue_indices'],'every complete stored common row domain');domain_count+=1
        for b in case['bounds']:
            family=b['family'];mask=b['subset_mask'];cells=[]
            for entry in case['admissible_original_rows']:
                scores=[]
                for j,r in admissible(entry['type_id'],N):
                    d=r['hub_deficits'];p=[int(x>0) for x in d]
                    v={'deficit':d,'positive_support':p,'deficit_excess':[x-y for x,y in zip(d,p)],
                       'HH_leave':[r['HH_leave_mask']>>a&1 for a in range(6)],
                       'HIGH_pair_overlap':[p[a]*p[c] for a,c in PAIRS],'LOW_SAT_friend_degree':r['low_sat_friend_degrees']}[family]
                    scores.append((sum(x for a,x in enumerate(v) if mask>>a&1),j))
                lower,index=min(scores);upper=max(x for x,j in scores);upper_index=min(j for x,j in scores if x==upper)
                cells.append([entry['type_id'],entry['multiplicity'],lower,upper,index,upper_index])
            need(cells==b['original_row_extrema'],'every whole original extrema value AND witness index');cell_count+=len(cells)
            lo=sum(n*l for i,n,l,h,li,hi in cells);hi=sum(n*h for i,n,l,h,li,hi in cells)
            targets={'deficit':D,'positive_support':list(N),'deficit_excess':Z,'HH_leave':L,
                     'HIGH_pair_overlap':[N[a]+N[c]-L[j] for j,(a,c) in enumerate(PAIRS)],
                     'LOW_SAT_friend_degree':[n*(n-1) for n in N]}[family]
            target=sum(x for a,x in enumerate(targets) if mask>>a&1);upper_only=family in ('HIGH_pair_overlap','LOW_SAT_friend_degree')
            need((lo,hi,target,upper_only)==(b['minimum'],b['maximum'],b['target'],b['upper_only']),'entire original bound aggregate')
            need(b['passes']==(lo<=target and (upper_only or target<=hi)),'original complete bound prefix truth value');bound_count+=1
    if time.monotonic()-start>45:raise RuntimeError('INCOMPLETE fixed45-second late correspondence guard')
    result=dict(actual_reviewer='six-reviewer-5',kind='late data correspondence, primary kernel unchanged',
                scalar_branches=84,full_scalar_vectors=30944,entire_preliminary_population_domain=11077,
                differing_preliminary_failure_flag_sets=flag_differences,physical_complete_signature_frequency_records=7729,
                every_original_quadruple_witness_independently_validated=7729,
                differing_valid_witness_minimum_policies=witness_policy_differences,
                primary_policy='minimum(fixture,ordered role tuple)',original_policy='minimum(fixture,sorted H,heavy index,light role tuple)',
                full_carrier_population_coordinate_and_coupled_records=coordinate_records,compact_certificate_entries=969,
                common_domain_records=domain_count,entire_original_bounds=bound_count,whole_original_extrema_cells=cell_count,
                native_whole_outputs_matched=validation['whole_outputs_matched'],native_whole_mathematical_bytes=validation['complete_mathematical_bytes'],
                native_mathematical_sha256=validation['complete_mathematical_sha256'],
                native_transition_counts_not_claimed_equal_to_independent_kernel=True,
                native_replay_mode=validation['mode'],native_optimized_mode_not_replayed=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--primary',type=pathlib.Path,required=True);p.add_argument('--native',type=pathlib.Path,required=True);p.add_argument('--original',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
    r=compare(a.primary,a.native,a.original);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
