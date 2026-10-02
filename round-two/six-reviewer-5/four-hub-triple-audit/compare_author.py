import pathlib,json,hashlib,collections
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--work',type=pathlib.Path,required=True);args=ap.parse_args();W=args.work.resolve()
P=pathlib.Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def read(p):return json.loads(p.read_text())
seal=read(P/'first-seal.json')
for f in seal['files']:
    if f['publish']:need(hashlib.sha256((P/f['path']).read_bytes()).hexdigest()==f['sha256'],'all primary sealed bytes unchanged')
owned=read(P/'EVIDENCE.json');phys=read(P/'PHYSICAL.json')
import audit;support=audit.support_check()
need(hashlib.sha256(audit.enc(support)).hexdigest()==next(f['sha256'] for f in seal['files'] if f['path']=='SUPPORT.json'),'whole regenerated independent support record')
first=read(W/'normal/MATHEMATICAL.json');second=read(W/'optimized/MATHEMATICAL.json')
need(first==second,'every whole native mathematical output normal/O')
own_stars=read(P/'fixtures.json')['stars'];native_stars=read(W/'author/baseline/fixtures.json')['stars']
need(own_stars==native_stars,'every literal star position identical, serialization differs')
inv=first['pass19-high-T-producer']['inventory']
aliases={'g1':'g1_S','sigma':'ss_excess','w':'hub_weight','histogram':'ss_hist'}
ot=[{aliases.get(k,k):v for k,v in t.items()} for t in owned['types']]
need(ot==inv['types'],'every60 semantic type field')
import sys
sys.path.insert(0,str(P));import prior_rows
raw=prior_rows.marks(own_stars)
compiled=[]
for r in raw:
    hist=[sum(r['delta'][p]==j for p in r['high'] if p not in r['hubs']) for j in range(1,6)]
    compiled.append(dict(fixture=r['star'],hub_high=r['hubs'],h=r['h'],e=r['e'],k=r['k'],q=r['q'],eligible=r['eligible'],g1_S=r['g1'],ss_excess=r['sigma'],hub_weight=sum(r['delta'][p] for p in r['hubs']),psi=r['psi'],margin=r['old_margin'],ss_hist=hist))
compiled.sort(key=lambda r:(r['fixture'],r['hub_high']))
need(compiled==first['pass19-high-T-producer']['rows']==first['pass19-high-T-polynomial']['rows'],'all426 raw row fields including k5 negative uncorrected margins')
np=first['pass16-first-engine-low-friends']
need(phys['membership_hex']==''.join(r['accepted_membership_hex'] for r in np['records']),'every218960 physical marking bit')
freq=collections.Counter()
for r in np['records']:
    for i,c in r['accepted_type_multiplicities']:freq[i]+=c
need(dict(freq)=={int(k):v for k,v in phys['type_frequencies'].items()},'every type frequency')
branches={tuple(c['case'][k] for k in ('Q','T','X','tau')):c for c in owned['cases']}
names={'color_parity':'odd_weight_layer','distinct_partners':'too_few_weighted_partners','relaxed_radius13':'hub_complete_radius_two'}
diff=[];checked=0
for b in inv['branches']:
    key=tuple(b[k] for k in ('Q','T','X','tau'));c=branches[key]
    need([b['E'],b['K'],b['margin_budget']]==[c['case']['E'],c['case']['K'],c['case']['budget']],'whole branch totals')
    ov={tuple((i,n) for i,n in enumerate(r['counts']) if n):r['cut'] for r in c['records']}
    need(set(ov)=={tuple(tuple(z) for z in r['population']) for r in b['templates']},'every full sparse vector')
    for t in b['templates']:
        pop=tuple(tuple(z) for z in t['population']);cut=ov[pop]
        failures=sorted(names[z] for z in cut.get('failures',[]))
        need(bool(failures)==bool(t['failures']),'every survival decision agrees')
        if failures!=t['failures']:diff.append(dict(branch=key,population=pop,own=failures,author=t['failures']))
        checked+=1
target=first['pass19-high-T-cut-producer'];smap={(r['B'],r['C'],r['J']):r for r in support['populations']};certificate_records=0;target_rows=0;weak_witnesses=0
for r in target['records']:
    certificate_records+=1
    if r['kind']=='DISJOINT_SUPPORT':
        s=smap[r['B_rows'],r['C_rows'],r['J_rows']];freq=collections.Counter(tuple(a['D']) for a in s['degree_allocations'])
        need(len(r['target_rows'])==489,'every ordered degree target')
        for a in r['target_rows']:
            need(a['pre_support_typed_allocations']==freq[tuple(a['D4'])] and a['passing_support']==[],'every D multiplicity and absence')
            target_rows+=1
        converted=[{k+'4':list(a[k]) for k in ('B','C','J','N','D')} for a in s['weakened_C4']]
        converted.sort(key=lambda a:(a['D4'],a['N4'],a['J4']))
        need(converted==r['weakened_threshold_witnesses'],'every weakened support witness')
        weak_witnesses+=len(converted)
    elif r['kind']=='UNIT_CAPACITY':
        need(r['unit_demand']==16 and (r['internal_incidence_upper'],r['external_incidence_upper']) in ((0,12),(12,3)),'whole unit certificate arithmetic')
    elif r['kind']=='CLOSED_UNIT_PARITY':need(r['closed_unit_degree_sum']==19 and r['external_incidence_upper']==0,'whole original odd handshake')
    elif r['kind']=='GENERALIZED_RADIUS':need((r['root_type'],r['graph_regular_degree'],r['hub_friend_upper'],r['two_step_ball_lower'],r['two_step_ball_upper'])==(19,3,3,11,10),'whole original radius certificate')
    else:raise ValueError('unexpected native certificate')
result=dict(actual_reviewer='six-reviewer-5',role='independent mathematical reviewer',primary_files_unchanged=True,literal_star_positions_equal=True,owned_fixture_sha256=hashlib.sha256((P/'fixtures.json').read_bytes()).hexdigest(),native_fixture_sha256=hashlib.sha256((W/'author/baseline/fixtures.json').read_bytes()).hexdigest(),raw_rows=426,type_records=60,physical_membership_bits=218960,ordered_vectors=checked,all_survival_decisions_equal=True,failure_list_differences=diff,complete_original_certificates=certificate_records,ordered_support_target_rows=target_rows,complete_weakened_support_witnesses=weak_witnesses,entire_native_normal_optimized_equal=True,whole_native_sha256=hashlib.sha256((W/'normal/MATHEMATICAL.json').read_bytes()).hexdigest(),independent_sha256=hashlib.sha256((P/'EVIDENCE.json').read_bytes()).hexdigest(),independent_core_sealed_at=seal['sealed_at'],late_target_files_materialized_at=read(P/'target-source.json')['first_materialized_at'])
(W/'INDEPENDENT-COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
