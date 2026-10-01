"""Definition-level base screens, activated APs, and complete anchor covers.

No numerical library or proposal generator is imported. References use
Euler's criterion; all actual APs, loads and full domains use Python ints.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path

P, N, C, CAP = 617, 3704, 1852, 197
HERE = Path(__file__).parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def domain_sha(vertices):
    return hashlib.sha256((','.join(map(str, sorted(vertices)))+'\n').encode()).hexdigest()


def actual_ap(a, d):
    need(type(a) is int and type(d) is int and d > 0 and 0 <= a < a+6*d < N,
         'Actual nonconstant integer seven-AP')
    return {a+j*d for j in range(7)}


def base_premise(path, zero_tree=None):
    raw = path.read_bytes()
    data = json.loads(raw)
    need(type(data) is dict and set(data) == {'format','P','N','terms','seam','s','t','g',
         'denominator','color0_APs'}, 'Base schema')
    need(data['format'] == 'QR617_REFLECTION_WEIGHTS_1', 'Base format')
    need(all(type(data[k]) is int for k in ('P','N','terms','seam','s','t','g','denominator')), 'Base integers')
    need((data['P'],data['N'],data['terms'],data['seam']) == (P,N,7,C), 'Base geometry')
    s,t = data['s'],data['t']
    need(0 <= s < P and t == (1-s) % P and data['g'] == 1, 'Reflection reference key')
    need(all(P % d for d in range(2,isqrt(P)+1)), 'Prime617 by complete trial division')
    q = [-1]+[int(pow(r,308,P) == P-1) for r in range(1,P)]
    need(all(pow(r,308,P) in (1,P-1) for r in range(1,P)), 'Euler character values')
    colors = []
    for x in range(N):
        r = (x-C+(s if x<C else t)) % P
        colors.append(-1 if r == 0 else q[r] ^ int(x>=C))
    need(all(colors[N-1-x] == (-1 if colors[x] == -1 else 1-colors[x]) for x in range(N)),
         'Actual reference antisymmetry, no candidate symmetry')
    D = data['denominator']
    need(D > 0 and type(data['color0_APs']) is list and data['color0_APs'], 'Positive base packing')
    loads = [0]*N
    totals = [0,0]
    seen = set()
    for row in data['color0_APs']:
        need(type(row) is list and len(row) == 3 and all(type(v) is int for v in row), 'Base AP row')
        a,d,w = row
        need(w > 0, 'Positive base AP weight')
        for c,aa in ((0,a),(1,N-1-a-6*d)):
            A = actual_ap(aa,d)
            need(min(A)<C<=max(A), 'Base actual crossing AP')
            need((aa,d) not in seen, 'Distinct base AP');seen.add((aa,d))
            need(all(colors[x] == c for x in A), 'Base actual reference color, no pole')
            for x in A:
                loads[x] += w
            totals[c] += w
    need(totals[0] == totals[1] > 0 and max(loads) <= D, 'Both base totals and every exact point capacity')
    S = totals[0]
    delta = CAP*D-S
    vertices = [{x for x in range(N) if colors[x] == c and D-loads[x] <= delta} for c in (0,1)]
    need(vertices[1] == {N-1-x for x in vertices[0]}, 'Actual reflected necessary cap197 screens')
    sizes = [colors.count(c) for c in (0,1)]
    need(sizes[0] == sizes[1], 'Equal original reference class sizes')
    summary = {'phase':s,'key':[s,t,1],'base_certificate_sha256':hashlib.sha256(raw).hexdigest(),
               'base_denominator':D,'base_weight_numerator':S,'cap197_defect_numerator':delta,
               'base_floor_per_class':(S+D-1)//D,'proved_floor_per_class':(S+D-1)//D,'cap197_screen_sizes':[len(v) for v in vertices],
               'cap197_screen_sha256':[domain_sha(v) for v in vertices],
               'original_class_sizes':sizes,'free_poles':colors.count(-1),'checked_base_actual_APs':len(seen)}
    if zero_tree is not None:
        zero_info = check_zero_tree(zero_tree, colors, loads, S, D, summary)
        vertices = [vertices[c]-set(zero_info['fixed_positions'][c]) for c in (0,1)]
        summary.update({'zero_loss_premise':zero_info,'proved_floor_per_class':max(197,summary['base_floor_per_class']),
                        'cap197_screen_sizes':[len(v) for v in vertices],
                        'cap197_screen_sha256':[domain_sha(v) for v in vertices]})
    return colors,vertices,summary


def check_removed_zero_leaf(data, colors, V, K, c, T, X, phase, base_sha):
    need(type(data) is dict and set(data)=={"format","phase","class_cap","base_certificate_sha256",
         "denominator","color0_APs","color0_cover2","color0_surcharges"}, "Residual leaf schema")
    need(data["format"]=="QR617_UNIFORM_SCREENED_COVER2_1", "Residual leaf format")
    need(type(data["phase"]) is int and data["phase"]==phase, "Residual leaf phase")
    need(type(data["class_cap"]) is int and data["class_cap"]==196, "Residual cap196")
    need(data["base_certificate_sha256"]==base_sha, "Residual base dependency")
    D = data["denominator"]
    need(type(D) is int and D>0, "Positive integer denominator")
    need(T<=V and X<=V and not(T&X), "Inherited disjoint states within screen")
    need(all(type(data[k]) is list for k in ("color0_APs","color0_cover2","color0_surcharges")), "Weight lists")
    F = V-T-X
    loads = {x:0 for x in F}
    losses = {z:0 for z in K}
    W,checked = 0,0

    def actual(a,d):
        nonlocal checked
        need(type(a) is int and type(d) is int and d>0 and 0<=a<a+6*d<N, "Actual nonconstant seven-AP")
        aa = a if c==0 else N-1-a-6*d
        A = {aa+j*d for j in range(7)}
        need(all(colors[x]==c for x in A), "Actual original-color AP, no pole")
        checked += 1
        return A

    seen = set()
    for row in data["color0_APs"]:
        need(type(row) is list and len(row)==3 and all(type(x) is int for x in row), "Integer AP row")
        a,d,w = row
        need(w>0 and (a,d) not in seen, "Unique positive AP weight")
        seen.add((a,d))
        A = actual(a,d)
        b = int(not(A&V&T))
        W += b*w
        for x in A&F: loads[x] += w
        for z in A&K: losses[z] += b*w
    seen = set()
    for row in data["color0_cover2"]:
        need(type(row) is list and len(row)==2, "Triple row schema")
        triple,w = row
        need(type(triple) is list and len(triple)==3 and type(w) is int and w>0, "Positive triple")
        need(all(type(ap) is list and len(ap)==2 and all(type(x) is int for x in ap) for ap in triple), "Actual triple coordinates")
        key = tuple(sorted(tuple(ap) for ap in triple))
        need(len(set(key))==3 and key not in seen, "Distinct APs and unique triple")
        seen.add(key)
        As = [actual(a,d) for a,d in triple]
        ps = [A&V for A in As]
        need(all(ps) and not set.intersection(*ps), "Screened triple requires two edits")
        U = set.union(*ps)
        b = max(0,2-len(U&T))
        W += b*w
        for x in U&F: loads[x] += w
        for z in K:
            count = sum(z in A for A in As)
            ell = 2 if count==3 else int(count>0)
            losses[z] += min(b,ell)*w
    sur,nu = {},0
    for row in data["color0_surcharges"]:
        need(type(row) is list and len(row)==2 and all(type(x) is int for x in row), "Integer surcharge row")
        x,w = row
        x = x if c==0 else N-1-x
        need(x in F and x not in sur and w>0, "Unique positive free-point surcharge")
        sur[x]=w; nu+=w
    need(all(loads[x]<=D+sur.get(x,0) for x in F), "Exact capacity at EVERY free screen point")
    worst = max(losses.values())
    old_gap = W-nu-(196-len(T))*D
    gap = old_gap-worst
    need(gap>0, "Strict contradiction for EVERY removed zero edit")
    return {"original_class":c,"forced":sorted(T),"forbidden":sorted(X),"free_screen_size":len(F),
            "denominator":D,"weighted_numerator":W,"penalty_numerator":nu,"old_gap_numerator":old_gap,
            "worst_removed_loss_numerator":worst,"worst_removed_loss_positions":sorted(z for z in K if losses[z]==worst),
            "strict_gap_numerator":gap,"strict_gap":str(Fraction(gap,D)),"removed_positions_checked":len(K),
            "positive_AP_weights":len(data["color0_APs"]),"positive_triple_weights":len(data["color0_cover2"]),
            "checked_actual_APs":checked,"loss_profile":[[z,losses[z]] for z in sorted(K)]}


def check_zero_tree(path, colors, loads, S, D, summary):
    raw=path.read_bytes();data=json.loads(raw);phase=summary['phase'];base_sha=summary['base_certificate_sha256']
    need(type(data) is dict and set(data)=={'format','phase','class_cap','base_certificate_sha256','tree'},'Old complete tree schema')
    need(data['format']=='QR617_CLASS196_BINARY_COVER_1' and type(data['phase']) is int and data['phase']==phase,'Old tree format/phase')
    need(type(data['class_cap']) is int and data['class_cap']==196 and data['base_certificate_sha256']==base_sha,'Old cap and actual checked base hash')
    delta=196*D-S;need(0<=delta<D,'Removed zero outside old class196 screen')
    V=[{x for x in range(N) if colors[x]==c and D-loads[x]<=delta} for c in (0,1)]
    K=[{x for x in range(N) if colors[x]==c and loads[x]==0} for c in (0,1)]
    need(all(K[c] and not(K[c]&V[c]) for c in (0,1)),'All actual zero candidates outside residual screens')
    leaves=[];nodes=0
    def walk(node,T,X,branch):
        nonlocal nodes
        nodes+=1;need(nodes<=127,'Bounded full old tree')
        need(type(node) is dict,'Old node object')
        if set(node)=={'leaf'}:
            pair=[]
            for c in (0,1):
                tc=T if c==0 else {N-1-x for x in T};xc=X if c==0 else {N-1-x for x in X}
                pair.append(check_removed_zero_leaf(node['leaf'],colors,V[c],K[c],c,tc,xc,phase,base_sha))
            leaves.append({'path':branch,'colors':pair});return
        need(set(node)=={'split','unchanged','edited'},'BOTH old children required, no hidden states')
        x=node['split'];need(type(x) is int and x in V[0]-T-X,'Fresh old-screen split point')
        walk(node['unchanged'],T,X|{x},branch+['unchanged'])
        walk(node['edited'],T|{x},X,branch+['edited'])
    walk(data['tree'],set(),set(),[])
    need(leaves,'Nonempty complete old tree')
    return {'tree_certificate_sha256':hashlib.sha256(raw).hexdigest(),'fixed_positions':[sorted(k) for k in K],
            'fixed_counts':[len(k) for k in K],'old_screen_sizes':[len(v) for v in V],
            'nodes':nodes,'leaves':leaves,'other_class_cap_required':False}


def check_stage(data, colors, vertices, phase, root):
    need(type(data) is dict, 'Stage object')
    need(type(phase) is int and 0 <= phase < P and type(root) is int and 0 <= root < N and colors[root] == 0,
         'Actual original0 root hypothesis')
    if data.get('format') == 'QR617_ACTIVATED_EMPTY_PETAL_1':
        need(set(data) == {'format','phase','root','domain_sha256','AP'}, 'Empty-petal schema')
    else:
        need(set(data) == {'format','phase','root','domain_sha256','denominator','AP_weights',
                          'bundle_weights','surcharges'}, 'Packing schema without hidden restrictions')
        need(data['format'] == 'QR617_ACTIVATED_DOMAIN_PACK_1', 'Packing format')
    need(type(data['phase']) is int and data['phase'] == phase and type(data['root']) is int and data['root'] == root,
         'Inherited phase and root')
    need(data['domain_sha256'] == domain_sha(vertices), 'FULL independently inherited domain')
    need(all(type(x) is int and 0 <= x < N and colors[x] == 1 for x in vertices), 'Original1 permitted points')
    checked = activated = 0

    def petal(a,d):
        nonlocal checked,activated
        A = actual_ap(a,d)
        mono = all(colors[x] == 1 for x in A)
        active = root in A and all(colors[x] == 1 for x in A-{root})
        need(mono or active, 'Mandatory original1 or exactly root-activated actual AP')
        checked += 1;activated += int(active)
        return A & vertices

    if data['format'] == 'QR617_ACTIVATED_EMPTY_PETAL_1':
        need(type(data['AP']) is list and len(data['AP']) == 2, 'Empty mandatory AP row')
        need(not petal(*data['AP']), 'Actual mandatory petal empty in FULL inherited domain')
        return {'root':root,'exclusion':True,'direct_empty_petal':True,'old_domain_size':len(vertices),
                'next_domain':[],'next_domain_sha256':domain_sha(set()),'checked_actual_APs':checked,
                'activated_AP_occurrences':activated}
    D = data['denominator']
    need(type(D) is int and D > 0 and vertices, 'Positive packing denominator and inherited domain')
    need(all(type(data[k]) is list for k in ('AP_weights','bundle_weights','surcharges')), 'Weight lists')
    loads = {x:0 for x in vertices}
    W = 0;seen = set()
    for row in data['AP_weights']:
        need(type(row) is list and len(row) == 3 and all(type(v) is int for v in row), 'Integer AP row')
        a,d,w = row
        need(w > 0 and (a,d) not in seen, 'Unique positive AP row');seen.add((a,d))
        ps = petal(a,d)
        need(ps, 'Nonempty mandatory weighted AP petal')
        for x in ps:
            loads[x] += w
        W += w
    seen = set()
    for row in data['bundle_weights']:
        need(type(row) is list and len(row) == 2, 'Triple row')
        aps,w = row
        need(type(aps) is list and len(aps) == 3 and type(w) is int and w > 0, 'Positive triple weight')
        need(all(type(ap) is list and len(ap) == 2 and all(type(x) is int for x in ap) for ap in aps), 'Triple APs')
        key = tuple(sorted(tuple(ap) for ap in aps))
        need(len(set(key)) == 3 and key not in seen, 'Distinct APs and unique triple');seen.add(key)
        ps = [petal(a,d) for a,d in aps]
        need(all(ps) and not set.intersection(*ps), 'Three mandatory petals without common permitted point')
        U = set.union(*ps)
        for x in U:
            loads[x] += w
        W += 2*w
    sur = {};nu = 0
    for row in data['surcharges']:
        need(type(row) is list and len(row) == 2 and all(type(v) is int for v in row), 'Integer surcharge row')
        x,w = row
        need(x in vertices and x not in sur and w > 0, 'Unique positive full-domain surcharge')
        sur[x] = w;nu += w
    need(all(loads[x] <= D+sur.get(x,0) for x in vertices), 'Capacity at EVERY inherited domain point')
    gap = W-nu-CAP*D
    screen = set() if gap > 0 else {x for x in vertices if D-min(loads[x],D) <= -gap}
    return {'root':root,'denominator':D,'weighted_numerator':W,'surcharge_numerator':nu,
            'gap_to_cap_numerator':gap,'strict_gap':str(Fraction(gap,D)) if gap > 0 else None,
            'exclusion':gap > 0,'direct_empty_petal':False,'old_domain_size':len(vertices),
            'next_domain':sorted(screen),'next_domain_sha256':domain_sha(screen),
            'maximum_raw_load_numerator':max(loads.values()),'positive_AP_weights':len(data['AP_weights']),
            'positive_triple_weights':len(data['bundle_weights']),'checked_actual_APs':checked,
            'activated_AP_occurrences':activated}


def check_cover(base, cover, directory=HERE, documents=None, zero_tree=None):
    colors,V,summary = base_premise(base,zero_tree)
    need(type(cover) is dict and set(cover) == {'format','phase','caps','anchor','chains'}, 'Complete cover schema')
    need(cover['format'] == 'QR617_BASESCREEN_ANCHOR_COVER_1', 'Complete cover format')
    need(type(cover['phase']) is int and cover['phase'] == summary['phase'], 'Cover base phase')
    need(type(cover['caps']) is list and cover['caps'] == [CAP,CAP] and all(type(c) is int for c in cover['caps']), 'Joint original-class197 caps')
    need(type(cover['anchor']) is list and len(cover['anchor']) == 2, 'Actual anchor row')
    anchor = actual_ap(*cover['anchor'])
    need(all(colors[x] == 0 for x in anchor), 'Actual original0 monochromatic anchor')
    roots = anchor & V[0]
    need(type(cover['chains']) is list and all(type(c) is dict and set(c) == {'root','certificates'} for c in cover['chains']), 'Root chains schema')
    supplied = [c['root'] for c in cover['chains']]
    need(all(type(r) is int for r in supplied) and len(set(supplied)) == len(supplied) and set(supplied) == roots,
         'Every possible anchor edit root, no missing or extra case')
    if documents is not None:
        need(type(documents) is dict and set(documents) == roots, 'Complete root documents')
    results = []
    for chain in sorted(cover['chains'],key=lambda c:c['root']):
        root = chain['root'];vertices = set(V[1]);out = []
        need(type(chain['certificates']) is list and chain['certificates'], 'Nonempty complete root chain')
        if documents is None:
            paths = [Path(f) for f in chain['certificates']]
            need(all(not f.is_absolute() and '..' not in f.parts and f.parts[0] == 'certificates' for f in paths), 'Local certificate paths')
            docs = [json.loads((directory/f).read_text()) for f in paths]
        else:
            docs = documents[root]
            need(type(docs) is list and len(docs) == len(chain['certificates']), 'All stages retained')
        for data in docs:
            need(not out or not out[-1]['exclusion'], 'No extra stage after exact contradiction')
            checked = check_stage(data,colors,vertices,summary['phase'],root)
            out.append(checked);vertices = set(checked['next_domain'])
        need(out and out[-1]['exclusion'], 'Each covered root strictly excluded')
        results.append({'root':root,'stages':out})
    sizes = summary['original_class_sizes']
    floor = summary['proved_floor_per_class']
    return {'agent':'six-vdw-3','role':'researcher','status':'EXACT_BASESCREEN_JOINT197_EXCLUSION',
            **summary,'anchor':cover['anchor'],'anchor_points':sorted(anchor),'complete_anchor_roots':sorted(roots),
            'fixed_anchor_positions_under_e0_cap197':sorted(anchor-V[0]),'root_results':results,
            'necessary_max_class_edits':198,'necessary_min_class_edits_at_most':sizes[0]-198,
            'proved_individual_floor_per_class':floor,'necessary_total_nonpole_edits_min':max(2*floor,198+floor),
            'necessary_total_nonpole_edits_max':sum(sizes)-max(2*floor,198+floor),
            'pole_colors_free':True,'candidate_symmetry_assumed':False,'solver_trusted':False,
            'new_W_bound':False,'external_review_claimed':False,'attainability_claim':False}


def main():
    p = argparse.ArgumentParser();p.add_argument('certificates',type=Path,nargs='*')
    p.add_argument('--base',type=Path,default=HERE/'base/phase-170.json')
    p.add_argument('--root',type=int);p.add_argument('--cover',type=Path);p.add_argument('--zero-tree',type=Path);p.add_argument('--output',type=Path)
    p.add_argument('--expected',type=Path);a = p.parse_args()
    if a.cover:
        out = check_cover(a.base,json.loads(a.cover.read_text()),HERE,zero_tree=a.zero_tree)
    else:
        colors,V,summary = base_premise(a.base,a.zero_tree);vertices = set(V[1]);results = []
        need(a.certificates and a.root is not None, 'Root and certificate chain required')
        for f in a.certificates:
            need(not results or not results[-1]['exclusion'], 'No continuation after contradiction')
            row = check_stage(json.loads(f.read_text()),colors,vertices,summary['phase'],a.root)
            row['certificate_sha256'] = hashlib.sha256(f.read_bytes()).hexdigest();results.append(row)
            vertices = set(row['next_domain'])
        out = {'agent':'six-vdw-3','role':'researcher',**summary,'root':a.root,'stages':results,
               'root_excluded':results[-1]['exclusion'],'other_class_cap_required_for_root':False}
    if a.expected:
        need(out == json.loads(a.expected.read_text()), 'Expected full exact result')
    if a.output:
        a.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    compact = {k:v for k,v in out.items() if k not in ('root_results','stages')}
    rows = out.get('root_results',[{'root':out.get('root'),'stages':out.get('stages',[])}])
    compact['root_results'] = [{'root':r['root'],'stages':[{k:v for k,v in s.items() if k != 'next_domain'} for s in r['stages']]} for r in rows]
    print(json.dumps(compact))


if __name__ == '__main__':
    main()
