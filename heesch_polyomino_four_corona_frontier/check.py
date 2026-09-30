"""Exact P17 atlas, local-star compatibility, small caps, and fifth obstruction.

CPython 3.11+ standard library. No SAT solver or discovery output is read.
"""
from pathlib import Path
from functools import lru_cache
import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PINS = {
 'check.py':'c6befbcb674e7da66cfb6abd5fe6ef2537e536595af87e0f70f2e70eba75cc01',
 'certificates.json':'ff9a9d5b81cc65a36049fe8d3077fe2908c77a76d44b608047a243284b672665',
 'expected.json':'a6d03c197d823a78800ff00eb45310a649bdcb71561454a2b843f3a6d7d10869'}
ROOT = (3,0,0)
ROWS = [1,25,50,72,96,133,134]


def require(condition,message):
    if not condition:
        raise ValueError(message)


def dependencies(repository):
    prior = repository/'heesch_polyomino_third_prefix_reduction'
    for name,digest in PINS.items():
        require(hashlib.sha256((prior/name).read_bytes()).hexdigest()==digest,'changed rigidity input: '+name)
    spec = importlib.util.spec_from_file_location('p17_rigidity',prior/'check.py')
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    dep = reader.dependencies(repository)
    # This also replays the earlier thirteen-subset census and positive control.
    run = subprocess.run([sys.executable,*(['-O'] if sys.flags.optimize else []),'-B',str(prior/'check.py'),
                          '--repository',str(repository),'--expected',str(prior/'expected.json')],
                         capture_output=True,text=True,timeout=55)
    require(run.returncode==0 and run.stdout==(prior/'expected.json').read_text(),'prior rigidity replay failed: '+run.stderr[:300])
    return reader,dep,json.loads((prior/'certificates.json').read_text())


class Geometry:
    def __init__(self,g,library):
        self.g = g
        self.library = library
        self.shapes = g.orientations()

    @lru_cache(maxsize=None)
    def cells(self,q):
        return self.g.moved(self.shapes,q)

    @lru_cache(maxsize=None)
    def vertices(self,q):
        return frozenset(self.g.vertices(self.cells(q)))

    @lru_cache(maxsize=None)
    def pair(self,a,b):
        return self.g.forbidden(self.cells(a),self.cells(b),self.shapes,self.library)

    @lru_cache(maxsize=None)
    def conflict(self,a,b):
        return a!=b and (bool(self.cells(a)&self.cells(b)) or self.pair(a,b))

    def packing(self,first,second):
        return not any(self.conflict(a,b) for a in first for b in second)

    def transport(self,star,receiver):
        # Enumerate the eight exact isometries on doubled cell centres.
        transforms = []
        for k in range(4):
            for mirror in (False,True):
                image = self.g.image(self.cells(ROOT),k,mirror)
                if self.g.normalize(image)==self.shapes[receiver[0]]:
                    transforms.append((k,mirror,receiver[1]-min(x for x,y in image),receiver[2]-min(y for x,y in image)))
        require(len(transforms)==1,'P17 transport not unique')
        k,mirror,tx,ty = transforms[0]
        out = []
        for q in star:
            image = {(x+tx,y+ty) for x,y in self.g.image(self.cells(q),k,mirror)}
            code = (self.shapes.index(self.g.normalize(image)),min(x for x,y in image),min(y for x,y in image))
            require(self.cells(code)==image,'transport changes whole footprint')
            out.append(code)
        require(receiver in out and len(out)==len(set(out))==len(star),'transport loses root or copy')
        return tuple(sorted(out))


def complete_atlas(reader,dep,certificates,geom):
    _,_,required,_,_ = dep
    shapes,g = geom.shapes,geom.g
    all_prefixes = set()
    reports = []
    root_halo = reader.halo(geom.cells(ROOT))
    for row in ROWS:
        fixed = tuple(sorted([tuple(q) for q in required[row]]+
                             [tuple(c['conclusion_poses'][0]) for c in certificates['forced_copies'] if c['source_row']==row]))
        require(len(fixed)==len(set(fixed)) and geom.packing(fixed,fixed),'bad guaranteed first subset')
        occupied = set().union(*(geom.cells(q) for q in fixed))
        targets = root_halo-occupied
        # Cell joins differ from the independent bounded-translation inventory.
        joined = {(i,x-a,y-b) for x,y in targets for i,shape in enumerate(shapes) for a,b in shape}
        raw = sorted(q for q in joined if not geom.cells(q)&occupied)
        require(raw==g.bound_candidates(shapes,sorted(targets),occupied),'complete owner inventories differ')
        candidates = [q for q in raw if geom.packing(fixed,(q,))]
        positive = set()
        examined = 0
        # Each extra first-layer copy covers a distinct missing root-halo cell.
        for size in range(min(len(targets),len(candidates))+1):
            for chosen in itertools.combinations(candidates,size):
                examined += 1
                if not targets<=set().union(*(geom.cells(q) for q in chosen)):
                    continue
                if not geom.packing(chosen,chosen):
                    continue
                prefix = tuple(sorted(fixed+chosen))
                require(all(q==ROOT or geom.vertices(q)&geom.vertices(ROOT) for q in prefix),'extra copy fails root contact')
                g.boundary_disc(set().union(*(geom.cells(q) for q in prefix)))
                positive.add(prefix)
        all_prefixes.update(positive)
        reports.append({'source_row':row,'missing_halo_cells':len(targets),'raw_candidates':len(raw),
                        'pair_allowed_candidates':len(candidates),'subsets_examined':examined,'completions':len(positive)})
    return tuple(sorted(all_prefixes)),reports


