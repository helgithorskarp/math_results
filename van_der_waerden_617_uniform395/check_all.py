"""Exact new-case replay and explicit combination with four prior results.

The four byte-pinned dependency summaries are mathematical imports. This
module does not pretend to replay the old 602 strong-phase certificates or
the separate phase201/269 proofs. The new 13 covers are fully replayed here.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import verify

HERE = Path(__file__).parent
NEW_PHASES = [156,170,174,184,198,205,213,220,235,252,287,560,611]
PINS = {
    'base_profile':'f2a45d467cefc5ec605c84417742bbac7a9531211c01baba6770b0d499a61db5',
    'individual197':'7eaa9259df5ce7da09ea008f53a76d75f661cfb25ec6019b93b4a7ee152f7b42',
    'joint201':'a76947d81e6a2c138568a2ed286ceb7d3b103e384c8880044df1d815e4693182',
    'joint269':'9a870c5cbf8ef20af9513d36c63186e4ad3d45fcc2561c142a70a90c65572099',
}


def local(path):
    verify.need(type(path) is str, 'Local path string')
    p=Path(path)
    verify.need(p.parts and not p.is_absolute() and '..' not in p.parts, 'Local relative path')
    return p


def dependencies(manifest, directory=HERE):
    entries=manifest['dependencies']
    verify.need(type(entries) is list and len(entries)==4, 'Four explicit mathematical dependencies')
    names=[d['name'] for d in entries]
    verify.need(len(set(names))==4 and set(names)==set(PINS), 'All distinct pinned dependency names')
    out={}
    for d in entries:
        verify.need(type(d) is dict and set(d)=={'name','path','directory','source_commit',
                    'graph_ref','sha256','reader_url'}, 'Dependency provenance schema')
        name=d['name'];raw=(directory/local(d['path'])).read_bytes()
        verify.need(d['sha256']==PINS[name] and hashlib.sha256(raw).hexdigest()==PINS[name],
                    'Unchanged byte-pinned published dependency summary')
        out[name]=json.loads(raw)
    return out


def actual_sizes():
    """Count actual original classes for every reference, without candidate symmetry."""
    q=[-1]+[int(pow(r,308,617)==616) for r in range(1,617)]
    result=[]
    for s in range(617):
        colors=[]
        for x in range(3704):
            r=(x-1852+(s if x<1852 else (1-s)%617))%617
            colors.append(-1 if not r else q[r]^int(x>=1852))
        sizes=[colors.count(c) for c in (0,1)]
        verify.need(sizes==([1848,1848] if s==1 else [1849,1849]), 'Every actual reference class size')
        verify.need(all(colors[3703-x]==(-1 if colors[x]<0 else 1-colors[x]) for x in range(3704)),
                    'Every actual reference is reflected with complemented colors')
        result.append(sizes)
    return result


def combine(imports, cases):
    """Pure quantified coverage step; imported theorems are identified explicitly."""
    profile=imports['base_profile'];individual=imports['individual197']
    verify.need(profile['status']=='VERIFIED_COMPLETE_REFLECTION_FAMILY' and
                profile['complete'] is True and type(profile['phase_count']) is int and
                profile['phase_count']==617 and profile['solver_trusted'] is False, 'Prior complete profile scope')
    floors=profile['per_phase_lower_bound_each_color']
    verify.need(type(floors) is list and len(floors)==617 and
                all(type(v) is int and v>=196 for v in floors), 'Exact imported per-phase bounds for all617 phases')
    weak={s for s,v in enumerate(floors) if v<198}
    verify.need(weak==set(NEW_PHASES)|{201,269}, 'Exactly15 old weak phases')
    verify.need(individual['status']=='EXACT_COMPLETE_FOUR_PHASE_CLASS196_EXCLUSION' and
                individual['phases']==[184,201,205,269] and
                type(individual['required_edits_per_reference_color_each_phase']) is int and
                individual['required_edits_per_reference_color_each_phase']==197,
                'Imported197 floor covers each of the four old floor196 phases')
    verify.need({s for s,v in enumerate(floors) if v==196}==set(individual['phases']),
                'Every old floor196 phase upgraded')
    for s in [201,269]:
        old=imports[f'joint{s}']
        verify.need(type(old['phase']) is int and old['phase']==s and
                    old['status']==f'EXACT_PHASE{s}_JOINT197_EXCLUSION' and
                    old['excluded_original_class_caps']==[197,197] and
                    all(type(v) is int for v in old['excluded_original_class_caps']) and
                    type(old['necessary_max_original_class_edits']) is int and
                    old['necessary_max_original_class_edits']==198 and
                    old['candidate_symmetry_assumed'] is False and old['solver_trusted'] is False,
                    'Both original-class caps excluded by the imported phase result')
    verify.need(type(cases) is list and len(cases)==13, 'All13 new cases supplied')
    phases=[r['phase'] for r in cases]
    verify.need(all(type(s) is int for s in phases) and len(set(phases))==13 and
                set(phases)==set(NEW_PHASES), 'No missing or duplicated new phase')
    for r in cases:
        verify.need(r['status']=='EXACT_BASESCREEN_JOINT197_EXCLUSION' and
                    r['base_floor_per_class']==floors[r['phase']] and
                    r['proved_individual_floor_per_class']>=197 and
                    r['necessary_max_class_edits']==198 and
                    r['necessary_total_nonpole_edits_min']>=395 and
                    r['candidate_symmetry_assumed'] is False and r['solver_trusted'] is False,
                    'Each fully replayed new box has the required uncapped-candidate scope')
    strong={s for s,v in enumerate(floors) if v>=198}
    verify.need(len(strong)==602 and not(strong&weak) and strong|weak==set(range(617)),
                '602+13+2 disjointly cover every phase')
    individual_floors=[max(197,v) for v in floors]
    total_floors=[max(395,2*v) for v in individual_floors]
    sizes=actual_sizes()
    zero_cases=[r for r in cases if r['phase'] in [184,205]]
    zero_counts=[r['zero_loss_premise']['fixed_counts'] for r in zero_cases]
    verify.need(zero_counts==[[80,80],[81,81]], 'Both actual zero-load masks fully checked')
    return {'status':'EXACT_UNIFORM617_TOTAL395_FROM_EXPLICIT_PRIOR_RESULTS',
            'phase_count':617,'old_each198_or_stronger_count':602,'new_joint197_exclusions':NEW_PHASES,
            'prior_joint197_exclusions':[201,269],'coverage_counts':[602,13,2],
            'required_individual_original_class_edits':197,'necessary_max_original_class_edits':198,
            'necessary_min_original_class_edits_at_most_formula':'M_s-198',
            'minimum_total_nonpole_edits':min(total_floors),'maximum_total_nonpole_edits_formula':'2*M_s-395',
            'uniform_total_upper_bound':3303,'phase1_total_upper_bound_from_uniform_floor':3301,
            'per_phase_total_lower_bounds':total_floors,'per_phase_total_upper_bounds':[sum(m)-b for m,b in zip(sizes,total_floors)],
            'total_floor_histogram':dict(sorted(Counter(map(str,total_floors)).items())),
            'new_root_cases':sum(len(r['root_results']) for r in cases),
            'new_packing_stages':sum(len(c['stages']) for r in cases for c in r['root_results']),
            'all_new_stages_AP_only':all(c['positive_triple_weights']==0 for r in cases for z in r['root_results'] for c in z['stages']),
            'new_zero_loss_rigid_phases':[r['phase'] for r in zero_cases],
            'new_zero_loss_fixed_counts':[r['zero_loss_premise']['fixed_counts'][0] for r in zero_cases],
            'poles_free_and_uncounted':True,'candidate_symmetry_assumed':False,'new_W_bound':False,
            'attainability_claim':False,'external_review_claimed':False,'solver_trusted':False,
            'prior602_and201_269_proofs_replayed_here':False}


def replay(directory=HERE):
    manifest=json.loads((directory/'manifest.json').read_text())
    verify.need(type(manifest) is dict and set(manifest)=={'format','phases','cases','dependencies','proposals'} and
                manifest['format']=='QR617_UNIFORM395_COVER_MANIFEST_1', 'Full source manifest schema')
    verify.need(manifest['phases']==NEW_PHASES and all(type(s) is int for s in manifest['phases']), 'Exact new phase list')
    specs=manifest['cases']
    verify.need(type(specs) is list and len(specs)==13 and [c['phase'] for c in specs]==NEW_PHASES,
                'One fully replayed source case per new phase')
    cases=[]
    for c in specs:
        verify.need(type(c) is dict and set(c)=={'phase','base','cover','zero_tree'}, 'Case paths schema')
        base=directory/local(c['base']);cover=json.loads((directory/local(c['cover'])).read_text())
        tree=directory/local(c['zero_tree']) if c['zero_tree'] is not None else None
        verify.need((tree is not None)==(c['phase'] in [184,205]), 'Zero-loss premises needed exactly at184/205')
        result=verify.check_cover(base,cover,directory,zero_tree=tree)
        verify.need(result['phase']==c['phase'], 'Manifest phase matches actual checked case')
        cases.append(result)
    deps=dependencies(manifest,directory)
    return {'agent':'six-vdw-3','role':'researcher','uniform':combine(deps,cases),'new_cases':cases}


def compact(data):
    """Omit reproducible point lists, retaining all exact weights/gaps and domain hashes."""
    omit={'next_domain','fixed_positions','loss_profile','worst_removed_loss_positions'}
    if type(data) is dict:return {k:compact(v) for k,v in data.items() if k not in omit}
    if type(data) is list:return [compact(v) for v in data]
    return data


def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE)
    p.add_argument('--expected',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    out=compact(replay(a.directory))
    if a.expected:verify.need(out==json.loads(a.expected.read_text()), 'Full compact expected exact result')
    if a.output:a.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(out['uniform'],sort_keys=True))


if __name__=='__main__':main()
