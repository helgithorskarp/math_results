"""Exact actual-AP packing and nonnegative-defect domain refinement.

Replays the published phase201 premise. New stages import no numerical
proposal code and reconstruct all capacities, bundle multiplicities and
derived edit domains using Euler colors, sets and integer arithmetic.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

N,P,C=3704,617,1852
HERE=Path(__file__).parent
PARENT_ROOT_SHA="caff24aba426512f1f44b66b33030a8aacda8feaabe767990ff2a91ffa3081b5"


def need(ok,message):
    if not ok:raise ValueError(message)


def domain_sha(vertices):
    return hashlib.sha256((','.join(map(str,sorted(vertices)))+'\n').encode()).hexdigest()


def premise(directory=HERE,root=1427):
    spec=importlib.util.spec_from_file_location('published_phase201_exact',directory/'parent/verify.py')
    parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
    colors,K,_=parent.premise(directory/'parent')
    need(type(root) is int and 0<=root<N and colors[root]==0 and root not in K[0], 'Original reference0 trial edit')
    vertices={x for x in range(N) if colors[x]==1 and x not in K[1]}
    prior=None
    if root==1427:
        raw=(directory/'parent/root1427.json').read_bytes()
        need(hashlib.sha256(raw).hexdigest()==PARENT_ROOT_SHA,'Frozen published root1427 packing')
        prior=parent.check_screen(json.loads(raw),colors,K)
        vertices=set(prior['necessary_permitted_screen'])
    return colors,K,vertices,prior


def check_stage(data,colors,vertices,root=1427,cap=197):
    need(type(cap) is int and cap==197,'Exact original reference-class cap197')
    need(type(data) is dict and set(data)=={'format','phase','root','denominator','domain_sha256',
         'AP_weights','bundle_weights','surcharges'},'Stage schema: no hidden forced or forbidden edits')
    need(data['format']=='QR617_PHASE201_DOMAIN_PACK_1','Stage format')
    need(type(data['phase']) is int and data['phase']==201,'Stage phase')
    need(type(data['root']) is int and data['root']==root and colors[root]==0,'Inherited root hypothesis')
    need(data['domain_sha256']==domain_sha(vertices),'Full inherited domain, no unproved restriction')
    D=data['denominator']
    need(type(D) is int and D>0,'Positive integer denominator')
    need(all(type(data[k]) is list for k in ('AP_weights','bundle_weights','surcharges')),'Weight lists')
    need(vertices and all(0<=x<N and colors[x]==1 for x in vertices),'Actual reference1 domain')
    loads={x:0 for x in vertices};W=0;checked=activated=0

    def petal(a,d):
        nonlocal checked,activated
        need(type(a) is int and type(d) is int and d>0 and 0<=a<a+6*d<N,'Actual nonconstant integer seven-AP')
        A={a+j*d for j in range(7)}
        mono=all(colors[x]==1 for x in A)
        active=root in A and all(colors[x]==1 for x in A-{root})
        need(mono or active,'Mandatory original1 or exactly trial-root-activated AP')
        checked+=1;activated+=int(active)
        return A&vertices

    seen=set()
    for row in data['AP_weights']:
        need(type(row) is list and len(row)==3 and all(type(x) is int for x in row),'Integer AP row')
        a,d,w=row
        need(w>0 and (a,d) not in seen,'Unique positive AP weight');seen.add((a,d))
        ps=petal(a,d)
        need(ps,'Nonempty mandatory AP petal')
        for x in ps:loads[x]+=w
        W+=w
    seen=set();counts={3:0,5:0}
    for row in data['bundle_weights']:
        need(type(row) is list and len(row)==2,'Bundle row')
        aps,w=row
        need(type(aps) is list and len(aps) in (3,5) and type(w) is int and w>0,'Three or five distinct APs with positive integer weight')
        need(all(type(ap) is list and len(ap)==2 and all(type(x) is int for x in ap) for ap in aps),'Bundle AP coordinates')
        key=tuple(sorted(tuple(ap) for ap in aps))
        need(len(set(key))==len(key) and key not in seen,'Unique bundle with distinct APs');seen.add(key)
        ps=[petal(a,d) for a,d in aps]
        need(all(ps),'Every mandatory bundle petal nonempty')
        U=set.union(*ps)
        if len(aps)==3:
            need(not set.intersection(*ps),'Three petals have no common permitted point')
            rhs=2
        else:
            need(all(sum(x in p for p in ps)<=2 for x in U),'Five-petal union has maximum membership two')
            rhs=3
        for x in U:loads[x]+=w
        W+=rhs*w;counts[len(aps)]+=1
    sur={};nu=0
    for row in data['surcharges']:
        need(type(row) is list and len(row)==2 and all(type(x) is int for x in row),'Integer surcharge row')
        x,w=row
        need(x in vertices and x not in sur and w>0,'Unique positive inherited-domain surcharge')
        sur[x]=w;nu+=w
    need(all(loads[x]<=D+sur.get(x,0) for x in vertices),'Exact capacity at EVERY inherited-domain point')
    # min(L,D)<=D and sum_E min(L,D)>=W-sum_all_surcharges.
    # This safely handles capacities with a positive surcharge; no negative
    # defect is ever used to justify an individual-point screen.
    effective={x:min(loads[x],D) for x in vertices}
    adjusted=W-nu;gap=adjusted-cap*D
    screen=set() if gap>0 else {x for x in vertices if D-effective[x]<=cap*D-adjusted}
    result={'root':root,'opposite_original_class':1,'cap':cap,'denominator':D,'weighted_numerator':W,
            'surcharge_numerator':nu,'adjusted_weight_numerator':adjusted,'gap_to_cap_numerator':gap,
            'strict_gap':str(Fraction(gap,D)) if gap>0 else None,'exclusion':gap>0,
            'old_domain_size':len(vertices),'next_domain_size':len(screen),
            'newly_forbidden_positions':sorted(vertices-screen) if gap<=0 else [],
            'next_domain':sorted(screen),'next_domain_sha256':domain_sha(screen),
            'maximum_raw_load_numerator':max(loads.values()),'positive_AP_weights':len(data['AP_weights']),
            'positive_triple_weights':counts[3],'positive_five_bundle_weights':counts[5],
            'checked_actual_APs':checked,'weighted_activated_AP_occurrences':activated,
            'solver_trusted':False,'new_W_bound':False}
    return result


ROOT_FILES={1427:['01-zero2382.json','02-root1427-exclusion.json'],
            1662:['root1662-exclusion.json'],1897:['root1897-exclusion.json'],
            2132:['root2132-01-domain.json','root2132-02-forbid462-1790.json','root2132-03-exclusion.json'],
            2367:['root2367-exclusion.json']}


def check_complete(directory=HERE,documents=None):
    colors,K,_,_=premise(directory)
    need(all(colors[N-1-x]==(-1 if colors[x]==-1 else 1-colors[x]) for x in range(N)),
         'Reference reflection interchanges colors and pairs poles')
    anchor={957+j*235 for j in range(7)}
    need(all(colors[x]==0 for x in anchor),'Actual original0 anchor seven-AP')
    need(anchor&K[0]=={957,1192},'Exact two fixed zero-load anchor positions')
    roots=anchor-K[0]
    need(roots==set(ROOT_FILES),'All five mandatory anchor edit roots')
    if documents is None:
        documents={root:[json.loads((directory/'certificates'/f).read_text()) for f in files]
                   for root,files in ROOT_FILES.items()}
    need(type(documents) is dict and set(documents)==roots,'Complete root documents, no omitted case')
    results=[]
    for root in sorted(roots):
        colors2,K2,V,prior=premise(directory,root)
        need(colors2==colors and K2==K,'Consistent original reference and zero masks')
        need(type(documents[root]) is list and documents[root],'Nonempty rooted certificate chain')
        chain=[]
        for data in documents[root]:
            need(not chain or not chain[-1]['exclusion'],'No extra stage after a contradiction')
            row=check_stage(data,colors,V,root=root)
            chain.append(row);V=set(row['next_domain'])
        need(chain[-1]['exclusion'],'Every one of the five anchor roots strictly excluded')
        results.append({'root':root,'initial_domain_size':1023 if prior else 1771,'stages':chain})
    # The older selected complete class196 tree is already replayed by the
    # parent premise. Its positive OLD gaps also give the unconditional
    # phase201 individual class197 floor, without any removed-edit premise.
    spec=importlib.util.spec_from_file_location('replayed_zero_exact',directory/'parent/zero/verify.py')
    zero=importlib.util.module_from_spec(spec);spec.loader.exec_module(zero)
    prior_zero=zero.check_all(directory/'parent/zero')
    need(all(c['old_gap_numerator']>0 for leaf in prior_zero['leaf_results'] for c in leaf['colors']),
         'Both old class196 leaves in both colors strictly excluded')
    return {'agent':'six-vdw-3','role':'researcher','status':'EXACT_PHASE201_JOINT197_EXCLUSION',
            'phase':201,'key':[201,417,1],'excluded_original_class_caps':[197,197],
            'necessary_max_original_class_edits':198,'necessary_min_original_class_edits_at_most':1651,
            'required_edits_per_reference_color':197,'necessary_total_nonpole_edits_min':395,
            'necessary_total_nonpole_edits_max':3303,'individual_reference_class_edit_upper_bound':1652,
            'individual_lower197_dependency':'bafkreidd54kxpyjlspt4tww57ib3p5ldcdc72h7isybb6onoeugb2u7eta',
            'selected_individual_lower197_tree_replayed':True,
            'anchor_AP':[957,235],'anchor_points':sorted(anchor),'anchor_fixed_positions':sorted(anchor&K[0]),
            'complete_anchor_roots':sorted(roots),'root_results':results,
            'conditional_e1_cap197_requires_E0_hit':[957,1192],
            'conditional_e0_cap197_requires_E1_hit':[2511,2746],
            'original_reference_class_sizes':[1849,1849],'pole_colors_free':True,
            'candidate_symmetry_assumed':False,'solver_trusted':False,'new_W_bound':False,
            'attainability_claim':False,'external_review_asserted':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('certificates',type=Path,nargs='*')
    p.add_argument('--root',type=int,default=1427);p.add_argument('--output',type=Path)
    p.add_argument('--expected',type=Path);a=p.parse_args()
    if not a.certificates:
        out=check_complete()
        if a.expected:need(out==json.loads(a.expected.read_text()),'Expected complete exact result')
        if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
        compact={k:v for k,v in out.items() if k!='root_results'}
        compact['root_results']=[{'root':r['root'],'stages':[{k:v for k,v in s.items() if k not in ('next_domain','newly_forbidden_positions')} for s in r['stages']]} for r in out['root_results']]
        print(json.dumps(compact));return
    colors,K,V,prior=premise(root=a.root);results=[]
    for path in a.certificates:
        need(not results or not results[-1]['exclusion'],'No continuation after a proved contradiction')
        r=check_stage(json.loads(path.read_text()),colors,V,root=a.root)
        r['certificate_sha256']=hashlib.sha256(path.read_bytes()).hexdigest();results.append(r)
        V=set(r['next_domain'])
    out={'agent':'six-vdw-3','role':'researcher','phase':201,'root':a.root,'results':results,
         'conditional_other_class_cap_required':False,'published_initial_screen_size':1023 if prior else 1771,
         'root_excluded':bool(results and results[-1]['exclusion']),'pole_colors_free':True,
         'candidate_symmetry_assumed':False,'solver_trusted':False,'new_W_bound':False}
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({**{k:v for k,v in out.items() if k!='results'},'results':[{k:v for k,v in r.items() if k not in ('next_domain','newly_forbidden_positions')} for r in results]}))


if __name__=='__main__':main()