def star_model(atlas,geom,reader):
    reports = []
    all_second = {}
    for first_id,fixed in enumerate(atlas):
        domains = []
        for receiver in fixed:
            options = []
            for star_id,star in enumerate(atlas):
                placed = geom.transport(star,receiver)
                if not geom.packing(fixed,placed):
                    continue
                if any(geom.vertices(receiver)&geom.vertices(q) and q not in placed for q in fixed):
                    continue
                if any(geom.vertices(ROOT)&geom.vertices(q) and q not in fixed for q in placed):
                    continue
                options.append((star_id,placed))
            domains.append(options)
        examined = 0
        completions = set()
        # This direct Cartesian product differs from the discovery's pruned DFS.
        for assignment in itertools.product(*domains):
            examined += 1
            if not all(geom.packing(a[1],b[1]) for a,b in itertools.combinations(assignment,2)):
                continue
            if any(geom.vertices(receiver)&geom.vertices(q) and q not in assignment[i][1]
                   for i,receiver in enumerate(fixed) for _,star in assignment for q in star):
                continue
            second = tuple(sorted({q for _,star in assignment for q in star}))
            occupied = set().union(*(geom.cells(q) for q in second))
            require(reader.halo(set().union(*(geom.cells(q) for q in fixed)))<=occupied,'second prefix lacks halo')
            geom.g.boundary_disc(occupied)
            completions.add(second)
        all_second[first_id] = tuple(sorted(completions))
        reports.append({'first_prefix_id':first_id,'domain_source_ids':[[i for i,_ in ds] for ds in domains],
                        'products_examined':examined,'second_prefixes':len(completions)})
    return all_second,reports


def validate_tables(data,atlas,second):
    require(data.get('schema')==1 and data.get('agent')=='six-heesch-1' and data.get('role')=='researcher','bad atlas provenance')
    require(data['three_corona_first_prefixes']==[[list(q) for q in p] for p in atlas],'complete first atlas differs')
    require(data['four_corona_second_prefixes']==[[list(q) for q in p] for p in second],'complete second atlas differs')


def cap_certificate(cert,second,geom):
    case = cert['second_prefix_case']
    require(type(case) is int and case in (0,1),'unknown cap exclusion')
    fixed = tuple(map(tuple,cert['fixed_codes']))
    codes = tuple(map(tuple,cert['poses']))
    require(all(len(q)==3 and all(type(z) is int for z in q) and 0<=q[0]<8 for q in fixed+codes),'bad cap pose')
    require(len(fixed)==len(set(fixed)) and set(fixed)<=set(second[case]),'cap not contained in second prefix')
    require(geom.packing(fixed,fixed),'fixed cap copies conflict')
    require(len(codes)==len(set(codes)),'duplicate cap provider')
    occupied = set().union(*(geom.cells(q) for q in fixed))
    require(not any(geom.cells(q)&occupied for q in codes),'provider overlaps fixed cap')
    require(len(cert['clauses'])==len(cert['reasons']),'missing cap clause reason')
    covers = 0
    pairs = 0
    for clause,reason in zip(cert['clauses'],cert['reasons']):
        geom.g.validate_clause(clause,len(codes))
        if reason['kind']=='cover':
            target = tuple(reason['target'])
            require(len(target)==2 and all(type(z) is int for z in target),'bad target')
            require(target in geom.g.corner_targets(geom.g.vertices(occupied),occupied),'not a protected isolated gap')
            require(all(z>0 for z in clause),'bad cover signs')
            require(sorted(codes[z-1] for z in clause)==geom.g.bound_candidates(geom.shapes,[target],occupied),'incomplete cap owner list')
            covers += 1
        elif reason['kind']=='interior_pair':
            require(len(clause)==1 and clause[0]<0,'bad cap pair unit')
            q = codes[-clause[0]-1]
            require(any(geom.vertices(q)&geom.vertices(p) for p in fixed),'owner lacks contact-interiority license')
            require(any(geom.pair(q,p) for p in fixed),'false cap pair exclusion')
            pairs += 1
        else:
            raise ValueError('unknown cap clause reason')
    geom.g.rup(cert['clauses'],cert['rup'],len(codes))
    return {'second_prefix_id':case,'support_copies':len(fixed),'complete_cover_clauses':covers,
            'interior_pair_units':pairs,'core_clauses':len(cert['clauses']),'rup_additions':len(cert['rup'])}


