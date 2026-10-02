"""Late entry-level comparison; own independent proof was sealed first.
Reads original public replay JSON only; never imports researcher algorithms.
"""
import argparse
from independent import *
from controls import tuple_key

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--original-work',type=pathlib.Path,required=True);ap.add_argument('--own-work',type=pathlib.Path,required=True);a=ap.parse_args()
    S=a.original_work/'round-two/six-code-3/scratch';W=a.own_work
    def original(n):return json.loads((S/(n+'.json')).read_text())
    census=json.loads((W/'independent-census.json').read_text());phys=json.loads((W/'independent-physical.json').read_text());unit=json.loads((W/'independent-unit-flow.json').read_text());support=json.loads((W/'independent-support.json').read_text())
    orig=original('pass16-p21-producer');types=orig['inventory']['types']
    converted=[(r['e'],r['k'],r['q'],r['eligible'],r['h'],r['g1_S'],r['ss_excess'],r['psi'],r['margin']) for r in types]
    need([tuple(t) for t in census['types']]==converted,'every ordered60 type coordinate')
    need(census['histograms']==[r['ss_hist'] for r in types],'every full60 color histogram')
    stars=json.loads((W/'fixtures.json').read_text())['stars'];raw=prior_rows.marks(stars);mapped={}
    for r in raw:
        H=set(r['hubs']);hist=[sum(r['delta'][p]==j for p in r['high'] if p not in H) for j in range(1,6)]
        mapped[r['star'],tuple(r['hubs'])]={'fixture':r['star'],'hub_high':r['hubs'],'h':r['h'],'e':r['e'],'k':r['k'],'q':r['q'],'eligible':r['eligible'],'g1_S':r['g1'],'ss_excess':r['sigma'],'hub_weight':sum(r['delta'][p] for p in H),'psi':r['psi'],'margin':r['old_margin'],'ss_hist':hist}
    need(mapped=={(r['fixture'],tuple(r['hub_high'])):r for r in orig['rows']},'all426 original signed-scope raw rows including eight k5 negatives')
    screen=original('pass16-first-engine-low-friends');screen_bits=[]
    for row in screen['records']:
        value=int.from_bytes(bytes.fromhex(row['accepted_membership_hex']),'little');screen_bits.extend(int(value>>j&1) for j in range(9520))
        own_bad=phys['first_failure_points'][row['fixture']*9520:(row['fixture']+1)*9520];point=next((x for x in own_bad if x>=0),None)
        need(point==(row['first_failure']['point'] if row['first_failure'] else None),'each original first failing physical point')
    need(screen_bits==phys['all_218960_membership_bits'],'every218960 actual placement membership bit')
    need(screen['surviving_type_projection']==census['physically_admissible_types'],'every physically admissible type')
    original_cases={tuple(b[k] for k in ('Q','T','X','tau')):b for b in orig['inventory']['branches']};labels={'color_parity':'odd_weight_layer','distinct_partners':'too_few_weighted_partners','relaxed_radius13':'hub_complete_radius_two'};wholeold=0
    for c in census['cases']:
        key=tuple(c['case'][k] for k in ('Q','T','X','tau'));b=original_cases[key]
        own={tuple((i,n) for i,n in enumerate(r['counts']) if n):sorted(labels[x] for x in r['graph'].get('all_prior_failures',[])) for r in c['records']}
        other={tuple(tuple(p) for p in r['population']):r['failures'] for r in b['templates']}
        need(own==other,'every full population and all old failure labels: '+str(key));wholeold+=len(own)
    def population_key(case,counts):return tuple(case[k] for k in ('Q','T','X','tau')),tuple((i,n) for i,n in enumerate(counts) if n)
    def orig_key(row):return tuple(row['branch']),tuple(tuple(p) for p in row['population'])
    old_masks={orig_key(r):r for r in original('pass16-p21-unit-graphs')['records']};mask_total=0
    for r in unit['records']:
        o=old_masks[population_key(r['case'],r['counts'])];check=r['mask_check']
        need(check['potential_unit_edges']==o['potential_internal_edges'],'every labeled potential unit edge')
        need([j for j,b in enumerate(check['all_mask_accept_bits']) if b]==o['accepted_internal_masks'],'every accepted mask matches independently computed flow')
        mask_total+=len(check['all_mask_accept_bits'])
    need({population_key(s['case'],s['counts']) for s in unit['survivors']}=={orig_key(s) for s in original('pass16-p21-unit-graphs')['survivors']},'every final eleven population')
    old_sigs={tuple_key((r['type_id'],r['hub_deficits'],r['HH_leave_mask'],r['HHH_covered_mask'],r['word_hub_counts'],r['eligible_hub_mask'])):(r['frequency'],r['witness']['fixture'],r['witness']['hub_roles']) for r in original('pass16-hub-role-catalogue')['records']}
    ours={tuple_key(r['signature']):(r['frequency'],r['first_witness'][0],r['first_witness'][1]) for r in support['selected_signatures']}
    need(ours==old_sigs,'all837 signatures, frequencies and full literal smallest witnesses')
    for r in original('pass17-support-census-exact')['records']:need(r['status']=='COMPLETE_SUPPORT_CENSUS' and not r['surviving_ordered_states'],'original complete support emptiness')
    for r in original('pass17-independent-support')['records']:need(not r['surviving_states'],'original weaker support emptiness')
    result={'agent':'six-reviewer-5','role':'independent mathematical reviewer','after_independent_seal':True,'all426_raw_rows':426,'all60_types_histograms':60,'physical_membership_bits':len(screen_bits),'whole_population_and_failure_lists':wholeold,'every_unit_mask':mask_total,'literal_signatures_frequencies_smallest_witnesses':len(ours),'all_final_population_vectors':len(unit['survivors']),'native_support_populations':11,'independent_raw_population_carriers':4032,'native_whole_sha256':hashlib.sha256((a.original_work/'MATHEMATICAL.json').read_bytes()).hexdigest(),'all_checked_equal':True,'scope':'Independent radius-neighbor subset cuts need not reproduce original forced-cut witness format; whole final14 pre-unit carrier and all98315 unit acceptance bits agree. Original runtime counters and source self-checks are corroboration only.'}
    (W/'LATE-COMPARISON.json').write_bytes(enc(result));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