def cap_family(data,second,geom):
    require(data.get('schema')==1 and data.get('agent')=='six-heesch-1' and data.get('role')=='researcher','bad cap provenance')
    require([r['second_prefix_case'] for r in data['exclusions']]==[0,1],'cap exclusion coverage differs')
    return [cap_certificate(c,second,geom) for c in data['exclusions']]


def controls(data,caps,atlas,second,geom):
    variants = []
    bad = copy.deepcopy(data);bad['three_corona_first_prefixes'].pop();variants.append(('atlas',bad))
    bad = copy.deepcopy(data);bad['four_corona_second_prefixes'][0][0][1]+=1;variants.append(('atlas',bad))
    bad = copy.deepcopy(caps);bad['exclusions'].pop();variants.append(('caps',bad))
    bad = copy.deepcopy(caps);bad['exclusions'][0]['clauses'][0].pop();variants.append(('caps',bad))
    bad = copy.deepcopy(caps);bad['exclusions'][0]['rup']=[];variants.append(('caps',bad))
    bad = copy.deepcopy(caps);bad['exclusions'][1]['fixed_codes'][0][1]+=1;variants.append(('caps',bad))
    for i,(kind,bad) in enumerate(variants):
        try:
            if kind=='atlas':validate_tables(bad,atlas,second)
            else:cap_family(bad,second,geom)
        except (ValueError,KeyError,IndexError,TypeError):
            continue
        raise ValueError('malformed control accepted: '+str(i))
    return len(variants)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=HERE.parent)
    parser.add_argument('--atlas',type=Path,default=HERE/'atlas.json')
    parser.add_argument('--certificates',type=Path,default=HERE/'certificates.json')
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--controls',action='store_true')
    args = parser.parse_args()
    reader,dep,certificates = dependencies(args.repository)
    geom = Geometry(dep[0],dep[1])
    atlas,atlas_reports = complete_atlas(reader,dep,certificates,geom)
    require(len(atlas)==11,'necessary first atlas size differs')
    second_map,star_reports = star_model(atlas,geom,reader)
    require([i for i,ps in second_map.items() if ps]==[8],'four-corona first prefix is not unique')
    second = second_map[8]
    require(len(second)==3 and all(len(p)==19 for p in second),'four-corona second frontier differs')
    data = json.loads(args.atlas.read_text())
    caps = json.loads(args.certificates.read_text())
    validate_tables(data,atlas,second)
    cap_reports = cap_family(caps,second,geom)
    # Every H>=5 packing re-roots to four coronas at A=(0,4,0).
    receiver = (0,4,0)
    require(receiver in atlas[8],'fifth obstruction receiver absent')
    forced = geom.transport(atlas[8],receiver)
    clash = (6,-1,-1)
    require(clash in forced and clash!=ROOT and geom.cells(clash)&geom.cells(ROOT),'missing physical fifth-corona clash')
    positive = dep[4]
    first_control = tuple(sorted(tuple(r['code']) for r in positive['poses'] if r['level']<=1))
    second_control = tuple(sorted(tuple(r['code']) for r in positive['poses'] if r['level']<=2))
    require(first_control==atlas[8] and second_control in second,'known three-corona control fails necessary frontier')
    result = {'agent':'six-heesch-1','role':'researcher','status':'verified necessary four-corona frontier and no fifth real-motion corona',
              'prior_rigidity_checker_replayed':True,'three_corona_first_prefixes':len(atlas),'first_atlas_enumeration':atlas_reports,
              'four_corona_star_models':star_reports,'four_corona_first_prefix_id':8,'four_corona_first_prefix_copies':len(atlas[8]),
              'four_corona_second_prefixes_before_caps':len(second),'second_prefix_caps':cap_reports,
              'remaining_four_corona_second_prefix_id':2,'remaining_four_corona_second_prefix_copies':len(second[2]),
              'fifth_obstruction':{'receiver':list(receiver),'forced_pose':list(clash),'root_pose':list(ROOT),
                                  'overlap_cell':list(min(geom.cells(clash)&geom.cells(ROOT)))},
              'positive_control':{'copies':36,'complete_disc_coronas':3,'first_prefix_id':8,'second_prefix_id':second.index(second_control)},
              'conclusion':'3 <= Hc(P17) <= Hh(P17) <= 4; four-corona existence is unresolved'}
    if args.controls:
        result['malformed_controls_rejected'] = controls(data,caps,atlas,second,geom)
    output = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.expected:
        require(output==args.expected.read_text(),'expected result differs')
    print(output,end='')


if __name__=='__main__':
    main()
